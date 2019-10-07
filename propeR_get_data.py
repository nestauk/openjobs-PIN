#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# imports needed for propeR
from rpy2.robjects import pandas2ri, numpy2ri
pandas2ri.activate()
numpy2ri.activate()
from rpy2.robjects.packages import importr
propeR = importr('propeR')

# general imports
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import time
import os
import pickle
from importlib import reload
import random
import tempfile
import shutil

# transport
import requests
import geopy.distance

#get_ipython().run_line_magic('matplotlib', 'inline')


# In[ ]:


# import all filenames (stored in a file that is in common to multiple scripts)
import all_filenames
from all_filenames import *


# In[ ]:


import utils_pin
from utils_pin import print_elapsed#, draw_map, draw_map_and_landmarks
importMAP = False
if importMAP:
    import maputils_pin
    from maputils_pin import draw_map, draw_map_and_landmarks

# argument parser
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--region', help='set which region/nation to use',
    default = 'em')
parser.add_argument('--modes', help='set which transport mode to use',
    default = 'car')
parser.add_argument('--ttwastart', help='ttwa index location from which to start OTP calls',
    default = 0, type = int)
parser.add_argument('--ttwaend', help='ttwa index location at which to end OTP calls',
    default = 1, type = int)
args = parser.parse_args()

# In[ ]:


# plot saving folder
plot_save_dir = '/Users/stefgarasto/Google Drive/Documents/results/PIN/plots/'
# file where I'm storing all the information
res_folder_local = savelocaloutput = '/Users/stefgarasto/Local-Data/Results/'
save_oa_file = res_folder+ 'PIN/oa_distances_and_occupations_v2.pickle'
save_oa_file_jobs = res_folder + 'PIN/oa_jobs_breakdown.pickle'
tmp_proper_folder = res_folder_local + 'PIN/tmp-propeR-data'
tmp_proper_results = res_folder_local + 'PIN/tmp-propeR-res'
FIGSAVE = False


# In[ ]:

t_start = time.time()

# first, load the list of all TTWA
ttwa_data = pd.read_csv(ttwa_file)
# first column is ttwa codes, second column is ttwa names
ttwa_info11 = pd.read_excel(ttwa_info11_file)
ttwa_info16 = pd.read_excel(ttwa_info16_file)
#print(ttwa_info11.tail(n=3))
#print(ttwa_info16.tail(n=3))

# get small TTWAs
small_ttwas = list(ttwa_info11['ttwa11cd'][ttwa_info11['LSOAs']<40])
print('There are {} TTWAs with less than 40 LSOAs.'.format(len(small_ttwas)))

# now set the ttwa code as the index
ttwa_data = ttwa_data.set_index('ttwa11cd')
ttwa_info11 = ttwa_info11.set_index('ttwa11cd')
ttwa_info16 = ttwa_info16.set_index('ttwa11cd')

# drop rows
ttwa_data = ttwa_data.drop(small_ttwas, axis = 0)
ttwa_info11 = ttwa_info11.drop(small_ttwas, axis = 0)
ttwa_info16 = ttwa_info16.drop([t for t in small_ttwas if t in ttwa_info16.index], axis = 0)
ttwa_info16 = ttwa_info16.sort_index()
ttwa_info11 = ttwa_info11.sort_index()
#ttwa_data['Region/Country'] = ttwa_info16['Region/Country']

'''
East Midlands:
0: Grantham 054
1: Peterborough 108
2: Spalding 124
3: Banbury 161
4: Boston 174
5: Burton upon Trent 183
6: Chesterfield 190
7: Corby 194
8: Derby 200
9: Grimsby 211
10: Kettering and Wellingborough 224
11: Leicester 230
12: Lincoln 231
13: Mansfield 240
14: Northampton 247 ***
15: Nottingham 249
16: Skegness and Louth 264
17: Worksop and Retford 291
'''

# Create aliases for the column names (need to be shorter to be plotted correctly)
rename_cols16 = {'Employment rate ': 'Employment rate',
       '% of economically inactive who want a job':'Job-seeking economically inactive',
       'Claimant Count, % aged 16-64, April 2015 to March 2016 ': 'Claimant count',
       'All in employment who are 1: managers, directors and senior officials (SOC2010)':
                 'Employed in SOC code 1',
       ' All in employment who are 2: professional occupations or 3: associate prof & tech occupations (SOC2010)':
                 'Employed in SOC code 2',
       'All in employment who are 5: skilled trades occupations (SOC2010)':
                 'Employed in SOC code 5',
       'All in employment who are 6: caring, leisure and other service occupations (SOC2010)':
                 'Employed in SOC code 6',
       'All in employment who are 8: process, plant and machine operatives (SOC2010)':
                 'Employed in SOC code 8',
       'All in employment who are 9: elementary occupations (SOC2010)':
                 'Employed in SOC code 9'}

