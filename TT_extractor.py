import sys
sys.path.append('config_files/')
from tiktok_video_hash_data import main_collection,get_access_token
import argparse
from pathlib import Path
import pickle
import re
import os
import subprocess
import time
from folders import base_folder

def extract_digits_from_string(input_string):
    # Use regular expression to find all digits in the string
    digits = re.findall(r'\d', input_string)
    
    # Convert the list of digits to a string
    result = ''.join(digits)
    
    return result

def read_pickle_files(folder: Path):
    """ Reads as tuples all pickle files that start with # in folder
    """
    files = list(folder.iterdir())
    rows = []
    digits = []
    #print(files)
    # Find the parquet file (usually starts with "part-")
    for file in files:
        if file.name.startswith("recover") and file.name.endswith(".pickle"):
            with open(str(folder)+'/'+file.name, 'rb') as f:
                rows.append(pickle.load(f))
            f.close()
        digits.append(int(extract_digits_from_string(file.name)))
    first_date = min(digits)
    last_date = max(digits)
    
    rows.append((first_date,last_date))
    return rows

def calc_dates(i,j):
    if i<10: # for now we just check untile the 30 of the month, the residual 31 will be taken another time
        START_DATE = f'{j}0{i}01'
        if(i==2):
            END_DATE = f'{j}0{i}28'
        else:
            END_DATE = f'{j}0{i}30'
    else:
        START_DATE = f'{j}{i}01'
        END_DATE = f'{j}{i}30'
    return START_DATE,END_DATE

parser = argparse.ArgumentParser()
parser.add_argument("-by", "--begin_year", type=int,
                    help='First year of the extraction',default=None)
parser.add_argument("-fy", "--finish_year", type=int,
                    help='Last year of the extraction',default=None)                    
parser.add_argument("-n", "--num_queries", type=str,
                    help='How many queries to perform by month',default=None)
parser.add_argument("-rnd", "--random", action='store_true',
                    help='Return random results',default=False)
parser.add_argument("-d","--day",type=str,
                    help='Date of the collection',default=None)
args = parser.parse_args()

#REMEMBER ABOUT THE QUERY BUDGET!

if __name__ == "__main__":
    ACCESS_TOKEN = get_access_token()
    T = time.process_time() # get new access token every hour (good for 2 hours)
    if(args.random is False):
        raise Exception('Not implemented, will be available in a future commit!')
    else:#we do the random sample 
        a,b,c=args.begin_year,args.finish_year,1 #we set the period 
        for j in range(a,b,c):#iterate over the years
            ELAPSED = time.process_time() - T
            ELAPSED_HOURS = time.gmtime(ELAPSED).tm_hour
            if ELAPSED_HOURS > 0: # we use it to refresh the access token
                ACCESS_TOKEN = get_access_token()
                T = time.process_time()
            if not os.path.exists(f"{base_folder}/data/random_sample_historical/{args.day}/{j}"): 
                # if the demo_folder directory is not present  
                # then create it. 
                os.makedirs(f"{base_folder}/data/random_sample_historical/{args.day}/{j}")
                os.makedirs(f"{base_folder}/historical/{args.day}/{j}")
            for i in range(1,13,1):#from 1 to 12 ->  months
                    DATA_FILE = f'{base_folder}/data/random_sample_historical/{args.day}/{j}/{j}_{i}.json'
                    CS_FILE = f'{base_folder}/historical/{args.day}/{j}/recover_{j}_{i}.pickle'
                    START_DATE,END_DATE = calc_dates(i,j)
                    print(f"Performing collection from {START_DATE} to {END_DATE}")
                    main_collection(ACCESS_TOKEN,None,args.num_queries,int(START_DATE),int(END_DATE),DATA_FILE,CS_FILE,IS_RANDOM=True)