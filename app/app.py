from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import requests
from serpapi import GoogleSearch
import os, json
from types import SimpleNamespace
import boto3
from botocore.config import Config

#aws config
awsConfig = Config(
    region_name = 'ap-southeast-2'
)


#init s3 client
s3 = boto3.client(
    's3',
    aws_access_key_id="ASIA5DYSEEJ4XIKIVBPM",
    aws_secret_access_key="bcqDJi7yFj7zq5d1BX34ujLkeSW6pFP8mPLbjPay",
    aws_session_token="IQoJb3JpZ2luX2VjEGMaDmFwLXNvdXRoZWFzdC0yIkgwRgIhANN5jkW5YEEuF2sxC26CfjMOgzSpjdN5a/Z6Ew8bliQdAiEAsKWizA455YXEg3C4AHhk8Hdx/G75fCwNe59LGVADRHgquQMI/P//////////ARACGgw5MDE0NDQyODA5NTMiDG6Vato/nvIWMxZnRyqNA8Y9b6u6xC2/D0mw6jmxthPTwcB9evYmEse+4X/g3UF1l8ytN94c0XpuEuzmmJN5B0L3vec/rCILz5I/HwdEKD1Rxk0l20oBgsp9y2zEPuVv5Xv9XEl8ta5QK+lGr1fOCxxzpO5ucHPjXwg+JHJTh37mdp0BxBPFPPBHYQ0XtTvdp7I0EdXffOkWkpzxzJGTP9Sik5KV7VrbOGUeZ+gGhnfYFQhKYFNv28CqI+dNA13eG8vJJ2bGtgboPDeyRi4MCsqwuUZoTylbGrkAckYV2gdOH8lGK9OW6HvBKVR2i7iF8pCq5HM+VjZddlIE73iVxCBwO1YoCNQPkJ83XaiIVb8JYF5FZRt9qd1FpdJ56P1cUoXKYW+rQuIj82+Uyh/1bDX0LrQYk4j7sHLd/BhilHtzfym9tgaRgs46RaAh7piE8ueU+l1KBvJ+YrpDnM7qxqzxX/c09WWQMQyrbSId9dnjlqcqdn9AD9O2N4Ww3hdWmlXouwUScpLSHNJuNy6jIwXDHWdAz84zv8FfFiMwvPaUmQY6pQFqHiKUbCYR4M8C65L+a8Xe+/5nVw7op9bHL6hftQin2qXbjFmQve2cSsgi6HcBW1s+EU9F22aiT+eEmhGxLBO6ib2iy4sh5/0i68BLsaG5nn+2t1Vp6pJ19akF3ILQjKLMe/GJwLxBHH6sPx/e5FYufD9Z15L9iqXcz9CYkDR7I56EqNFsI4jg8jLtGVU1W7Bn+Xm2TffjlqaNrdTMx9MuJEPdBvg=",
    config=awsConfig
)

serpKey = '2d71a3fcd8c12e9ec250ddb9dd9743f008a2f71d795430ea67fb3aaa7d0b2247'
ninjaKey = 'k97Uta4mX0lUYEmNVdUDEg==c8U5pnVM77PBhcXP'

app = Flask(__name__)

app.config['SECRET_KEY'] = "thisIsASecret;)" #config secret key fpr WTF

Bootstrap(app) #init Flask Bootstrap

#config forms
class SelectionForm(FlaskForm):
    carModel = StringField("Enter a Car model!",validators=[DataRequired()])
    submit = SubmitField("Submit")


