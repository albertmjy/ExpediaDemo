from flask import Flask, render_template, jsonify, request, session

import hashlib
import time
import requests

app = Flask(__name__)

@app.route('/')
def index():  # put application's code here
    # data = request()
    return render_template('index.html')

@app.route('/list')
def list():  # put application's code here
    return render_template('list.html')

@app.route('/rooms')
def rooms():  # put application's code here

    return render_template('rooms.html')

@app.route('/auth')
def auth_api():  # put application's code here

    return jsonify({'auth': auth()})


@app.route('/data')
def data():  # put application's code here
    region_data = request_region(request.args['regionId'])
    print(region_data)

    content_data = request_content(region_data['property_ids'])
    # print(content_data)

    shopping_data = request_shopping(request.args, region_data['property_ids'], region_data['country_code'])

    print(shopping_data)

    return jsonify({'content_data':content_data, 'shopping_data':shopping_data, 'c_code':region_data['country_code']})

@app.route('/shoppingData')
def shopping_data():  # put application's code here
    content_data = request_rooms(request.args.get('prop_id'))
    shopping_data = request_shopping(request.args, [request.args.get('prop_id')], request.args.get('c_code'), n=1)

    # return jsonify(shopping_data)
    return jsonify({'content_data':content_data, 'shopping_data':shopping_data})


def auth():
    apiKey = "1m6lfng9fqd5fkv57r1c0cms70"
    secret = "60mdjb6pisd5u"
    timestamp = str(int(time.time()))
    data_to_hash = (apiKey + secret + timestamp).encode('utf-8')
    authHeaderValue = "EAN APIKey=" + apiKey + ",Signature=" + hashlib.sha512(
        data_to_hash).hexdigest() + ",timestamp=" + timestamp

    return authHeaderValue

def request_region(region_id):

    url = f"https://test.ean.com/v3/regions/{region_id}?language=en-US&include=details&include=property_ids"

    headers = {
        'Authorization': auth(),
        'Content-Type': 'application/json'
    }

    response = requests.request("GET", url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Failed to retrieve data: {response.status_code}")

def request_content(property_ids):
    prop_id_str = ''
    for i in range(6):
        prop_id_str = prop_id_str + '&property_id='+property_ids[i]

    content_url = f'https://test.ean.com/v3/properties/content?language=en-US&supply_source=expedia&include=property_id' + \
                  '&include=name&include=amenities&include=ratings&include=location&include=address&include=airports&include=fees&include=descriptions&include=images' +\
                  prop_id_str

    print(prop_id_str, '*'*50)

    headers = {
        'Authorization': auth(),
        'Content-Type': 'application/json'
    }
    response = requests.request("GET", content_url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Failed to retrieve data: {response.status_code}")

def request_rooms(property_id):

    content_url = f'https://test.ean.com/v3/properties/content?language=en-US&supply_source=expedia&include=property_id&include=amenities&include=name&include=rooms&property_id={property_id}'

    headers = {
        'Authorization': auth(),
        'Content-Type': 'application/json'
    }
    response = requests.request("GET", content_url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Failed to retrieve data: {response.status_code}")


def request_shopping(args, property_ids, country_code, n=3):
    prop_id_str = ''
    print(n, property_ids)
    for i in range(n):
        prop_id_str = prop_id_str + '&property_id=' + property_ids[i]

    shopping_url = 'https://test.ean.com/v3/properties/availability?checkin='+args.get('checkin')+'&checkout='+args.get('checkout')+\
                   '&country_code='+country_code+'&currency=USD&language=en-US&occupancy='+ args.get('occupancy') +'&rate_plan_count=1&sales_channel=website&sales_environment=hotel_only'+\
                    prop_id_str
    print(shopping_url)

    headers = {
        'Authorization': auth(),
        'Content-Type': 'application/json'
    }
    response = requests.request("GET", shopping_url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Failed to retrieve data: {response.status_code}")



if __name__ == '__main__':

    app.run()
