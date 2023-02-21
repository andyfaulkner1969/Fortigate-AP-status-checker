#!/usr/bin/env python3
import os 
import json
import datetime
#import ssl
import requests
import urllib3
import time
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

###########################################################################################
# This script will go to a Fortigate via the JSON and check the access points that are  
# connected.  It will give you the Name, ap profile, interface it's connected, state, status,
# os version installed number of clients.
# Created by Andy Faulkner afaulkner@fortinet.com a.k.a. The Evil Bastard
###########################################################################################

#  FGT and Token can be hard coded or input based.

token = "typGXXXXXXXXXXXXXXXwgz0s"
host = "x.x.x.x"
client_cnt_total = 0
ap_count = 0
time_sleep = 15
ap_name = ""
connected_count = 0


def ap_data_collect():
	global client_cnt_total, ap_list,ap_name
	connected_count = 0
	client_cnt_total = 0
	ap_count = 0
	url = "https://" + host +"/api/v2/monitor/wifi/managed_ap?access_token=" +token
	x = requests.get(url, verify=False)
	parsed_json = json.loads(x.text)
	#print(parsed_json)
	#print(parsed_json['results'][0])
	ap_count = len(parsed_json['results'])
	count = 0
	current_time = time.time()
#	print(current_time)
	lookback_time = current_time - 600 # 300 seconds is 5 minutes
#	print(lookback_time)
	
	
	while count < ap_count:
	#	print(count)
		try:
			ap_name = parsed_json['results'][count]['name']
		except:
			ap_name = "EMPTY"
		try:
			ap_profile = parsed_json['results'][count]['ap_profile']
		except:
			ap_profile = "EMPTY"
		try:
			state = parsed_json['results'][count]['state']
		except:
			state = "EMPTY"
		try:
			interface = parsed_json['results'][count]['connecting_interface']
		except:
			interface = "EMPTY"
		try:
			clients = parsed_json['results'][count]['clients']
			client_cnt_total = client_cnt_total + clients
		except:
			pass
		try:
			os_version = parsed_json['results'][count]['os_version']
		except:
			pass
		try:
			status = parsed_json['results'][count]['status']
			if status == "connected":
				connected_count = connected_count + 1
				status = "CONNECTED"
			else:
				pass
		except:
			pass
		try:
			join_time = parsed_json['results'][count]['join_time_raw']
#			print(join_time)
			if join_time >= lookback_time:
#				print(lookback_time)			print("AP NAME: " + ap_name)
				print("Name: " + ap_name + "    AP Profile: " + ap_profile + " Interface " + interface + "    State: " + state + "  Status: "+ status + "   Clients: " + str(clients))
#				try:
#					print("    OS_VER: " + os_version + "    Clients: " + str(clients))
#				except:
#					pass
			else:
				pass
	
		except:
			pass
		count = count + 1
#		print(count)
	return ap_count,connected_count,client_cnt_total

		

counter = 100
count_up = 0
while count_up != counter:

	return_data = ap_data_collect()
	print("_________________________________________________________")
	print("Total number of access points: " + str(return_data[0]))
	print("Number of connected access points: " + str(return_data[1]))
	print("Total Clents : " + str(return_data[2]))
#	print("_________________________________________________________")

	print("Sleeping for " + str(time_sleep) + " seconds.....")
	time.sleep(time_sleep)
	count_up = count_up + 1
	

	
