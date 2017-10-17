from flask import Flask, render_template
import data_access as db

app = Flask(__name__)

@app.route('/')
def home():
	data = db.getDataQ(30)
	return render_template("index.html", data=data)

@app.route('/view/<imgID>')
def view(imgID = None):
	return render_template("view.html", img_id=imgID)

if __name__ == "__main__": 
	app.run(host='0.0.0.0', debug=True)