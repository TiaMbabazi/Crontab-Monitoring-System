# Crontab-Monitoring-System
This project is a  system that monitors cron jobs on a local machine, tracks their execution status, and logs this information into a SQLite database. It also supports integrating results into Power BI dashboards for visualization.

**What It Does**
- Reads all cron jobs scheduled on a user’s system using python-crontab
- Stores metadata (like next scheduled run and job comments) in a SQLite database
- Logs successful job executions via POST requests to a FastAPI endpoint
- Runs in Docker for easy automation and deployment
- Data can be connected to Power BI for monitoring job frequency, failures, and timing trends

**How It Works**

**Cron Metadata Extraction (access_crontab.py)**

- Reads the user’s crontab entries
- Extracts the command/comment and next run time
- Stores only new or unlogged jobs in the SQLite database under a table called Crontab

 **Job Run Logging API (main.py)**
 
- Hosts a FastAPI server that listens for POST / requests
- When a cron job executes, it sends a POST with its name to this endpoint
- The job name and execution timestamp are logged in the AccessTime table

**Data Visualization (Power BI)**

- Connect Power BI to the SQLite database
- Create visualizations like:
- Job frequency over time
- Success/failure trend analysis
- Runtime duration and anomalies

**Example POST Request and Job**

Any successful cron job should include a line like this in its definition:
`curl -X POST "http://localhost:8000/?name=backup_script"`
This triggers the FastAPI server to log that the job ran successfully

For example, a full job with a POST request and the comment for the database would look like:

`0 2 * * * /home/user/scripts/backup.sh && curl -X POST "http://localhost:8000/?name=DailyBackup" # DailyBackup`

**Breakdown:**

`0 2 * * *` - runs every day at 2:00 AM

`/home/user/scripts/backup.sh ` - your actual script or task

`&& curl -X POST ... ` - sends a signal to the FastAPI server once the script runs successfully

`?name=DailyBackup`  - the job name logged in the database (used by the API)

`# DailyBackup `-  The cron comment used for metadata tracking (captured by access_crontab.py)


**Running with Docker**

To containerize and run the app:

`docker run -it --publish 8000:8000 --mount "type=bind,src=$PWD,target=/src" cronjob`

**Requirements**

- Python 3.8+
- SQLite
- FastAPI
- pandas
- python-crontab
- Docker (optional but recommended)
- Power BI (for visualization)

**Install dependencies:**

`pip install fastapi uvicorn pandas python-crontab`

**Future Improvements**
- Build a visual dashboard as a frontend
- Add alerting (e.g., email or Slack) for failed or missed jobs
