from flask import Flask, render_template
from are_you_lost_puka import mapGare, fullList
import secrets
import datetime

from flask_wtf import CSRFProtect

#TODO: fix margin @ popup

app = Flask(__name__)
foo = secrets.token_urlsafe(16)
app.secret_key = foo

# Flask-WTF requires this line
csrf = CSRFProtect(app)

@app.route("/")
def home():
    today = datetime.datetime.now()
    today = today.strftime('%d %b %Y')
    mapGare.get_root().render() # render the map
    return render_template('index.html', today=today)

@app.route("/map")
def openMap():
    return render_template('output.html')

@app.route("/gare/<id>")
def openGare(id):
    uicList = fullList(id)
    return render_template('gare.html', uicList = uicList)
    
if __name__ == "__main__":
    app.run(debug=True)