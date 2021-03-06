from flask import Flask, request, jsonify
import json

app = Flask(__name__)
port = '5000'

Org_Dict = {'oss': 'Operations & Shared Service', 'hr2': 'HR II', 'pr': 'Procurement',
            'iam': 'Identity & Accessmanagement', 's/4': 'IT S/4 HANA Program Office', 'app': 'IT Application Services Mgmt', 'cross': 'Cross IT & Operations Management', 'hr': 'HR I', 'cont': 'Controlling', 'CorpFin': 'Coprporate Finance Mgmt', 'shared': 'Shared IT Applications'}


@app.route('/mike', methods=['POST'])
def index():
    data = (json.loads(request.get_data()))
    org_unit = data['conversation']['memory']['Org_unit']['value']
    cost = data['conversation']['memory']['number']['value']
    cost_type = data['conversation']['memory']['costtype']['value']
    return jsonify(
        status=200,
        replies=[{
            'type': 'text',
            'content': str(cost_type)
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
