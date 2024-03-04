"""Main Entry point for job run"""
from datetime import date
import sys
import os
# insert current path to system path, so that we can import python file
sys.path.insert(1, os.getcwd())
#pylint: disable=wrong-import-position
from jobs.google_analytics_jobs import GoogleAnalyticsJobs
#pylint: enable=wrong-import-position

if __name__ == "__main__":
    ga = GoogleAnalyticsJobs()
    end_date = date(2021, 5, 1)
    ga.age_daily(end_date)
