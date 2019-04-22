from flask import Flask, request, jsonify
import json
import requests
import math

app = Flask(__name__)
port = '5000'

NodeDict = {'IT Human resource': 'M3CIT03009', 'IT S/4 HANA Program Office': 'M3CIT04053', 'IT Application Services Mgmt': 'M3ITIN0206', 'Cross IT & Operations': 'M3CIT03003', 'IT Corporate Finance': 'M2CIT00302',
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
Marketing = ['101035106', '109463005', '108404039', '101034801', '101040258']
FranchiseApp = ['IT Sales Fran Ap SE', 'IT Sales Fran Ap SGD']
PartnerManagement = ['IT PMgt CAN', 'IT PMgt FRAN', 'Core Processes - SGD']
SalesII = ['IT Sales II SGD', 'IT Gtm ServSal II US']
SalesI = ['IT GTM ServSal I SE', 'IT GTM ServSal I ROM', 'IT GTM ServSal I ROM', 'IT Sales I SGD',
          'IT GTM SerSal I SMAT', 'IT DES - Sal I SMAT', 'IT GTM ServSal I US', 'IT DES - Sale I DUB', 'IT SolCent IND']
SolutionCenter = ['IT SolCent IND']
C2RMgmtUS = ['IT Field Fin Mgmt US']
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
    org_unit = data['conversation']['memory']['org_unit']['value']
    cost = data['conversation']['memory']['numbers']['value']
    cost_group = data['conversation']['memory']['costtype']['value'].lower()
    date = data['conversation']['memory']['date']['value']
    userid = data['conversation']['memory']['userid']['value']
    name = data['conversation']['memory']['person']['fullname']
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

    payload['CostCenter']['DeliveryUnit']['OrganizationalUnit']['OU'] = org_unit
    payload[cleandate] = cleancost
    payload['Resource']['Name'] = cleanname
    payload['Resource']['UserID'] = cleanid
    payload['CostCenter']['DeliveryUnit']['DU'] = cleanDU
    payload['CostCenter']['DeliveryUnit']['OrganizationalUnit']['Node'] = NodeDict[org_unit]
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
def DU():
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
    data = (json.loads(request.get_data()))
    Del_unit = str(data['conversation']['memory']['deliveryunit']['raw'])
    if Del_unit == 'IT S/4 HANA Program Office':
        CClist = S4HANACC
    elif Del_unit == 'IT Application Services Mgmt':
        CClist = ITAPPSERV
    elif Del_unit == 'HR I':
        CClist = HRI
    elif Del_unit == 'HR II':
        CClist = HRII
    elif Del_unit == 'Cross IT & Operations Management':
        CClist = CrossIT
    elif Del_unit == 'Operations & Shared Service':
        CClist = OpsShared
    elif Del_unit == 'Identity & Accessmanagement':
        CClist = IAM
    elif Del_unit == 'Shared IT Applications':
        CClist = SharedIT
    elif Del_unit == 'Core Finance':
        CClist = CoreFinance
    elif Del_unit == 'Controlling':
        CClist = Controlling
    elif Del_unit == 'Corporate Finance Mgmt':
        CClist = CorporateFin
    elif Del_unit == 'Procurement':
        CClist = Procurement
    elif Del_unit == 'Compliance':
        CClist = Compliance
    elif Del_unit == 'Gtm Management':
        CClist = GTMManagement
    elif Del_unit == 'Marketing':
        CClist = Marketing
    elif Del_unit == 'Franchise Apps':
        CClist = FranchiseApp
    elif Del_unit == 'Partner Management':
        CClist = PartnerManagement
    elif Del_unit == 'Sales II':
        CClist = SalesII
    elif Del_unit == 'Sales I':
        CClist = SalesI
    elif Del_unit == 'Solution Center':
        CClist = SolutionCenter
    elif Del_unit == 'C2R Mgmt. US':
        CClist = C2RMgmtUS
    elif Del_unit == 'C2R Mgmt. SE':
        CClist = C2RMgmtSE
    elif Del_unit == 'CtRI':
        CClist = CtRI
    elif Del_unit == 'CtRII':
        CClist = CtRII
    elif Del_unit == 'IND':
        CClist = IND
    elif Del_unit == 'Revenue Acounting':
        CClist = RevenueAcounting
    elif Del_unit == 'US':
        CClist = US
    elif Del_unit == 'IT Application Architecture':
        CClist = ITAppArchit
    elif Del_unit == 'Entitlement & Fullfillment Mgmt':
        CClist = Entitlement
    elif Del_unit == 'Services Delivery':
        CClist = ServiceDelivery
    elif Del_unit == 'CVCS Mgmt':
        CClist = ITCoreValueChain

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
