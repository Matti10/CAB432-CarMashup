from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import requests
from serpapi import GoogleSearch
import os, json

serpKey = '2d71a3fcd8c12e9ec250ddb9dd9743f008a2f71d795430ea67fb3aaa7d0b2247'
ninjaKey = 'k97Uta4mX0lUYEmNVdUDEg==c8U5pnVM77PBhcXP'

app = Flask(__name__)

app.config['SECRET_KEY'] = "thisIsASecret;)" #config secret key fpr WTF

Bootstrap(app) #init Flask Bootstrap

#config forms
class SelectionForm(FlaskForm):
    carModel = StringField("Enter a Car model!",validators=[DataRequired()])
    submit = SubmitField("Submit")



@app.route("/",methods = ['POST', 'GET'])
def index():
    form = SelectionForm()
    model = ""
    carData = ""
    if form.validate_on_submit():
        model = form.carModel.data
        form.carModel.data  = "" #reset the form
        
        #get model data
        api_url = 'https://api.api-ninjas.com/v1/cars?model={}'.format(model)
        response = requests.get(api_url, headers={'X-Api-Key': ninjaKey})
    

        carData = response.text

        if carData == []:
            carData = "Unfortunaterly, your car is too rare (and cool) for us to get info on it!! Enjoy the below pictures"

        #get images
        params = {
            "api_key": serpKey,
            "engine": "google",
            "q": model + "car",
            "tbm": "isch"
        }

        # search = GoogleSearch(params)
        # results = search.get_dict()

        # images = results
        # images = (json.dumps(results['images_results'], indent=2, ensure_ascii=False))

    return render_template('index.html',carData=carData,form=form,model=model,images=images)

@app.route("/hello/")
@app.route("/hello/<var>")
def helloFlask(var="DefaultValue"):
    return render_template('helloFromFlask.html',carData=var)
    


if __name__ == "__main__":
    app.run()
