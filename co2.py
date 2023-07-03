import wlan
import time
import urequests

# Aktuelle Unixtime (seit 1970) in Millisekunden ermitteln
now = time.time()
now = int(now)
now = (now + 946677638) * 1000  
# now = str(now)

# Unixtime (seit 1970 ) vor X Minuten ermitteln 
Minuten = 30
before = time.time() - (Minuten * 60)
before = int(before)
before = (before + 946677638) * 1000
before = str(before)


url = 'http://192.168.178.32:2090/api/ds/query'
headers = {}
data = {
    'queries': [
        {
            'refId': 'B',
            'datasource': {
                'uid': 'ud0tJxxMk',
                'type': 'mysql'
            },
            'rawSql': 'SELECT\n  $__timeGroupAlias(Zeit,10s),\n  avg(Wert) AS "Co2"\nFROM Werte\nWHERE\n  $__timeFilter(Zeit) AND\n  SensorID = 39\nGROUP BY 1\nORDER BY $__timeGroup(Zeit,10s)',
            'format': 'time_series',
        }
    ],
    'from': str(before),
    'to': str(now)
}

response = urequests.post(url,headers=headers, json=data)
response.encoding = 'utf-8'
print(response.content)
