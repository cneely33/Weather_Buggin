# -*- coding: utf-8 -*-
"""
Created on Tue Jul  5 20:49:40 2016

@author: Christopher
"""
import smtplib, requests, bs4
from os import getenv
#import time, datetime
#from twilio.rest import TwilioRestClient
from mods.secrets import secrets

secrets.load_env_vars()

# zip code is 21046
from lxml import html

#zip code is 21046
res = requests.get('http://forecast.weather.gov/MapClick.php?lat=39.17512184649712&lon=-76.84004571823453')

#Check to see if the download worked
try:
    res.raise_for_status()
except Exception as exc:
    print('There was a problem: {exc}'.format(exc=exc))

###check the type of the request
#type(res)
###manual check to see if get worked
#res.status_code == requests.codes.ok 

#place text into BS4 object and html ojbect
WeatherSoup = bs4.BeautifulSoup(res.text, "lxml")
tree = html.fromstring(res.content)

#select desired element to parse for

pElems = tree.xpath('//*[@id="seven-day-forecast-list"]/li[2]/div/p[4]/text()')

#Get the conditions

condition = tree.xpath('//*[@id="seven-day-forecast-list"]/li[2]/div/p[3]/text()')
condition = str(condition[0])
#get the Temperature  
#######this will break if the temp goes over TODO: make it go from space to space######
tempRaw = str(pElems[0])
tempStr = tempRaw[6:8]
tempInt = int(tempRaw[6:8])


if tempInt >= 90:
    tempText = "Phew! It's going to be %s degrees tomorrow! That's almost as hot as Neely! Stay hydrated!" % tempStr
elif tempInt > 70 and tempInt < 90:
    tempText = "Tomorrow is going to be a steamy %s degrees! You're a big, tough boy though! You can handle that!" % tempStr
elif tempInt > 50 and tempInt < 70:
    tempText = "It's going to be a lovely %s degrees tomorrow! If only you had friends to go outside and enjoy they day with." % tempStr
elif tempInt > 30 and tempInt < 50:
    tempText = "It's going to be a chilly %s degrees tomorrow! Bring a light coat with you!" % tempStr
elif tempInt < 30:
    tempText = "Buuurrrr! It's going to be %s degrees tomorrow! Your micro is going to be smaller than ever!" % tempStr


################################################
######## Start Mail Portion of Project #########
################################################

#Create SMTP Object for Gmail
smtpObj = smtplib.SMTP('smtp.gmail.com', 587)

#Wake up the SMTP connection
smtpObj.ehlo()

#stat up TLS connection
smtpObj.starttls()

#Login to Gmail account
smtpObj.login('ruokjohn@gmail.com', getenv('analytics_pass'))

#send a test email
smtpObj.sendmail('ruokjohn@gmail.com', 'jtm3@g.clemson.edu', 
             'Subject: Tomorrow\'s Forecast! \nLooks like it is going to be {condition} Tomorrow!\n{tempText}'.format(condition=condition, tempText=tempText))
smtpObj.sendmail('ruokjohn@gmail.com', '3364135724@vtext.com', 
             'Looks like it is going to be {condition} Tomorrow! \n{tempText}'.format(condition=condition, tempText=tempText))
#close the SMTP connetion
smtpObj.quit()

################################################
######## Start SMS Portion of Project ##########
################################################
accountSID = getenv('twil_account')
authToken = getenv('twil_auth')

#twilioCli = TwilioRestClient(accountSID, authToken)

##myTwilioNumber = '+12259537214'
#myCellPhone = '+13364135724'

#message = twilioCli.messages.create(body='\nLooks like it is going to be %s Tomorrow!\n%s' % (condition, tempText), 
                                #from_=myTwilioNumber, to=myCellPhone)    

