import os

'''
compiles smaller files to master list
'''

path = '/home/hollis/dev/linkdata/data/'

master = open(path + "randomdiaglinks.pdstor","a")

for a in range(2,11):
	temp = open(path + "from_randomdiagram/"+str(a)+"/" + str(a)+".pdstor")
	master.write(temp.read())
	temp.close()

master.close()
