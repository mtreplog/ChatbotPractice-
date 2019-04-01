from flask import Flask, request, jsonify
import json

app = Flask(__name__)
port = '5000'


@app.route('/', methods=['POST'])
def index():
    data = (json.loads(request.get_data()))
    org_unit = data['conversation']['memory']['Org_unit']['value']
    cost = data['conversation']['memory']['number']['value']
    cost_type = data['conversation']['memory']['costtype']['value']
    return jsonify(
        status=200,
        replies=[{
            'type': 'text',
            'content': str(org_unit) + ', ' + str(cost) + ', ' + str(cost_type)
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
