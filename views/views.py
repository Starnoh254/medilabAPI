# Import Required Modules
import pymysql 
from flask_restful import * 
from flask import *
from functions import *
import pymysql.cursors

# import JWT Packages
from flask_jwt_extended import create_access_token, jwt_required, create_refresh_token


#Member Signup
class MemberSignup(Resource):
    def post(self):
        #Connect to MySQL
        json = request.json
        surname = json['surname']
        others = json['others']
        gender = json['gender']
        email = json['email']
        phone = json['phone']
        dob = json['dob']
        password = json['password']
        location_id = json['location_id']

        # Validate password
        response = passwordValidity(password)
        if response == True:
            if check_phone(phone):
                connection = pymysql.connect(host='localhost',
                                             user='root',
                                             password='',
                                             database='medilab')
                cursor = connection.cursor()
                # Insert Data
                sql = '''Insert into members(surname, others, gender, email, phone, 
                dob, password, location_id)values(%s, %s, %s, %s, 
                %s, %s, %s, %s) '''
                # Provide Data
                
                data = (surname, others, gender, encrypt(email), encrypt(phone), 
                        dob, hash_password(password), location_id)
                try:
                    cursor.execute(sql, data)
                    connection.commit()
                    #Send Sms/Email
                    code = gen_random(4)
                    send_sms(phone,'''Thank you for joining Medilab. Your secret NO: {}. Do not share.'''.format(code))
                    return jsonify({'message': 'Succesfully registered'})
                except:
                    connection.rollback()
                    return jsonify({'message': 'Failed.Try Again'})
            
            
            else:
                 return jsonify({'message': 'Invalid Phone +254'})



        else:
            return jsonify( response)
    
class MemberSignin(Resource):
    def post(self):
            json = request.json
            surname = json['surname']
            password = json['password']

              #the user enters plain text Email
            sql = "select * from members where surname = %s"
            

            connection = pymysql.connect(host='localhost',
                                             user='root',
                                             password='',
                                             database='medilab')
            cursor = connection.cursor(pymysql.cursors.DictCursor)
            cursor.execute(sql,surname)
            count = cursor.rowcount
            if count == 0:
                 return jsonify({'message': 'User does not exist'})
            else:
                 #user exists
                 member = cursor.fetchone()
                 hashed_password = member['password'] # this password is hashed
                 # Jane proided a plain password
                 if hash_verify(password,hashed_password):
                        #TODO JSON web Tokens
                        access_token = create_access_token(identity=surname, fresh=True)
                        refresh_token = create_refresh_token(surname)
                        
                        return jsonify({'message': member,
                                        'access_token': access_token,
                                        'refresh__token': refresh_token})
                 else:
                        return jsonify({'message': 'Login Failed'})

class MemberProfile(Resource):
     @jwt_required(refresh=True) #Refresh Token
     def post(self):
          json = request.json
          member_id = json['member_id']
          sql = "select * from members where member_id = %s"
            

          connection = pymysql.connect(host='localhost',
                                             user='root',
                                             password='',
                                             database='medilab')
          cursor = connection.cursor(pymysql.cursors.DictCursor)
          cursor.execute(sql,member_id)
          count = cursor.rowcount
          if count == 0:
               return jsonify({'message': 'Member does not exist'})
          else:
               member = cursor.fetchone()
               return jsonify(member)
               
        
     
class AddDependant(Resource):
    def post(self):
        #Connect to MySQL
        json = request.json
        member_id = json['member_id']
        surname = json['surname']
        others = json['others']
       
        dob = json['dob']

        sql = '''Insert into dependants(member_id, surname, others, dob)values(%s, %s, %s, %s) '''
        data = (member_id,surname,others,dob)     


        connection = pymysql.connect(host='localhost',
                                             user='root',
                                             password='',
                                             database='medilab')
        cursor = connection.cursor()
                # Insert Data
        
                # Provide Data
        
        try:
             cursor.execute(sql,data)
             connection.commit()
             return jsonify({'message': 'Dependant Added'})
        except:
             connection.rollback()
             return jsonify({'message': 'Failed. Try Again'})
        



