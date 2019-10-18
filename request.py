import requests
import json

fp = open('../timeout.py', 'r')
string = fp.read()
x = {'code': string,
     'language': 'py',
     'problem_id': 'p1',
     'student_id': 'sharath',
     'contest_id': 'c1',
     'time_out': 2}

r = requests.post('http://localhost:5001/v1/run_code', data=json.dumps(x),
                  headers={'Content-Type': 'application/json'})
print(r.status_code, r.json())
