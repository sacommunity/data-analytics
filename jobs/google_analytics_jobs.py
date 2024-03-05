"""Google Analytics Jobs Module"""
import logging
from datetime import date, timedelta
from data_retrieval.google_analytics_api_retrieval import GoogleAnalyticsApiRetrieval, \
    GoogleAuthenticationMethod, PageDto
from dtos.date_range_dto import DateRangeDto

from helpers.metadata_helper import load_metadata, \
    DataFrequency, DataModule, JobStatus, get_start_date, save_metadata, JobConfig
from helpers.file_helper import save_list_to_csv, get_data_path
from helpers.settings_helper import get_google_analytics_view_id_from_settings, \
    get_file_storage_root_folder_from_settings

ga_jobs_log = logging.getLogger(__name__)

class GoogleAnalyticsJobs():
    """Google Analytics Jobs"""
    def __init__(self, credentials_file_path='./credentials/credentials.json',
                 token_file_path='./credentials/token.json',
                 metadata_file_path="./metadata/metadata.json",
                 settings_file_path='./settings/app_settings.json') -> None:
        self.credentials_file_path = credentials_file_path
        self.token_file_path = token_file_path
        self.metadata_file_path = metadata_file_path
        self.settings_file_path = settings_file_path
        self.view_id = get_google_analytics_view_id_from_settings()

    def run_job(self, data_frequency: DataFrequency,
                data_module: DataModule,
                end_date: date):
        """Run Job"""
        job_log = f'data frequency: {data_frequency.name}, data module: {data_module.name}'
        metadata = load_metadata(data_frequency, data_module)
        if metadata.job_status.get('value') == JobStatus.IN_PROGRESS.value:
            ga_jobs_log.info("Another job is in progress for %s", job_log)
            return
        start_date = get_start_date(
            metadata.last_data_extraction_date, metadata.job_status)
        try:
            # of the current job is in progress, then don't run another job
            while start_date < end_date:
                ga = GoogleAnalyticsApiRetrieval(GoogleAuthenticationMethod.OAUTH,
                                                 self.credentials_file_path,
                                                 self.token_file_path,
                                                 self.view_id)
                ga_jobs_log.info("Running job %s for start date %s", job_log, start_date)
                save_metadata(JobConfig(data_frequency, data_module),
                              start_date,
                              JobStatus.IN_PROGRESS,
                              file_path=self.metadata_file_path)
                date_range = DateRangeDto(start_date, start_date)
                page_dto = PageDto(1000, None)
                data = None
                if data_module.value == DataModule.AGE.value:
                    data = ga.get_sessions_by_age(date_range, page_dto)
                elif data_module.value == DataModule.GENDER.value:
                    data = ga.get_sessions_by_gender(date_range, page_dto)
                elif data_module.value == DataModule.LANDING_PAGE.value:
                    data = ga.get_sessions_by_landing_page(
                        date_range, page_dto)
                else:
                    raise ValueError(f'Invalid data module {data_module.value}')

                root_dir = get_file_storage_root_folder_from_settings()
                file_path = get_data_path(
                    root_dir, data_frequency.name, data_module.name, start_date)
                print('saving file to ', file_path)
                save_list_to_csv(data, file_path)

                save_metadata(JobConfig(data_frequency, data_module),
                              start_date,
                              JobStatus.SUCCESS,
                              file_path=self.metadata_file_path)

                start_date = start_date + timedelta(days=1)
        except Exception as ex:
            failure_reason = str(ex)
            ga_jobs_log.error(ex)
            save_metadata(JobConfig(data_frequency, data_module),
                          start_date,
                          JobStatus.FAILED,
                          failure_reason=failure_reason,
                          file_path=self.metadata_file_path)
            raise ex

    def age_daily(self, end_date: date):
        """Job: Age, Daily Data"""
        self.run_job(DataFrequency.DAILY, DataModule.AGE, end_date)

    def gender_daily(self, end_date: date):
        """Job: Gender, Daily Data"""
        self.run_job(DataFrequency.DAILY, DataModule.GENDER, end_date)

    def landing_page_daily(self, end_date: date):
        """Job: Landing Page, Daily Data"""
        self.run_job(DataFrequency.DAILY, DataModule.LANDING_PAGE, end_date)