def getImgURLs(searchTerm):
    # https://stackoverflow.com/questions/49952518/trying-to-extract-the-source-link-of-the-first-image-of-a-google-search-using-be
    # get images
    # params = {
    #     "api_key": serpKey,
    #     "engine": "google",
    #     "q": searchTerm + "car",
    #     "tbm": "isch"
    # }

    # search = GoogleSearch(params)
    # results = search.get_dict()

    
    # results = (json.dumps(results['images_results'], indent=2, ensure_ascii=False))
    # results = json.loads(results, object_hook=lambda d: SimpleNamespace(**d))

    # images = []
    # for image in results[:6]:
    #     images.append(image.original)

    images = ['https://cars.usnews.com/pics/size/350x262/images/Auto/izmo/309572/2010_toyota_camry_angularfront.jpg', 'https://pictures.dealer.com/k/keyestoyotaofvannuys/0501/4872b675b5becbdecc9474d949bf3187x.jpg?impolicy=resize&w=414', 'https://akimage.vinsolutions.com/v/1893240000/1893243192/r640', 'https://imgd.aeplcdn.com/1280x720/n/cw/ec/110233/2022-camry-exterior-right-front-three-quarter.jpeg?isig=0&q=75', 'https://platform.cstatic-images.com/xxlarge/in/v2/895a83c1-23e5-5f56-b89e-31ed1b8c29a6/3818da75-fb63-40a8-9766-0ec4bf772a55/Gfg9DPiKUNcjtceRll9ZtItiYGI.jpg', 'https://imgd.aeplcdn.com/1056x594/n/hn7kpua_1557405.jpg?q=75']

    return images

def getCarInfo(model, year=""):
    #get model data
    if year != "":
        print("using year")
        api_url = 'https://api.api-ninjas.com/v1/cars?model={}&year={}'.format(model,year)
    else:
        print("no year")
        api_url = 'https://api.api-ninjas.com/v1/cars?model={}'.format(model)
    response = requests.get(api_url, headers={'X-Api-Key': ninjaKey})


    carData = response.text

    print(carData)

    if carData == '[]':
        return ""

    return json.loads(carData, object_hook=lambda d: SimpleNamespace(**d))



def getSimilarCars(someCar):
    api_url = 'https://api.api-ninjas.com/v1/cars?limit=6&fuel_type={fuel}&drive={drive}&cylinders={cyl}&year={year}'.format(fuel= someCar.fuel_type, drive = someCar.drive, cyl = someCar.cylinders, year = someCar.year)
    response = requests.get(api_url, headers={'X-Api-Key': ninjaKey})

    carData = response.text

    if carData == '[]':
        return ""

    #convert to an objecy
    carData = json.loads(carData, object_hook=lambda d: SimpleNamespace(**d))

    # getImages for each car
    for car in carData:
        car.images = getImgURLs(car.model + " " + str(car.year))

    return carData

def getSiteCounter():
    print(s3.download_file('sitecounter', 'siteCounter', 'count.txt'))

# def setSiteCounter():

@app.route("/",methods = ['POST', 'GET'])
def index():
    form = SelectionForm()
    model = ""
    carData = ""
    similar = ""
    images = ""
    year = ""
    
    if form.validate_on_submit():
        search = form.carModel.data
        form.carModel.data  = "" #reset the form

        #look for a year in the search
        searchTerms = search.split(" ")

        for term in searchTerms:
            try:
                #see if the term is an int
                int(term)                

                print("year,model")
                print(term,model)

                if len(term) == 4 and (term[:2] == "19" or term[:2] == "20"):
                    year = term
                    model = search.replace(year, "")
                    break
            except Exception as e:
                print('nothing to see here: '+ str(e))
                model = search
        
        print("model:",model,",year:",year,",search:",search)
        #getData on searched Car
        carData = getCarInfo(model,year)
        if carData != "":
            carData = carData[0]
            similar = getSimilarCars(carData)
            year = carData.year

            #convert to list to make it easier to work with in flask
            carData = list(carData.__dict__.items())

            #format the keys so they look nicer
            for item in carData:
                item = list(item)
                item[0].replace("_"," ")
                title = item[0].split(" ")
                for word in title:
                    word.capitalize() 
                item[0] = ' '.join(title)

        #get images of car
        images = getImgURLs(model+" "+str(year))


    return render_template('index.html',carData=carData,form=form,model=model,images=images,similar=similar)


if __name__ == "__main__":
    app.run()
