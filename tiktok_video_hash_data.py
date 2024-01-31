import requests
import json
import time
import sys
sys.path.append('config_files/')
from dotenv import load_dotenv
import os
import pickle
from folders import env_folder

ALL_FIELDS = 'id,video_description,create_time, region_code,share_count,view_count,like_count,\
    comment_count, music_id,hashtag_names, username,effect_ids,playlist_id,voice_to_text'
"""
FUNCTION TO GET ACCESS TOKEN
"""

def get_access_token():
    load_dotenv(env_folder)
    CLIENT_KEY = os.getenv('C_KEY') ## substitute with your client key
    CLIENT_SECRET = os.getenv('C_SECRET') ## substitute with your secret key
    r = requests.post('https://open.tiktokapis.com/v2/oauth/token/',
                      headers={'Content-Type': 'application/x-www-form-urlencoded',
                           'Cache-Control': 'no-cache'
                      },
                      data={'client_key':CLIENT_KEY,
                           'client_secret':CLIENT_SECRET,
                           'grant_type':'client_credentials'})
    ACCESS_TOKEN = r.json()['access_token']
    return ACCESS_TOKEN

"""
WRITE DATA TO FILE
"""
def write_data(DATA_FILE,DATA_LIST):
    with open(DATA_FILE, 'w') as f:
        json.dump(DATA_LIST, f, indent=2)

"""
QUERY
"""
def query(query,start_date,end_date,max_count,access_token,cursor=None,search_id=None,is_random = None):
    if(cursor is None or search_id is None):#new search
        D = requests.post('https://open.tiktokapis.com/v2/research/video/query/?fields=%s'%ALL_FIELDS,
                                    headers = {'authorization':'bearer '+access_token},
                                    data = {'query':json.dumps(query),
                                        'start_date':start_date,
                                        'end_date':end_date,
                                        'max_count':max_count,
                                        'is_random':is_random
                                        }
            )
    elif(cursor is not None and search_id is not None):
        D = requests.post('https://open.tiktokapis.com/v2/research/video/query/?fields=%s'%ALL_FIELDS,
                                    headers = {'authorization':'bearer '+access_token},
                                    data = {'query':json.dumps(query),
                                        'start_date':start_date,
                                        'end_date':end_date,
                                        'max_count':max_count,
                                        'cursor':cursor,
                                        'search_id':search_id,
                                        'is_random':is_random}
            )
    else:
        raise Exception("CURSOR or SEARCH_ID is None")
    return D

