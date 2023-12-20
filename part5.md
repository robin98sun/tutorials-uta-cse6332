# How to build a Web Application on Azure - Part 5 - Speedup with in-memory cache

In this tutorial, we are going to explore in-memory cache on cloud. 

As per the description on Azure, an in-memory data store (cache) improves the *performance* and *scalability* of an application that uses backend data stores heavily. Redis brings a critical *low-latency* and *high-throughput* data storage solution to modern applications. 

Optional references:
1. [Optimize your web applications by caching read-only data with Redis](https://learn.microsoft.com/en-us/training/modules/optimize-your-web-apps-with-redis/?WT.mc_id=APC-AzureCacheforRedis).
1. [Shared memory in distributed application](https://learn.microsoft.com/en-us/training/modules/accelerate-scale-spring-boot-application-azure-cache-redis/?WT.mc_id=APC-AzureCacheforRedis)


## [Use Azure Cache for Redis in Python](https://learn.microsoft.com/en-us/azure/azure-cache-for-redis/cache-python-get-started)

Before getting started, prepare your web app and database according to [tutorial - part4](part4.md)

### Prepare a Redis service:

1. goto [Azure portal](https://portal.azure.com/)
1. search for `Azure Cache for Redis` service and create a new instance according to the [reference](https://learn.microsoft.com/en-us/azure/azure-cache-for-redis/cache-python-get-started)
1. note: 
    - select the same resource group as your web app
    - for `Cache type`, select `Basic C0 (250MB Cache, No SLA)` to minimize the cost.
1. wait until you seel "Your deployment is complete" on the web page.
1. retrieve the `Access keys` of the Redis instance, copy the `Primary`
1. the `Properties` of the Redis instance, copy `Host name`, `SSL Port`

### Prepare a client in your application:

1. create a file `requirements.txt` at the root directory of your application, file content:
```bash
redis>=5.0
azure-core>=1.29.0
azure-cosmos>=4.5.0
```
2. install the package in the terminal according to `requirements.txt`
```bash
pip install -r requirements.txt
```
3. in your app, prepare a redis client:
```python
import redis
# password is the "Primary" copied in "Access keys"
redis_passwd = "b9Q42F5LUEahwEb2D6HCbXLzTcIupxtPtAzCaEpdjYE="
# "Host name" in properties
redis_host = "tutorial-uta-cse6332-redis.redis.cache.windows.net"
# SSL Port
redis_port = 6380

cache = redis.StrictRedis(
            host=redis_host, port=redis_port, 
            db=0, password=redis_passwd,
            ssl=True,
        )

if cache.ping():
    print("pong")

```
4. run the app at local, "pong" shall appear in the log if the connection to the Redis instance is ready

### Understand the two fundamental operations of a key-value store: write and read

A in-memory data store is usually implemented as a key-value store (all data stored in memory). Redis is among the most popular ones. You can imagine it as a dictionary or map data structure.

* write: store data
    - to store a value in a `dict` variable (say, `data`), we use `data[key] = value`.
    - in a key-value store, the corresponding operation is `cache.set(key, value)`
* read: retrieve data
    - to retrieve the value from that `dict` variable `data`, we use `value = data[key]`.
    - in a key-value store, the corresponding operation is `value = cache.get(key)`

###  Naive in-memory cache for queries

Here we may use some other basic methods of in-memory cache: 
1. `exists`: to see if a key exists or not `if cache.exists(key): ...`.
1. `delete`: to delete a key in the cache: `cache.delete(key)`

First, in the `fetch_database` function, cache a query if it does not exist in the cache, or return an already cached query.

Second, delete all keys whenever there is any updates.

For the example code, please refer to the [source code](src/part5/app.py). Note, the source code is not a fully functional program, please fill in the necessary code for to your case.

### Questions to think about:

1. When will the in-memory be useful?
1. How useful will it be? 
1. Is it always useful?

## A hint for debugging Azure services:

In the Azure extension of VS Code, right click the service that you want to debug and select `Start Streams Logs`.

In very few cases, you may want to `SSH into Web App`.














