from socket import *

hostname = gethostname()
ip = gethostbyname(hostname)
port = 8080
print("Esse é seu ip: ", ip)

while True:
  start = input("Digite 'START' para iniciar o bate-papo: ")
  try:
    if start == "START":
      socket = socket(AF_INET, SOCK_STREAM)
      socket.bind((hostname, port))
      nickname = input("Insira seu apelido: ")
      break  
  except:
     print("Algo inesperado aconteceu, tente novamente.")

#Esperando por conexões
print("Aguardando conexão de usuário")
try: 
  socket.listen()
  client, addr = socket.accept()
  print("Conexão estabelecida com: ", addr[0])
except:
  print("Conexão mal sucedida, tente novamente mais tarde.")


#Tratamento da conexão
userName = (client.recv(1024)).decode()
print(f'usuário "{userName}" se conectou a você!')
client.send(nickname.encode())

#Envio de mensagens
def handleUserMsg():
  message = (client.recv(1024)).decode()
  global userName
  oldName = userName
  match message.split()[0]:
    case "NICK":
      userName = " ".join(message.split()[1:])
      print(f'"{oldName}" mudou seu apelido para "{userName}"')
    case "QUIT":
      print(f'"{userName}" encerrou a conexão, pressione qualquer tecla para sair do bate-papo...')
      client.close()
    case _:
      print(userName + ": " + message)

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
      client.send(sendMessage.encode())

    case "QUIT":
      print("Você encerrou a conexão, saindo do bate-papo...")
      client.send(sendMessage.encode())
      client.close()
      
    case _:
     client.send(sendMessage.encode())
     

#Inicio da conversa
while True:
  handleCommand()
  
  handleUserMsg()

  
