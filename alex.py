
#Grabs the top 8 processes and then scatters them across nodes
#The nodes need to be divisible by two and no greater than the amount of processes
import psutil
import sys
import math
import random
from concurrent.futures import ThreadPoolExecutor
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
	for i in psutil.process_iter():
		executor.submit(process, (i,battery_life.secsleft))