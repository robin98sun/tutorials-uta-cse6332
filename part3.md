# How to build a Web Application on Azure - Part 3 - Interactive Web Application

Now we are going to add some buttons on the webpage to make it interactive.

### Step 1: Show a button on the webpage

Update the file `templates/index.html` to:
```html
<html>
    <head>
        <title>Tutorial of Building a Simple Web Application</title>
        <script src="https://code.jquery.com/jquery-3.7.1.min.js"/>
    </head>
    <body align="center">
        <h1>{{message}}</h1>
        <img src="/static/thumbs-up.png" width="100" hight="100"/>
        <p>
        <button>Alert</button>
    <body>
</html>
```
A button is added at the bottom.

### Step 2: 
