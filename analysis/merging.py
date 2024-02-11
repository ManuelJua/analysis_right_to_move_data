import pandas as pd
import datetime
import os
from time import time

def days_on_market(frames,df):
    df_days_on_market=(
        #Concateantes all the dataframes
        pd.concat(frames,ignore_index=True)
        ['address']
        .value_counts()
        .reset_index()
    )
    #Merges this data with the original property dataframe matching each url and renames variable 'count'
    df=pd.merge(df,df_days_on_market,on='address').rename(columns={'count':'days_on_market'})

    return df



#Deletes previous final_data file
def delete_previous_data_file():
    
    #Gets the path of current directory
    dir=os.path.realpath('.')
    #Lists files in current directory, excluding child directories
    list_files=list(os.walk(dir))[0][2]
    
    try:
        #Selects final_data csv file name
        final_data_file_name=[file for file in list_files if 'final_data' in file][0]
        print(f'\nFound existing file: {final_data_file_name}')
        #Deletes the file if it does exist
        os.remove(f'{dir}/{final_data_file_name}')
        print(f"'{final_data_file_name}' has been deleted")
    except:
        print('Final data file does not exists')


#creates the file names to date
def get_names(start_date,finish_date,delta): 
    file_names=[]
    while start_date<=finish_date: 
        file_names.append('clean_{}.csv'.format(start_date))
        start_date+=delta
    return file_names

#get the files if they exist
def get_files(file_names):
    frames=[]
    for file_name in file_names:
        try:
            df=pd.read_csv('clean_right_to_move_files/'+file_name) #right_to_move_files is the directory with all the files
            frames.append(df)
        except:
            print("File {} not found".format(file_name))
            continue

    return frames

#drops duplicated registers, keeping only the first of them
def drop_duplicates(frames):
    df=pd.concat(frames,ignore_index=True)
    df_cleaned=df.drop_duplicates(subset=['address'])
    df_cleaned=days_on_market(frames=frames,df=df_cleaned)
    
    return df_cleaned

#saves file to csv
def save_df(df,final_name):
    df.to_csv(final_name,index=False)
    print(f'\nFile {final_name} saved')

#main function to execute the previous functions
def main():
    start=time()
    
    print('\n')
    print('*'*50)
    print('STARTING SCRIPT TO MERGE FILES'.center(50))
    print('*'*50)

    start_date=datetime.date(2022,9,30)
    finish_date=datetime.date.today()
    delta=datetime.timedelta(days=1)

    file_names=get_names(start_date,finish_date,delta)
    frames=get_files(file_names)
    df=drop_duplicates(frames)
    delete_previous_data_file()
    save_df(df,'final_data-{}.csv'.format(datetime.date.today()))

    print("Script executed succesfully")
    print("df shape:",df.shape)

    end=time()
    print(f'Execution time: {round(end-start,2)} seconds')

#Execution of main()    
main()
