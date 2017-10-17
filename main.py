from flask import Flask, render_template
import data_access as db

app = Flask(__name__)

@app.route('/')
def home():
	data = db.getDataQ(30)
	return render_template("index.html", data=data)

if __name__ == "__main__": 
	app.run(host='0.0.0.0', debug=True)