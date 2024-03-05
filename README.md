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
check warnings from pylint with following command (do not supress warning from pylint unless necessary, resolve as many warnings as possible)

pylint $(git ls-files '*.py')

2. Run unit tests

python -m unittest discover -s ./tests/helpers -p "*_tests.py"


## How to run code
1. Jobs to fetch daily data (job_run.py)

## Future Plan (TODO)
2. Prepare report (Invoke Manually)

i. User enters date range (say fiscal year)

ii. System downloads 3 files data and transforms it into 5 files

iii. Automate Power BI report
