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


a = [{'id':1,'vlues':2},{'id':2,'vlues':3}]
b = [ {'id' : 1, 'count': 2}, {'id': 2, 'count': 3}]
for (a,b) in [(a_dict,b_dict) for a_dict in a
              for b_dict in b
              ]:
    if a['id'] == b['id']:
        print({'a_dict': a,'b_dict': b})