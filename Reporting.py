from flask import Flask, request, jsonify
import json
import requests
import math

app = Flask(__name__)
port = '5000'

Org_Dict = {'oss': 'Operations & Shared Service', 'hr2': 'HR II', 'pr': 'Procurement',
            'iam': 'Identity & Accessmanagement', 's/4': 'IT S/4 HANA Program Office', 'app': 'IT Application Services Mgmt', 'cross': 'Cross IT & Operations Management', 'hr': 'HR I', 'cont': 'Controlling', 'corpfin': 'Coprporate Finance Mgmt', 'shared': 'Shared IT Applications', 'dummy': 'Dummy'}

Del_dict = {1: 'IT Contract to Revenue', 2: 'Cross IT & Operations', 3: 'IT Human Resources', 4: 'IT Corporate Finance',
            5: 'IT Services, Entitlement & Delivery', 6: 'IT Application Services Mgmt', 7: 'IT S/4 HANA Program Office', 8: 'IT Go-To-Market Services', 9: 'Dummy'}
Node_dict = {1: 'M3CIT03008', 2: 'M3CIT03003', 3: 'M3CIT03009', 4: 'M2CIT00302',
             5: 'M3CIT03010', 6: 'M3ITIN0206', 7: 'M3CIT04054', 8: 'M2CIT00312', 9: 'M3456'}
Cost_Center_ID = {'oss': '108611700', 'hr2': '115000402',
                  'pr': '101035030', 'iam': '101000452', 's/4': '101004059', 'app': '108004071', 'cross': '108004036', 'hr': '101004080', 'cont': '181010088', 'corpfin': '101030010', 'shared': '176223020', 'dummy': '11238769'}
Cost_Center_Dict = {'oss': 'IT Ops & SharServ US', 'hr2': 'IT HR II SGD',
                    'pr': 'IT Procurement SE', 'iam': 'M3CIT03003', 's/4': 'IT S/4 Hana PO SE', 'app': 'IT AppServ Mgmt US', 'cross': 'Cross IT & Ops Mg US', 'hr': 'IT HR I SE', 'cont': 'IT Controlling ROM', 'corpfin': 'IT Fin Serv Mgmt SE', 'shared': 'SharIT App IND', 'dummy': 'Dummy IT APP'}


@app.route('/mike', methods=['POST'])
def index():
    data = (json.loads(request.get_data()))
    org_unit = str(data['conversation']['memory']['Org_Unit']['raw']).lower()

    actuals = requests.get(
        'https://cost-center-management-production2.cfapps.eu10.hana.ondemand.com/rest/restactuals/v1/GetActuals', timeout=10)

    planned = requests.get(
        'https://cost-center-management-production2.cfapps.eu10.hana.ondemand.com/rest/restplanning/v1/Planning', timeout=10)

    actualsjson = json.loads(actuals.text)
    plannedjson = json.loads(planned.text)

    PercentTraveled = 0
    PercentICO = 0
    PercentThirdParty = 0
    Actuallist = []
    Planninglist = []
    travelplanned = 0
    ICOplanned = 0
    ThirdPartyplanned = 0
    Travel = 0
    ICO = 0
    ThirdParty = 0
    for i in actualsjson:
        try:
            if i['CostCenter']['DeliveryUnit']['DU'] == Org_Dict[org_unit]:
                Actuallist.append(i)
        except KeyError:
            pass

    for x in Actuallist:
        if x['CostGroups'][0]['CostGroup'] == '3rd Party':
            ThirdParty += math.floor(x['Budget_Actuals'])

    for k in Actuallist:
        if k['CostGroups'][0]['CostGroup'] == 'Travel':
            Travel += math.floor(x['Budget_Actuals'])

    for l in Actuallist:
        if l['CostGroups'][0]['CostGroup'] == 'ICO':
            ICO += math.floor(x['Budget_Actuals'])

    for m in plannedjson:
        try:
            if m['CostCenter']['DeliveryUnit']['DU'] == Org_Dict[org_unit]:
                Planninglist.append(m)
        except KeyError:
            pass
    for z in Planninglist:
        if z['CostGroup']['CostGroup'] == '3rd Party':
            ThirdPartyplanned += math.floor(z['Sum'])

    for q in Planninglist:
        if q['CostGroup']['CostGroup'] == 'Travel':
            travelplanned += math.floor(q['Sum'])

    for p in Planninglist:
        if p['CostGroup']['CostGroup'] == 'ICO':
            ICOplanned += math.floor(p['Sum'])

    try:
        PercentTraveled = Travel/travelplanned * 100
    except ZeroDivisionError:
        PercentTraveled = math.floor(0)

    try:
        PercentThirdParty = ThirdParty/ThirdPartyplanned * 100
    except ZeroDivisionError:
        PercentThirdParty = math.floor(0)

    try:
        PercentICO = ICO/ICOplanned * 100
    except ZeroDivisionError:
        PercentICO = math.floor(0)

    return jsonify(
        status=200,
        replies=[{
            'type': 'text',
            'content': 'Travel:\nYou have spent $%s on Travel compared to $%s planned, this is %i%% of your total budget.\n\nThird Party:\nYou have spent $%s on 3rd Party Consultants compared to %s planned, this is %i%% of your total budget.\n\nICO:\nYou have spent $%s on ICO compared to $%s planned, this is %i%% of your total budget.' % ("{:,}".format(Travel), "{:,}".format(travelplanned), PercentTraveled, "{:,}".format(ThirdParty), "{:,}".format(ThirdPartyplanned), PercentThirdParty, "{:,}".format(ICO), "{:,}".format(ICOplanned), PercentICO)
        }],
        conversation={
            'memory': {'key': 'value'}
        }
    )


