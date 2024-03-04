from datetime import date
import sys
import os
# insert current path to system path, so that we can import python file
sys.path.insert(1, os.getcwd())
from jobs.google_analytics_jobs import GoogleAnalyticsJobs

if __name__ == "__main__":
    ga = GoogleAnalyticsJobs()
    end_date = date(2021, 5, 1)
    ga.age_daily(end_date)
