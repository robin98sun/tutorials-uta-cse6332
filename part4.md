# How to build a Web Application on Azure - Part 3 - Using Database

When data size scales up, and when the complexity of data pattern and query goes high, database is inevitably a good choice to handle data.

Now, it's time to plug a database into your web application.

### Step 1: create a database *server* on Azure

1. Right click "PostgreSQL servers (Flexible)" in the Azure Tools extention of VS Code, and select "Create Server".
1. Select "Core (SQL)".
1. After providing a unique name, select "Serverless"
1. Select "Create a new Resource Group" and accept the default value
1. Select the recommended zone
1. Wait for a little while...

When the process complete, the newly created database *server* will appear under the sub-menu "Azure Cosmos DB".

Note: right now it's only a server with a fundamental DBMS running on it. To store data in the database system, we need to create a database instance, in short, a database.

### Step 2: create a database on the database server

1. Right click the newly created database *server*, select "Create Database..."
1. input the database name.
1. input "us-cities" as the id of the collection.
1. leave it empty for the partition key for we don't have much data yet.

Now the database instance is ready to store data. However, it's empty now. We'll move our data into the database so that it can start to work.

### Step 3: import data into the database

1. unfold the newly created database instance there shall be a collection (table) named "us-cities". If not, please find a way to create it.
1. right click on the collection "us_cities" and select "Import Document into a Collectin...". Note: the collection name shall follow the rules similar as naming variables in a program, where a "-" is not allowed in the middle of a variable name.
1. while trying to select the "us-cities.csv" file, it's gray and unselectable...why?

Because by default it only upload JSON files. So, we need to convert the csv file into a collection of JSON documents.

That's why in this kind of databases, unlike the rational SQL database, each row of data is called a document and the whole table is called a collection.

This kind of databases usually have a common name: Non-SQL Database, or Key-Value Store (Key-Value Store is an increasing hot topic and if you are interested please refer to CSE 6350 Advanced Topics in Computer Architecture instructed by Dr. Song Jiang).

After converting the csv file into a collection of JSON documents (in case you don't know how to, please refer to [this](./src/part4/convert-csv-to-documents.py)), select all those generated JSON files by press "Cmd-A" on MacOS or "Ctrl-A" if on Windows. Then you will see they are imported into the "Documents" folder under the collection "us-cities"

### Step 4: connect to the database in your application 

Please refer to [this document](https://learn.microsoft.com/en-us/azure/cosmos-db/nosql/how-to-python-get-started?tabs=env-virtual%2Cazure-cli%2Cwindows) for detailed introduction of how to connect to a `Azure Cosmos DB`. Some notes:

1. how to get the connection string of the newly created database: right click the database server in Azure Tools and select "Copy Connection String", then it is in your clipboard.
2. use database connection string to connect to the database, for example:
```python
import uuid
from azure.core.exceptions import AzureError
from azure.cosmos import CosmosClient, PartitionKey

# update the connection string to your own string
# the database in the tutorial has been deleted.
DB_CONN_STR = "AccountEndpoint=https://tutorial-uta-cse6332.documents.azure.com:443/;AccountKey=eWrWM8m3zWEQI1uBsWgFEOEBOuue7m68PRANCQCTGCRf3tnPEYvyNXoNGNBnowsmxR7UmxiC5aKTACDbpN0wdw=="
db_client = CosmosClient.from_connection_string(conn_str = DB_CONN_STR)
```

### Step 5: query the database

Please refer to [this document](https://learn.microsoft.com/en-us/python/api/overview/azure/cosmos-readme?view=azure-python).

Notes:

1. In the `Azure Tools` the term "Table" in Rational DB is substituted with "Collection". But in the referred document it is using another term "Container". They are representing the same thing but different names in their own context. This is just kind of traditions from different cultures. At some point it reveals the complexity of the industry world.
1. You will get identical results by replacing the `fetch_data` function in the app with querying database like this:
```python
def fetch_data(city_name = None, include_header = False, exact_match = False):
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
    row_id = 0
    if include_header:
        line = [x for x in headers]
        line.insert(0, "")
        result.append(line)
    
    for item in container.query_items(
        query=QUERY, parameters=params, enable_cross_partition_query=True,
    ):
        row_id += 1
        line = [str(row_id)]
        for col in headers:
            line.append(item[col])
        result.append(line)
    return result
```

### Step 6: for creating/updating/deleting records, or complex queries

Please try it out according to the referred document above and the example code for simple query.

### An interesting character of Azure Cosmos DB:

Maybe you have noticed in *`step 3`* we call it as a Non-SQL database, while in *`step 5`* a SQL is used to query the database. What does it mean? Is Azure Cosmos DB still a Non-SQL database? If yes, why does it support SQL query interface but being called Non-SQL database?

That's a long but interesting story, you may do your research on Google if you are interested.