class ViewDependants(Resource):
     @jwt_required(refresh=True) #Refresh Token
     def post(self):
          json = request.json
          member_id = json['member_id']
          sql = "select * from dependants where member_id = %s"
            

          connection = pymysql.connect(host='localhost',
                                             user='root',
                                             password='',
                                             database='medilab')
          cursor = connection.cursor(pymysql.cursors.DictCursor)
          cursor.execute(sql,member_id)
          count = cursor.rowcount
          if count == 0:
               return jsonify({'message': 'Member does not exist'})
          else:
               dependants = cursor.fetchall()
               return jsonify(dependants)
          # {} - means Object in JSON, comes wit key-value
          # []- means a JSON array
          # [{},{}] - Json Array - With JSON objects

class Laboratories(Resource):
     def get(self):
          sql = "select * from laboratories"
          connection = pymysql.connect( host='localhost',
                                        user='root',
                                        password='', 
                                        database='medilab')
          cursor = connection.cursor(pymysql.cursors.DictCursor)
          cursor.execute(sql)
          count = cursor.rowcount
          if count == 0:
            return jsonify({'message': 'No Laboratories Listed'})
          else:
            laboratories = cursor.fetchall()
            return jsonify(laboratories)


class LabTests(Resource):
     def post(self):
          json = request.json
          lab_id = json['lab_id']
          sql = "select * from lab_tests where lab_id = %s"
          connection = pymysql.connect(host='localhost',
                                       user='root',
                                       password='',
                                       database='medilab')
          cursor = connection.cursor(pymysql.cursors.DictCursor)
          cursor.execute(sql,lab_id)
          count = cursor.rowcount
          if count == 0:
               return jsonify({'message': 'NO Lab Test Found'})
          else:
               lab_tests = cursor.fetchall()
               return jsonify(lab_tests)

class MakeBooking(Resource):
     def post(self):
          json = request.json
          member_id = json['member_id']
          booked_for = json['booked_for']
          dependant_id = json['dependant_id']
          test_id = json['test_id']
          appointment_date = json['appointment_date']
          appointment_time = json['appointment_time']
          where_taken = json['where_taken']
          latitude = json['latitude']
          longitude = json['longitude']
          lab_id = json['lab_id']
          invoice_no = json['invoice_no']

          connection = pymysql.connect(host='localhost',
                                       user='root',
                                       password='',
                                       database='medilab')
          cursor=connection.cursor()
          
          #Insert Data
          sql= '''Insert into bookings(member_id,booked_for, dependant_id,test_id,appointment_date,
          appointment_time, where_taken, latitude, longitude, lab_id, invoice_no)values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
           #provide Data
          data = (member_id,booked_for,dependant_id,test_id,appointment_date,
                    appointment_time, where_taken, latitude, longitude, lab_id, invoice_no)
          try:
               cursor.execute(sql, data)
               connection.commit()
               #select from members to find phone number
               sql = '''select * from members where member_id=%s'''
               cursor = connection.cursor(pymysql.cursors.DictCursor)
               cursor.execute(sql, member_id)
               member = cursor.fetchone()
               # Get Phone
               phone = member['phone']
               #Send sms to above phone number . NB decrypt the phone number
               send_sms(phone, "Booking scheduled for {} at {}".format(appointment_date,appointment_time,invoice_no))

               return jsonify({'message':'BOOKING RECEIVED.'})
          except:
               connection.rollback()

               return jsonify({'message':'Failed , Try Again'})
           
class MyBookings(Resource):
     @jwt_required(refresh=True)
     def get(self):
          json = request.json
          member_id = json['member_id']
          sql = "select * from bookings where member_id=%s"
          connection = pymysql.connect(host='localhost',
                                       user='root',
                                       password='',
                                       database='medilab')
          cursor = connection.cursor(pymysql.cursors.DictCursor)
          cursor.execute(sql, member_id)
          count = cursor.rowcount
          if count == 0:
               return jsonify({'messsage':'No Bookings'})
          else:
              bookings = cursor.fetchall()
          #     return str(bookings)
          import json
          jsonStr = json.dumps(bookings, indent=1, sort_keys=True, default=str)
          # then convert json string to json oject
          return json.loads(jsonStr)
          
class MakePayment(Resource):
     @jwt_required(fresh=True)
     def post(self):
          json = request.json
          phone = json['phone']          
          total_amount = json['total_amount']
          invoice_no = json['invoice_no']
          # Access M-pesa functions located in functions.py
          mpesa_payment(total_amount,phone,invoice_no)
          return jsonify({'message': 'Sent - Complete Payment on Your Phone.'})
     
#Log Out

     