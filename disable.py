import requests

url = "https://cosmovision.smartolt.com/api/onu/bulk_disable"

payload={'onus_external_ids': 'ZTEGC9679DE0,ZTEGC9650939,ZTEGC97E9E45,ZTEGC961A96A,ZTEGC96261A9'}
files=[

]
headers = {
  'X-Token': '78200d43cae043d597f0be1c5c66f0e5'
}

response = requests.request("POST", url, headers=headers, data=payload, files=files)
print(response.text)