rename_cols11 = {'Supply-side self-containment (% employed residents who work locally)':
                 'Supply-side self-containment',
       'Demand-side self-containment (% local jobs taken by local residents)':
                 'Demand-side self containment',
       'Number of economically active residents (aged 16+)':'Economically active residents'}
ttwa_info16.rename(rename_cols16, axis = 1, inplace = True)
ttwa_info11.rename(rename_cols11, axis = 1, inplace = True)

ttwa_data = ttwa_data.sort_index().join(ttwa_info11, rsuffix = '_2').join(ttwa_info16,
                                                                            rsuffix = '_3')

ttwa_data = ttwa_data.reset_index()


# In[ ]:


# load the extracted dictionaries of OA centroids
loadOA = True
loadLSOA = True
oa_path = ons_der_folder + 'oa_centroids_dictionary.pickle'
lsoa_path = ons_der_folder + 'lsoa_centroids_dictionary.pickle'
exists = os.path.isfile(oa_path)
if exists and loadOA:
    print('Loading the OA data')
    oa_data = pd.read_pickle(oa_path)
oa_data.rename(columns = {'long': 'lon'}, inplace = True)

exists = os.path.isfile(lsoa_path)
if exists and loadLSOA:
    print('Loading the LSOA data')
    lsoa_data = pd.read_pickle(lsoa_path)
lsoa_data.rename(columns = {'long': 'lon'}, inplace = True)

# Load the data dictionaries which then should be transformed to dataframes and joined.
# They should also be joined with the list of TTWAs for each OA
# Then, I can make the relevant plots
# What I want is a breakdown of mean travel distances for occupations and for ttwa

# first, load the data
with open(save_oa_file, 'rb') as f:
    _,_,oa_occupations,oa_residents,socGroups,_,_ = pickle.load(f)

with open(save_oa_file_jobs, 'rb') as f:
    _,oa_number_of_jobs,oa_jobs_breakdown,jobs_socGroups,_,_ = pickle.load(f)

print('Loaded LMIforALL data. Now joining')
t0 = time.time()
# join all dictionaries with oa_data and delete?
# first create the residents column and change the column title
oa_data = oa_data.join(pd.DataFrame.from_dict(oa_residents, orient = 'index'))
# now add everything else
oa_data.rename(columns = {0: 'residents'}, inplace = True)
oa_data = oa_data.join(
    pd.DataFrame.from_dict(oa_occupations, orient = 'index')).join(
    pd.DataFrame.from_dict(oa_number_of_jobs, orient = 'index')).join(
    pd.DataFrame.from_dict(oa_jobs_breakdown, orient = 'index'))
print('It took {:2f}s to create the full dataframe with {} rows'.format(time.time()- t0,
                                                                        len(oa_data)))
# finally, rename the number of jobs column
oa_data.rename(columns = {0: 'number of jobs'}, inplace = True)
print(oa_data.head(n=2))

oa_occupations = None
oa_residents = None
oa_number_of_jobs = None
oa_jobs_breakdown = None
print('Done')


# In[ ]:


print(list(ttwa_data.columns))


# In[ ]:


# set up propeR
# set the region to use
region2use = args.region #'wm'
region_names = {'wm': 'West Midlands', 'em': 'East Midlands',
    'ee': 'East of England', 'ne': 'North East', 'nw': 'North West',
    's': 'Scotland', 'w': 'Wales', 'ni': 'Northern Ireland',
    'se': 'South East', 'sw': 'South West',
    'y': 'Yorkshire and The Humber', 'gl': 'Greater London'}
region_name = region_names[region2use]
# open the connection to Open Trip Planner
otpcon = propeR.otpConnect(router = 'default_{}'.format(region2use))

# [TODO] how to check the connection is open?


# In[ ]:


# get all the TTWA in the region
regional_ttwa = ttwa_data[ttwa_data['Region/Country'] == region_name][['ttwa11cd','ttwa11nm','LSOAs']]
print(regional_ttwa)


