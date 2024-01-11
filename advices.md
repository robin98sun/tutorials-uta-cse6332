# Some advices about the assigments

1. Cloud computing is nothing different with multi-process computing except being overwhelming at every aspect, including but not limited in:

     volume of data, velocity of generating data, variety of data (3V of bigdata)

2. It's never safe to directly access database in cloud computing, that would be the last thing you want to do if you could get data somewhere else.

3. In-memory cache is one of the most powerful tools in cloud computing when

    a) volume of data is overwhelming 

    b) computing cost is overwhelming

4. In Assignment3 and Assignment4, it is a readonly scenario, there is no updates, the database itself is in readonly mode if you had ever noticed. For more complicated but very common scenario should be the separation of read and write. Here in this case, the problem is:

    a) volume of data is too big for a single VM system to process

    b) the computing cost is too big for a single thread program

5. Solutions would be: pre-fetching, pre-computing, etc., in other words: warm the system up as much as possible before accepting user requests (queries).

6. In Assignment4, you could pre-fetch the entire "cities" table and store in Redis, and then pre-compute the intermediate results and cache them in Redis:

    distance matrix of all cities,

    population table, 

    average score table,

    popular words per city, and so on.

7. When serving the incoming request, there shall not have any on-the-fly database access and all the computing work shall only rely on Redis. Moreover, the computing should never start from the beginning for serving the requests, it should reuse as much of the intermediate results as possible.

8. Why not cache data literally in the memory? Why Redis?

     You may already noticed the memory of the container where your app is deployed on the cloud is not sufficient to store all the intermediate results. That's also true for all the production systems of those big internet companies. So we use in-memory cache products like Redis, Memcached, etc.

9. Why don't use large memory machines instead? Because it is not scalable. For deeper discussions, please contact us in ACES lab (https://aceslab.uta.edu/Links to an external site.).