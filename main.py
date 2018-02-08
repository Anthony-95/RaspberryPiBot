#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
#System Info, Time, External Calls
import psutil , time
import requests, json
#Random Numbers
from random import randint
#Twitter API
from twython import Twython
#Pyjockes Lib
import pyjokes

#Define our constant variables.
CONSUMER_KEY = ''
CONSUMER_SECRET = ''
ACCESS_KEY = ''
ACCESS_SECRET = ''

#AccuWeather constants
ACCU_ACCOUNT_KEY = ''
CITY_LOCATION_KEY = 310683 # Valencia

#Create a copy of the Twython object with all our keys and secrets to allow easy commands.
api = Twython(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_KEY, ACCESS_SECRET) 

#We have five options to post a tweet, using a random number we choose what to do
op = randint(1, 100)

# 1. Print usage of CPU, RAM, HDD, RED & UPTIME => 22% of probability
if op < 23:
    cpu = psutil.cpu_percent(interval = 1)
    aux = psutil.virtual_memory()
    #Operation to get the percentage
    ram = aux.total / aux.used
    disk = psutil.disk_usage('/')
    net = psutil.net_connections()
    upT = time.time() - psutil.boot_time()
    #Calculate times individually
    upTm, upTs = divmod(upT, 60)
    upTh, upTm = divmod(upTm, 60)
    # ---------------- PRETTY TIME ---------------- #
    #prints hours
    if upTh == 1:
        ttime = "hace una hora"
    elif upTh > 1:
        ttime = "hace " + str(int(upTh)) + " horas"
    #prints minutes
    if upTm == 1:
        if 'ttime' in vars():
            ttime += " y un minuto"
        else:
            ttime = "hace un minuto"
    elif upTm > 1:
        if 'ttime' in vars():
            ttime += " y " + str(int(upTm)) + " minutos"
        else:
            ttime = "hace " + str(int(upTm)) + " minutos"
    #prints when time < 1 min
    if 'ttime' not in vars():
        ttime = "ahora mismo"
    # ---------------- PRETTY TIME ---------------- #

    tweet = "Ahora mismo estoy usando un {}% de CPU, {}% de RAM, {}% de disco, tengo {} conexiones \
de red abiertas y me he encendido {}".format(cpu, float(ram), disk.percent, len(net), ttime)

# 2. Weather in Valencia, Spain => 20% of probability
if op > 22 and op < 43:
    #get info of the weather from AccuWeather.com
    accu_baseURL = 'http://dataservice.accuweather.com/'
    payload = {'apikey': ACCU_ACCOUNT_KEY, 'language': 'es-es', 'details': 'false'}
    r = requests.get(accu_baseURL + "/currentconditions/v1/" + str(CITY_LOCATION_KEY), params = payload)
    responseJSON = json.loads(r.content)
    #string conversion
    data = " ºC de temperatura. Más info: "
    udata = data.decode("utf-8")

    tweet = "En estos momentos el tiempo en Valencia es " + responseJSON[0]['WeatherText'] + \
    " y estamos a " + str(responseJSON[0]['Temperature']['Metric']['Value']) + udata + responseJSON[0]['Link']

# 3. Pyjokes (ALL) => 25% of probability
if op > 42 and op < 68:
    tweet = pyjokes.get_joke(category = "all")
 
# 4. TT in Spain => 33% of probability
if op > 67:
   ttresults = api.get_place_trends(id = 23424950)
   rand = randint(1, len(ttresults[0]['trends']) - 2)
   
   tweet = "Parece que {}, {} y {} son Trending Topics en España".format(ttresults[0]['trends'][0]['name'], 
   ttresults[0]['trends'][rand]['name'], ttresults[0]['trends'][len(ttresults[0]['trends']) - 1]['name'])

#Finally upload the tweet
api.update_status(status=tweet)
#End