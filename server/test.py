import requests
import json
se = requests.Session()
base_url = 'http://localhost:5000'

def test_main():
    # login
    login_info = json.dumps({'account':'16010120100', 'password':'1234'})
    r1 = se.post(base_url+'/login', data=login_info).text
    re = se.get(base_url+'/student/exam_info').text
    print(re)

test_main()
