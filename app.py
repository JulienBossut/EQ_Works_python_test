# -*- coding: utf-8 -*-

import os
from flask import Flask, jsonify
import sqlalchemy
import threading

FIFTEEN_MINUTES = 120 

# web app
app = Flask(__name__)

# database engine
engine = sqlalchemy.create_engine(os.getenv('SQL_URI'))

def resetCalls():
	global eventsHourlyC
	global eventsDailyC 
	global statsHourlyC 
	global statsDailyC
	global poiC
	eventsHourlyC =0
	eventsDailyC = 0
	statsHourlyC = 0
	statsDailyC = 0
	poiC = 0
	t = threading.Timer(120.0, resetCalls)
	t.start()
    
t = threading.Timer(120.0, resetCalls)
t.start()

eventsHourlyC =0
eventsDailyC = 0
statsHourlyC = 0
statsDailyC = 0
poiC = 0

@app.route('/')
def index():
	

	return 'Welcome to EQ Works 😎'


@app.route('/events/hourly')
def events_hourly():
	global eventsHourlyC
	if eventsHourlyC == 15 :
		return "too much calls"
	else :	
		eventsHourlyC += 1		
		return queryHelper('''
			SELECT date, hour, events
			FROM public.hourly_events
			ORDER BY date, hour
			LIMIT 168;
		''')
		



@app.route('/events/daily')
def events_daily():
	global eventsDailyC
	if eventsDailyC == 15 :
		return "too much calls"
	else :	
		eventsDailyC += 1		
		return queryHelper('''
		    SELECT date, SUM(events) AS events
		    FROM public.hourly_events
		    GROUP BY date
		    ORDER BY date
		    LIMIT 7;
		''')


@app.route('/stats/hourly')
def stats_hourly():
	global statsHourlyC
	if statsHourlyC == 15 :
		return "too much calls"
	else :	
		statsHourlyC += 1	
		return queryHelper('''
		    SELECT date, hour, impressions, clicks, revenue
		    FROM public.hourly_stats
		    ORDER BY date, hour
		    LIMIT 168;
		''')


@app.route('/stats/daily')
def stats_daily():
	global statsDailyC
	if statsDailyC == 15 :
		return "too much calls"
	else :	
		statsDailyC += 1	
		return queryHelper('''
		    SELECT date,
		        SUM(impressions) AS impressions,
		        SUM(clicks) AS clicks,
		        SUM(revenue) AS revenue
		    FROM public.hourly_stats
		    GROUP BY date
		    ORDER BY date
		    LIMIT 7;
		''')


@app.route('/poi')
def poi():
	global poiC
	if poiC == 15 :
		return "too much calls"
	else :	
		poiC += 1	
		return queryHelper('''
		    SELECT *
		    FROM public.poi;
		''')

def queryHelper(query):
    with engine.connect() as conn:
        result = conn.execute(query).fetchall()
        return jsonify([dict(row.items()) for row in result])
