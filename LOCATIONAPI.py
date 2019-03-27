from flask import Flask, request, jsonify
import json
import requests
from KEY import API_key
import googlemaps
import operator
import sapcai


app = Flask(__name__)
port = '5000'

client = sapcai.Client('deaf5a1884c93db71f9d487d02b935e7')
gmaps = googlemaps.Client(key=API_key)


@app.route('/', methods=['POST'])
def index():
    data = json.loads(request.get_data())
    location = data['conversation']['memory']['location']['raw']
    type = str(data['conversation']['memory']['type']['raw'])
    t = requests.get(
        'https://maps.googleapis.com/maps/api/place/textsearch/json?query=restaurants+in+'+location + '&key='+API_key)
    restaurants = t.json()['results']
    final = {}
    for restaurant in restaurants:
        if restaurant["opening_hours"]["open_now"] is True:
            for x in restaurant["types"]:
                if x == type.lower():
                    final[restaurant['name']] = restaurant['rating']
        else:
            final["none"] = 3.3
    march = sorted(final.items(), key=operator.itemgetter(1))
    madness = march[-1][0]
    score = march[-1][1]
    madnessone = march[-2][0]
    scoreone = march[-2][1]
    madnesstwo = march[-3][0]
    scoretwo = march[-3][1]

    number = len(march)
    return jsonify(
        status=200,
        replies=[{

            "type": "buttons",
            "content": {
                    "title":  "We've found %s locations currently open that fit your criteria.\nOur highest rated restaurant in the area was '%s' with a rating of  %s/5. \n" % (str(number), str(madness), str(score)),
                    "buttons": [
                        {
                            "title": str(madness),
                            "type": "web_url",
                            "value": "https://www.yelp.com/search?find_desc=" + str(madness.strip().replace(' ', "+")) + "&find_loc=" + str(location.strip().replace(' ', '+')) + "&ns=1",
                        },
                        {
                            "title": str(madnessone),
                            "type": "web_url",
                            "value": "https://www.yelp.com/search?find_desc=" + str(madnessone.strip().replace(' ', "+")) + "&find_loc=" + str(location.strip().replace(' ', '+')) + "&ns=1",
                        },
                        {
                            "title": str(madnesstwo),
                            "type": "web_url",
                            "value": "https://www.yelp.com/search?find_desc=" + str(madnesstwo.strip().replace(' ', "+")) + "&find_loc=" + str(location.strip().replace(' ', '+'))+"&ns=1",
                        },


                    ],

            }




        }]


    )


@app.route('/errors', methods=['POST'])
def errors():
    print(json.loads(request.get_data()))
    return jsonify(status=200)


app.run(port=port)
