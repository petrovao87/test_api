# test_API

## This application allows you to work with simple API.

## Setting up

##### Clone the repo

```
$ git clone https://github.com/petrovao87/test_api.git
$ cd test_api
```

##### Install the dependencies

```
$ pip install -r requirements.txt
```

##### Create the database

```
$ python db.py
```

## Running the app and Add Environment Variables
```
$ python api.py
```

## GET the list of Processes
```
/api/v1/processes
```

## GET a single process
```
/api/v1/processes/<process_id>
```

## DELETE a task
```
/api/v1/processes/delete/process/<process_id>
```

## Update a task
Update value in tables: Process Parameter, Process Start Condition, Process Performer and Process Quota
```
/api/v1/processes/update/process_parameter/<process_id>
/api/v1/processes/update/process_start_condition/<process_id>
/api/v1/processes/update/process_performer/<process_id>
/api/v1/processes/update/process_quota/<process_id>
```

## Add a new task
```
/api/v1/processes
```
## Parameters to send in your POST 
```
process_id (Integer)
process_name (String)
process_description (String)
activity_flag (String)
process_performer_id (Integer)
parameter_name (String)
parameter_value (String)
condition_type (String)
condition_value (String)
performer_name (String)
performer_description (String)
quota_type (String)
quota_value (String)
```