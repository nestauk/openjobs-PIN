#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 12 11:57:20 2019

@author: stef
"""


#
# Copyright 2014 Google Inc. All rights reserved.
#
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License. You may obtain a copy of
# the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.
#

"""Tests for the directions module."""

import googlemaps
from datetime import datetime
import pickle
import numpy as np

key_file = '/Users/stefgarasto/Local-Data/sensitive-data/misc_keys.csv'
keys = pd.read_csv(key_file)
app_key = keys[keys['Key name']=='maps_api_key_old']['Key value']
gmaps = googlemaps.Client(key=app_key)

# Geocoding an address
#geocode_result = gmaps.geocode('SE23 2UN, UK')
#print(geocode_result)

# Look up an address with reverse geocoding
#reverse_geocode_result = gmaps.reverse_geocode((40.714224, -73.961452))
#print(reverse_geocode_result)

# Request directions via public transit
now = datetime.now()
for jj in range(0):
    for ii in range(0):
        directions_result = gmaps.directions("London Euston, UK",
                                             "SE{}, UK".format(jj),
                                             mode="transit",
                                             departure_time=now,
                                             region = 'gb',
                                             alternatives = True,
                                             language ='en-GB',
                                             units = 'metric',
                                             transit_mode = 'rail')
#%%
#Legend:
# subway = tube
# commuter train = overground
# bus = bus
# train = railway train
# get the duration + steps for all the routes:
Nroutes = len(directions_result)
routes_durations = []
routes_distances = []
routes_steps = []
for iroute in range(Nroutes):
    dct = directions_result[iroute]['legs'][0]
    routes_durations.append(dct['duration']['value']) #['text']
    routes_distances.append(dct['distance']['value'])
    routes_steps.append({})
    #routes_steps[iroute]['used_tube'] = False
    routes_steps[iroute]['used_bus'] = False
    routes_steps[iroute]['used_rail'] = False
    routes_steps[iroute]['total_walking_time'] = 0
    #routes_steps[iroute]['first_tube_station'] = ''
    #routes_steps[iroute]['last_tube_station'] = ''
    routes_steps[iroute]['first_rail_station'] = ''
    routes_steps[iroute]['last_rail_station'] = ''
    for istep in range(len(dct['steps'])):
        dct2 = dct['steps'][istep]
        travel_mode = (dct2['travel_mode'],
                       dct2['html_instructions'])
        if travel_mode[0] == 'TRANSIT' and 'bus' not in travel_mode[1].lower():
            routes_steps[iroute]['used_rail'] = True
            if routes_steps[iroute]['first_rail_station']== '':
                routes_steps[iroute]['first_rail_station'] = \
                        dct2['transit_details']['departure_stop']
            routes_steps[iroute]['last_rail_station'] = \
                    dct2['transit_details']['arrival_stop']
        elif travel_mode[0] == 'TRANSIT' and 'bus' in travel_mode[1].lower():
            routes_steps[iroute]['used_bus'] = True
        elif travel_mode[0] == 'WALKING':
            routes_steps[iroute]['total_walking_time'] += \
                dct2['duration']['value']

#%%
        '''
        if travel_mode[0] == 'TRANSIT' and 'Subway' in travel_mode[1]:
            routes_steps[iroute]['used_tube'] = True
            if routes_steps[iroute]['first_tube_station']== '':
                routes_steps[iroute]['first_tube_station'] = dct2['transit_details']['departure_stop']
            routes_steps[iroute]['last_tube_station'] = dct2['transit_details']['arrival_stop']

        elif travel_mode[0] == 'TRANSIT' and 'Commuter train' in travel_mode[1]:
            routes_steps[iroute]['used_tube'] = True
            if routes_steps[iroute]['first_tube_station']== '':
                routes_steps[iroute]['first_tube_station'] = dct2['transit_details']['departure_stop']
            routes_steps[iroute]['last_tube_station'] = dct2['transit_details']['arrival_stop']

        elif travel_mode[0] == 'TRANSIT' and 'Train' in travel_mode[1]:
            routes_steps[iroute]['used_rail'] = True
        '''

#Request distance matrix with public transit
lon_from= '-0.134649'
lat_from = '51.539258'
lat_from2 = '52.539258'
lon_to = '-0.088780'
lat_to = '51.506383'
origins = ["London Euston, UK", "SE19, UK",
           (lat_from,lon_from), [lat_from2, lon_from]]
destinations = ["Nottingham, UK",
                "London Victoria, UK",{'lat': lat_to, 'lng': lon_to}]


# TODO: change departure date/time using a string or datetime object

#%%
for ii in range(0):
    matrix = gmaps.distance_matrix(origins, destinations,
                                    mode="transit",
                                    language="en-GB",
                                    avoid="tolls",
                                    units="metric",
                                    departure_time=now)#,
                                    #traffic_model="optimistic")


#%% try to print the distance and the duration for all pairs of origins and destinations
distance = np.zeros((len(origins),len(destinations)))
duration = np.zeros((len(origins),len(destinations)))
for ii,iorig in enumerate(origins):
    orig_name = matrix['origin_addresses'][ii]
    for jj, jdest in enumerate(destinations):
        dest_name = matrix['destination_addresses'][jj]
        dct = matrix['rows'][ii]['elements'][jj]
        STATUS = dct['status']
        if STATUS == 'OK':
            distance[ii,jj] = dct['distance']['value']
            #['value'] gives the distance in meters,
            # 'text' gives a string in an appropriate distance
            duration[ii,jj] = dct['duration']['value']
            #['value'] gives time in seconds,
            # 'text' gives a string in an appriopriate measure (minutes, hours, etc)
            #print('Going from {} to {}.'.format(orig_name,dest_name))
            print('Takes {} to travel {}'.format(duration[ii,jj],distance[ii,jj]))


#%%
'''
# if I were to call the url it would be:
'https://maps.googleapis.com/maps/api/distancematrix/json?'
                    'origins=Perth%%2C+Australia%%7CSydney%%2C+Australia%%7C'
                    'Melbourne%%2C+Australia%%7CAdelaide%%2C+Australia%%7C'
                    'Brisbane%%2C+Australia%%7CDarwin%%2C+Australia%%7CHobart%%2C+'
                    'Australia%%7CCanberra%%2C+Australia'

                    '&language=en-GB&'

                    'avoid=tolls&mode=transit&key={KEY}&units=metric&'

                    'destinations=Uluru%%2C+Australia%%7CKakadu%%2C+Australia%%7C'
                    'Blue+Mountains%%2C+Australia%%7CBungle+Bungles%%2C+Australia'
                    '%%7CThe+Pinnacles%%2C+Australia'

                    &departure_time=%d'

'''
#%%
with open('res_from_google_api1.pickle','wb') as f:
    pickle.dump((directions_result,matrix),f)

# TODO: pickling doesn't work, I think there is a non-standard class hidden
# somewhere, might need to convert to standard python formats first

#%%
with open('res_from_google_api1.pickle','rb') as f:
    a = pickle.load(f)
