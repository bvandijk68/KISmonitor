#!/usr/bin/python
# Pi controler for my boat, It sends status data to Ubidots.
# the Dashboard is here: https://app.ubidots.com/ubi/public/getdashboard/page/LtX75_ZWgkaYvIyo8KmAdvsOh38
# Written by Bas van Dijk, 2017 (vandijk.bastiaan@gmail.com)


# Load library for meteo I2C sensor
import Adafruit_BMP.BMP085 as BMP085

#load library to push http requests (needed for Ubidots)
import requests
import time

#Load library needed to communicate with Ubidots
from ubidots import ApiClient

# create an object that contains the meteo sensor data
sensor = BMP085.BMP085()

# These are the API keys that are given by Ubidots, needed to update data

TempSensorID='5882697e7625421e8a4e620b'
TimeIntervalSliderID='5882979e7625421e8a5032d1'
AlarmModeButtonID='588395a776254263119a4bd0'

# Create the API object used for pushing data to Ubidots
api=ApiClient(token='k87aANJuF15lflouIVzPqN9LkGcBgG')

# Variables that contain the data for Ubidots
tempvariable=api.get_variable(TempSensorID)

timervariable=api.get_variable(TimeIntervalSliderID)
alarmmodevariable=api.get_variable(AlarmModeButtonID)


while 1:  # do forever..
	
	temperature=sensor.read_temperature()   					# Read temperature from Meteo sensor

	print('Pushing Temp = {0:0.2f} *C'.format(temperature))  			# print to terminam (for debugging)
	
	response=tempvariable.save_value({"value":temperature})   	# This sends the temperature to Ubidots
	
	
	WaitTime=(timervariable.get_values(1)[0]['value'])  		# This is the Waittime in minutes
	print("waittime = "+ str(WaitTime))  						# Print to terminal for debugging
	WaitTime=int(WaitTime*6)									# Was real value but need integer, number of 10 seconds wait
	
	AlarmMode=alarmmodevariable.get_values(1)[0]["value"]
	if not(AlarmMode):											# When not in alarm mode wait for the specified time, when in alarm mode send update every 10 seconds
		for i in range(1,WaitTime+1):							# This waits for the next update value
			time.sleep(10)
			print(str(i)+ "of" +str(WaitTime) +" waitblocks passed till next update")
			AlarmMode=alarmmodevariable.get_values(1)[0]["value"] # Check is alarm has been activated
			if AlarmMode:
				print('alarm raised, exiting loop')
				break
				
	else:														# Alarmmode !!
		 time.sleep(10)
		 print('ALARM!!!')



