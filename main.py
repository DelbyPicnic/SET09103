from flask import Flask, request, render_template
import data_access as db

app = Flask(__name__)

@app.route('/')
def home():
	sTerm = request.args.get('search', '')
	
	if sTerm == '':
		data = db.getDataQ(30)
	else:
		data = db.searchData(sTerm)

	return render_template("index.html", data=data)

@app.route('/search/')
def search():
	sTerm = request.args.get('t', '')
	if sTerm == '':
		return "Could not be found"
	else:
		data = db.searchData(sTerm)

	return render_template("index.html", data=data)

@app.route('/view/<imgID>')
def view(imgID = None):
	data = db.getRecord(imgID)
	return render_template("view.html", data=data)

if __name__ == "__main__": 
	app.run(host='0.0.0.0', debug=True)