@app.route('/', methods=['POST'])
def index2():
    data = (json.loads(request.get_data()))
    org_unit = data['conversation']['memory']['Org_unit']['value'].lower()
    cost = data['conversation']['memory']['number']['value']
    cost_group = data['conversation']['memory']['costtype']['value'].lower()
    date = data['conversation']['memory']['date']['value']
    userid = data['conversation']['memory']['userid']['value']
    name = data['conversation']['memory']['person']['fullname']
    headers = {'content-type': 'application/json'}
    cleanDU = Org_Dict[org_unit]
    newcost = ''.join(e for e in cost if e.isalnum())
    cleancost = int(newcost)
    cleandate = date[:3].title()
    cleanid = userid.title()
    cleanname = name.title()
    cleantype = ''
    org_org = 0
    if cost_group[:2] == 'tr':
        cleantype = 'Travel'
    elif cost_group[0] == 'i':
        cleantype = 'ICO'
    else:
        cleantype = '3rd Party'

    payload = {
        "Jan": 0,
        "JanCom": "string",
        "Feb": 0,
        "FebCom": "string",
        "Mar": 0,
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
            "CCID": "string",
            "Name": "string",
            "DeliveryUnit": {
                "DU": "string",
                "OrganizationalUnit": {
                    "OU": "string",
                    "Node": "string"
                }
            }
        },
        "CostGroup": {
            "CostGroup": "string"
        },
        "CostType": {
            "CostType": "string"
        },
        "Resource": {
            "Name": "string",
            "UserID": "string",
            "Email": "string"
        }
    }
    if org_unit == 'oss':
        org_org = 2
    elif org_unit == 'hr2':
        org_org = 3
    elif org_unit == 'pr':
        org_org = 4
    elif org_unit == 'iam':
        org_org = 2
    elif org_unit == 's/4':
        org_org = 7
    elif org_unit == 'cross':
        org_org = 2
    elif org_unit == 'hr':
        org_org = 3
    elif org_unit == 'app':
        org_org = 6
    elif org_unit == 'cont':
        org_org = 4
    elif org_unit == 'corpfin':
        org_org = 4
    elif org_unit == 'shared':
        org_org = 2
    elif org_unit == 'dummy':
        org_org = 9
    payload['CostCenter']['DeliveryUnit']['OrganizationalUnit']['OU'] = Del_dict[org_org]
    payload[cleandate] = cleancost
    payload['Resource']['Name'] = cleanname
    payload['Resource']['UserID'] = cleanid
    payload['CostCenter']['DeliveryUnit']['DU'] = cleanDU
    payload['CostCenter']['DeliveryUnit']['OrganizationalUnit']['Node'] = Node_dict[org_org]
    payload['CostGroup']['CostGroup'] = cleantype
    payload['CostCenter']['CCID'] = Cost_Center_ID[org_unit]
    payload['CostCenter']['Name'] = Cost_Center_Dict[org_unit]
    post = requests.post(
        'https://cost-center-management-production2.cfapps.eu10.hana.ondemand.com/rest/restplanning/v1/Planning', json=payload, headers=headers)
    return jsonify(
        status=200,
        replies=[{
            'type': 'text',
            'content': str(payload)
        }],
        conversation={
            'memory': {'key': 'value'}
        }
    )


@app.route('/errors', methods=['POST'])
def errors():
    print(json.loads(request.get_data()))
    return jsonify(status=200)


app.run(port=port)