# In[ ]:


print(lsoa_data.loc['E01008881'])#[lsoa_data['ttwa']==regional_ttwa['ttwa11cd'].iloc[0]])


# In[ ]:


def get_sample_oas(ttwa, origin_lsoa, destination_lsoa, oa_data, lsoa_data, n = 3):
    '''
    This function is needed to sample OAs to be origins and destinations when computing travel
    time between two LSOAs.
    I will sample n OAs in each LSOA (origin and destination) and return a dataframe with
    names and centroids of the selected OAs.
    '''
    oa_list_origin = lsoa_data.loc[origin_lsoa]['oa_list']
    oa_list_destination = lsoa_data.loc[destination_lsoa]['oa_list']
    # random selection of indices
    ix_origin = random.sample(range(0,len(oa_list_origin)), n)
    ix_destination = random.sample(range(0,len(oa_list_destination)), n)
    # get the corresponding OAs and add them to a dataframe
    tmp_origin = [oa_list_origin[t] for t in ix_origin]
    sampled_oa_origin = pd.DataFrame(tmp_origin, columns = ['name'])
    tmp_destination = [oa_list_destination[t] for t in ix_destination]
    sampled_oa_destination = pd.DataFrame(tmp_destination, columns = ['name'])
    sampled_oa_origin = pd.merge(sampled_oa_origin,
                            oa_data[['lat', 'lon', 'ttwa' ,'lsoa11']].loc[tmp_origin],
                            left_on = 'name', right_index = True)
    sampled_oa_destination = pd.merge(sampled_oa_destination,
                            oa_data[['lat', 'lon', 'ttwa' ,'lsoa11']].loc[tmp_destination],
                            left_on = 'name', right_index = True)
    # rename destinations and origins to make sure the name is a unique ID
    sampled_oa_destination['name'] = sampled_oa_destination['name'].map(lambda x : 'd' + x)
    sampled_oa_origin['name'] = sampled_oa_origin['name'].map(lambda x : 'o' + x)
    # reduce number of digits
    sampled_oa_origin['lon'] = sampled_oa_origin['lon'].map(lambda x: np.around(x,3))
    sampled_oa_origin['lat'] = sampled_oa_origin['lat'].map(lambda x: np.around(x,3))
    sampled_oa_destination['lon'] = sampled_oa_destination['lon'].map(lambda x: np.around(x,3))
    sampled_oa_destination['lat'] = sampled_oa_destination['lat'].map(lambda x: np.around(x,3))
    return sampled_oa_origin, sampled_oa_destination


def convert_to_propeR(locations, tmp_proper_folder, tmp_file_name = 'tmp_location_0.csv',
                      remove = False):
    '''
    This function is to save the dataframe as csv, reload it with propeR and then
    delete the file, if necessary
    '''
    locations.to_csv(os.path.join(tmp_proper_folder, tmp_file_name), index = False)
    # now reload them with propeR
    locations_df = propeR.importLocationData(os.path.join(tmp_proper_folder, tmp_file_name))
    if remove:
        os.remove(os.path.join(tmp_proper_folder, tmp_file_name))
    return locations_df


# get number of jobs in each LSOA
local_lsoas_number_of_jobs = {}
for t,ttwa in enumerate(regional_ttwa.index):
    local_lsoas_number_of_jobs[ttwa] = []
    t0 = time.time()
    ttwa_code = regional_ttwa['ttwa11cd'].loc[ttwa]
    local_lsoa = lsoa_data[lsoa_data['ttwa']==ttwa_code]
    for lsoa in local_lsoa.index:
        oa_list = local_lsoa['oa_list'].loc[lsoa]
        tot_lsoa_jobs = []
        for oa in oa_list:
            tot_lsoa_jobs.append(oa_data['number of jobs'].loc[oa])
        # add the absolute number of jobs
        local_lsoas_number_of_jobs[ttwa].append(sum(tot_lsoa_jobs))
        #local_lsoa_density_of_jobs.append(np.mean(tot_lsoa_jobs))
        #local_lsoa_max_of_jobs.append(max(tot_lsoa_jobs))
    # turn the list into a series
    local_lsoas_number_of_jobs[ttwa] = pd.DataFrame(local_lsoas_number_of_jobs[ttwa], columns = ['number of jobs'],
                                                   index= local_lsoa.index)


