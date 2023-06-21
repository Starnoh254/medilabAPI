from flask import Flask
from flask_jwt_extended import JWTManager
from flask_restful import Api
from flask_jwt_extended import JWTManager

app = Flask(__name__)

# Set up JWT


from datetime import timedelta
app.secret_key = "hfjdfhgjkdfhgjkdf865785"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=1)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(minutes=20)
jwt = JWTManager(app)



# Make the app an api
api = Api(app)

# configure Views/Endpoints here
# ....
from views.views import AddDependant, MemberProfile, MemberSignin, MemberSignup, ViewDependants 
from views.views import Laboratories, LabTests, MakeBooking, MyBookings, MakePayment


api.add_resource(MemberSignup, "/api/member_signup")
api.add_resource(MemberSignin, "/api/member_signin")
api.add_resource(MemberProfile, "/api/member_profile")
api.add_resource(AddDependant, "/api/add_dependant")
api.add_resource(ViewDependants, "/api/view_dependants")
api.add_resource(Laboratories, "/api/laboratories")
api.add_resource(LabTests, "/api/lab_tests")
api.add_resource(MakeBooking, "/api/make_booking")
api.add_resource(MyBookings, "/api/my_bookings")
api.add_resource(MakePayment, "/api/make_payment")

#Dashboard
from views.views_dashboard import LabSignup,LabSignin,LabProfile,AddLabtest,ViewLabTest,ViewBooking,AddNurse
from views.views_dashboard import ViewNurses,TaskAllocations
api.add_resource(LabSignup, "/api/lab_signup")
api.add_resource(LabSignin, "/api/lab_signin")
api.add_resource(LabProfile, "/api/lab_profile")
api.add_resource(AddLabtest, "/api/add_labtest")
api.add_resource(ViewLabTest, "/api/view_labtest")
api.add_resource(ViewBooking, "/api/view_booking")
api.add_resource(AddNurse, '/api/add_nurse')
api.add_resource(ViewNurses, '/api/view_nurses')
api.add_resource(TaskAllocations, '/api/task_allocations')

# configure urls for nurses
from views.view_nurse import NurseLogin,ViewAssignments,ViewInvoiceDetails,ChangePassword
api.add_resource(NurseLogin, '/api/nurse_login')
api.add_resource(ViewAssignments, '/api/view_assignments')
api.add_resource(ViewInvoiceDetails, '/api/view_invoice_details')
api.add_resource(ChangePassword,'/api/change_password')
if __name__ == "__main__":
    app.run(debug=True , port=4000)
