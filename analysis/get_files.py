import pandas as pd
import datetime
import boto3
import io
import os

print('\n','*'*32)
print('STARTING SCRIPT TO GET NEW FILES')
print('*'*32)

dir=os.path.realpath('right_to_move_files')
#Finds all file names in right_to_move_files
right_to_move_files=pd.Series(list(os.walk(dir))[0][2])
#Searches for the lastest date in the directory righ_to_move_files
last_file_date=right_to_move_files.sort_values().str.findall('\d\d\d\d-\d\d-\d\d').iloc[-1][0]
print(f'\nLast file date: {last_file_date}')

#Adds one more day to the last file date in order to start downloading the next files from s3
next_start_date=str(pd.to_datetime(last_file_date).date()+datetime.timedelta(days=1))

#Creates a list of the file names to download using a list comprehension and pd.date_range
file_names_to_download=[
                        f'right_to_move_files/right_to_move-{date.date()}.csv' 
                        for date in pd.date_range(next_start_date,datetime.date.today())
                        ]
print('\nTrying to download the following files:')
for file in file_names_to_download:
    print(file.split('/')[1])

s3=boto3.client('s3')

response = s3.list_objects_v2(
Bucket='rtm-edinburgh-scraper',
Prefix='right_to_move_files'
)
objects_name=[file['Key'] for file in response['Contents'] ]
for obj in objects_name:
    if obj in file_names_to_download:
        file=s3.get_object( Bucket='rtm-edinburgh-scraper',Key=obj)
        file_content=file['Body'].read()
        df=pd.read_csv(io.BytesIO(file_content))
        df.to_csv(obj,index=False)
        print(f'{obj} saved')