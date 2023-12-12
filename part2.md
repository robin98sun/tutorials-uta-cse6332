# How to build a Web Application on Azure - Part 2 - RESTful API

## What is and why using RESTful API ([full reference](https://aws.amazon.com/what-is/restful-api/))

APIs that follow the REST architectural style are called REST APIs, where Representational State Transfer (REST) is a software architecture that imposes conditions on how an API should work. [The introduction from Amazon](https://aws.amazon.com/what-is/restful-api/) is good enough that we don't have to go through it again. Only one thing to remind, REST architecture in HTTP only serves one possibility, it does not deny the possibility of implementing RESTful APIs in other protocols such as MQTT.


## An example: a RESTful API for querying data from a document

Copy the datafile `us-cities.csv` to the root directory of your code.

In case you want to know how to represent a table using HTML, here is the [introduction](https://www.w3schools.com/html/html_tables.asp).

### Step 1: to query data:
```python
import csv
def fetch_data(city_name = None, include_header = False, exact_match = False):
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
```
You'll see the data of the Orland Park when accessing in the browser like `http://localhost:8080/data?city_name=orland`, and you'll see all the data if omitting the `city_name` parameter in the URL.

### Step 2: to append or update data in the datafile

Add the following code in the file `app.py`:
```python
def append_or_update_data(req):
    city_name = req['city_name']
    lat = req['lat']
    lng = req['lng']
    country = req['country']
    state = req['state']
    population = req['population']

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
```

Create a new file `client.py` with the following code:
```python
import requests

url = 'http://127.0.0.1:8080/data'
myobj = {
    'city_name': 'New Rome',
    'lat': 19.8987,
    'lng': -155.6659,
    'country': 'Utopia',
    'state': 'Nowhere',
    'population': '1442000',
}

res = requests.put(url, json = myobj)

print(res.text)
```

In the terminal run `client.py`
```bash
python3 client.py
```

Then, you'll see the appended data when accessing `http://127.0.0.1:8080/data` in the browser, and you'll see the updated value if the city already exist.

### Step 3: To delete a data entry in the file

Add the following code in file `app.py`:
```python
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
```

Update the code in file `client.py` to:
```python
url = 'http://127.0.0.1:8080/data?city_name="New Rome"'
res = requests.delete(url)

print(res.text)
```

After running `client.py` you shall see the data entry "New Rome" has been deleted

Please note, the CRUD (Create, Retrieve, Update, Delete) APIs are defined at the same path `/data` with different HTTP methods: PUT, GET, PUT, DELETE respectively. This is a classic way to define RESTful APIs for a web service. In this way the user can understand what the API works for just by reading its path and method.

`POST` method is not used here, because as a best practice the semantic meaning of POST is for batch inserting or updating, while PUT is for the same functions on a single row of record.

#### Now you shall be able to create your own RESTful APIs through which you can provide services to third-party users, e.g., downstream services on the internet, or be integrated in any other applications.



