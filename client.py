from socket import *
# class bcolors:
#     HEADER = '\033[95m'
#     OKBLUE = '\033[94m'
#     OKCYAN = '\033[96m'
#     OKGREEN = '\033[92m'
#     WARNING = '\033[93m'
#     FAIL = '\033[91m'
#     ENDC = '\033[0m'
#     BOLD = '\033[1m'
#     UNDERLINE = '\033[4m'

socket = socket(AF_INET, SOCK_STREAM)
hostname = gethostname()
ip = gethostbyname(hostname)
port = 8080

print("Esse é seu ip: ", ip)

#Tratamento de conexão
while True:
  connect = input("Digite 'JOIN' + o endereço ip que deseja se conectar: ")
  line = connect.split()
  command = line[0]
  serverAddress = line[1]
  if command == "JOIN":
    try:
      socket.connect((serverAddress, port))
      nickname = input("insira seu apelido: ")
      print("Conectando...")
      socket.send(nickname.encode())
      serverName = (socket.recv(1024)).decode()

      print(f'usuário "{serverName}" se conectou a você!')
    except:
      print("Não foi possível conectar, tente novamente mais tarde")
  break

#Recebimento de mensagens
def handleServerMsg():
  message = (socket.recv(1024)).decode()
  global serverName
  oldName = serverName
  match message.split()[0]:
    case "NICK":
      serverName = " ".join(message.split()[1:])
      print(f'"{oldName}" mudou seu apelido para "{serverName}"')
    case "QUIT":
      print(f'"{serverName}" encerrou a conexão, pressione qualquer tecla para sair do bate-papo...')
      socket.close()
    case _:
      print(serverName + ": " + message)

#Envio de mensagens
def handleCommand():
  global nickname
  sendMessage = input(f"Eu({nickname}): ")
  line = sendMessage.split()
  command = line[0]
  match command:
    case "NICK":
      nickname = " ".join(line[1:])
      print(f"Você mudou seu apelido para {nickname}")
      socket.send(sendMessage.encode())
    
    case "QUIT":
      print("Você encerrou a conexão, saindo do bate-papo...")
      socket.send(sendMessage.encode())
      socket.close()
    case _:
      socket.send(sendMessage.encode())

#inicio da conversa
while True:
  handleServerMsg()
  
  handleCommand()
