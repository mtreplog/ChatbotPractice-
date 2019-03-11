from flask import Flask, request, jsonify
import json
import requests
from KEY import API_key
import imghdr
import googlemaps

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
    picture_reference = t.json()['results'][0]['photos'][0]['photo_reference']
    photo_request = requests.get(
        'https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference='+picture_reference+'&key='+API_key)
    query = 'https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference=' + \
        picture_reference+'&key='+API_key
    photo_type = imghdr.what("", photo_request.content)
    # path = "C:\Users\I506992\Desktop\" + "static\ "
    #photo_name = path.trim() + query + '.' + photo_type

    # with open(photo_name, "wb") as photo:
    # photo.write(photo_request.content)
    return jsonify(
        status=200,
        replies=[{
            'type': 'text',
            'content': photo_type
        }]


    )


@app.route('/errors', methods=['POST'])
def errors():
    print(json.loads(request.get_data()))
    return jsonify(status=200)


app.run(port=port)
