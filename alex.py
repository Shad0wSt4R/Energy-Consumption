
#Grabs the top 8 processes and then scatters them across nodes
#The nodes need to be divisible by two and no greater than the amount of processes
import psutil
import sys
import math
import random
from concurrent.futures import ThreadPoolExecutor
import subprocess
from bs4 import BeautifulSoup as soup

def runpowerreport():
	value = subprocess.Popen(['powercfg', '/batteryreport' ,'/output', 'test.html'])
	value.wait()
	file = open('test.html', 'r')
	my_soup = soup(file, 'html.parser')
	#result =  my_soup.findAll("tr", {"class": "odd dc 30"})[0]
	result = my_soup.findAll('table')[2].findAll('tr')[-1].findAll('td')
	time = result[0].findAll('span', {"class":"time"})[0].text
	percent = int(result[-2].text.split()[0])
	mwh = int(result[-1].text.split()[0].replace(',', ''))
	print(time)
	print(percent)
	print(mwh)

def process(p):
	batt_start = psutil.sensors_battery().secsleft
	for i in range(5):
		#randomNum = random.randrange(5)
		name = p[0].name()
		cpu_percent = p[0].cpu_percent(interval=0.1)
		battery = psutil.sensors_battery()
		if float(cpu_percent) > 0 and name != "System Idle Process":
			##do calculations here
			b= "Process: {}\nCPU: {}% Memory: {:2f}% Battery Used: {:0.2f}%\n".format(name, cpu_percent, p[0].memory_percent(),(battery.secsleft/p[1]))
			print(b)
			#pass
	#batt_diff = (batt_start - psutil.sensors_battery().secsleft) / p[1]
	#print("process: {} took battery {}".format(p[0].name(), batt_diff))


if __name__ == "__main__":
	executor = ThreadPoolExecutor()
	battery_life = psutil.sensors_battery()
	runpowerreport()
	#for i in psutil.process_iter():
		#executor.submit(process, (i,battery_life.secsleft))