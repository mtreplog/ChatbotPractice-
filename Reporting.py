from flask import Flask, request, jsonify
import json
import requests
import math


app = Flask(__name__)
port = '5000'
Org_unit = ''
cost = 0
del_unit = ''
Node = ''
CClist = ''
CCDict = {}
Travel = 0
ICO = 0
ThirdParty = 0


@app.route('/mike', methods=['POST'])
def index():
    data = (json.loads(request.get_data()))

    planned = requests.get(
        'https://cost-center-management-production2.cfapps.eu10.hana.ondemand.com/rest/restplanning/v1/Planning', timeout=15)

    plannedjson = json.loads(planned.text)

    PercentTraveled = 0
    PercentICO = 0
    PercentThirdParty = 0
    Planninglist = []
    travelplanned = 0
    ICOplanned = 0
    ThirdPartyplanned = 0
    global ThirdParty
    global ICO
    global Travel

    for m in plannedjson:
        try:
            if m['CostCenter']['DeliveryUnit']['DU'] == del_unit:
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
    global cost
    global Org_unit
    global del_unit
    global CCDict
    global Node
    date = data['conversation']['memory']['date']['value'].lower()
    CostType = data['conversation']['memory']['cost_group']['raw']
    userid = data['conversation']['memory']['userid']['value']
    name = data['conversation']['memory']['person']['fullname']
    CCname = data['conversation']['memory']['costcenter']['raw']
    headers = {'content-type': 'application/json'}
    CostGroup = data['conversation']['memory']['cost_type']['raw']
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

    if date == 'q1':
        payload['Jan'] = int(cost/3)
        payload['Feb'] = int(cost/3)
        payload['Mar'] = int(cost/3)
    elif date == 'q2':
        payload['Apr'] = int(cost/3)
        payload['May'] = int(cost/3)
        payload['Jun'] = int(cost/3)
    elif date == 'q3':
        payload['Jul'] = int(cost/3)
        payload['Aug'] = int(cost/3)
        payload['Sep'] = int(cost/3)
    elif date == 'q4':
        payload['Oct'] = int(cost/3)
        payload['Nov'] = int(cost/3)
        payload['Dec'] = int(cost/3)
    else:
        payload[date.title()[:3]] = cost
    payload['CostCenter']['DeliveryUnit']['OrganizationalUnit']['OU'] = Org_unit
    payload['Resource']['Name'] = name.title()
    payload['Resource']['UserID'] = userid.title()
    payload['CostCenter']['DeliveryUnit']['DU'] = del_unit
    payload['CostCenter']['DeliveryUnit']['OrganizationalUnit']['Node'] = Node
    payload['CostGroup']['CostGroup'] = CostType
    payload['CostCenter']['CCID'] = CCDict[CCname]
    payload['CostCenter']['Name'] = CCname
    payload['CostType']['CostType'] = CostGroup
    post = requests.post(
        'https://cost-center-management-production2.cfapps.eu10.hana.ondemand.com/rest/restplanning/v1/Planning', json=payload, headers=headers)
    return jsonify(
        status=200,
        replies=[{
            'type': 'text',
            'content': 'Success!'
        }],
        conversation={
            'memory': {'key': 'value'}
        }
    )