"""
START DATA COLLECTION
"""
def data_collection(ACCESS_TOKEN,HASH_SEARCH=None,MAX_QUERIES=100,START_DATE=20230101,END_DATE=20230101,CURSOR=None,SEARCH_ID=None,IS_RANDOM = False):
    #T = time.process_time() # get new access token every hour (good for 2 hours)

    """
    QUERY: all videos with hashtags provided in argument list
    ..feel free to customize!
    """
    if HASH_SEARCH != None:
        QUERY = {
            'and':[{
            'operation':'EQ',
            'field_name':'hashtag_name',
            'field_values': [HASH_SEARCH] #here we pass the hashtag
            },     
            {
            "operation": "IN",
            "field_name": "region_code",
            "field_values": ["US"] # we look for videos posted only in the US
            }
            ],
            "not": [
                {
                        "operation": "IN",
                        "field_name": "video_length",
                        "field_values": ["SHORT","MID"]#exclude videos under 1 min of length
                }
                ]
        }
    else:
        QUERY = {
            'and':[
            {
            "operation": "IN",
            "field_name": "region_code",
            "field_values": ['FR', 'TH', 'MM', 'BD', 'IT', 'NP', 'IQ', 'BR', 'US', 'KW', 'VN', 'AR', 'KZ', 'GB', 'UA', 'TR', 'ID', 'PK', 'NG', 'KH', 'PH', 'EG', 'QA', 'MY', 'ES', 'JO', 'MA', 'SA', 'TW', 'AF', 'EC', 'MX', 'BW', 'JP', 'LT', 'TN', 'RO', 'LY', 'IL', 'DZ', 'CG', 'GH', 'DE', 'BJ', 'SN', 'SK', 'BY', 'NL', 'LA', 'BE', 'DO', 'TZ', 'LK', 'NI', 'LB', 'IE', 'RS', 'HU', 'PT', 'GP', 'CM', 'HN', 'FI', 'GA', 'BN', 'SG', 'BO', 'GM', 'BG', 'SD', 'TT', 'OM', 'FO', 'MZ', 'ML', 'UG', 'RE', 'PY', 'GT', 'CI', 'SR', 'AO', 'AZ', 'LR', 'CD', 'HR', 'SV', 'MV', 'GY', 'BH', 'TG', 'SL', 'MK', 'KE', 'MT', 'MG', 'MR', 'PA', 'IS', 'LU', 'HT', 'TM', 'ZM', 'CR', 'NO', 'AL', 'ET', 'GW', 'AU', 'KR', 'UY', 'JM', 'DK', 'AE', 'MD', 'SE', 'MU', 'SO', 'CO', 'AT', 'GR', 'UZ', 'CL', 'GE', 'PL', 'CA', 'CZ', 'ZA', 'AI', 'VE', 'KG', 'PE', 'CH', 'LV', 'PR', 'NZ', 'TL', 'BT', 'MN', 'FJ', 'SZ', 'VU', 'BF', 'TJ', 'BA', 'AM', 'TD', 'SI', 'CY', 'MW', 'EE', 'XK', 'ME', 'KY', 'YE', 'LS', 'ZW', 'MC', 'GN', 'BS', 'PF', 'NA', 'VI', 'BB', 'BZ', 'CW', 'PS', 'FM', 'PG', 'BI', 'AD', 'TV', 'GL', 'KM', 'AW', 'TC', 'CV', 'MO', 'VC', 'NE', 'WS', 'MP', 'DJ', 'RW', 'AG', 'GI', 'GQ', 'AS', 'AX', 'TO', 'KN', 'LC', 'NC', 'LI', 'SS', 'IR', 'SY', 'IM', 'SC', 'VG', 'SB', 'DM', 'KI', 'UM', 'SX', 'GD', 'MH', 'BQ', 'YT', 'ST', 'CF', 'BM', 'SM', 'PW', 'GU', 'HK', 'IN', 'CK', 'AQ', 'WF', 'JE', 'MQ', 'CN', 'GF', 'MS', 'GG', 'TK', 'FK', 'PM', 'NU', 'MF', 'ER', 'NF', 'VA', 'IO', 'SH', 'BL', 'CU', 'NR', 'TP', 'BV', 'EH', 'PN', 'TF', 'RU'] # we look for videos posted only in the US
            }
            ]
        }

    """
    MAKE INITIAL QUERY
    """
    if(not IS_RANDOM):#apparently, for  random query we do not have pagination
        try:
            D = query(QUERY,START_DATE,END_DATE,100,ACCESS_TOKEN,CURSOR,SEARCH_ID,IS_RANDOM)#THE CHECK IS DONE AFTER IN THE QUERY FUNCTION
            SEARCH_ID = D.json()['data']['search_id']
        except:
            print('We had an error!!')
            #print(D.json()['error'])
            #print(D.json())
            #print(START_DATE)
            exit()
        CURSOR = D.json()['data']['cursor']
        DATA_LIST = [D.json()]
    else:#if it is random, we perform everything in here since we don't have meaning to use the CURSOR AND SEARCH ID
        DATA_LIST = []
        for i in range(1,MAX_QUERIES,1):
            try:
                D = query(QUERY,START_DATE,END_DATE,100,ACCESS_TOKEN,CURSOR,SEARCH_ID,IS_RANDOM)#THE CHECK IS DONE AFTER IN THE QUERY FUNCTION
                '''if(D.json()['error']['code'] != 'ok'):
                    raise Exception()'''
            except:
                print('We had an error!!')
                print(D.json()['error'])
                #print(D.json())
                #print(START_DATE)
                exit()

            
            DATA_LIST.append(D.json())
            time.sleep(1)
        return DATA_LIST,i,None,None
        

    """
    MAKE UP TO A TOTAL OF 1000 REQUESTS
    (stop if/when there's no more data)
    """

    i = 0
    if not D.json()['data']['has_more']: # if no more data, cut to end of script
        i == 1000
    limit = MAX_QUERIES-1 if MAX_QUERIES < 999 else 999 #we put a max number of queries to be performed 
    while i < limit:
        try:
            D = query(QUERY,START_DATE,END_DATE,100,ACCESS_TOKEN,CURSOR,SEARCH_ID,IS_RANDOM)

            DATA_LIST.append(D.json())

            
            CURSOR = D.json()['data']['cursor']

            if not D.json()['data']['has_more']:
                print(f"    Performed only {i} queries, you will have residual at the end of the process!")
                break
            i += 1
        except Exception as e: # just in case! sometimes things happen!
            print(f"AN exception has occourred we dump the response")
            print(D.json()['error'])
            return
        
        time.sleep(1)#we do this for rate limiting, just to be safe
    if i>=limit:
        return DATA_LIST,i,CURSOR,SEARCH_ID #-> we return the data to continue the search the day after
    return DATA_LIST,i,None,None

def main_collection(ACCESS_TOKEN,HASH_SEARCH,MAX_QUERIES,START_DATE,END_DATE,DATA_FILE,CS_FILE,CURSOR=None,SEARCH_ID=None,IS_RANDOM=False):
    print('    Beginning the collection')
    data,n_q,c,s = data_collection(ACCESS_TOKEN,HASH_SEARCH,MAX_QUERIES,START_DATE,END_DATE,CURSOR,SEARCH_ID,IS_RANDOM)
    print('    Concluded the collection')
    print('    Writing the data file')
    write_data(DATA_FILE,data)
    
    if(c is not None and s is not None): #we save the search status
        print('    Writing the recovery file')
        p= (c,s)  
        with open(CS_FILE, "wb") as internal_filename:
            pickle.dump(p, internal_filename)
    print(f'    Concluded the month {START_DATE} - {END_DATE}')
    return n_q

