import json
import requests
headers = {'content-type': 'application/json'}
payload = {
    "Jan": 0,
    "JanCom": "string",
    "Feb": 0,
    "FebCom": "string",
    "Mar": 269,
    "MarCom": "string",
    "Apr": 0,
    "AprCom": "string",
    "May": 0,
    "MayCom": "string",
    "Jun": 0,
    "JunCom": "string",
    "Jul": 0,
    "JulCom": "string",
    "Aug": 0,
    "AugCom": "string",
    "Sep": 0,
    "SepCom": "string",
    "Oct": 0,
    "OctCom": "string",
    "Nov": 0,
    "NovCom": "string",
    "Dec": 0,
    "DecCom": "string",
    "CostCenter": {
        "CCID": "101004059",
        "Name": "IT S/4 Hana PO SE",
        "DeliveryUnit": {
            "DU": "IT S/4 HANA Program Office",
            "OrganizationalUnit": {
                "OU": "IT S/4 HANA Program Office",
                "Node": "M3CIT04053"
            }
        }
    },
    "CostGroup": {
        "CostGroup": "3rd Party"
    },
    "CostType": {
        "CostType": "String"
    },
    "Resource": {
        "Name": "John Doe",
        "UserID": "I506992",
        "Email": "string"
    }
}


put = requests.delete(
    'https://cost-center-management-production2.cfapps.eu10.hana.ondemand.com/rest/restplanning/v1/Planning', json=payload, headers=headers)
print(put.status_code)
print(put.content)
