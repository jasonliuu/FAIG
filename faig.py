#IF YOU FOUND THIS USEFUL, Please Donate some Bitcoin .... 1FWt366i5PdrxCC6ydyhD8iywUHQ2C7BWC

#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import datetime
import requests
import json
import logging
import sys
import urllib
from time import time, sleep
import random
import time as systime
from statistics import mean, median
import numpy as np
# We are gonna use Scikit's LinearRegression model
from sklearn.linear_model import LinearRegression


#Joke here
#REAL_OR_NO_REAL = 'https://api.ig.com/gateway/deal'
REAL_OR_NO_REAL = 'https://demo-api.ig.com/gateway/deal'

API_ENDPOINT = "https://demo-api.ig.com/gateway/deal/session"
API_KEY = '**************************************'
data = {"identifier":"'**************************************'","password": "'**************************************'"}

# FOR REAL....
#API_ENDPOINT = "https://api.ig.com/gateway/deal/session"
#API_KEY = '**************************************'
#data = {"identifier":'**************************************',"password": '**************************************'}

headers = {'Content-Type':'application/json; charset=utf-8',
        'Accept':'application/json; charset=utf-8',
        'X-IG-API-KEY':API_KEY,
        'Version':'2'
		}

r = requests.post(API_ENDPOINT, data=json.dumps(data), headers=headers)
 
headers_json = dict(r.headers)
CST_token = headers_json["CST"]
print (R"CST : " + CST_token)
x_sec_token = headers_json["X-SECURITY-TOKEN"]
print (R"X-SECURITY-TOKEN : " + x_sec_token)

#GET ACCOUNTS
base_url = REAL_OR_NO_REAL + '/accounts'
authenticated_headers = {'Content-Type':'application/json; charset=utf-8',
        'Accept':'application/json; charset=utf-8',
        'X-IG-API-KEY':API_KEY,
        'CST':CST_token,
		'X-SECURITY-TOKEN':x_sec_token}

auth_r = requests.get(base_url, headers=authenticated_headers)
d = json.loads(auth_r.text)

# print(auth_r.status_code)
# print(auth_r.reason)
# print (auth_r.text)

for i in d['accounts']:
	if str(i['accountType']) == "SPREADBET":
		print ("Spreadbet Account ID is : " + str(i['accountId']))
		spreadbet_acc_id = str(i['accountId'])

#SET SPREAD BET ACCOUNT AS DEFAULT
base_url = REAL_OR_NO_REAL + '/session'
data = {"accountId":spreadbet_acc_id,"defaultAccount": "True"}
auth_r = requests.put(base_url, data=json.dumps(data), headers=authenticated_headers)

# print(auth_r.status_code)
# print(auth_r.reason)
# print (auth_r.text)
#ERROR about account ID been the same, Ignore! 

###################################################################################
##########################END OF LOGIN CODE########################################
##########################END OF LOGIN CODE########################################
##########################END OF LOGIN CODE########################################
##########################END OF LOGIN CODE########################################
###################################################################################

#HACKY/Weekend Testing - DO NOT USE!!! UNLESS YOU KNOW WHAT YOU ARE DOING!!
#epic_id = "CS.D.BITCOIN.TODAY.IP" #Bitcoin
#epic_id = "IX.D.SUNFUN.DAILY.IP" #Weekend Trading
#epic_id = "CS.D.ETHUSD.TODAY.IP" #Ether
#epic_id = "CS.D.BCHUSD.TODAY.IP" #Bitcoin Cash

#LIVE TEST
#epic_id = "CS.D.USCGC.TODAY.IP" #Gold - OK, Not Great
#epic_id = "CS.D.USCSI.TODAY.IP" #Silver - NOT RECOMMENDED 
#epic_id = "IX.D.FTSE.DAILY.IP" #FTSE 100 - Within Hours only, Profitable
#epic_id = "IX.D.DOW.DAILY.IP" #Wall St - Definitely Profitable between half 6 and half 8 GMT
epic_id = "CS.D.GBPUSD.TODAY.IP" # - Very Profitable 

# PROGRAMMABLE VALUES
# UNIT TEST FOR CRYPTO'S
# limitDistance_value = "1"
# orderType_value = "MARKET"
# size_value = "5"
# expiry_value = "DFB"
# guaranteedStop_value = True
# currencyCode_value = "GBP"
# forceOpen_value = True
# stopDistance_value = "150"

#UNIT TEST FOR OTHER STUFF
limitDistance_value = "4"
orderType_value = "MARKET"
size_value = "1"
expiry_value = "DFB"
guaranteedStop_value = True
currencyCode_value = "GBP"
forceOpen_value = True
stopDistance_value = "150" #Initial Stop loss, Worked out later per trade

