from flask import Flask, request, jsonify
import json
import requests
from KEY import API_key
import googlemaps
import os
import sapcai


app = Flask(__name__)
port = '5000'

client = sapcai.Client('deaf5a1884c93db71f9d487d02b935e7')
gmaps = googlemaps.Client(key=API_key)


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
    raw_image_data = gmaps.places_photo(
        photo_reference=picture_reference, max_height=40, max_width=40)

    f = open("googleimage.png", "wb")

    for i in raw_image_data:
        if i:
            f.write(i)

    f.close()
    # path = "C:\Users\I506992\Desktop\" + "static\ "
    #photo_name = path.trim() + query + '.' + photo_type

    # with open(photo_name, "wb") as photo:
    # photo.write(photo_request.content)

    return jsonify(
        status=200,
        replies=[{
            'type': 'text',
            'content': "{}\googleimage.png".format(os.getcwd()),
        }]


    )


@app.route('/errors', methods=['POST'])
def errors():
    print(json.loads(request.get_data()))
    return jsonify(status=200)


app.run(port=port)
