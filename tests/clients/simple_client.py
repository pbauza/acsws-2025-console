from Acspy.Clients.SimpleClient import PySimpleClient
client = PySimpleClient()
m = client.getComponent("CONSOLE")
print(m.printHello())
