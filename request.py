import requests
import json

fp = open('../timeout.py', 'r')
string = fp.read()
x = {'code': string,
     'language': 'py'}

r = requests.post('http://localhost:5001/v1/run_code', data=json.dumps(x),
                  headers={'Content-Type': 'application/json'})
print(r.status_code, r.json())
