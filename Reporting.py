from flask import Flask, request, jsonify
import json
import requests
import math
import pandas as pd

app = Flask(__name__)
port = '5000'
Org_unit = ''
cost = 0
del_unit = ''
Node = ''
CClist = ''
CCDict = {}
NodeDict = {'IT Human Resources': 'M3CIT03009', 'IT S/4 HANA Program Office': 'M3CIT04053', 'IT Application Services Mgmt': 'M3ITIN0206', 'Cross IT & Operations': 'M3CIT03003', 'IT Corporate Finance': 'M2CIT00302',
            'IT Go-to-Market Services': 'M2CIT00312', 'IT Contract to Revenue': 'M3CIT03008', 'IT Application Architecture': 'M3ITIN0214', 'IT Services, Entitlement & Delivery': 'M3CIT03010', 'IT Core Value Chain Services Mgmt': 'M2CIT00305'}
S4HANACC = ['IT S/4 Hana PO SE', 'IT S/4 HANA PO FRAN', 'IT S/4 Hana PO SE', 'IT S/4 HANA PO US']
ITAPPSERV = ['IT AppServ Mgmt SE', 'IT AppServ Mgmt US']
HRI = ['IT HR I SE', 'IT HR I FR', 'IT HR I US', 'IT HR I ARG', 'IT HR I MEX']
HRII = ['IT HR II SE', 'IT HR II SGD']
CrossIT = ['Cross IT & Ops Mg US', 'Cross IT & Ops Mg SE']
OpsShared = ['IT Ops & SharServ US', 'IT O & SS CAN', 'IT Ops & SharServ SE']
IAM = ['IT I&DM CAN', 'IT IAM SE']
SharedIT = ['SharIT App SE', 'SharIT App IND']
CoreFinance = ['IT Core Finance SE', 'IT Core Finance US',
               'IT Core Finance ROM', 'IT Core Finance SGD']
Controlling = ['IT Controlling SE', 'IT Controlling US', 'IT Controlling SGD', 'IT Controlling ROM']
Procurement = ['IT Procurement SE', 'IT Procurement US', 'IT Procurement SGD', 'IT Procurement IND']
CorporateFin = ['IT Corp Fin Mgmt SE']
GTMManagement = ['IT GTM Serv Mgmt US', 'IT GTM Serv Mgmt SE',
                 'IT GTM Serv Mgmt SGP', 'IT GTM Serv Mgmt IND']
Marketing = ['IT Marketing CAN', 'IT Marketing US', 'IT Marketing SE']
FranchiseApp = ['IT Sales Fran Ap SE', 'IT Sales Fran Ap SGD']
PartnerManagement = ['IT PMgt CAN', 'IT PMgt FRAN', 'Core Processes - SGD']
SalesII = ['IT Sales II SGD', 'IT Gtm ServSal II US']
SalesI = ['IT GTM ServSal I SE', 'IT GTM ServSal I ROM', 'IT GTM ServSal I ROM', 'IT Sales I SGD',
          'IT GTM SerSal I SMAT', 'IT DES - Sal I SMAT', 'IT GTM ServSal I US', 'IT DES - Sale I DUB', 'IT SolCent IND']
SolutionCenter = ['IT SolCent IND']
C2RMgmtUS = ['IT Field Fin Mgmt Us']
C2RMgmtSE = ['IT Field Fin Mgmt SE']
CtRI = ['IT Field Fin I SE', 'IT Field Fin I SGD', 'IT Rev Acc SGD']
CtRII = ['IT Field Fin II ROM', 'Core Processes - GY']
IND = ['Field Finance IT IND', 'IT Field Fin I IND']
RevenueAcounting = ['IT Rev Acc SE', 'IT Rev Acc US']
US = ['IT Field Loc US']
ITAppArchit = ['IT Appl Arch SE', 'IT Appl Arch US', 'IT Appl Arch CAN']
Entitlement = ['AS i E&F Mgmt ROM', 'IT Ent & Ful Mgmt SE']
ServiceDelivery = ['IT Serv EngDel SE', 'IT Serv Del US',
                   'IT Serv Del Old SE', 'IT Serv EngDel US', 'IT Serv EngDel SGD']
ITCoreValueChain = ['IT SVC Svc Mgmt SE']
DU_dict = ['1GtM Management', '1Marketing', '1Franchise Apps', '1Partner Management', '1Sales II', '1Sales I', '1Solution Center',
           '2C2R Mgmt. US', '2C2R Mgmt. SE', '2CtRI', '2CtRII', '2IND', '2Revenue Acounting', '2US', '3IT Application Architecture', '4Entitlement & Fullfillment Mgmt', '4Services Delivery', '5CVCS Mgmt', '6IT S/4 HANA Program Office', '7IT Application Services Mgmt', '8HR I', '8HR II', '9Cross IT & Operations Management', '9Operations & Shared Service', '9Identity & Accessmanagement', '9Shared IT Applications', 'zCore Finance', 'zControlling', 'zCorporate Finance Mgmt', 'zProcurement']
Compliance = ['IT Compliance FR', 'IT Compliance DUB']
CCDict = {'IT GtM Serv Mgmt US': '108001010', 'IT GtM Serv Mgmt SE': '101000378'}


@app.route('/mike', methods=['POST'])
def index():
    data = (json.loads(request.get_data()))
    del_unit = str(data['conversation']['memory']['deliveryunit']['raw'])

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
            if i['CostCenter']['DeliveryUnit']['DU'] == del_unit:
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
    date = data['conversation']['memory']['date']['value'].lower()
    CostType = data['conversation']['memory']['cost_group']['raw']
    userid = data['conversation']['memory']['userid']['value']
    name = data['conversation']['memory']['person']['fullname']
    CCname = data['conversation']['memory']['costcenter']['raw']
    headers = {'content-type': 'application/json'}

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
    df = pd.read_excel('C:/Users/I506992/Desktop/NodesCC.xlsx')
    CCname2 = df['Unnamed: 4']
    CC = df['Unnamed: 3']
    Dict = dict(zip(CCname2, CC))

    df = pd.read_excel('C:/Users/I506992/Desktop/NodesCC.xlsx', sheet_name='Session2')
    CCname1 = df['Unnamed: 4']
    CC1 = df['Unnamed: 3']
    Dict2 = (zip(CCname1, CC1))

    z = Dict.copy()
    z.update(Dict2)

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
    payload['CostCenter']['DeliveryUnit']['OrganizationalUnit']['Node'] = NodeDict[Org_unit]
    payload['CostGroup']['CostGroup'] = CostType
    payload['CostCenter']['CCID'] = z[CCname]
    payload['CostCenter']['Name'] = CCname
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
    global CCnum
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
                    CCnum.append(i['CostCenter']['CCID'])

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
