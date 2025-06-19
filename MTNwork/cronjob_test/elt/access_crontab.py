import sqlite3
from crontab import CronTab
from datetime import datetime
from fastapi import FastAPI
from pydantic import BaseModel
from pathlib import Path
import os 
import pandas as pd
cron  = CronTab(user=True)  # current users cron
def readCronjob():
    timeList= []
    commandList =[]
    for job in cron:
        time = job.schedule().get_next()
        timeList.append(str(time))
        commandList.append(str(job.comment))
    d = {'Job': commandList, 'Next run': timeList}
    df = pd.DataFrame(data=d)
    print ("the data to insert")
    return df

def getnewrecordsonly(dataframetoinsert, connection ):
    existing = pd.read_sql("""SELECT * FROM Crontab""", connection)
    #compare existing data to datato insert to find unique ones 
    #use tuple to compare both the whole rows 
    df_unique = dataframetoinsert[~dataframetoinsert.apply(tuple, axis=1).isin(existing.apply(tuple, axis=1))]
    # Reset the index of the new data frame
    df_unique.reset_index(drop=True, inplace=True)
    return df_unique  


def inserttodb(db_uri,dataframetoinsert):
    """ get dataframe and write dataframe to db
    """
    with sqlite3.connect(db_uri) as connection:
            frame = getnewrecordsonly(dataframetoinsert, connection)
            frame.to_sql("Crontab", con=connection, if_exists='append',index=False)


path = Path(os.path.dirname(__file__))
BASEDIR = path.parent.absolute()
inserttodb(f"{BASEDIR}/data/crontab.db",readCronjob())
print(BASEDIR)


