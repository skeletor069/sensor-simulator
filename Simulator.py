import time
import random
from urllib.parse import urlencode
from urllib.request import Request, urlopen
import json
import requests

timescale = 600
min_stay_time = (30 * 60)
max_stay_time = (240 * 60)
# base_url = "http://ec2-52-29-117-217.eu-central-1.compute.amazonaws.com:8080"
base_url = "http://localhost:8080"


class Parking:
	def __init__(self, parking_id):
		self.parking_id = parking_id
		self.state = random.randint(0,1)
		self.ticks_to_change_state = 1
		self.ticks_gone = 0
		self.url = base_url + '/parkingInformation/'+str(self.parking_id)+'/currentParkingState/'
		self.data = {}
		self.data["parkingState"] = str(self.state)
		self.data["sensorState"] = "1"
		print(self.url)

	def update(self):
		self.ticks_gone = self.ticks_gone + 1
		# print(self.parking_id, " ", self.ticks_to_change_state, " ", self.ticks_gone)
		if self.ticks_gone >= self.ticks_to_change_state:
			self.changeState()
			self.ticks_to_change_state = random.randint(min_stay_time, max_stay_time)
			self.ticks_gone = 0

	def changeState(self):
		self.state = abs(self.state - 1)
		print(self.parking_id, " : state changed to ", self.state)
		self.apiCall()
		print("-------------------------------------------------")

	def apiCall(self):
		self.data["parkingState"] = self.state
		headers = {
			'content-type': 'application/json; charset=utf-8',
			'Access-Control-Allow-Credentials' : 'true',
        	'Access-Control-Allow-Origin':'*',
        	'Access-Control-Allow-Headers':'application/json',
		}
		resp = requests.post(self.url, data = json.dumps(self.data), headers = headers)
		print(self.parking_id, " calling api with state ", self.state)
		print(resp)
		# try:
		# 	self.data["parkingState"] = self.state
		# 	headers = {
		# 		'content-type': 'application/json; charset=utf-8',
		# 		'Access-Control-Allow-Credentials' : 'true',
  #           	'Access-Control-Allow-Origin':'*',
  #           	'Access-Control-Allow-Headers':'application/json',
		# 	}
		# 	resp = requests.post(self.url, data = json.dumps(self.data), headers = headers)
		# 	print(self.parking_id, " calling api with state ", self.state)
		# 	print(resp)
		# except:
		# 	print("could not call api")



parking_list = []
parking_list.append(Parking(1))
parking_list.append(Parking(2))
parking_list.append(Parking(3))
parking_list.append(Parking(4))
parking_list.append(Parking(5))
parking_list.append(Parking(6))
parking_list.append(Parking(7))
parking_list.append(Parking(8))
parking_list.append(Parking(9))
parking_list.append(Parking(10))
parking_list.append(Parking(11))
parking_list.append(Parking(12))

while 1:
	for parking in parking_list:
		parking.update()

	time.sleep(1.0/timescale)


