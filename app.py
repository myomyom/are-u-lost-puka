from flask import Flask, render_template, redirect, url_for, request
from are_you_lost_babygirl import mapGare, fullList
# from are_you_lost_babygirl import changeYear, changeMonth, changeUrl
import secrets
import os

from flask_wtf import CSRFProtect
from FormDate import DateForm

app = Flask(__name__)
foo = secrets.token_urlsafe(16)
app.secret_key = foo

# Flask-WTF requires this line
csrf = CSRFProtect(app)

@app.route("/")
def home():
    mapGare.get_root().render() # render the map
    # form = DateForm()
    return render_template('index.html')

#TODO: Make a form for year & month and then redirect it to homeCustom
#TODO: Responsive height for markers

# @app.route("/")
# @app.route("/<year>/<month>", methods=['GET', 'POST'])
# def homeCustom(year, month):
#     year=year
#     month=month
#     print(year, month)
#     mapGare.get_root().render() # render the map
#     os.system('python are_you_lost_babygirl.py "{0}" "{1}"').format(year, month)
#     return render_template('index.html', year = year, month = month)

def errorNotFound():
    return render_template('error.html')

@app.route("/ree", methods=['GET', 'POST'])
def formuwu():
    form = DateForm()
    if form.validate_on_submit():
        year = request.args.get('year')
        month = request.args.get('month')
        print(year, month)
    return render_template('index.html', year = year, month = month)

@app.route("/map")
def openMap():
    return render_template('output.html')

@app.route("/gare/<id>")
def openGare(id):
    uicList = fullList(id)
    # topFive = top5(idk(id))
    return render_template('gare.html', uicList = uicList)
    
if __name__ == "__main__":
    app.run(debug=True)