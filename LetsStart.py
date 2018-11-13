
#Grabs the top 8 processes and then scatters them across nodes
#The nodes need to be divisible by two and no greater than the amount of processes
import os
import keyboard

def returnNth(lst, n):
	return lst[::n]

process = os.popen('top -b -n 1 | grep brandon > show_top.txt')


with open('show_top.txt') as f:
    content = f.readlines()

process.close()

content = [x.strip("\n") for x in content] 
content = [word for line in content for word in line.split()]

pidContent = returnNth(content, 12)
pidContent = pidContent[:8]
pidContent = ','.join(map(str, pidContent)) 
cpu = '%cpu'
mem = '%mem'
process = os.popen('ps -fp %s -o %s,%s,cmd > output.txt' % (pidContent, cpu, mem))
with open('output.txt') as g:
	pidList = g.readlines()
process.close()
pidList = [x.strip("\n") for x in pidList]
pidList = [x.split(None, 2) for x in pidList]
del pidList[0]
print(pidList)





