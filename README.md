# tiktok-research-api-python
A simple Python wrapper for querying video & user data with [TikTok's Research API](https://developers.tiktok.com/products/research-api/).

To use this code, you must first apply for and receive access to the Research API. 

This repo is a fork of the code provided by **adinagit**.


# Querying Random Video Data Iteratively, year by year 
**For more general info, consult [TikTok's Research API Reference for querying videos](https://developers.tiktok.com/doc/research-api-specs-query-videos/).**

Use the script **TT_extractor.py**

For the script to run, you must insert your **CLIENT KEY** and **CLIENT SECRET** in a .env file and then pass that path in the folder.py file in /config_files
This way you can work on git without having to write in clear your keys.

The script takes the following arguments: 
1. Begin Year -> First year of the extraction
2. Finish Year -> Last year of the extraction
3. num-queries -> How many queries to perform by month
4. RANDOM? -> Use this if you want to have random results returned, currently only function implemented
5. day -> date of the collection, useful for creating folders
## Things to note 
* Access tokens are good for 2 hours, but the script is set up to generate a new one every hour.

## EXAMPLE:
I want to gather 1000 videos a day for all the months from 2020 to 2023

python TT_extractor.py -by 2020 -fy 2023 -n 10 -rnd -day $(date +\%Y-\%m-\%d)   <- this last piece will give you the current date, you can also set this up in a crontab job ( n=10 since it will do 10 queries of 100 elements)

The original scripts by **adinagit** are stored in /base_code. For documentation about those, you should refer to the original repo.
