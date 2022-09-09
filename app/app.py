from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)

app.config['SECRET_KEY'] = "thisIsASecret;)" #config secret key fpr WTF

Bootstrap(app) #init Flask Bootstrap

#config forms
class SelectionForm(FlaskForm):
    name = StringField("Please pick a car!",validators=[DataRequired()])
    submit = SubmitField("Submit")

#get car data


@app.route("/",methods = ['POST', 'GET'])
def index():
    form = SelectionForm()
    name = ""
    if form.validate_on_submit():
        name = form.name.data
        form.name.data  = "" #reset the form


    return render_template('index.html',name=name,form=form)

@app.route("/hello/")
@app.route("/hello/<var>")
def helloFlask(var="DefaultValue"):
    return render_template('helloFromFlask.html',name=var)
    


if __name__ == "__main__":
    app.run()
