# Import Required Modules
import pymysql 
from flask_restful import * 
from flask import *
from functions import *
import pymysql.cursors
from views.views_dashboard import AddNurse
# import JWT Packages
from flask_jwt_extended import create_access_token, jwt_required, create_refresh_token

# Nurse login
class NurseLogin(Resource):
    def post(self):
        json = request.json
        surname = json['surname']
        password1 = json['password']
        sql = '''select * from nurses where surname = %s'''
        connection = pymysql.connect(host='localhost',
                                                user='root',
                                                password='',
                                                database='medilab')
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        cursor.execute(sql, surname)
        count = cursor.rowcount
        if count == 0 :
            return jsonify({'message':'There is no such nurse'})
        else:
             #nurse exists
                 nurse = cursor.fetchone()
                 hashed_password = nurse['password'] # this password is hashed
                 # Jane proided a plain password
                 if hash_verify(password1,hashed_password):
                        #TODO JSON web Tokens
                        access_token = create_access_token(identity=surname, fresh=True)
                        refresh_token = create_refresh_token(surname)
                        
                        return jsonify({'message': nurse,
                                        'access_token': access_token,
                                        'refresh__token': refresh_token})
                 else:
                        return jsonify({'message': 'Login Failed'})


class ViewAssignments(Resource):
      @jwt_required(refresh=True) # Refresh token
      def post(self):
            json = request.json
            nurse_id = json['nurse_id']
            flag = json['flag']
            
            sql = ''' select * from nurse_lab_allocations where nurse_id = %s and flag = %s'''
            connection = pymysql.connect(host='localhost',
                                                user='root',
                                                password='',
                                                database='medilab')
            cursor = connection.cursor(pymysql.cursors.DictCursor)
            cursor.execute(sql, (nurse_id,flag))
            
            count = cursor.rowcount
            if count == 0:
                  message = "No {} Assignments".format(flag)
                  return jsonify({'message': message})
            else:
                  assignment = cursor.fetchall()
                  return jsonify(assignment)
            
            
class ViewInvoiceDetails(Resource):
      @jwt_required(refresh=True) # refresh token
      def post(self):
            json = request.json
            invoice_no = json['invoice_no']
            sql = ''' select * from bookings where invoice_no = %s'''
            connection = pymysql.connect(host='localhost',
                                                user='root',
                                                password='',
                                                database='medilab')
            cursor = connection.cursor(pymysql.cursors.DictCursor)
            cursor.execute(sql, invoice_no)
            count = cursor.rowcount
            if count == 0:
                  message = "Invoice no {} Does not exist".format(invoice_no)
                  return jsonify({'message': message})
            else:
                bookings = cursor.fetchall()
                for booking in bookings:
                    booking['appointment_date'] = str(booking['appointment_date'])
                    booking['appointment_time'] = str(booking['appointment_time'])
                return jsonify({'message': bookings})
            

class ChangePassword(Resource):
      def post(self):
            json = request.json
            nurse_id = json['nurse_id']
            otp = json['otp']
            password1 = json['password1']
            password2 = json['password2']
            

            sql = ''' select * from nurses where nurse_id = %s'''
            connection = pymysql.connect(host='localhost',
                                                user='root',
                                                password='',
                                                database='medilab')
            cursor = connection.cursor(pymysql.cursors.DictCursor)
            cursor.execute(sql, (nurse_id))
            the_password = cursor.fetchone()
            count = cursor.rowcount
            if count == 0 :
                message = 'The nurse does not exist'
                return jsonify({'message ': message})
            
            else:
                password = the_password['password']
                if hash_verify(otp,password):
                      if password1 == password2:
                            hashed_new_password = hash_password(password1)
                            sql2 = '''update nurses set password = %s where nurse_id = %s'''
                            connection2 = pymysql.connect(host='localhost',
                                                user='root',
                                                password='',
                                                database='medilab')
                            cursor2 = connection2.cursor(pymysql.cursors.DictCursor)
                            cursor2.execute(sql2, (hashed_new_password,nurse_id))
                            return jsonify({'message': 'you changed your password successfully'})
                      else:
                            return jsonify({'message': 'you password do not match.Please try again'})
                else: 
                      return jsonify({'message': "You entered the wrong otp"})

