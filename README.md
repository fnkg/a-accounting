## Export automation
I'm not very experienced in python, but I've been doing some manual work for accounting all last year and decided to automate the process. 

### description
Each month the accounting department requested uploads for
1. payment cards
2. cash
3. realisations
There are also uploads for online payments and payments via SBP.

items 1-3 are uploaded from postgresql database.
online and sbp are unloaded from personal accounts

the script does the following:
1. requests the year and month for uploads and creates working directories
3. changes dates in sql files 
4. executes them and exports the data in json and xlsx formats
5. asks for paths for online and sbp
6. processes all files: xlsx to a readable form for accounting,
json to a format for uploading to 1C

### plans
- make the code more flexible and reusable
- wrap it in an interface (web or desktop)
- test coverage

## how to use
1. git clone https://github.com/vsenichego/astra-accounting.git
2. python -m venv .venv
3. source .venv/bin/activate or ./.venv/Scripts/activate
4. pip install -r requirements.txt
5. get creds for .env 🙂
6. run the run_scripts.py