from flask import Flask, request, render_template, url_for, session, redirect
import data_access as db

app = Flask(__name__)
app.secret_key = 'qGseyftsYb9rdYIIfz2cXjhJT9ZJwIxI8Pr0YvUd'

# Route for the main homepage of the site
@app.route('/')
def home():
	sTerm = request.args.get('search', '')
	
	if sTerm == '':
		data = db.getFeatured()
	else:
		data = db.searchData(sTerm)

	return render_template("index.html", data=data)

# Route for user sign in and credential validation
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
		return render_template("sign-in.html")

# Route for the user session termination
@app.route('/sign-out')
def logout():
	session.clear()
	return redirect(url_for('home'))

# Route for account information page
@app.route('/account')
def account():
	return render_template("account.html")

@app.route('/mk-feat', methods=['POST','GET'])
def feature():
	if request.method == 'POST':
		if request.form['img_id'] == "" or request.form['img_id'] == None:
			# die with content fault
			print("Cannot add image to featured without image id!")
		else:
			if session.get('status', None) < 2:
				# die with uac fault
				print("A non-admin user tried to modify content status!")
			else:
				# change status
				if db.toggleFeat(request.form['img_id']):
					print("Added an image to featured")
				else:
					print("Failed to change featured status, check IMG-ID")
		

	return redirect(url_for('home'))	

# Route for the view content page	
@app.route('/view/<imgID>')
def view(imgID = None):
	data = db.getRecord(imgID)
	data["img_id"] = imgID

	return render_template("view.html", data=data)

if __name__ == "__main__": 
	app.run(host='0.0.0.0', debug=True)