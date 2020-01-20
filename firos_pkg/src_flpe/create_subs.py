from fiware import OrionClient

head = {"Content-Type": "application/json"}
host = "150.162.6.64"
port = 1026

client = OrionClient(host, port)
print("Ois")
client.subscription("pickandplace")
