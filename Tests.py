myDoc = open('C:/PAUL/Science/GISofBALI/TEST.txt', 'w')
myDoc.write('newdata')
myDoc.close()

myDoc = open('C:/PAUL/Science/GISofBALI/TEST.txt', 'r')
message = myDoc.read()
print type(message)
