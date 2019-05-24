from flask import Flask, request, jsonify
import json
import requests
import math

app = Flask(__name__)
port = '5000'
Org_unit = ''
cost = 0
del_unit = ''
CCDict = {'IT S/4 Hana PO SE': '101004059',
          'IT S/4 HANA PO FRAN': '105410111', 'IT S/4 Hana PO US': '108004032', 'IT AppServ Mgmt SE': '101030073', 'IT AppServ Mgmt US': '108004071', 'IT HR I SE': '101004080', 'IT HR I FR': '105410113', 'IT HR I US': '108004051', 'IT HR I ARG': '161004073', 'IT HR I MEX': '135004021', 'IT HR II SE': '101035010', 'IT HR II SGD': '115000402', 'Cross IT & Ops Mg US': '108004036', 'Cross IT & Ops Mg SE': '101035101', 'IT Ops & SharServ US': '108611700', 'IT O &SS CAN': '109004102', 'IT Ops & SharServ SE': '101000432', 'IT Op & ShServ SGD': '115004535', 'IT I&DM CAN': '109420400', 'IT IAM SE': '101000452', 'SharIT App SE': '101035103', 'SharIT App IND': '176223020', 'IT Core Finance SE': '101000348', 'IT Controlling SE': '101004002', 'IT Corp Fin Mgmt SE': '101030010', 'IT Procurement SE': '101035030', 'IT Compliance FR': '10500616', 'IT Core Finance US': '108000402', 'IT Controlling US': '108061152', 'IT Procurement US': '108611541', 'IT Procurement SGD': '115000330', 'IT Controlling SGD': '115004913', 'IT Core Finance SGD': '115800024', 'IT Procurement IND': '176074148', 'IT Core Finance ROM': '181000170', 'IT Controlling ROM': '181010088', 'IT Compliance DUB': '700092330', 'IT GtM Serv Mgmt US': '108001010', 'IT GtM Serv Mgmt SE': '101000378', 'IT GtM Serv Mgmt SGP': '115040229', 'IT GtM Serv Mgmt IND': '176000414', 'IT Marketing CAN': '109463005', 'IT Marketing SE': '101035106', 'IT Marketing US': '108404039', 'IT Marketing SE': '101034801', 'IT Sales Fran Ap SE': '101000353', 'IT Sales Fran Ap SGD': '115004013', 'IT PMgt CAN': '109000402', 'IT PMgt FRAN': '105410107', 'Core Processes-SGD': '115004912', 'IT Sales II SGD': '115000140', 'IT GtM ServSal II US': '108040540', 'IT GtM ServSal I SE': '101004081', 'IT GtM ServSal I ROM': '181000400', 'IT Sales I SGD': '115414000', 'IT GtM SerSal I SMAT': '750200749', 'IT DES - Sal I SMAT': '750200746', 'IT GtM ServSal I US': '108611537', 'IT DES - Sale I DUB': '700092217', 'IT SolCent IND': '176017610', 'IT Field Fin Mgmt Us': '108004029', 'IT Field Fin Mgmt SE': '101011236', 'IT Field Fin I SE': '101062161', 'IT Field Fin I SGD': '115004902', 'IT Field Fin I ROM': '181000200', 'IT Rev Acc SGD': '115049115', 'IT Field Fin II ROM': '181004017', 'Core Processes - GY': '101000426', 'Field Finance IT IND': '176017006', 'IT Field Fin I IND': '176014210', 'IT Rev Acc SE': '101000499', 'IT Rev Acc US': '108004025', 'IT Field Loc US': '108404036', 'IT Appl Arch SE': '101004027', 'IT Appl Arch US': '108000428', 'IT Appl Arch CAN': '109000403', 'AS - E&F Mgmt ROM': '181071071', 'IT Ent & Ful Mgmt SE': '101004007', 'IT Serv EngDel SE': '101035080', 'IT Serv Del US': '108471123', 'IT Serv Del Old SE': '101040225', 'IT Serv EngDel US': '108471123', 'IT Serv EngDel SGD': '115000490'}
