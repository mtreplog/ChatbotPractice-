from flask import Flask, request, jsonify
import json
import requests

app = Flask(__name__)
port = '5000'

Org_Dict = {'cross': 'M3CIT03003', 'finance': 'M2CIT00302', 'c2r': '',
            'g2m': '', 'sed': '', 'hr': 'M3CIT03009', 's/4': 'M3CIT04054', 'app': 'M3ITIN0206', }


@app.route('/', methods=['POST'])
def index():
    data = (json.loads(request.get_data()))
    org_unit = str(data['conversation']['memory']['Org_Unit']['raw']).lower()

    actuals = requests.get(
        'https://cost-center-management-production2.cfapps.eu10.hana.ondemand.com/rest/restactuals/v1/GetActuals')

    planned = requests.get(https: // cost-center-management-production2.cfapps.eu10.hana.ondemand.com/rest/restplanning/v1/GetPlanningByOrgunit)

    test = ''
    new = json.loads(actuals.text)
    TargetList = []
    Travel = 0
    ICO = 0
    ThirdParty = 0
    for i in new:
        try:
            if i['CostCenter']['DeliveryUnit']['OrganizationalUnit']['Node'] == Org_Dict[org_unit]:
                TargetList.append(i)
        except KeyError:
            pass

    for x in TargetList:
        if x['CostGroups'][0]['CostGroup'] == '3rd Party':
            ThirdParty += x['Budget_Actuals']

    for x in TargetList:
        if x['CostGroups'][0]['CostGroup'] == 'Travel':
            Travel += x['Budget_Actuals']

    for x in TargetList:
        if x['CostGroups'][0]['CostGroup'] == 'ICO':
            ICO += x['Budget_Actuals']

    return jsonify(
        status=200,
        replies=[{
            'type': 'text',
            'content': 'Travel:\nYou have spent $%i on Travel compared to 000 planned, this is percentage of your total budget.\n\nThird Party:\nYou have spent $%i on 3rd Party Consultants compared to 000 expected, this is pecentage of your total budget.\n\nICO:\nYou have spent $%i on ICO compared to 000 expected, this is percentage of your total budget.' % (Travel, ThirdParty, ICO)
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
