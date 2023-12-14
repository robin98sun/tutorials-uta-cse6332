# How to build a Web Application on Azure - Part 3 - Interactive Web Application

Now we are going to add some buttons on the webpage to make it interactive.

### Step 1: Show an alert button on the webpage to pop out a message window

Update the file `templates/index.html` to:
```html
<html>
    <head>
        <title>Tutorial of Building a Simple Web Application</title>
        <script src="https://code.jquery.com/jquery-3.7.1.js" 
                integrity="sha256-eKhayi8LEQwp4NKxN+CfCh+3qOVUtJn3QNZ0TciWLP4=" 
                crossorigin="anonymous"></script>
    </head>
    <body align="center">
        <h1>{{message}}</h1>
        <img src="/static/thumbs-up.png" width="100" hight="100"/>
        <p>
        <button id="btn">Alert</button>
    </body>
    <script>
        $('document').ready(
            function(){
                $('#btn').click(function() {
                    alert("Hello");
                });
            }
        );
    </script>
</html>
```

Note, at the top of the html file we included a jQuery library using `<script>` tag, in which the "src" attribute is set to the remote location of the library file. The browser will automatically load the file from that location. Since the jQuery library is very common and widely used, we can reuse an existing one on the internet instead of downloading and deploying again.

While at the bottom of the html file, a segment of Javascript code is wrapped in `<script>` tag as inline JS code. These are the two ways of how Javascript code get loaded by the browser.

In the `<button>` tag of the "Alert" button, it is defined as `id="btn"`. In the inline JS code, an anonymous function is loaded to define what the browser should do when an object with an `id="btn"` is clicked.

For `jQuery` tutorial please refer to [here](https://www.w3schools.com/jquery/default.asp)

### Step 2: Change the button click function to query data via the RESTful APIs
Now, we change the inline JS code to:
```javascript
$('document').ready(
    function(){
        $('#btn').click(function() {
            $.get('/data',  // url
                function (data, textStatus, jqXHR) {  // success callback
                    alert('status: ' + textStatus + ', data:' + data);
                }
            );
        });
    }
);
```
You will see the document `us-cities.csv` content in the alert window.

### Step 3: Show the data in the webpage

Add a `<div>` tag in the html file within the pair of `<body>` tags like this:
```html
<div id="data" align="center"></div>
```

Change the `alert` function in the inline JS code to:
```javascript
$('#data').html(data)
```

Then the data will appear in the web instead of in an pop-out alert window when clicking the button.

After changing the title of the button to "Show Data", now the html file `index.html` is:
```html
<html>
    <head>
        <title>Tutorial of Building a Simple Web Application</title>
        <script src="https://code.jquery.com/jquery-3.7.1.js" 
                integrity="sha256-eKhayi8LEQwp4NKxN+CfCh+3qOVUtJn3QNZ0TciWLP4=" 
                crossorigin="anonymous"></script>
    </head>
    <body align="center">
        <h1>{{message}}</h1>
        <img src="/static/thumbs-up.png" width="100" hight="100"/>
        <div id="data" align="center"></div>
        <p>
        <button id="btn">Show Data</button>
    </body>
    <script>
        $('document').ready(
            function(){
                $('#btn').click(function() {
                    $.get('/data',  // url
                        function (data, textStatus, jqXHR) {  // success callback
                            $('#data').html(data)
                        }
                    );
                });
            }
        );
    </script>
</html>
```

### Step 4: to append new data

Add some inputs and a "Append" button in between the `body` tags:
```html
<div align="center">
    <table>
        <tr>
            <td><input id="city_name" placeholder="city name"/></td>
            <td><input id="lat" placeholder="lat"/></td>
            <td><input id="lng" placeholder="lng"/></td>
            <td><input id="country" placeholder="country"/></td>
            <td><input id="state" placeholder="state"/></td>
            <td><input id="population" placeholder="population"/></td>
            <td><button id="btn-append">Append</button></td>
        </tr>
    </table>
</div>
```

Add a jQuery function in the inline JS code:
```javascript
$('#btn-append').click(function() {
    $.ajax({
        type: "PUT",
        url: "/data",
        contentType: "application/json",
        data: JSON.stringify({
            city_name: $('#city_name').val(),
            lat: $("#lat").val(),
            lng: $("#lng").val(),
            country: $("#country").val(),
            state: $("#state").val(),
            population: $("#population").val(),
        }),
        success: function(res) {
            alert(res)
        }
    })
});
```

Please try it by yourself.

### Step 5: to delete data entry

Because the data is dynamically fetched from the server, to put a delete button besides each row of data is also dynamic, including setting the reaction for the click events of those buttons.

Hence, we are going to update the JS code block of query to enable deleting data entries, by adding these two functions below the line of showing data `$('#data').html(data)`:

```javascript
$("#data").find("tr").each( function(tr_id, tr_elem){
    if (tr_id > 0 && tr_elem.children.length > 1) {
        var city_name = tr_elem.children[1].innerHTML
        buttonStr = '<button class="btn-del" id="btn-del-'+city_name+'">Delete</button>'
        tr_elem.innerHTML += "<td>"+buttonStr+"</td>"
    }
});
$('.btn-del').click(function(elem){
    var city_name = elem.target.id.split('-')[2]
    $.ajax({
        type: "DELETE",
        url: "/data?city_name="+city_name,
        success: function(res) {
            alert(res)
        }
    })
})
```

#### Now, the web page is able to handle data by interacting with the RESTful APIs.

### A hint for handling database

Replace the following three functions with database operations:

```python
def fetch_data(city_name = None, include_header = False, exact_match = False):
def append_or_update_data(req):
def delete_data(city_name):
```
