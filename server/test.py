import requests
import json
se =requests.Session()



base_url = 'http://localhost:5000'
r = se.get(url = base_url+'/teacher/tea_class',data= json.dumps({'class_id':'SE3002L_1'}) ).text
print(r)