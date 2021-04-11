# Parallelization
parallel ant colony algorithm for the CVRP

## Website
http://35.225.216.59:5000/

## Github repository
https://github.com/tanglz/cvrp

## Compile
### Step 1: Install Python
##### Python virtual environment
### Step 2: Install libraries using pip from requirements.txt
### Step 3: Install MySQL
#### modify the configuration in db_connector.py
### Step 4: Install Redis
#### start redis : redis-server
### Step 5: Start master
#### python app.py
### step 6: Start worker
#### celery -A job worker --loglevel=info
### step 7 (option): start task monitor
#### celery -A job flower
### step 8 (option): start web request test
#### locust

## Test
### Create task
#### * parameter 'name' is unique
### Task list
#### click 'display result'
