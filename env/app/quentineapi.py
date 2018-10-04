from flask import Flask
from flask_restful import Resource, Api, reqparse
from flask_mysqldb import MySQL
from passlib.hash import sha256_crypt

app = Flask(__name__)
api = Api(app)

#Config MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'quentinedb'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

# init MySQL
mysql = MySQL(app)

########ADMIN ENDPOINTS

class CreateAdmin(Resource):
    def post(self):
    	try:
            parser = reqparse.RequestParser()
            parser.add_argument('name', type=str, help='Name address to create user')
            parser.add_argument('email', type=str, help='Email address to create user')
            parser.add_argument('username', type=str, help='Username address to create user')
            parser.add_argument('password', type=str, help='Password to create user')
            parser.add_argument('phone_no', type=str, help='Phone Number address to create user')

            args = parser.parse_args()
            _name = args['name']
            _email = args['email']
            _username = args['username']
            _password = sha256_crypt.encrypt(str(args['password']))
            _phone_no = args['phone_no']

    		#insert data to MySQL database

    		#Create cursor
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO admin(name, email, username, password, phone_no) VALUES(%s, %s, %s, %s, %s)", (_name, _email, _username, _password, _phone_no))
    		
    		#get error if any
            data = cur.fetchall()
            if len(data) is 0:
    			mysql.connection.commit()
    			return {'StatusCode':'200','message': 'User creation success', 'name': args['name'], 'email': args['email'], 'username': args['username'], 'password': args['password'], 'phone_no': args['phone_no']}
            else:
    			return {'StatusCode':'1000','message': str(data[0])}

    		#Close connection
            cur.close()
        except Exception as e:
            return {'error': str(e)}

class AuthenticateAdmin(Resource):
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('username', type=str, help='Username address to authenticate admin')
            parser.add_argument('password', type=str, help='Password to authenticate admin')
            args = parser.parse_args()

            _username = args['username']
            _password = args['password']

            #Create cursor
            cur = mysql.connection.cursor()
            query = "SELECT * FROM admin WHERE username = %s"
            cur.execute(query, (_username,))
            data = cur.fetchall()

            if(len(data)>0):
                password_hash = str(data[0]['password'])

                if(sha256_crypt.verify(_password, password_hash)):
                    return {'status':200,'message': 'Authentication success', 'id': str(data[0]['id']),'name': str(data[0]['name']),'username': str(data[0]['username']),'phone_no': str(data[0]['phone_no']),'register_date': str(data[0]['register_date'])}
                else:
                    return {'status':100,'message':'Authentication failure'}
            else:
                return {'status':100,'message':'Authentication failure'}
            #Close connection
            cur.close()
        except Exception as e:
            return {'error': str(e)}

class FetchAdmin(Resource):
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('id', type=str, help='ID to get specific admin')
            args = parser.parse_args()

            _admin_id = args['id']

            #Create cursor
            cur = mysql.connection.cursor()
            query = "SELECT * FROM admin WHERE id = %s"
            cur.execute(query, (_admin_id,))
            data = cur.fetchall()

            if(len(data)>0):
                return {'status':200,'message': 'Admin found', 'id': str(data[0]['id']),'name': str(data[0]['name']),'username': str(data[0]['username']),'phone_no': str(data[0]['phone_no']),'register_date': str(data[0]['register_date'])}
            else:
                return {'status':100,'message':'Could not find admin'}
            #Close connection
            cur.close()
        except Exception as e:
            return {'error': str(e)}


class FetchAllAdmins(Resource):
    def post(self):
        try:
            #Create cursor
            cur = mysql.connection.cursor()
            query = "SELECT name, username, email, phone_no, register_date FROM admin"
            cur.execute(query)
            data = cur.fetchall()

            if(len(data)>0):
                return {'status':200,'message': str(data)}
            else:
                return {'status':100,'message':'Could not find admins'}
            #Close connection
            cur.close()
        except Exception as e:
            return {'error': str(e)}

class UpdateAdminName(Resource):
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('id', type=str, help='ID to get update admin name')
            parser.add_argument('new_name', type=str, help='New name')
            args = parser.parse_args()

            _admin_id = args['id']
            _new_name = args['new_name']

            #Create cursor
            cur = mysql.connection.cursor()
            query = "UPDATE admin SET name = %s WHERE id = %s"
            cur.execute(query, (_new_name, _admin_id,))
            data = cur.fetchall()
            
            #Commit to DB
            mysql.connection.commit()

            if(cur.rowcount>0):
                return {'status':200,'message': 'Admin name updated'}
            else:
                return {'status':100,'message':'Could not update admin name'}
            #Close connection
            cur.close()
        except Exception as e:
            return {'error': str(e)}