NodeDict = {'IT Human Resources': 'M3CIT03009', 'IT S/4 HANA Program Office': 'M3CIT04054', 'IT Application Services Mgmt': 'M3ITIN0206', 'Cross IT & Operations': 'M3CIT03003', 'IT Corporate Finance': 'M2CIT00302',
            'IT Go-to-Market Services': 'M2CIT00312', 'IT Contract to Revenue': 'M3CIT03008', 'IT Application Architecture': 'M3ITIN0214', 'IT Services, Entitlement & Delivery': 'M3CIT03010', 'IT Core Value Chain Services Mgmt': 'M2CIT00305'}
S4HANACC = ['IT S/4 Hana PO SE', 'IT S/4 HANA PO FRAN', 'IT S/4 Hana PO SE', 'IT S/4 HANA PO US']
ITAPPSERV = ['IT AppServ Mgmt SE', 'IT AppServ Mgmt US']
HRI = ['IT HR I SE', 'IT HR I FR', 'IT HR I US', 'IT HR I ARG', 'IT HR I MEX']
HRII = ['IT HR II SE', 'IT HR II SGD']
CrossIT = ['Cross IT & Ops Mg US', 'Cross IT & Ops Mg SE']
OpsShared = ['IT Ops & SharServ US', 'IT O &SS CAN', 'IT Ops & SharServ SE', 'IT Op & ShServ SGD']
IAM = ['IT I&DM CAN', 'IT IAM SE']
SharedIT = ['SharIT App SE', 'SharIT App IND']
CoreFinance = ['IT Core Finance SE', 'IT Core Finance US',
               'IT Core Finance ROM', 'IT Core Finance SGD']
Controlling = ['IT Controlling SE', 'IT Controlling US', 'IT Controlling SGD', 'IT Controlling ROM']
Procurement = ['IT Procurement SE', 'IT Procurement US', 'IT Procurement SGD', 'IT Procurement IND']
CorporateFin = ['IT Corp Fin Mgmt SE']
GTMManagement = ['IT GtM Serv Mgmt US', 'IT GtM Serv Mgmt SE',
                 'IT GtM Serv Mgmt SGP', 'IT GtM Serv Mgmt IND']
Marketing = ['IT Marketing CAN', 'IT Marketing US', 'IT Marketing SE']
FranchiseApp = ['IT Sales Fran Ap SE', 'IT Sales Fran Ap SGD']
PartnerManagement = ['IT PMgt CAN', 'IT PMgt FRAN', 'Core Processes - SGD']
SalesII = ['IT Sales II SGD', 'IT GtM ServSal II US']
SalesI = ['IT GtM ServSal I SE', 'IT GtM ServSal I ROM', 'IT GtM ServSal I ROM', 'IT Sales I SGD',
          'IT GtM SerSal I SMAT', 'IT DES - Sal I SMAT', 'IT GtM ServSal I US', 'IT DES - Sale I DUB', 'IT SolCent IND']
SolutionCenter = ['IT SolCent IND']
C2RMgmtUS = ['IT Field Fin Mgmt US']
C2RMgmtSE = ['IT Field Fin Mgmt SE']
CtRI = ['IT Field Fin I SE', 'IT Field Fin I SGD', 'IT Rev Acc SGD', 'IT Field Fin I ROM']
CtRII = ['IT Field Fin II ROM', 'Core Processes - GY']
IND = ['Field Finance IT IND', 'IT Field Fin I IND']
RevenueAcounting = ['IT Rev Acc SE', 'IT Rev Acc US']
US = ['IT Field Loc US']
ITAppArchit = ['IT Appl Arch SE', 'IT Appl Arch US', 'IT Appl Arch CAN']
Entitlement = ['AS - E&F Mgmt ROM', 'IT Ent & Ful Mgmt SE']
ServiceDelivery = ['IT Serv EngDel SE', 'IT Serv Del US',
                   'IT Serv Del Old SE', 'IT Serv EngDel US', 'IT Serv EngDel SGD']
