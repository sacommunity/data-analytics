<!-- To preview markdown in vscode in MAC: press CMD + Shift + V  . This helps in editing markdown-->
# data-analytics-volunteer

This repository will contain the codes for data analysis for sacommunity


1. Create Python Virtual Environment. Let's name it sacommunity_data_analytics_venv
Reference: https://docs.python.org/3/library/venv.html

2. create command
python -m venv ./sacommunity_data_analytics_venv


3. activate the virtual environment
source sacommunity_data_analytics_venv/bin/activate


4. install dependencies from requirements.txt
pip install -r requirements.txt


## Coding Convention
1. pylint
https://pylint.readthedocs.io/en/stable/

    check warnings from pylint with following command (do not supress warning from pylint unless necessary, resolve as many warnings as possible)

    pylint $(git ls-files '*.py')

2. Run unit tests

    python -m unittest discover -s ./tests/helpers -p "*_tests.py"

3. Logging (File based)
https://docs.python.org/3/library/logging.html

    Persistent logging enables to go through the error messages to debug. We are storing logs in file in logs folder

## How to run code
1. Jobs to fetch daily data (job_run.py)

## Future Plan - Roadmap (TODO)
2. Prepare report (Invoke Manually)

    i. User enters date range (say fiscal year)

    ii. System downloads 3 files data and transforms it into 5 files

    iii. Automate Power BI report

3. Implement Airflow for jobs (ETL - Extract, Transform and Load)

4. Extract - Extract data from google analytics api

    Verify that the downloads are working as expected. Compare, cross-check some samples against google analytics web portal

5. Transform - 

    Clean the data, 
    
    find missing data,
    
    resolve data issues, 
    
    prepare new data format for power BI

    prepare new data format for canva

6. Load - 

    Save the files in local disk
    (iff we get appropriate permissions to write in sharepoint, then will upload files to sharepoint)

7. Automate Power BI report

8. Automate Canva Report

9. Make GUI for all the operations

