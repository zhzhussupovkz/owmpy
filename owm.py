# -*- coding: utf-8 -*-

# The MIT License (MIT)

# Copyright (c) 2014 Zhussupov Zhassulan zhzhussupovkz@gmail.com

# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
# the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
# FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
# IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


import urllib
import urllib2
import json

# OWM
class OWM:

	def __init__(self, city = 'Pavlodar', country = 'kz'):
		self.city = city
		self.country = country
		self.weather_url = "http://api.openweathermap.org/data/2.5"

	# get main data
	def get_json_data(self, url):
		req = urllib2.Request(url)
		resp = urllib2.urlopen(req)
		try:
			page = json.loads(resp.read())
			resp.close()
			return page
		except:
			resp.close()
			return False

	# get weather data by city, country
	def get_weather_by_name(self, weather = 'current', query_args = {}):
		query_args = urllib.urlencode(query_args)
		if weather == 'current':
			url = "%s/weather?q=%s, %s" % (self.weather_url, self.city, self.country)
		elif weather == 'historical':
			url = "%s/history/city?q=%s,%s&%s" % (self.weather_url, self.city, self.country, query_args)
		return self.get_json_data(url)

	# get current weather by city id
	def get_weather_by_cityid(self, weather = 'current', city_id = 1520240, query_args = {}):
		if weather == 'historical':
			query_args['id'] = city_id
		query_args = urllib.urlencode(query_args)
		if weather == 'current':
			url = "%s/weather?id=%s" % (self.weather_url, city_id)
		elif weather == 'historical':
			url = "%s/history/city?%s" % (self.weather_url, query_args)
		return self.get_json_data(url)

	# get weather data by geo coords
	def get_current_weather_by_coords(self, lat = 35, lon = 139):
		url = "%s/weather?lat=%s&lon=%s" % (self.weather_url, lat, lon)
		return self.get_json_data(url)

	# data from cities within the defined rectangle specified by the geographic coordinates
	def get_current_weather_rect(self, left_lat = 12, left_lon = 32, right_lat = 15, right_lon = 37, zoom = 10):
		url = "%s/find/city/?bbox=%s,%s,%s,%s,%s" % (self.weather_url, left_lat, left_lon, right_lat, right_lon, zoom)
		return self.get_json_data(url)

	# data from cities laid within definite circle that is specified by center point and radius
	def get_current_weather_in_circle(self, lat = 55.5, lon = 37.5, cnt = 10):
		url = "%s/weather?lat=%s&lon=%s&cnt=%s" % (self.weather_url, lat, lon, cnt)
		return self.get_json_data(url)

	# historical data
	def get_historical_by_name(self, start = None, end = None, count = 10):
		q = {'start' : start, 'end' : end, 'cnt' : int(count)}
		q = dict((k,v) for k,v in q.iteritems() if v is not None)
		return self.get_weather_by_name(weather = 'historical', query_args = q)

	# current data
	def get_current_by_name(self):
		return self.get_weather_by_name(weather = 'current')

	# convert temperature
	def kelvin_to_celsius(self, temp):
		c = round(temp - 273.15, 2)
		return c
