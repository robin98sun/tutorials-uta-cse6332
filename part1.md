# How to build a Web Application on Azure - Part 1 - the basic

In this tutorial, we are going to build a basic web application and deploy it on the Azure using VS Code.

### Prerequisites
1. Programming in Python.
2. Basic networking knowledge in HTTP and TCP/IP protocols, DNS. 
3. Basic knowledge in [HTML/CSS/Javascript](https://www.w3schools.com/), and [how does a web brower work](https://www.browserstack.com/guide/what-is-browser).
4. Basic coding experience with Microsoft Visual Studio Code.

## 1 Background

### What is a Web Application

According to [the definition from Amazon](https://aws.amazon.com/what-is/web-application/#:~:text=A%20web%20application%20is%20software,with%20customers%20conveniently%20and%20securely), a Web Appication (Web App) is a software runs in the web browser. Whereas according to [the definition from Wikipedia](https://en.wikipedia.org/wiki/Web_application), it is an application software that is accessed using a web browser and is delivered on the World Wide Web (WWW) to users with an active network connection. They are slightly different in wording. However, there is no such a formal definition exists even though it has been a norm in the industry for decades. This indicates a wide variance in the ways that web applications could be. Here are some most common scenarios:

1. Web sites.
2. [Single Page Application (SPA)](https://developer.mozilla.org/en-US/docs/Glossary/SPA) which can be used to build web sites, but also can be:
3. Integrated as part of the UI in any other kinds of applications such as mobile applications, desktop applications, etc..

Due to its strong cross-technique-culture adaptability, cross-platform compatibility, coding flexibility, and clearly-layered and well-standardized structure, web app is widely adopted in the industry from startup companies to tech giants.
As a consequence, web applications are not only the main compositions of WWW, but also very popular and common in our daily life.

### What does it have to do with Cloud Computing and BigData?

It's all about the scale.

In general, there are two ends of computing: on one end it is user, on the other end is data. It's clear and simple for an application to work on small amount of data (say, a database in megabytes or even gigabytes) and only serves a small group of users, typically a sales and inventory management system for a convenience store downstaires, a human-resource management system for a small business.

However, issues of client-compatibility, platform-compatibility and structure-complexity start to appear when either end of computing scales, e.g., the daily-alive-users (DAU) scales to tens of thousands or more ([DAU of Twitter in Q2'2022 reached 237.8 million](https://www.statista.com/statistics/970920/monetizable-daily-active-twitter-users-worldwide/)), service-requests-per-second scales to hundreds or more ([Google processes over 99,000 searches per second in 2022](https://www.oberlo.com/blog/google-search-statistics#:~:text=We%20know%20that%20there%20are,Internet%20Live%20Stats%2C%202022)), or the size of data store scales to terabytes or more ([Amazon stores over 160 exabytes of data - 163,840 terabytes](https://www.quora.com/How-much-data-is-currently-stored-by-Amazon#:~:text=However%2C%20estimates%20suggest%20that%20Amazon,exabytes%20of%20data%20by%202025)). Usually both ends scale simultaneously. Web application will be inevitably introduced to solve the problems of user end when the system scales or to be prepared for the possible scaling (either up or down). 

In short, because of the strong correlation between user end and data end, no matter what kind of service we are building on the cloud and no matter what scale it is, most likely we will deliver and present it to the users as a web application, and learning web application development becomes a good start point to solve real-world problems and to handle the challenges of BigData by leveraging Cloud Computing. 

## 2 Getting Started

### Step 1: setup the Python developing environment with Microsoft Visual Studio Code (VS Code)

please refer to: [Python environments in VS Code](https://code.visualstudio.com/docs/python/environments)

### Step 2: initiate a HTTP server using Python Flask ([the full reference](https://realpython.com/python-web-applications/))

In the CLI (command-line interface, a terminal), type the following command:

```bash
pip install flask
```

Create a file `my_app.py` using the following code:

```python
from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return "Congratulations, it's a web app!"

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)

```

### Step 3: start the HTTP server:

In the terminal, type the following commands:
```bash
pthon3 ./my_app.py
```
You should see:
```bash
 * Serving Flask app 'http_server'
 * Debug mode: off
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:8080
 * Running on http://192.168.64.157:8080
Press CTRL+C to quit
```

**Leave the terminal as it be** through out the tutorial, only restart if necessary (such as crashed). It can also be used as a clue to debug you code.

### Step 4: test in the browser

Then open the web browser, in the address input:
```
http://127.0.0.1:8080
```

You should see the following content in the browser if everything works well:

```text
Congratulations, it's a web app!
```

### Step 5: serve web pages with HTML templates:

Create a sub-directory `./templates` in which create a file `index.html` with the following content:
```html
<html>
    <head>
        <title>Tutorial of Building a Simple Web Application</title>
    </head>
    <body>
        <h1>{{message}}</h1>
    <body>
<html>

```

Update the HTTP server code in file `my_app.py` to:
```python
from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route("/", methods=['GET'])
def index():
    message = "Congratulations, it's a web app!"
    return render_template(
            'index.html',  
            message=message,
    )

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)
```

You will see HTTP server has been automatically updated in the terminal.

Repeat *Step 4* you shall see nothing changes in the browser.


### Step 6: serve static files, e.g., images:

1. Create a directory `./static`. 
2. Then move the image file (suppose, `thumbs-up.png`) to that directory (`./static`).
3. Update the HTML file `index.html` in the directory `./templates`:
```html
<html>
    <head>
        <title>Tutorial of Building a Simple Web Application</title>
    </head>
    <body>
        <h1>{{message}}</h1>
        <img src="/static/thumbs-up.png" width="100" hight="100"/>
    <body>
<html>
```

You shall see the image when refreshing the browser, or by directly accessing `http://127.0.0.1:8080/static/thumbs-up.png`

### A few useful tips of Flask

1. using part of url as a variable: add the following code to `my_app.py` and try to access `http://127.0.0.1:8080/alex` in the browser
```python
@app.route('/<name>')
def my_view_func(name):
    return name
```

2. to get variables from a url encoding like: `http://127.0.0.1:8080/login?username=alex&password=pw123456`: add the following code into `my_app.py` and try
```python
from flask import request
@app.route('/login', methods=['GET'])
def login():
    username = request.args.get('username')
    print(username)
    password= request.args.get('password')
    print(password)
    return username
    # You will see the username and password in the terminal logs   
```

3. A suggested directory structure:
```
App1/
│   my_app.py
│
└───static/css/
|   │   |   style.css
|
└───static/js/
|   │   |   myapp.js
|   |   |   jquery.js
|
└───static/img/
|   │   |   myimage.png
|
└───templates/
|   │   index.html
|
|   views.py
```

#### So far, you shall be able to convert a data file in `csv` format to a HTML file with some python functions and show in the browser.

## 3 Deploy the web app to Microsoft Azure ([reference](https://code.visualstudio.com/docs/python/python-on-azure))

### Step 1: Modify the code for deploying ([reference](https://github.com/Microsoft/python-sample-vscode-flask-tutorial))

It's kind of mystical for VS Code working out the whole thing and especially making your program automatically running on Azure just by clicking several buttons. Actually, behind the simplicity there are huge amount of engineering efforts.

However, we have to understand at least one thing before leaving everything to VS Code: how does Azure know how to start your program? Please refer to [this document](https://learn.microsoft.com/en-us/azure/developer/python/configure-python-web-app-on-app-service)

To be quick, we need to rename the `my_app.py` file to `application.py` or `app.py`, because by default Azure will look for that file and import the object `app` from that file to start a Flask application with default settings.
```
mv my_app.py app.py
```

### Step 2: Install the Azure Tools extension in VS Code

1. Search for Azure or cloud extensions in the VS Code Extensions view (⇧⌘X) and type 'azure'.
1. Install the extension `Azure Tools`

### Step 3: Sign in Azure
1. After installing, there shall be a icon like a capital A below the icons on the left. When hovering on the icon, it shows "Azure". Click it and the `Azure` sub-area will appear
1. In the `Azure` sub-area, `sign in to Azure...`

### Step 4: Create the app service on Azure

1. Unfold the root menu item `Azure for Students`
1. On the menu item `App Services`, right click the mouse and select `Create New Web App`
1. Follow the instructions to create a web app. At the second step select `Python` with the newest version, and at the third step select `Free`
1. Wait for a few moment and you can see the progress in the output window of VS Code.
1. After successfully created the app, right click on the menu item `App Services` and select `refresh`, you shall see your newly created application.

### Step 5: Deploy the the app
1. on the newly created application menu item, right click and select `Deploy to Web App...`
1. select the folder to deploy and confirm
1. Wait for a little until it reports

### Step 6: Browse and share the app

1. Click the button of `Browse Website` when the deployment is done, or you can find the button when right click the newly created app menu item.
1. Copy the URL of the app in the browser and share with others to access your app.

#### Congratulations! Now your app is on the cloud and part of the internet!
