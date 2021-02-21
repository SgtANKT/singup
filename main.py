from flask import Flask, render_template, request, session, logging, url_for, redirect, flash
from flask_mysqldb import MySQL

# initializing flask app and MySQL Database
app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'ABCD'
app.config['MYSQL_DB'] = 'register'
mysql = MySQL(app)

# home page
@app.route('/')
def home():
	return render_template('home.html')


# login form page
@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == "POST":
		cur = mysql.connection.cursor()
		# Extract user details from the form and feeding it into our query
		login_details = request.form
		login_username = login_details["username"]
		login_password = login_details["password"]
		user_data = cur.execute("SELECT username FROM users WHERE username=(%s)", (login_username,))
		pass_data = cur.execute("SELECT password FROM users WHERE username =%s", (login_username, ))
		query_results = cur.fetchall() #query result for pass_data
		for password_data in query_results:
			# print(password_data)
			password = int(''.join(password_data))
			if password == int(login_password):
				session['log'] = True
				flash("You have successfully logged in", "success")
				return redirect(url_for("photo"))
			else:
				flash("Incorrect Password", "danger")
				return render_template("login.html")

	return render_template('login.html')

# register form
@app.route('/register', methods=['GET', 'POST'])
def register():

	if request.method =="POST":
		# Extract user details from the form and feeding it into our query
		details = request.form
		name = details["name"]
		username = details["username"]
		password = details["password"]
		confirm = details["confirm"]
		cur = mysql.connection.cursor()
		cur.execute('SELECT * FROM users WHERE username = % s', (username,))
		account = cur.fetchone()
		if account:
			flash("Username already taken", "danger")
			return redirect(url_for('register'))
		if password == confirm:
			
			cur.execute("INSERT INTO users(name, username, password) VALUES (%s, %s, %s)", (name, username, password))
			mysql.connection.commit()
			flash("You are successfully Registered", "success")
			# cur.close()
			return redirect(url_for('login'))
		else:
			flash("Password does not match", "danger")
			return render_template("register.html")
	return render_template('register.html')

@app.route('/photo')
def photo():
	return render_template('photo.html')

@app.route('/logout')
def logout():
	session.clear()
	flash("You have successfully logged out", 'success')
	return render_template('home.html')


if __name__ == '__main__':
    app.secret_key = "thisismysecretkey"
    app.run(debug=True)