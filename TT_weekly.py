import sys
sys.path.append('../../config_files/')
from tiktok_video_hash_data import main_collection,get_access_token
import argparse
from pathlib import Path
import pickle
import re
import os
import subprocess
import time
from datetime import datetime, timedelta, timezone


def get_start_end_dates(week_number, year):
    # Find the first day of the given year
    first_day = datetime(year, 1, 1)
    
    # Find the day of the week for January 1st (0: Monday, 6: Sunday)
    first_day_of_week = first_day.weekday()
    
    # Calculate the offset to the first day of the first week
    offset = (7 - first_day_of_week) % 7
    
    # Calculate the start date of the given week
    start_date = first_day + timedelta(days=offset + (week_number - 1) * 7)
    
    # Calculate the end date of the given week
    end_date = start_date + timedelta(days=6)
    
    # Return the start and end dates in the format YYYYMMDD
    return start_date.strftime('%Y%m%d'), end_date.strftime('%Y%m%d')

def time_until_midnight_utc():
    # Get current UTC time
    now_utc = datetime.now(timezone.utc)

    # Get midnight of the day after
    midnight_next_day_utc = datetime(now_utc.year, now_utc.month, now_utc.day, 0, 0, 0, tzinfo=timezone.utc) + timedelta(days=1)

    # Calculate time difference in seconds
    time_difference_seconds = (midnight_next_day_utc - now_utc).total_seconds()

    return time_difference_seconds


parser = argparse.ArgumentParser()
parser.add_argument("-t", "--hashtag", type=str,
                    help='Hashtag to look for, can be set to none',default=None)
parser.add_argument("-d","--day",type=str,
                    help='Date of the collection',default=None)
parser.add_argument("-f","--folder",type=str,
                    help='Target folder',default=None)
args = parser.parse_args()
#WE now perform data collection, we have a budget of 1k queries at day
if __name__ == "__main__":
    ACCESS_TOKEN = get_access_token()
    T = time.process_time() # get new access token every hour (good for 2 hours)
    
    a,b,c=2024,2025,1 #we set the period 
    counter_calls = 0 #count the queries
    for j in range(a,b,c):#iterate over the years
        
        ELAPSED = time.process_time() - T
        ELAPSED_HOURS = time.gmtime(ELAPSED).tm_hour
        if ELAPSED_HOURS > 0: # we use it to refresh the access token
            ACCESS_TOKEN = get_access_token()
            T = time.process_time()
        if not os.path.exists(f"{args.hashtag}/{args.day}/{j}"): 
            # if the directory is not present create it. 
            os.makedirs(f"{args.hashtag}/{args.day}/{j}")
        for i in range(6,8,1):#add here your weeks
            if(counter_calls >990):
                print(f'Performed {counter_calls} calls, we wait until midnight to begin again...')
                time.sleep(time_until_midnight_utc()+2)#wait until midnight UTC of the next day to proceed
                counter_calls=0 #reset the counter
                ACCESS_TOKEN = get_access_token()
            DATA_FILE = f'{args.hashtag}/{args.day}/{j}/{j}_{i}.json'
            CS_FILE = None
            START_DATE,END_DATE = get_start_end_dates(i,j)#the the coordinates of the week
            if(int(END_DATE)> j*10000+1231):#if the count of the week goes beyond the 
                END_DATE = f'{j}1231'#we set the last day to the 31 12 of the year
                i=54 #so that we know it will stop the cycle after the last collection
            print(f"Performing collection from {START_DATE} to {END_DATE}")
            main_collection(ACCESS_TOKEN,args.hashtag,1000,int(START_DATE),int(END_DATE),DATA_FILE,CS_FILE,IS_RANDOM=True)
            counter_calls += 1000
                
