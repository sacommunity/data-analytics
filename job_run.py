"""Main Entry point for job run"""

from datetime import datetime
from logging.handlers import TimedRotatingFileHandler
import sys
import os
import logging
# insert current path to system path, so that we can import python file
sys.path.insert(1, os.getcwd())
# pylint: disable=wrong-import-position
from helpers.file_helper import get_file_name_based_on_date
from jobs.google_analytics_jobs import GoogleAnalyticsJobs
# pylint: enable=wrong-import-position


def time_elapsed_seconds(start_date: datetime, end_date: datetime):
    """reurns time elapsed in seconds"""
    return (end_date - start_date).total_seconds()


def setup_logging():
    """setup logging"""
    log_file_name = get_file_name_based_on_date(datetime.now())
    logging.basicConfig(encoding='utf-8',
                        level=logging.DEBUG,
                        handlers=[
                            logging.StreamHandler(),
                            TimedRotatingFileHandler(
                                f'./logs/ga_jobs_{log_file_name}.log', when='midnight')
                        ])


def main():
    """main job to fetch data from google analytics"""
    setup_logging()
    logger = logging.getLogger(__name__)
    google_analytics_jobs = GoogleAnalyticsJobs()
    job_start_date = datetime.now()
    # end_date = date(2022, 5, 1)
    end_date = datetime.now().date()
    logger.info("Job Started at %s", datetime.now())
    logger.info("Running google analytics jobs till end date: %s", end_date)

    job_start_date = datetime.now()
    logger.info("Started running job AGE Daily %s", job_start_date)
    google_analytics_jobs.age_daily(end_date)
    job_end_date = datetime.now()
    logger.info("Completed running job AGE Daily %s . Time Elapsed %s",
                job_end_date,
                time_elapsed_seconds(job_start_date, job_end_date))

    job_start_date = datetime.now()
    logger.info("Started running job GENDER Daily %s", job_start_date)
    google_analytics_jobs.gender_daily(end_date)
    job_end_date = datetime.now()
    logger.info("Completed running job GENDER Daily %s . Time Elapsed %s",
                job_end_date,
                time_elapsed_seconds(job_start_date, job_end_date))

    job_start_date = datetime.now()
    logger.info("Started running job Landing Page Daily %s", job_start_date)
    google_analytics_jobs.landing_page_daily(end_date)
    job_end_date = datetime.now()
    logger.info("Completed running job Landing Page %s . Time Elapsed %s",
                job_end_date,
                time_elapsed_seconds(job_start_date, job_end_date))


if __name__ == "__main__":
    main()
