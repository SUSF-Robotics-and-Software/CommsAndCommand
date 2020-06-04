from CommsAndCommand import comms
import time

# localhost = '0.0.0.0'
localhost = "127.0.0.1"
port = 5000
server_address = comms.connection_address(localhost, port)
client_address = comms.connection_address(localhost, port + 1)


server = comms.tcp_server(server_address)
client = comms.tcp_client(client_address, server_address)

server.start()
client.start()

time.sleep(1)

client.send("hello world")

time.sleep(0.02)

print(server.recv())

time.sleep(1)

client.stop()
server.stop()
