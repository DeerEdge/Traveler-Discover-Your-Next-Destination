import os

path = "./User Reports"
directory = os.listdir(path)
print(len(directory))
fileName = ('User Report ' + str(len(directory)))
fileLocation = os.path.join(path, fileName)
with open(fileLocation, 'w') as f:
    f.write("User Information: ")
print(fileLocation)