class UpdateAdminEmail(Resource):
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('id', type=str, help='ID to get update admin email')
            parser.add_argument('new_email', type=str, help='New email')
            args = parser.parse_args()

            _admin_id = args['id']
            _new_email = args['new_email']

            #Create cursor
            cur = mysql.connection.cursor()
            query = "UPDATE admin SET email = %s WHERE id = %s"
            cur.execute(query, (_new_email, _admin_id,))
            data = cur.fetchall()
            
            #Commit to DB
            mysql.connection.commit()

            if(cur.rowcount>0):
                return {'status':200,'message': 'Admin email updated'}
            else:
                return {'status':100,'message':'Could not update admin email'}
            #Close connection
            cur.close()
        except Exception as e:
            return {'error': str(e)}

class UpdateAdminUsername(Resource):
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('id', type=str, help='ID to get update admin username')
            parser.add_argument('new_username', type=str, help='New username')
            args = parser.parse_args()

            _admin_id = args['id']
            _new_username = args['new_username']

            #Create cursor
            cur = mysql.connection.cursor()
            query = "UPDATE admin SET username = %s WHERE id = %s"
            cur.execute(query, (_new_username, _admin_id,))
            data = cur.fetchall()
            
            #Commit to DB
            mysql.connection.commit()

            if(cur.rowcount>0):
                return {'status':200,'message': 'Admin username updated'}
            else:
                return {'status':100,'message':'Could not update admin username'}
            #Close connection
            cur.close()
        except Exception as e:
            return {'error': str(e)}

class UpdateAdminPassword(Resource):
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('id', type=str, help='ID to get update admin password')
            parser.add_argument('previous_password', type=str, help='Previous Password')
            parser.add_argument('new_password', type=str, help='New Password')
            args = parser.parse_args()

            _admin_id = args['id']
            _previous_password = args['previous_password']
            _new_password = args['new_password']

            #Create cursor
            cur = mysql.connection.cursor()
            query = "SELECT password FROM admin WHERE id = %s"
            cur.execute(query, (_admin_id,))
            data = cur.fetchall()

            if(len(data)>0):
                previous_password_hash = str(data[0]['password'])

                #compare passwords
                if(sha256_crypt.verify(_previous_password, previous_password_hash)):
                    #encrypt new password
                    new_password = sha256_crypt.encrypt(str(_new_password))
                    query = "UPDATE admin SET password = %s WHERE id = %s"
                    cur.execute(query, (new_password, _admin_id,))
                    data = cur.fetchall()
                    #Commit to DB
                    mysql.connection.commit()
                    if(cur.rowcount>0):
                        return {'status':200,'message': 'Admin password updated'}
                    else:
                        return {'status':100,'message':'Could not update admin password'}
                else:
                    return {'status':100,'message':'password edit failed'}
            else:
                return {'status':100,'message':'Could not find admin password'}

            #Close connection
            cur.close()
        except Exception as e:
            return {'error': str(e)}

class UpdateAdminPhoneNumber(Resource):
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('id', type=str, help='ID to get update admin phone_no')
            parser.add_argument('new_phone_no', type=str, help='New phone_no')
            args = parser.parse_args()

            _admin_id = args['id']
            _new_phone_no = args['new_phone_no']

            #Create cursor
            cur = mysql.connection.cursor()
            query = "UPDATE admin SET phone_no = %s WHERE id = %s"
            cur.execute(query, (_new_phone_no, _admin_id,))
            data = cur.fetchall()
            
            #Commit to DB
            mysql.connection.commit()

            if(cur.rowcount>0):
                return {'status':200,'message': 'Admin phone number updated'}
            else:
                return {'status':100,'message':'Could not update admin phone number'}
            #Close connection
            cur.close()
        except Exception as e:
            return {'error': str(e)}

api.add_resource(CreateAdmin, '/CreateAdmin')
api.add_resource(AuthenticateAdmin, '/AuthenticateAdmin')
api.add_resource(FetchAdmin, '/FetchAdmin')
api.add_resource(FetchAllAdmins, '/FetchAllAdmins')
api.add_resource(UpdateAdminName, '/UpdateAdminName')
api.add_resource(UpdateAdminEmail, '/UpdateAdminEmail')
api.add_resource(UpdateAdminUsername, '/UpdateAdminUsername')
api.add_resource(UpdateAdminPassword, '/UpdateAdminPassword')
api.add_resource(UpdateAdminPhoneNumber, '/UpdateAdminPhoneNumber')



##########EMPLOYEE ENDPOINTS



if __name__ == '__main__':
    app.run(debug=True)