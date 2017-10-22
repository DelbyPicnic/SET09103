from flask import Flask, request, render_template, url_for, session, redirect
import data_access as db

app = Flask(__name__)
app.secret_key = 'qGseyftsYb9rdYIIfz2cXjhJT9ZJwIxI8Pr0YvUd'

@app.route('/')
def home():
	sTerm = request.args.get('search', '')
	
	if sTerm == '':
		data = db.getDataQ(30)
	else:
		data = db.searchData(sTerm)

	return render_template("index.html", data=data)

# TEMP
@app.route('/sign-in', methods=['POST','GET'])
def login():
	# Possibly check session here to make sure user is not already logged in
	if request.method == 'POST':
		if request.form['uName'] == "" or request.form['uPass'] == "":
			return "Username and Password required"
		else:
			usr = db.getUser(request.form['uName'])
			if usr != None:
				if usr["password"] == request.form['uPass']:
					# Create Session
					session['username'] = request.form['uName']
					session['email'] = usr['email']
					session['status'] = usr['status']

					return redirect(url_for('home'))
				else:
					return "Username or Password is incorrect"
			else:
				return "Username or Password is incorrect"
	else:
		page =''' 
			<html ><body >
				<form action="" method="post" name="form">
					<label for="uName">Username:</label>
					<input type="text" name="uName" id="uName"/>
					<label for="uPass">Password:</label>
					<input type="password" name="uPass" id="uPass"/> 
					<input type="submit" name="submit" id="submit"/>
				</form>
			</body><html>'''
		return page

@app.route('/sign-out')
def logout():
	session.clear()
	return redirect(url_for('home'))

@app.route('/account')
def account():
	if session['username'] != "":
		return "Username: %s. Email: %s. Status: %d." %(session['username'], session['email'], session['status']) 
	else:
		return "You aren't signed in!"

		
@app.route('/view/<imgID>')
def view(imgID = None):
	data = db.getRecord(imgID)
	return render_template("view.html", data=data)

if __name__ == "__main__": 
	app.run(host='0.0.0.0', debug=True)