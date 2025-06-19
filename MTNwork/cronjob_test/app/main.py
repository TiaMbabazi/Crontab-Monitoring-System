from fastapi import FastAPI, HTTPException
from datetime import datetime
#
import uvicorn
#database connecntion 
import sqlite3
import pandas as pd
import os 
from pathlib import Path

path = Path(os.path.dirname(__file__))

BASEDIR = path.parent.absolute()
# print(BASEDIR)

app = FastAPI(title="Cron tab monitoring")
def db_connection(db_url=f"/src/data/crontab.db"):
    with sqlite3.connect(db_url) as connection:
        return connection

async def sql(name, time):
    df = pd.DataFrame(columns=['Job', 'Time'])
    # adding index
    df.loc[0,]= [name,time]
    df.to_sql("AccessTime", con=db_connection(),if_exists="append", index=False)  
@app.post("/")
async def update_data_base(name:str):
    """asyn code"""
    nameofjob = name
    timeofrequest = datetime.now()
    await sql(nameofjob, timeofrequest)
#docker run -it --publish 8000:8000  --mount "type=bind,src=$pwd,target=/src" cronjob
