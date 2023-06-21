# Medilab Api 
This is an API Build in Python Flask framework and MySQl database

### The Api has 3 parts 
1. The api allows register a member, sigin , profile , add dependants , make booking , make payments etc
2. Other APIS include sign in , sign up laboratory , add lab tests , add nurses , allocate nurses
3. Nurse APIS allows nurse to login and access the allocated tasks, change password \

### How to install 
step 1 : Download xampp from https://www.apachefriends.org/
step 2 : create and import medilab.sql.

step3 : create a flask app and install these packages 

``` 
pip install flask
pip install pymysql
pip install bcrypt 
pip install africastalking
pip install fpdf
```

step 4 : python set up 

create a folder named views and place the view_nurses.py , views.py and views_dashboard.py Inside.
in the root folder create a function.py
in the root folder again create app.py and configure your urls

run your app 
useful links 
https://github.com/africastalking/Africastalking.sdk
https://pypi.python.org/pypi/Flask
https://flask.palletsprojects.com/en/1.0.x/quickstart