@app.route('/DU', methods=['POST'])
def DU():
    placeholder = ""
    count = 0
    Org_list = []
    global Org_unit
    global cost
    data = (json.loads(request.get_data()))
    global Node
    Org_unit = str(data['conversation']['memory']['org_unit']['raw'])
    cost = int(data['conversation']['memory']['money']['amount'])

    actuals = requests.get(
        'https://cost-center-management-production2.cfapps.eu10.hana.ondemand.com/rest/restactuals/v1/GetActuals')
    final = json.loads(actuals.text)

    for i in final:
        try:

            if i['CostCenter']['DeliveryUnit']['OrganizationalUnit']['OU'] == Org_unit:
                Node = i['CostCenter']['DeliveryUnit']['OrganizationalUnit']['Node']
                for key in Org_list:
                    if i['CostCenter']['DeliveryUnit']['DU'] == key:
                        count += 1
                if count == 0:
                    Org_list.append(i['CostCenter']['DeliveryUnit']['DU'])

            count = 0
        except KeyError:
            pass

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
    elif len(Org_list) == 7:
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
        },
            {
            "title": buttonname[6],
            "value": Org_list[6],
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


@app.route('/DU1', methods=['POST'])
def DU1():
    Actuallist = []
    global ThirdParty
    global Travel
    global ICO
    placeholder = ""
    Org_list = []
    count = 0
    data = (json.loads(request.get_data()))

    Org_unit = str(data['conversation']['memory']['org_unit']['raw'])

    actuals = requests.get(
        'https://cost-center-management-production2.cfapps.eu10.hana.ondemand.com/rest/restactuals/v1/GetActuals')
    final = json.loads(actuals.text)

    for i in final:
        try:
            if i['CostCenter']['DeliveryUnit']['OrganizationalUnit']['OU'] == Org_unit:
                for key in Org_list:
                    if i['CostCenter']['DeliveryUnit']['DU'] == key:
                        count += 1
                if count == 0:
                    Org_list.append(i['CostCenter']['DeliveryUnit']['DU'])

            count = 0
        except KeyError:
            pass

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
    elif len(Org_list) == 7:
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
        },
            {
            "title": buttonname[6],
            "value": Org_list[6],
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


@app.route('/CC', methods=['POST'])
def costcenter():
    CClist = []
    buttonname = []
    global CCDict
    global del_unit
    data = (json.loads(request.get_data()))
    del_unit = str(data['conversation']['memory']['deliveryunit']['raw'])

    count = 0

    actuals = requests.get(
        'https://cost-center-management-production2.cfapps.eu10.hana.ondemand.com/rest/restactuals/v1/GetActuals')
    final = json.loads(actuals.text)

    for i in final:
        try:
            if i['CostCenter']['DeliveryUnit']['DU'] == del_unit:
                for key in CClist:
                    if i['CostCenter']['Name'] == key:
                        count += 1
                if count == 0:
                    CClist.append(i['CostCenter']['Name'])
                    CCDict[(i['CostCenter']['Name'])] = (i['CostCenter']['CCID'])

            count = 0
        except KeyError:
            pass

    for q in CClist:
        if len(q) > 20:
            buttonname.append(q[:20])
        else:
            buttonname.append(q)
    if len(CClist) == 1:
        buttons = [{
            "title": buttonname[0],
            "value": CClist[0],
        }, ]
    elif len(CClist) == 2:
        buttons = [{
            "title": buttonname[0],
            "value": CClist[0],
        },
            {
            "title": buttonname[1],
            "value": CClist[1],
        }

        ]
    elif len(CClist) == 3:
        buttons = [{
            "title": buttonname[0],
            "value": CClist[0],
        },
            {
            "title": buttonname[1],
            "value": CClist[1],
        },
            {
            "title": buttonname[2],
            "value": CClist[2],
        },
        ]
    elif len(CClist) == 4:
        buttons = [{
            "title": buttonname[0],
            "value": CClist[0],
        },
            {
            "title": buttonname[1],
            "value": CClist[1],
        },
            {
            "title": buttonname[2],
            "value": CClist[2],
        },
            {
            "title": buttonname[3],
            "value": CClist[3],
        }
        ]
    elif len(CClist) == 5:
        buttons = [{
            "title": buttonname[0],
            "value": CClist[0],
        },
            {
            "title": buttonname[1],
            "value": CClist[1],
        },
            {
            "title": buttonname[2],
            "value": CClist[2],
        },
            {
            "title": buttonname[3],
            "value": CClist[3],
        },
            {
            "title": buttonname[4],
            "value": CClist[4],
        },
        ]
    elif len(CClist) == 6:
        buttons = [{
            "title": buttonname[0],
            "value": CClist[0],
        },
            {
            "title": buttonname[1],
            "value": CClist[1],
        },
            {
            "title": buttonname[2],
            "value": CClist[2],
        },
            {
            "title": buttonname[3],
            "value": CClist[3],
        },
            {
            "title": buttonname[4],
            "value": CClist[4],
        },
            {
            "title": buttonname[5],
            "value": CClist[5],
        }
        ]
    elif len(CClist) == 7:
        buttons = [{
            "title": buttonname[0],
            "value": CClist[0],
        },
            {
            "title": buttonname[1],
            "value": CClist[1],
        },
            {
            "title": buttonname[2],
            "value": CClist[2],
        },
            {
            "title": buttonname[3],
            "value": CClist[3],
        },
            {
            "title": buttonname[4],
            "value": CClist[4],
        },
            {
            "title": buttonname[5],
            "value": CClist[5],
        },
            {
            "title": buttonname[6],
            "value": CClist[6],
        }
        ]

    return jsonify(
        status=200,
        replies=[
            {
                "type": "quickReplies",
                "content": {
                    "title": "Please select a Cost Center:",
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