base_url = REAL_OR_NO_REAL + '/markets/' + epic_id
auth_r = requests.get(base_url, headers=authenticated_headers)
d = json.loads(auth_r.text)

# print ("-----------------DEBUG-----------------")
# print(r.status_code)
# print(r.reason)
# print (r.text)
# print ("-----------------DEBUG-----------------")

MARKET_ID = d['instrument']['marketId']

#*******************************************************************
#*******************************************************************
#*******************************************************************
#*******************************************************************

TIME_WAIT_MULTIPLIER = 60
#STOP_LOSS_MULTIPLIER = 4 #Not currently in use, 13th Jan
#THIS IS STILL NOT GOOD ENOUGH TO TRADE ON, TAKE OPPOSITE TRADE?????
predict_accuracy = 0.80
profitable_trade_count = 0

print ("START TIME : " + str(datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f%Z")))

for times_round_loop in range(1, 9999):

#*******************************************************************
#*******************************************************************
#*******************************************************************
#*******************************************************************
	DO_A_THING = False
	while not DO_A_THING:
		#BUG HERE???
		#TIME_WAIT_MULTIPLIER = int(TIME_WAIT_MULTIPLIER) * int(times_round_loop)
		print ("!!DEBUG TIME Top of Loop!! : " + str(datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f%Z")))
		systime.sleep(random.randint(1, TIME_WAIT_MULTIPLIER))
		low_price_list = []
		high_price_list = []
		close_price_list = []
		volume_list = []
		# Your input data, X and Y are lists (or Numpy Arrays)
		#THIS IS YOUR TRAINING DATA
		x = [] #This is Low Price, Volume
		y = [] #This is High Price
		

		base_url = REAL_OR_NO_REAL + '/prices/'+ epic_id + '/MINUTE/10'
		# Price resolution (MINUTE, MINUTE_2, MINUTE_3, MINUTE_5, MINUTE_10, MINUTE_15, MINUTE_30, HOUR, HOUR_2, HOUR_3, HOUR_4, DAY, WEEK, MONTH)
		auth_r = requests.get(base_url, headers=authenticated_headers)
		d = json.loads(auth_r.text)
		
		# print ("-----------------DEBUG-----------------")
		# print(auth_r.status_code)
		# print(auth_r.reason)
		# print (auth_r.text)
		# print ("-----------------DEBUG-----------------")
		
		price_compare = "bid"

		for i in d['prices']:
			tmp_list = []
			high_price = i['highPrice'][price_compare]
			low_price = i['lowPrice'][price_compare]
			volume = i['lastTradedVolume']
			#---------------------------------
			tmp_list.append(float(low_price))
			tmp_list.append(float(volume))
			x.append(tmp_list)
			#x is Low Price and Volume
			y.append(float(high_price))
			#y = High Prices
			
		###################################################################################
		###################################################################################
		###################################################################################
		###################################################################################
		
		base_url = REAL_OR_NO_REAL + '/prices/'+ epic_id + '/MINUTE_2/10'
		# Price resolution (MINUTE, MINUTE_2, MINUTE_3, MINUTE_5, MINUTE_10, MINUTE_15, MINUTE_30, HOUR, HOUR_2, HOUR_3, HOUR_4, DAY, WEEK, MONTH)
		auth_r = requests.get(base_url, headers=authenticated_headers)
		d = json.loads(auth_r.text)
		
		# print ("-----------------DEBUG-----------------")
		# print(auth_r.status_code)
		# print(auth_r.reason)
		# print (auth_r.text)
		# print ("-----------------DEBUG-----------------")
		
		price_compare = "bid"

		for i in d['prices']:
			tmp_list = []
			high_price = i['highPrice'][price_compare]
			low_price = i['lowPrice'][price_compare]
			volume = i['lastTradedVolume']
			#---------------------------------
			tmp_list.append(float(low_price))
			tmp_list.append(float(volume))
			x.append(tmp_list)
			#x is Low Price and Volume
			y.append(float(high_price))
			#y = High Prices
			
		###################################################################################
		###################################################################################
		###################################################################################
		###################################################################################
		
		base_url = REAL_OR_NO_REAL + '/prices/'+ epic_id + '/MINUTE_3/10'
		# Price resolution (MINUTE, MINUTE_2, MINUTE_3, MINUTE_5, MINUTE_10, MINUTE_15, MINUTE_30, HOUR, HOUR_2, HOUR_3, HOUR_4, DAY, WEEK, MONTH)
		auth_r = requests.get(base_url, headers=authenticated_headers)
		d = json.loads(auth_r.text)
		
		# print ("-----------------DEBUG-----------------")
		# print(auth_r.status_code)
		# print(auth_r.reason)
		# print (auth_r.text)
		# print ("-----------------DEBUG-----------------")
		
		price_compare = "bid"

		for i in d['prices']:
			tmp_list = []
			high_price = i['highPrice'][price_compare]
			low_price = i['lowPrice'][price_compare]
			volume = i['lastTradedVolume']
			#---------------------------------
			tmp_list.append(float(low_price))
			tmp_list.append(float(volume))
			x.append(tmp_list)
			#x is Low Price and Volume
			y.append(float(high_price))
			#y = High Prices
		

		###################################################################################
		###################################################################################
		###################################################################################
		###################################################################################
		
		base_url = REAL_OR_NO_REAL + '/prices/'+ epic_id + '/MINUTE_5/10'
		# Price resolution (MINUTE, MINUTE_2, MINUTE_3, MINUTE_5, MINUTE_10, MINUTE_15, MINUTE_30, HOUR, HOUR_2, HOUR_3, HOUR_4, DAY, WEEK, MONTH)
		auth_r = requests.get(base_url, headers=authenticated_headers)
		d = json.loads(auth_r.text)
		
		# print ("-----------------DEBUG-----------------")
		# print(auth_r.status_code)
		# print(auth_r.reason)
		# print (auth_r.text)
		# print ("-----------------DEBUG-----------------")
		
		price_compare = "bid"

		for i in d['prices']:
			tmp_list = []
			high_price = i['highPrice'][price_compare]
			low_price = i['lowPrice'][price_compare]
			volume = i['lastTradedVolume']
			#---------------------------------
			tmp_list.append(float(low_price))
			tmp_list.append(float(volume))
			x.append(tmp_list)
			#x is Low Price and Volume
			y.append(float(high_price))
			#y = High Prices

		###################################################################################
		###################################################################################
		###################################################################################
		###################################################################################
		
		base_url = REAL_OR_NO_REAL + '/prices/'+ epic_id + '/MINUTE_10/10'
		# Price resolution (MINUTE, MINUTE_2, MINUTE_3, MINUTE_5, MINUTE_10, MINUTE_15, MINUTE_30, HOUR, HOUR_2, HOUR_3, HOUR_4, DAY, WEEK, MONTH)
		auth_r = requests.get(base_url, headers=authenticated_headers)
		d = json.loads(auth_r.text)
		
		# print ("-----------------DEBUG-----------------")
		# print(auth_r.status_code)
		# print(auth_r.reason)
		# print (auth_r.text)
		# print ("-----------------DEBUG-----------------")
		
		price_compare = "bid"

		for i in d['prices']:
			tmp_list = []
			high_price = i['highPrice'][price_compare]
			low_price = i['lowPrice'][price_compare]
			volume = i['lastTradedVolume']
			#---------------------------------
			tmp_list.append(float(low_price))
			tmp_list.append(float(volume))
			x.append(tmp_list)
			#x is Low Price and Volume
			y.append(float(high_price))
			#y = High Prices
		
		###################################################################################
		###################################################################################
		###################################################################################
		###################################################################################
		
		base_url = REAL_OR_NO_REAL + '/prices/'+ epic_id + '/MINUTE_15/10'
		# Price resolution (MINUTE, MINUTE_2, MINUTE_3, MINUTE_5, MINUTE_10, MINUTE_15, MINUTE_30, HOUR, HOUR_2, HOUR_3, HOUR_4, DAY, WEEK, MONTH)
		auth_r = requests.get(base_url, headers=authenticated_headers)
		d = json.loads(auth_r.text)
		
		# print ("-----------------DEBUG-----------------")
		# print(auth_r.status_code)
		# print(auth_r.reason)
		# print (auth_r.text)
		# print ("-----------------DEBUG-----------------")
		
		price_compare = "bid"

		for i in d['prices']:
			tmp_list = []
			high_price = i['highPrice'][price_compare]
			low_price = i['lowPrice'][price_compare]
			volume = i['lastTradedVolume']
			#---------------------------------
			tmp_list.append(float(low_price))
			tmp_list.append(float(volume))
			x.append(tmp_list)
			#x is Low Price and Volume
			y.append(float(high_price))
			#y = High Prices
		
		###################################################################################
		###################################################################################
		###################################################################################
		###################################################################################
		
		base_url = REAL_OR_NO_REAL + '/prices/'+ epic_id + '/MINUTE_30/10'
		# Price resolution (MINUTE, MINUTE_2, MINUTE_3, MINUTE_5, MINUTE_10, MINUTE_15, MINUTE_30, HOUR, HOUR_2, HOUR_3, HOUR_4, DAY, WEEK, MONTH)
		auth_r = requests.get(base_url, headers=authenticated_headers)
		d = json.loads(auth_r.text)
		
		# print ("-----------------DEBUG-----------------")
		# print(auth_r.status_code)
		# print(auth_r.reason)
		# print (auth_r.text)
		# print ("-----------------DEBUG-----------------")
		
		price_compare = "bid"

		for i in d['prices']:
			tmp_list = []
			high_price = i['highPrice'][price_compare]
			low_price = i['lowPrice'][price_compare]
			volume = i['lastTradedVolume']
			#---------------------------------
			tmp_list.append(float(low_price))
			tmp_list.append(float(volume))
			x.append(tmp_list)
			#x is Low Price and Volume
			y.append(float(high_price))
			#y = High Prices

		###################################################################################
		###################################################################################
		###################################################################################
		###################################################################################
		
		base_url = REAL_OR_NO_REAL + '/prices/'+ epic_id + '/HOUR/10'
		# Price resolution (MINUTE, MINUTE_2, MINUTE_3, MINUTE_5, MINUTE_10, MINUTE_15, MINUTE_30, HOUR, HOUR_2, HOUR_3, HOUR_4, DAY, WEEK, MONTH)
		auth_r = requests.get(base_url, headers=authenticated_headers)
		d = json.loads(auth_r.text)
		
		# print ("-----------------DEBUG-----------------")
		# print(auth_r.status_code)
		# print(auth_r.reason)
		# print (auth_r.text)
		# print ("-----------------DEBUG-----------------")
		
		price_compare = "bid"

		for i in d['prices']:
			tmp_list = []
			high_price = i['highPrice'][price_compare]
			low_price = i['lowPrice'][price_compare]
			volume = i['lastTradedVolume']
			#---------------------------------
			tmp_list.append(float(low_price))
			tmp_list.append(float(volume))
			x.append(tmp_list)
			#x is Low Price and Volume
			y.append(float(high_price))
			#y = High Prices
		
		
		###################################################################################
		###################################################################################
		###################################################################################
		###################################################################################
		
		base_url = REAL_OR_NO_REAL + '/prices/'+ epic_id + '/HOUR_2/10'
		# Price resolution (MINUTE, MINUTE_2, MINUTE_3, MINUTE_5, MINUTE_10, MINUTE_15, MINUTE_30, HOUR, HOUR_2, HOUR_3, HOUR_4, DAY, WEEK, MONTH)
		auth_r = requests.get(base_url, headers=authenticated_headers)
		d = json.loads(auth_r.text)
		
		# print ("-----------------DEBUG-----------------")
		# print(auth_r.status_code)
		# print(auth_r.reason)
		# print (auth_r.text)
		# print ("-----------------DEBUG-----------------")
		
		price_compare = "bid"

		for i in d['prices']:
			tmp_list = []
			high_price = i['highPrice'][price_compare]
			low_price = i['lowPrice'][price_compare]
			volume = i['lastTradedVolume']
			#---------------------------------
			tmp_list.append(float(low_price))
			tmp_list.append(float(volume))
			x.append(tmp_list)
			#x is Low Price and Volume
			y.append(float(high_price))
			#y = High Prices
		
		###################################################################################
		###################################################################################
		###################################################################################
		###################################################################################
		
		base_url = REAL_OR_NO_REAL + '/prices/'+ epic_id + '/HOUR_3/10'
		# Price resolution (MINUTE, MINUTE_2, MINUTE_3, MINUTE_5, MINUTE_10, MINUTE_15, MINUTE_30, HOUR, HOUR_2, HOUR_3, HOUR_4, DAY, WEEK, MONTH)
		auth_r = requests.get(base_url, headers=authenticated_headers)
		d = json.loads(auth_r.text)
		
		# print ("-----------------DEBUG-----------------")
		# print(auth_r.status_code)
		# print(auth_r.reason)
		# print (auth_r.text)
		# print ("-----------------DEBUG-----------------")
		
		price_compare = "bid"

		for i in d['prices']:
			tmp_list = []
			high_price = i['highPrice'][price_compare]
			low_price = i['lowPrice'][price_compare]
			volume = i['lastTradedVolume']
			#---------------------------------
			tmp_list.append(float(low_price))
			tmp_list.append(float(volume))
			x.append(tmp_list)
			#x is Low Price and Volume
			y.append(float(high_price))
			#y = High Prices
			
		###################################################################################
		###################################################################################
		###################################################################################
		###################################################################################
		
		base_url = REAL_OR_NO_REAL + '/prices/'+ epic_id + '/HOUR_4/10'
		# Price resolution (MINUTE, MINUTE_2, MINUTE_3, MINUTE_5, MINUTE_10, MINUTE_15, MINUTE_30, HOUR, HOUR_2, HOUR_3, HOUR_4, DAY, WEEK, MONTH)
		auth_r = requests.get(base_url, headers=authenticated_headers)
		d = json.loads(auth_r.text)
		
		# print ("-----------------DEBUG-----------------")
		# print(auth_r.status_code)
		# print(auth_r.reason)
		# print (auth_r.text)
		# print ("-----------------DEBUG-----------------")
		
		price_compare = "bid"

		for i in d['prices']:
			tmp_list = []
			high_price = i['highPrice'][price_compare]
			low_price = i['lowPrice'][price_compare]
			volume = i['lastTradedVolume']
			#---------------------------------
			tmp_list.append(float(low_price))
			tmp_list.append(float(volume))
			x.append(tmp_list)
			#x is Low Price and Volume
			y.append(float(high_price))
			#y = High Prices
			
		###################################################################################
		###################################################################################
		###################################################################################
		###################################################################################
		
		base_url = REAL_OR_NO_REAL + '/prices/'+ epic_id + '/DAY/10'
		# Price resolution (MINUTE, MINUTE_2, MINUTE_3, MINUTE_5, MINUTE_10, MINUTE_15, MINUTE_30, HOUR, HOUR_2, HOUR_3, HOUR_4, DAY, WEEK, MONTH)
		auth_r = requests.get(base_url, headers=authenticated_headers)
		d = json.loads(auth_r.text)
		
		# print ("-----------------DEBUG-----------------")
		# print(auth_r.status_code)
		# print(auth_r.reason)
		# print (auth_r.text)
		# print ("-----------------DEBUG-----------------")
		
		price_compare = "bid"

		for i in d['prices']:
			tmp_list = []
			high_price = i['highPrice'][price_compare]
			low_price = i['lowPrice'][price_compare]
			volume = i['lastTradedVolume']
			#---------------------------------
			tmp_list.append(float(low_price))
			tmp_list.append(float(volume))
			x.append(tmp_list)
			#x is Low Price and Volume
			y.append(float(high_price))
			#y = High Prices
		
		
		#-------------------------------------------------------------------------------
		#-------------------------------------------------------------------------------
		#-------------------------------------------------------------------------------
		#x Array is made up of pairs of Low prices and Volume, We can predict High price
		#-------------------------------------------------------------------------------
		#-------------------------------------------------------------------------------
		#-------------------------------------------------------------------------------
		#TESTING - GENERATE RANDOM NUMBER BETWEEN HIGH AND LOW VOL/PRICE FOR TESTING
		# PREDICT_x = 0
		# PREDICT_y = 0 
		# PREDICT_x = random.uniform(float(low_price), float(high_price))
		# PREDICT_y = random.uniform(min(volume_list), max(volume_list))
		# print ("DEBUG PREDICTION FOR .... : " + str(PREDICT_x))
		# print ("DEBUG PREDICTION FOR .... : " + str(PREDICT_y))
		#-------------------------------------------------------------------------------
		#-------------------------------------------------------------------------------
		#-------------------------------------------------------------------------------

		base_url = REAL_OR_NO_REAL + '/prices/'+ epic_id + '/DAY/1'
		# Price resolution (MINUTE, MINUTE_2, MINUTE_3, MINUTE_5, MINUTE_10, MINUTE_15, MINUTE_30, HOUR, HOUR_2, HOUR_3, HOUR_4, DAY, WEEK, MONTH)
		auth_r = requests.get(base_url, headers=authenticated_headers)
		d = json.loads(auth_r.text)
		#I only need this API call for real world values
		remaining_allowance = d['allowance']['remainingAllowance']
		
		print ("-----------------DEBUG-----------------")
		print ("Remaining API Calls left : " + str(remaining_allowance))
		print ("-----------------DEBUG-----------------")
		
		# print ("-----------------DEBUG-----------------")
		# print(auth_r.status_code)
		# print(auth_r.reason)
		# print (auth_r.text)
		# print ("-----------------DEBUG-----------------")

		for i in d['prices']:
			low_price = i['lowPrice'][price_compare]
			volume = i['lastTradedVolume']
		
		
		#####################################################################
		#########################PREDICTION CODE#############################
		#########################PREDICTION CODE#############################
		#########################PREDICTION CODE#############################
		#########################PREDICTION CODE#############################
		#########################PREDICTION CODE#############################
		#####################################################################
		
		print (x)
		print (y)
		
		x = np.asarray(x)
		y = np.asarray(y)
		# Initialize the model then train it on the data
		genius_regression_model = LinearRegression()
		genius_regression_model.fit(x,y)
		# Predict the corresponding value of Y for X
		pred_ict = [low_price,volume]
		pred_ict = np.asarray(pred_ict) #To Numpy Array, hacky but good!! 
		pred_ict = pred_ict.reshape(1, -1)
		price_prediction = genius_regression_model.predict(pred_ict)
		print ("PRICE PREDICTION FOR PRICE " + epic_id + " IS : " + str(price_prediction))


		score = genius_regression_model.score(x,y)
		predictions = {'intercept': genius_regression_model.intercept_, 'coefficient': genius_regression_model.coef_,   'predicted_value': price_prediction, 'accuracy' : score}
		print ("-----------------DEBUG-----------------")
		print (score)
		print (predictions)
		print ("-----------------DEBUG-----------------")
		
		#####################################################################
		#########################PREDICTION CODE#############################
		#########################PREDICTION CODE#############################
		#########################PREDICTION CODE#############################
		#########################PREDICTION CODE#############################
		#########################PREDICTION CODE#############################
		#####################################################################


		base_url = REAL_OR_NO_REAL + '/markets/' + epic_id
		auth_r = requests.get(base_url, headers=authenticated_headers)
		d = json.loads(auth_r.text)
		# print ("-----------------DEBUG-----------------")
		# print(auth_r.status_code)
		# print(auth_r.reason)
		# print (auth_r.text)
		# print ("-----------------DEBUG-----------------")
		current_price = d['snapshot']['bid']
		Price_Change_Day = d['snapshot']['netChange']
		price_diff = current_price - price_prediction
		
			
		#THIS IS GOOD AND ALL HOWEVER MARKET (IG) SOMETIMES REQUIRES HIGHER STOP LOSS, SEE HARD CODED VALUE
		# if int(Price_Change_Day) < 0:
			# stopDistance_value = int(Price_Change_Day)
			# stopDistance_value = stopDistance_value * -1
			# stopDistance_value = stopDistance_value - 1 #Not all the way
		# else:
			# stopDistance_value = int(stopDistance_value)
			# stopDistance_value = stopDistance_value - 1 #Not all the way
			
		print ("STOP LOSS DISTANCE WILL BE SET AT : " + str(stopDistance_value))
		print ("Price Difference Away (Point's) : " + str(price_diff))
		#MUST NOTE :- IF THIS PRICE IS - THEN BUY!! i.e NOT HIT TARGET YET, CONVERSELY IF THIS PRICE IS POSITIVE IT IS ALREADY ABOVE SO SELL!!!
		#MUST NOTE :- IF THIS PRICE IS - THEN BUY!! i.e NOT HIT TARGET YET, CONVERSELY IF THIS PRICE IS POSITIVE IT IS ALREADY ABOVE SO SELL!!!
		#MUST NOTE :- IF THIS PRICE IS - THEN BUY!! i.e NOT HIT TARGET YET, CONVERSELY IF THIS PRICE IS POSITIVE IT IS ALREADY ABOVE SO SELL!!!
		
		
		################################################################
		#########################ORDER CODE#############################
		#########################ORDER CODE#############################
		#########################ORDER CODE#############################
		#########################ORDER CODE#############################
		################################################################
		
		
		if profitable_trade_count < 15:
			if price_diff < 0 and score > predict_accuracy:
				DIRECTION_TO_TRADE = "SELL"
				DIRECTION_TO_CLOSE = "BUY"
				DIRECTION_TO_COMPARE = 'offer'
				DO_A_THING = True
			elif price_diff > 0 and score > predict_accuracy:
				#Keep going but keep it tight??
				limitDistance_value = "1"
				DIRECTION_TO_TRADE = "BUY"
				DIRECTION_TO_CLOSE = "SELL"
				DIRECTION_TO_COMPARE = 'bid'
				DO_A_THING = True
		elif profitable_trade_count > 15: #15, Trades ... profit. Right??? 
			profitable_trade_count = 0
			if price_diff < 0 and score > predict_accuracy:
				#Be Extra Sure, Set stop loss very tight???
				limitDistance_value = "1"
				DIRECTION_TO_TRADE = "BUY"
				DIRECTION_TO_CLOSE = "SELL"
				DIRECTION_TO_COMPARE = 'bid'
				DO_A_THING = True
			elif price_diff > 0 and score > predict_accuracy:
				limitDistance_value = "1"
				DIRECTION_TO_TRADE = "SELL"
				DIRECTION_TO_CLOSE = "BUY"
				DIRECTION_TO_COMPARE = 'offer'
				DO_A_THING = True
		
		print ("!!DEBUG TIME!! : " + str(datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f%Z")))
		################################################################
		#############Predict Accuracy isn't that great. ################
		#############Predict Accuracy isn't that great. ################
		#############Predict Accuracy isn't that great. ################
		#############Predict Accuracy isn't that great. ################
		################################################################
		Prediction_Wait_Timer = int(1800) #Wait 30 mins and Try again, Enough data should have changed to make a suitable prediction by then.
		#Be-careful after hours, After 5PM and 9PM GMT, Volumes are low yada yada yada. Less likely to get a decent prediction
		print ("!!DEBUG TIME!! : " + str(datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f%Z")))
		if price_diff < 0 and score < predict_accuracy: 
				DO_A_THING = False
				print ("!!DEBUG TIME!! Prediction Wait Algo: " + str(datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f%Z")))
				systime.sleep(Prediction_Wait_Timer)
				print ("!!DEBUG TIME!! Prediction Wait Algo: " + str(datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f%Z")))
		elif price_diff > 0 and score < predict_accuracy: #BUY
				DO_A_THING = False
				print ("!!DEBUG TIME!! Prediction Wait Algo: " + str(datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f%Z")))
				systime.sleep(Prediction_Wait_Timer)
				print ("!!DEBUG TIME!! Prediction Wait Algo: " + str(datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f%Z")))
			
		
		
	base_url = REAL_OR_NO_REAL + '/positions/otc'
	authenticated_headers = {'Content-Type':'application/json; charset=utf-8',
			'Accept':'application/json; charset=utf-8',
			'X-IG-API-KEY':API_KEY,
			'CST':CST_token,
			'X-SECURITY-TOKEN':x_sec_token}
			
	data = {"direction":DIRECTION_TO_TRADE,"epic": epic_id, "limitDistance":limitDistance_value, "orderType":orderType_value, "size":size_value,"expiry":expiry_value,"guaranteedStop":guaranteedStop_value,"currencyCode":currencyCode_value,"forceOpen":forceOpen_value,"stopDistance":stopDistance_value}
	r = requests.post(base_url, data=json.dumps(data), headers=authenticated_headers)
	
	print ("-----------------DEBUG-----------------")
	print(r.status_code)
	print(r.reason)
	print (r.text)
	print ("-----------------DEBUG-----------------")
		
		
	
	d = json.loads(r.text)
	deal_ref = d['dealReference']
	systime.sleep(2)
	# MAKE AN ORDER
	#CONFIRM MARKET ORDER
	base_url = REAL_OR_NO_REAL + '/confirms/'+ deal_ref
	auth_r = requests.get(base_url, headers=authenticated_headers)
	d = json.loads(auth_r.text)
	DEAL_ID = d['dealId']
	print("DEAL ID : " + str(d['dealId']))
	print(d['dealStatus'])
	print(d['reason'])
		
	# the trade will only break even once the price of the asset being traded has surpassed the sell price (for long trades) or buy price (for short trades). 
	#READ IN INITIAL PROFIT
		
	base_url = REAL_OR_NO_REAL + '/positions/'+ DEAL_ID
	auth_r = requests.get(base_url, headers=authenticated_headers)		
	d = json.loads(auth_r.text)
		
	print ("-----------------DEBUG-----------------")
	print(r.status_code)
	print(r.reason)
	print (r.text)
	print ("-----------------DEBUG-----------------")
	
	if DIRECTION_TO_TRADE == "SELL":
		PROFIT_OR_LOSS = float(d['position']['openLevel']) - float(d['market'][DIRECTION_TO_COMPARE])
		PROFIT_OR_LOSS = PROFIT_OR_LOSS * float(size_value)
		print ("Deal Number : " + str(times_round_loop) + " Profit/Loss : " + str(PROFIT_OR_LOSS))
	else:
		PROFIT_OR_LOSS = float(d['market'][DIRECTION_TO_COMPARE] - float(d['position']['openLevel']))
		PROFIT_OR_LOSS = PROFIT_OR_LOSS * float(size_value)
		print ("Deal Number : " + str(times_round_loop) + " Profit/Loss : " + str(PROFIT_OR_LOSS))
		
	
	#KEEP READING IN FOR PROFIT
	try:
		#while PROFIT_OR_LOSS < float(limitDistance_value): 
		while PROFIT_OR_LOSS < float(4.00): #Take something from the market, Before Take Profit.
			base_url = REAL_OR_NO_REAL + '/positions/'+ DEAL_ID
			auth_r = requests.get(base_url, headers=authenticated_headers)		
			d = json.loads(auth_r.text)
			
			while not int(auth_r.status_code) == 200:
				#Cannot read from API, Wait and try again
				#Give the Internet/IG 30s to sort it's shit out and try again
				systime.sleep(30)
				print ("HTTP API ERROR!! Try again...")
				#Got some "basic" error checking after all
				base_url = REAL_OR_NO_REAL + '/positions/'+ DEAL_ID
				auth_r = requests.get(base_url, headers=authenticated_headers)		
				d = json.loads(auth_r.text)
			
			
			if DIRECTION_TO_TRADE == "SELL":
				PROFIT_OR_LOSS = float(d['position']['openLevel']) - float(d['market'][DIRECTION_TO_COMPARE])
				PROFIT_OR_LOSS = float(d['position']['openLevel']) - float(d['market'][DIRECTION_TO_COMPARE])
				PROFIT_OR_LOSS = float(PROFIT_OR_LOSS * float(size_value))
				print ("Deal Number : " + str(times_round_loop) + " Profit/Loss : " + str(PROFIT_OR_LOSS))
				systime.sleep(2) #Don't be too keen to read price
			else:
				PROFIT_OR_LOSS = float(d['market'][DIRECTION_TO_COMPARE] - float(d['position']['openLevel']))
				PROFIT_OR_LOSS = float(PROFIT_OR_LOSS * float(size_value))
				print ("Deal Number : " + str(times_round_loop) + " Profit/Loss : " + str(PROFIT_OR_LOSS))
				systime.sleep(2) #Don't be too keen to read price
				
			# ARTIFICIAL_STOP_LOSS = int(size_value) * STOP_LOSS_MULTIPLIER
			# ARTIFICIAL_STOP_LOSS = ARTIFICIAL_STOP_LOSS * -1 #Make Negative, DO NOT REMOVE!!
			# print (PROFIT_OR_LOSS)
			# print (ARTIFICIAL_STOP_LOSS)
			
			# if PROFIT_OR_LOSS < ARTIFICIAL_STOP_LOSS:
				# #CLOSE TRADE/GTFO
				# print ("WARNING!! POTENTIAL DIRECTION CHANGE!!")
				# SIZE = size_value
				# ORDER_TYPE = orderType_value
				# base_url = REAL_OR_NO_REAL + '/positions/otc'
				# data = {"dealId":DEAL_ID,"direction":DIRECTION_TO_CLOSE,"size":SIZE,"orderType":ORDER_TYPE}
				# #authenticated_headers_delete IS HACKY AF WORK AROUND!! AS PER .... https://labs.ig.com/node/36
				# authenticated_headers_delete = {'Content-Type':'application/json; charset=utf-8',
				# 'Accept':'application/json; charset=utf-8',
				# 'X-IG-API-KEY':API_KEY,
				# 'CST':CST_token,
				# 'X-SECURITY-TOKEN':x_sec_token,
				# '_method':"DELETE"}
				# auth_r = requests.post(base_url, data=json.dumps(data), headers=authenticated_headers_delete)	
				# #DEBUG
				# print(r.status_code)
				# print(r.reason)
				# print (r.text)
				# systime.sleep(random.randint(1, TIME_WAIT_MULTIPLIER)) #Obligatory Wait before doing next order
						
	except Exception as e:
		print(e) #Yeah, I know now. 
		print ("ERROR : ORDER MIGHT NOT BE OPEN FOR WHATEVER REASON")
		#WOAH CALM DOWN! WAIT .... STOP LOSS MIGHT HAVE BEEN HIT
		systime.sleep(random.randint(1, TIME_WAIT_MULTIPLIER))
		pass
	
		#systime.sleep(1)
			
	if PROFIT_OR_LOSS > 0:
		profitable_trade_count = int(profitable_trade_count) + 1
		print ("DEBUG : ASSUME PROFIT!! Profitable Trade Count " + str(profitable_trade_count))
		SIZE = size_value
		ORDER_TYPE = orderType_value
		
		base_url = REAL_OR_NO_REAL + '/positions/otc'
		data = {"dealId":DEAL_ID,"direction":DIRECTION_TO_CLOSE,"size":SIZE,"orderType":ORDER_TYPE}
		#authenticated_headers_delete IS HACKY AF WORK AROUND!! AS PER .... https://labs.ig.com/node/36
		authenticated_headers_delete = {'Content-Type':'application/json; charset=utf-8',
				'Accept':'application/json; charset=utf-8',
				'X-IG-API-KEY':API_KEY,
				'CST':CST_token,
				'X-SECURITY-TOKEN':x_sec_token,
				'_method':"DELETE"}
		
		auth_r = requests.post(base_url, data=json.dumps(data), headers=authenticated_headers_delete)	
		#CLOSE TRADE
		print(auth_r.status_code)
		print(auth_r.reason)
		print (auth_r.text)
		
		# #CONFIRM CLOSE - FUTURE
		# base_url = REAL_OR_NO_REAL + '/confirms/'+ deal_ref
		# auth_r = requests.get(base_url, headers=authenticated_headers)
		# d = json.loads(auth_r.text)
		# DEAL_ID = d['dealId']
		# print("DEAL ID : " + str(d['dealId']))
		# print(d['dealStatus'])
		# print(d['reason'])
		
		systime.sleep(random.randint(1, TIME_WAIT_MULTIPLIER)) #Obligatory Wait before doing next order
