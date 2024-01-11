#!/usr/bin/env python3
from flask import Flask
from flask import render_template

# Redis connection 
import redis
# the "Primary connection string" in the "Access keys"
redis_passwd = "tutorial-uta-cse6332-redis.redis.cache.windows.net:6380,password=b9Q42F5LUEahwEb2D6HCbXLzTcIupxtPtAzCaEpdjYE=,ssl=True,abortConnect=False"
redis_passwd = "b9Q42F5LUEahwEb2D6HCbXLzTcIupxtPtAzCaEpdjYE="
redis_host = "tutorial-uta-cse6332-redis.redis.cache.windows.net"
cache = redis.StrictRedis(
            host=redis_host, port=6380, 
            db=0, password=redis_passwd,
            ssl=True,
        )

if cache.ping():
    print("pong")

# to delete all data in the cache
def purge_cache():
    for key in cache.keys():
        cache.delete(key.decode())

# end of Redis connection

# Database connection part starts from here
import json
from azure.core.exceptions import AzureError
from azure.cosmos import CosmosClient, PartitionKey

DB_CONN_STR = "AccountEndpoint=https://tutorial-uta-cse6332.documents.azure.com:443/;AccountKey=fSDt8pk5P1EH0NlvfiolgZF332ILOkKhMdLY6iMS2yjVqdpWx4XtnVgBoJBCBaHA8PIHnAbFY4N9ACDbMdwaEw==;"
db_client = CosmosClient.from_connection_string(conn_str = DB_CONN_STR)
database = db_client.get_database_client("tutorial")
# Database connection part ends at here

def fetch_database(city_name = None, include_header = False, exact_match = False):
    container = database.get_container_client("us_cities")
    QUERY = "SELECT * from us_cities"
    params = None
    if city_name is not None:
        QUERY = "SELECT * FROM us_cities p WHERE p.city = @city_name"
        params = [dict(name="@city_name", value=city_name)]
        if not exact_match:
            QUERY = "SELECT * FROM us_cities p WHERE p.city like @city_name"
    
    headers = ["city", "lat", "lng", "country", "state", "population"]
    result = []

    # quickly fetch the result if it already in the cache
    if cache.exists(QUERY):
        result = json.loads(cache.get(QUERY).decode())
        print("cache hit: [{}]".format(QUERY))
    
    else:
        row_id = 0    
        for item in container.query_items(
            query=QUERY, parameters=params, enable_cross_partition_query=True,
        ):
            row_id += 1
            line = [str(row_id)]
            for col in headers:
                line.append(item[col])
            result.append(line)
        
        # cache the result for future queries
        cache.set(QUERY, json.dumps(result))
        print("cache miss: [{}]".format(QUERY))

    if include_header:
        line = [x for x in headers]
        line.insert(0, "")
        result.insert(0, line)

    return result


app = Flask(__name__)

@app.route("/", methods=['GET'])
def index():
    message = "Congratulations, it's a web app!"
    return render_template(
            'index.html',  
            message=message,
    )

import csv
def fetch_data(city_name = None, include_header = False, exact_match = False):
    return fetch_database(city_name=city_name, include_header = include_header, exact_match = exact_match)
    with open("us-cities.csv") as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        row_id = -1
        wanted_data = []
        for row in csvreader:
            row_id += 1
            if row_id == 0 and not include_header:
                continue
            line = []
            col_id = -1
            is_wanted_row = False
            if city_name is None:
                is_wanted_row = True
            for raw_col in row:
                col_id += 1
                col = raw_col.replace('"', '')
                line.append( col )
                if col_id == 0 and city_name is not None:
                    if not exact_match and city_name.lower() in col.lower():
                        is_wanted_row = True
                    elif exact_match and city_name.lower() == col.lower():
                        is_wanted_row = True
            if is_wanted_row:
                if row_id > 0:
                    line.insert(0, "{}".format(row_id))
                else:
                    line.insert(0, "")
                wanted_data.append(line)
    return wanted_data

from flask import request
@app.route('/data', methods=['GET'])
def query():
    city_name = request.args.get('city_name')
    if city_name is not None:
        city_name = city_name.replace('"', '')
    wanted_data = fetch_data(city_name = city_name, include_header = True)
    table_content = ""
    for row in wanted_data:
        line_str = ""
        for col in row:
            line_str += "<td>" + col + "</td>"
        table_content += "<tr>" + line_str + "</tr>"
    page = "<html><title>Tutorial of CSE6332 - Part2</title><body>"
    page += "<table>" + table_content + "</table>"
    page += "</body></html>"
    return page

def append_or_update_data(req):

    city_name = req['city_name'].replace('"', '')
    lat = req['lat'].replace('"', '')
    lng = req['lng'].replace('"', '')
    country = req['country'].replace('"', '')
    state = req['state'].replace('"', '')
    population = req['population'].replace('"', '')

    if city_name is None:
        return False

    input_line = '"{}","{}","{}","{}","{}","{}"'.format(
        city_name, lat, lng, country, state, population,
    )
    existing_records = fetch_data(city_name = city_name, exact_match=True)
    if len(existing_records) == 0:
        with open('us-cities.csv', 'a') as f:
            f.write(input_line)
            f.close()
    else:
        all_records = fetch_data(include_header=True)
        lines = []
        for row in all_records:
            line_to_write = ""
            if row[1].lower() != city_name.lower():
                line_to_write = ",".join(['"{}"'.format(col) for col in row[1:]])
            else:
                line_to_write = input_line
            lines.append(line_to_write + "\n")
        with open('us-cities.csv', 'w') as f:
            f.writelines(lines)
            f.close()
    return True

@app.route('/data', methods=['PUT'])
def append_or_update():
    req = request.json

    if append_or_update_data(req):
        return "done"
    else:
        return "invalid input"

def delete_data(city_name):
    existing_records = fetch_data(city_name = city_name, exact_match=True)
    if len(existing_records) > 0:
        all_records = fetch_data(include_header=True)
        lines = []
        for row in all_records:
            if row[1].lower() != city_name.lower():
                line_to_write = ",".join(['"{}"'.format(col) for col in row[1:]])
                lines.append(line_to_write + "\n")
        with open('us-cities.csv', 'w') as f:
            f.writelines(lines)
            f.truncate()
            f.close()
        return True
    return False

@app.route('/data', methods=['DELETE'])
def delete():
    city_name = request.args.get('city_name')
    if city_name is not None:
        city_name = city_name.replace('"', '')
    else:
        return "invalid input"

    if delete_data(city_name):
        return "done"
    else:
        return "city does not exist"

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)