# In[ ]:
modes_dict = {'car': 'CAR', 'public': 'WALK, TRANSIT'}
modes = modes_dict[args.modes] #'WALK, TRANSIT'
istart = args.ttwastart
iend = args.ttwaend
f = open(res_folder_local + 'PIN/info_about_time_{}_{}_{}.txt'.format(region2use,istart,iend),'w')
print('Time spent before starting the calls to OTP: {:.4f}s'.format(time.time()- t_start), file =f)
# cycle through all TTWAs in West Midlands and all LSOAs (selecting top 20 destinations given number of jobs)
t_start_otp = time.time()
for t,ttwa in enumerate(regional_ttwa.index[istart:iend]):
    ttwa_code = regional_ttwa['ttwa11cd'].loc[ttwa]
    ttwa_name = regional_ttwa['ttwa11nm'].loc[ttwa]
    print('Analysing region {}, TTWA {} ({})'.format(region_name,
                ttwa_name, ttwa_code), file= f)
    print('Analysing region {}, TTWA {} ({})'.format(region_name,
                regional_ttwa['ttwa11nm'].loc[ttwa] , ttwa_code))
    local_lsoa = lsoa_data[lsoa_data['ttwa']==ttwa_code].join(local_lsoas_number_of_jobs[ttwa]).sort_values(
        'number of jobs', ascending = False)
    all_lsoas = list(local_lsoa.index)
    for to, origin_lsoa in enumerate(all_lsoas):
        t0 = time.time()
        # only compute travel times for the top 20 destinations
        for td, destination_lsoa in enumerate(all_lsoas[:20]):
            # select 3 random origins and destinations OA to get travel times for
            origin_oas, destination_oas = get_sample_oas(ttwa_code, origin_lsoa,
                                                destination_lsoa, oa_data,
                                                 lsoa_data, n = 2)
            # now convert them to propeR
            origins_df = convert_to_propeR(origin_oas, tmp_proper_folder, remove = False)
            destinations_df = convert_to_propeR(destination_oas, tmp_proper_folder)
            # create a uniquely named folder where to save the output, since I can't control
            # the name with which the output is stored
            directoryID = os.path.join(tmp_proper_results,
                                       'ttwa{}_{}/o{}_d{}_{}'.format(ttwa_code,modes.replace(',','').replace(' ',''),
                                                              origin_lsoa,
                                                              destination_lsoa,modes.replace(',','').replace(' ','')))
            if not os.path.exists(directoryID):
                os.makedirs(directoryID)
            else:
                # overwrite the directory (not sure it's the best method - but it's
                # basically the same as overwriting a file)
                #shutil.rmtree(directoryID)
                #os.makedirs(directoryID)
                # first check the directory is not empty
                contents = os.listdir(directoryID)
                if len(contents)>0:
                    continue
                else:
                    print(directoryID)
                    #stop
            # if more than 15 miles (i.e. 25 km then assume the journey takes too long - >25 minutes)
            if True:
                propeR.pointToPointLoop(directoryID, otpcon = otpcon,
                                        originPoints = origins_df,
                                        destinationPoints = destinations_df,
                                        startDateAndTime = '2019-06-26 07:30:00',
                                        modes = modes, journeyReturn = True,
                                       preWaitTime = 60)
            else:
                print('Skipping this pair')
                pd.Dataframe.from_dict({'skipping': 1}).to_csv(os.path.join(directoryID,
                                                            'PointToPointLoop_skipped.csv'))
            # destination loop
            print_elapsed(t0, 'destination {} for origin {}'.format(
                destination_lsoa,origin_lsoa))
            print('Time spent for destination {} for origin {} is {:.4f}'.format(
                destination_lsoa,origin_lsoa, time.time()-t0), file = f)
        # origin loop
        print('Done with origin number {} in {:.4f} s'.format(to,time.time()-t0))
        print('Done with origin number {} in {:.4f} s'.format(to,time.time()-t0), file= f)
    # TTWA loop
    print('Done with whole TTWA {} in {:.4f} s'.format(ttwa_name,time.time()-t0))
    print('Done with whole TTWA {} in {:.4f} s'.format(ttwa_name,time.time()-t0), file = f)

print('Total time since starting the OTP calls: {:.4f} s'.format(time.time()-t0))
print('Total time since starting the OTP calls: {:.4f} s'.format(time.time()-t0),
file = f)

#to,td
#all_lsoas.index(destination_lsoa)
