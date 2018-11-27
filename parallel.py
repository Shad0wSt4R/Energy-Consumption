import psutil
import sys
import math
from concurrent.futures import ThreadPoolExecutor
import subprocess
from bs4 import BeautifulSoup as soup
import datetime

def generateReport():
	value = subprocess.Popen(['powercfg', '/batteryreport' ,'/output', 'test.html'])
	return value
def runpowerreport():
	file = open('test.html', 'rb')
	my_soup = soup(file, 'html.parser')
	#result =  my_soup.findAll("tr", {"class": "odd dc 30"})[0]
	result = my_soup.findAll('table')[2].findAll('tr')[-1].findAll('td')
	time = result[0].findAll('span', {"class":"time"})[0].text
	time = datetime.datetime.strptime(time,"%H:%M:%S")#.strftime('%H:%M:%S')

	percent = int(result[-2].text.split()[0])
	mwh = int(result[-1].text.split()[0].replace(',', ''))
	print(time)
	print(percent)
	print(mwh)

	return time, percent, mwh

def process(p):
	current_time = datetime.datetime.now().minute
	while current_time < p[2].minute:
		name = p[0].name()
		cpu_percent = p[0].cpu_percent(interval=0.1)
		battery = psutil.sensors_battery()
		if float(cpu_percent) > 0 and name != "System Idle Process":
			##do calculations here
			if name in results:
				results[name].append(cpu_percent)
			else:
				results[name] = list([cpu_percent])
			b= "Process: {}\nCPU: {}% Memory: {:2f}%\n".format(name, cpu_percent, p[0].memory_percent())
			print(b)

		current_time = datetime.datetime.now().minute

def findmean(results, diff_mwh):
	for key, value in results.items():
		average = sum(value)/float(len(value))
		try:
			results[key] = (average/diff_mwh)
			print("{} used {} mWh".format(key, results[key]))
		except ZeroDivisionError as e:
			print("Power Consumption didnt change over time, unplug your charger")
	return results




if __name__ == "__main__":
	results = {}
	executor = ThreadPoolExecutor()
	battery_life = psutil.sensors_battery()
	process_gen_report = generateReport()
	process_gen_report.wait()
	time, per, mwh = runpowerreport()
	end_time = time + datetime.timedelta(minutes=4)
	for i in psutil.process_iter():
		future = executor.submit(process, (i,battery_life.secsleft, end_time))
	executor.shutdown(True)
	#print(results)

	process_gen_report = generateReport()
	process_gen_report.wait()
	time_new, per_new, mwh_new = runpowerreport()
	diff_mwh = abs(mwh_new - mwh)
	results = findmean(results, diff_mwh)
	#print(results)
input("Press Enter")