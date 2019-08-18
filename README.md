# test_API

### This application allows you to work with simple API.

## Setting up


##### Clone the repo

```
$ git clone https://github.com/petrovao87/test_api.git
$ cd test_api
```

##### Virtual Environment install & activate
```
$ pip install virtualenv
$ env\scripts\activate  (for Windows systems)
$ env\bin\activate  (for Unix systems)
```

##### Install the dependencies

```
$ pip install -r requirements.txt
```

#### Connection to your PostgreSQL server and Create the database 

##### create connection to your db. Change db.py
```
engine = create_engine('postgresql://USERNAME:PASSWORD@localhost/YOUR_DB_NAME)
```
##### and create schemas
```
$ python db.py
```
## test_API methods:
### Running the app
```
$ python api.py
```

### GET the list of all Processes
```
/api/v1/processes
```

### GET a single process
```
/api/v1/processes/<process_id>
```

### DELETE a task
```
/api/v1/processes/delete/process/<process_id>
```
##### or:
```
from requests import delete


url = 'http://localhost:5000/api/v1/processes/delete/process/1'

req = delete(url)
```

##### for example:

```
curl http://localhost:5000/api/v1/processes/delete/process/1 -X DELETE
```

### Update a task

##### Update value in tables: Process Parameter, Process Start Condition, Process Performer and Process Quota
```
/api/v1/processes/update/process/<process_id>
/api/v1/processes/update/process_parameter/<process_id>
/api/v1/processes/update/process_start_condition/<process_id>
/api/v1/processes/update/process_performer/<process_id>
/api/v1/processes/update/process_quota/<process_id>
```

##### for example:
```
curl http://localhost:5000/api/v1/processes/update/process/1 -d "process_name=another process name" -X PUT
```
##### or:
```
from requests import put


url = 'http://localhost:5000/api/v1/processes/update/process/1'
data = {'process_name': 'name_name'}

req = put(url, json=data)
```

### Add a new process
```
/api/v1/processes
```
### Parameters to send in your POST 
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

##### for example:

```
from requests import post


url = 'http://localhost:5000/api/v1/processes'
data = {'process_id': 1,
        'process_name': 'your process name',
        'process_description': 'simple precess description',
        'activity_flag': 'active',
        'process_performer_id': 1,
        'parameter_name': 'your parameter name',
        'parameter_value': 'your parameter value',
        'condition_type': 'your condition_type',
        'condition_value': 'youur condition_value',
        'performer_name': 'Alex Petrov',
        'performer_description': 'Alex is the process owner',
        'quota_type': 'your quota type',
        'quota_value': 'your quota value'}
        
req = post(url, json=data)
```