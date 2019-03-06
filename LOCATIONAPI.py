from flask import Flask, request, jsonify
import json
import requests
from KEY import API_key

app = Flask(__name__)
port = '5000'


@app.route('/', methods=['POST'])
def index():
    data = json.loads(request.get_data())
    location = data['conversation']['memory']['location']['raw']
    t = requests.get(
        'https://maps.googleapis.com/maps/api/place/textsearch/json?query=restaurants+in+'+location + '&key='+API_key)
    restaurants = t.json()['results'][:4]
    final = []
    for restaurant in restaurants:
        final.append(restaurant['name'])

    new = (t.json()['results'][0]['photos'][0]['html_attributions'])
    k = str(new)
    mapquest = k.find('href')
    mapping = k[mapquest+5:]

    return jsonify(
        status=200,
        replies=[{
            'type': 'text',
            'content': 'In %s you can eat at %s or %s and finally %s.' % (location, str(final[0]), str(final[1]), str(final[2]))
        }]


    )


@app.route('/errors', methods=['POST'])
def errors():
    print(json.loads(request.get_data()))
    return jsonify(status=200)


app.run(port=port)