ITCoreValueChain = ['IT SVC Svc Mgmt SE']
DU_dict = ['1GtM Management', '1Marketing', '1Franchise Apps', '1Partner Management', '1Sales II', '1Sales I', '1Solution Center',
           '2C2R Mgmt. US', '2C2R Mgmt. SE', '2CtRI', '2CtRII', '2IND', '2Revenue Acounting', '2US', '3IT Application Architecture', '4Entitlement & Fullfillment Mgmt', '4Services Delivery', '5CVCS Mgmt', '6IT S/4 HANA Program Office', '7IT Application Services Mgmt', '8HR I', '8HR II', '9Cross IT & Operations Management', '9Operations & Shared Service', '9Identity & Accessmanagement', '9Shared IT Applications', 'zCore Finance', 'zControlling', 'zCorporate Finance Mgmt', 'zProcurement']
Compliance = ['IT Compliance FR', 'IT Compliance DUB']


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
    payload['CostCenter']['DeliveryUnit']['OrganizationalUnit']['Node'] = NodeDict[Org_unit]
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
    global Org_unit
    global cost
    data = (json.loads(request.get_data()))

    Org_unit = str(data['conversation']['memory']['org_unit']['raw'])
    cost = int(data['conversation']['memory']['money']['raw'])
    if Org_unit == 'IT Go-to-Market Services':
        placeholder = '1'
    elif Org_unit == 'IT Contract to Revenue':
        placeholder = '2'
    elif Org_unit == 'IT Application Architecture':
        placeholder = '3'
    elif Org_unit == 'IT Services, Entitlement & Delivery':
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


@app.route('/DU1', methods=['POST'])
def DU1():
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
    global del_unit
    data = (json.loads(request.get_data()))
    del_unit = str(data['conversation']['memory']['deliveryunit']['raw'])
    if del_unit == 'IT S/4 HANA Program Office':
        CClist = S4HANACC
    elif del_unit == 'IT Application Services Mgmt':
        CClist = ITAPPSERV
    elif del_unit == 'HR I':
        CClist = HRI
    elif del_unit == 'HR II':
        CClist = HRII
    elif del_unit == 'Cross IT & Operations Management':
        CClist = CrossIT
    elif del_unit == 'Operations & Shared Service':
        CClist = OpsShared
    elif del_unit == 'Identity & Accessmanagement':
        CClist = IAM
    elif del_unit == 'Shared IT Applications':
        CClist = SharedIT
    elif del_unit == 'Core Finance':
        CClist = CoreFinance
    elif del_unit == 'Controlling':
        CClist = Controlling
    elif del_unit == 'Corporate Finance Mgmt':
        CClist = CorporateFin
    elif del_unit == 'Procurement':
        CClist = Procurement
    elif del_unit == 'Compliance':
        CClist = Compliance
    elif del_unit == 'GtM Management':
        CClist = GTMManagement
    elif del_unit == 'Marketing':
        CClist = Marketing
    elif del_unit == 'Franchise Apps':
        CClist = FranchiseApp
    elif del_unit == 'Partner Management':
        CClist = PartnerManagement
    elif del_unit == 'Sales II':
        CClist = SalesII
    elif del_unit == 'Sales I':
        CClist = SalesI
    elif del_unit == 'Solution Center':
        CClist = SolutionCenter
    elif del_unit == 'C2R Mgmt. US':
        CClist = C2RMgmtUS
    elif del_unit == 'C2R Mgmt. SE':
        CClist = C2RMgmtSE
    elif del_unit == 'CtRI':
        CClist = CtRI
    elif del_unit == 'CtRII':
        CClist = CtRII
    elif del_unit == 'IND':
        CClist = IND
    elif del_unit == 'Revenue Acounting':
        CClist = RevenueAcounting
    elif del_unit == 'US':
        CClist = US
    elif del_unit == 'IT Application Architecture':
        CClist = ITAppArchit
    elif del_unit == 'Entitlement & Fullfillment Mgmt':
        CClist = Entitlement
    elif del_unit == 'Services Delivery':
        CClist = ServiceDelivery
    elif del_unit == 'CVCS Mgmt':
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
