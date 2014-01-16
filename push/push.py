import json
import urllib2

url = 'https://api.parse.com/1/push'

data = '{"where":{},"data":{"alert":"Hello, World!","badge":1,"sound":"doorbell-1.wav","ID":"HvedQbm6Ka"}}'

method = 'POST'

handler = urllib2.HTTPHandler()
opener = urllib2.build_opener(handler)
request = urllib2.Request(url,data)

request.add_header('X-Parse-Application-Id','rH4WNF3YUWEl0PtcmjQj40oIviGTHHoxPqgD0loS')
request.add_header('X-Parse-REST-API-Key','NKhmi1B1siNIj4Rd9rTDy1CeuwfticqfX1i6Js5R')
request.add_header('Content-Type','application/json')

request.get_method = lambda: method

opener.open(request)
