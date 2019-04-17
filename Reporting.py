from flask import Flask, request, jsonify
import json
import requests
import math

app = Flask(__name__)
port = '5000'

DU_dict = ['1GtM Management', '1Marketing', '1Franchise Apps', '1Partner Management', '1Sales II', '1Sales I', '1Solution Center',
           '2Contract to Revenue', '3IT Application Architecture', '4Entitlement & Fullfillment Mgmt', '4Services Delivery', '5CVCS Mgmt', '6IT S/4 HANA Program Office', '7IT Application Services Mgmt', '8HR I', '8HR II', '9Cross IT & Operations Management', '9Operations & Shared Service', '9Identity & Accessmanagement', '9Shared IT Applications', 'zCore Finance', 'zControlling', 'zCorporate Finance Mgmt', 'zProcurement']


@app.route('/mike', methods=['POST'])
def index():
    data = (json.loads(request.get_data()))
    org_unit = str(data['conversation']['memory']['Org_Unit']['raw']).lower()

    actuals = requests.get(
        'https://cost-center-management-production2.cfapps.eu10.hana.ondemand.com/rest/restactuals/v1/GetActuals', timeout=15)

    planned = requests.get(
        'https://cost-center-management-production2.cfapps.eu10.hana.ondemand.com/rest/restplanning/v1/Planning', timeout=15)

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


@app.route('/DU', methods=['POST'])
def costcenter():
    placeholder = ""
    Org_list = []

    data = (json.loads(request.get_data()))
    Org_unit = str(data['conversation']['memory']['org_unit']['raw'])
    if Org_unit == 'IT Go-to-Market Services':
        placeholder = '1'
    elif Org_unit == 'IT Contract to Revenue':
        placeholder = '2'
    elif Org_unit == 'IT Application Architecture':
        placeholder = '3'
    elif Org_unit == 'IT Services Entitlement & Delivery':
        placeholder = '4'
    elif Org_unit == 'IT Core Value Chain Services Mgmt':
        placeholder = '5'
    elif Org_unit == 'IT S/4 HANA Program Office':
        placeholder = '6'
    elif Org_unit == 'IT Application Services Mgmt':
        placeholder = '7'
    elif Org_unit == 'IT Human Resources':
        placeholder = '8'
    elif Org_unit == 'Cross IT & Operations':
        placeholder = '9'
    elif Org_unit == 'IT Corporate Finance':
        placeholder = 'z'

    for i in DU_dict:
        if i[0] == placeholder:
            Org_list.append(i[1:])
    buttonname = []
    for k in Org_list:
        if len(k) > 20:
            buttonname.append(k[:20])
        else:
            buttonname.append(k)
    if len(Org_list) == 1:
        buttons = [{
            "title": buttonname[0],
            "value": Org_list[0],
        }, ]
    elif len(Org_list) == 2:
        buttons = [{
            "title": buttonname[0],
            "value": Org_list[0],
        },
            {
            "title": buttonname[1],
            "value": Org_list[1],
        }

        ]
    elif len(Org_list) == 3:
        buttons = [{
            "title": buttonname[0],
            "value": Org_list[0],
        },
            {
            "title": buttonname[1],
            "value": Org_list[1],
        },
            {
            "title": buttonname[2],
            "value": Org_list[2],
        },
        ]
    elif len(Org_list) == 4:
        buttons = [{
            "title": buttonname[0],
            "value": Org_list[0],
        },
            {
            "title": buttonname[1],
            "value": Org_list[1],
        },
            {
            "title": buttonname[2],
            "value": Org_list[2],
        },
            {
            "title": buttonname[3],
            "value": Org_list[3],
        }
        ]
    elif len(Org_list) == 5:
        buttons = [{
            "title": buttonname[0],
            "value": Org_list[0],
        },
            {
            "title": buttonname[1],
            "value": Org_list[1],
        },
            {
            "title": buttonname[2],
            "value": Org_list[2],
        },
            {
            "title": buttonname[3],
            "value": Org_list[3],
        },
            {
            "title": buttonname[4],
            "value": Org_list[4],
        },
        ]
    elif len(Org_list) == 6:
        buttons = [{
            "title": buttonname[0],
            "value": Org_list[0],
        },
            {
            "title": buttonname[1],
            "value": Org_list[1],
        },
            {
            "title": buttonname[2],
            "value": Org_list[2],
        },
            {
            "title": buttonname[3],
            "value": Org_list[3],
        },
            {
            "title": buttonname[4],
            "value": Org_list[4],
        },
            {
            "title": buttonname[5],
            "value": Org_list[5],
        }
        ]

    return jsonify(
        status=200,
        replies=[
            {
                "type": "quickReplies",
                "content": {
                    "title": "Which Delivery Unit?",
                    "buttons": buttons
                }
            }
        ],
        conversation={
            'memory': {'key': 'value'}
        }
    )


@app.route('/errors', methods=['POST'])
def errors():
    print(json.loads(request.get_data()))
    return jsonify(status=200)


app.run(port=port)
