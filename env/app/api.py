from flask import Flask
from flask_restful import Resource, Api, reqparse
from flask_mysqldb import MySQL

app = Flask(__name__)
api = Api(app)

#Config MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'ItemListDb'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

# init MySQL
mysql = MySQL(app)

class CreateUser(Resource):
    def post(self):
    	try:
    		parser = reqparse.RequestParser()
    		parser.add_argument('email', type=str, help='Email address to create user')
    		parser.add_argument('password', type=str, help='Password to create user')

    		args = parser.parse_args()
    		_userEmail = args['email']
    		_userPassword = args['password']

    		#insert data to MySQL database

    		#Create cursor
    		cur = mysql.connection.cursor()
    		cur.execute("INSERT INTO tblUser(UserName, password) VALUES(%s, %s)", (_userEmail, _userPassword))
    		
    		#get error if any
    		data = cur.fetchall()
    		if len(data) is 0:
    			mysql.connection.commit()
    			return {'StatusCode':'200','Message': 'User creation success'}
    		else:
    			return {'StatusCode':'1000','Message': str(data[0])}

    		#Close connection
    		cur.close()

    		return {'Email': args['email'], 'Password': args['password']}
    	except Exception as e:
    		return {'error': str(e)}

class AuthenticateUser(Resource):
	def post(self):
		try:
			parser = reqparse.RequestParser()
			parser.add_argument('email', type=str, help='Email address to create user')
			parser.add_argument('password', type=str, help='Password to create user')
			args = parser.parse_args()

			_userEmail = args['email']
			_userPassword = args['password']

			#Create cursor
			cur = mysql.connection.cursor()
			query = "SELECT * FROM tblUser WHERE UserName = %s"
			cur.execute(query, (_userEmail,))
			data = cur.fetchall()

			if(len(data)>0):
				if(str(data[0]['Password'])==_userPassword):
					return {'status':200,'UserId':str(data[0]['UserId'])}
				else:
					return {'status':100,'message':'Authentication failure'}
			#Close connection
			cur.close()

		except Exception as e:
			return {'error': str(e)}

api.add_resource(CreateUser, '/CreateUser')
api.add_resource(AuthenticateUser, '/AuthenticateUser')

if __name__ == '__main__':
    app.run(debug=True)