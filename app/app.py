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
import flask


#aws config
awsConfig = Config(
    region_name = 'ap-southeast-2'

)

#init s3 client
siteConterPath = 'app\siteCount.txt'
AWS_Bucket = 'sitecounter'
AWS_Object = 'siteCounter/count.txt'
s3 = boto3.client(
    's3',
    aws_access_key_id="ASIA5DYSEEJ4TR7N6PHO",
    aws_secret_access_key="X57pkLDRQ97c3rHxpdnQq3aZoKihk+BNoOM8ihAO",
    aws_session_token="IQoJb3JpZ2luX2VjEJf//////////wEaDmFwLXNvdXRoZWFzdC0yIkYwRAIgXrlUy8/wzJYLuVAidkeefDM8LOP1TfrWflQyYj/xQJECIC2RZvFdtW7Nzh6avsEf2bOVxYltKDFdo7WyASP/Zy2PKrADCEAQAhoMOTAxNDQ0MjgwOTUzIgyt7qiC3fXIsxYR+7YqjQOt6mGoyvoUrcxxDVTVm4mZUxZbZwIKMhopisvIz3kE5vYcP/meHBAqmtcAOqoOcAZPvOuBAtJYGEy3rNDXQ/nUqfA6wk0wdegAENVKB4SeSg5X9E9OY6Ay1g9vXUiS+m+zMTlUreHqhlFcdPKsrwIIJ/G3eS1sqONSxC71dQWi/8rPsPmtRdy/5pC4DWD6Dh2u9gbUwvgeD3RzAQxdKSybiP06HbMSTkW8zsm4uvUlMNhPNlP3fxRklj09lDag3Vc3iM4gLGlYrOdDRl2HKObzUJ2bWT1eL3opPMMgPTEYu/jx/uRIYncnc/oPT44kL8/ZxWpnKOI26BYh+DU0dRm0ws090cLg61FR1LpRRtogaEKJong5dEnKGj08Z6zUUGTsA4whAPziRG+G/rFT7RWo6n71TRTrWJKJ2rzPD2d/85Ln81t121VObpdBcB2mnEHCx56nisSd15kDTPSrpusygH5xjj4A72XjTa37UYZBqsYrsn/gS9zEG37W33RA7feu5zvgiQnZ1e89d8MpMImroJkGOqcBedfNNTiffGh0HnV0xiDluEyewXwqwIlImZoQLAljYn+eN6oTIrHkpZg3b8Z8/aniX73iDciblKDjaPmjp3ElstptK7/5nycl4BpO3rPPCxxZ5M06PjkEqerLGe31nzCCuIPFdYdo3kGjcpdpgVUffjmr+aIQAnmKokx0NfJcJpXdhONv7d5qnLPQWQjqncuXtl9lFeqCqhGptYJeB4nuGv4H7mBScZg=",
    config=awsConfig
)


#in a 'real' deployment,  these keys would this stored far more securely... Lucky this isn't a web security course ;)

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
    params = {
        "api_key": serpKey,
        "engine": "google",
        "q": searchTerm + "car",
        "tbm": "isch"
    }

    search = GoogleSearch(params)
    results = search.get_dict()

    
    results = (json.dumps(results['images_results'], indent=2, ensure_ascii=False))
    results = json.loads(results, object_hook=lambda d: SimpleNamespace(**d))

    images = []
    for image in results[:6]:
        images.append(image.original)

    #static links to some test images, to save API calls when testing
    # images = ['https://cars.usnews.com/pics/size/350x262/images/Auto/izmo/309572/2010_toyota_camry_angularfront.jpg', 'https://pictures.dealer.com/k/keyestoyotaofvannuys/0501/4872b675b5becbdecc9474d949bf3187x.jpg?impolicy=resize&w=414', 'https://akimage.vinsolutions.com/v/1893240000/1893243192/r640', 'https://imgd.aeplcdn.com/1280x720/n/cw/ec/110233/2022-camry-exterior-right-front-three-quarter.jpeg?isig=0&q=75', 'https://platform.cstatic-images.com/xxlarge/in/v2/895a83c1-23e5-5f56-b89e-31ed1b8c29a6/3818da75-fb63-40a8-9766-0ec4bf772a55/Gfg9DPiKUNcjtceRll9ZtItiYGI.jpg', 'https://imgd.aeplcdn.com/1056x594/n/hn7kpua_1557405.jpg?q=75']

    return images

def getCarInfo(model, year=""):
    #get model data
    if year != "":
        print("using year")
        api_url = 'https://api.api-ninjas.com/v1/cars?model={model}&year={year}'.format(model=model,year=str(year))
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
    api_url = 'https://api.api-ninjas.com/v1/cars?limit=60&fuel_type={fuel}&drive={drive}&cylinders={cyl}&year={year}'.format(fuel= someCar.fuel_type, drive = someCar.drive, cyl = someCar.cylinders, year = someCar.year)
    response = requests.get(api_url, headers={'X-Api-Key': ninjaKey})

    carData = response.text

    if carData == '[]':
        return ""

    #convert to an objecy
    carData = json.loads(carData, object_hook=lambda d: SimpleNamespace(**d))

    carData = iter(carData)
    filteredCarData = []

    def innerLoopHelper(car):
        for filteredCar in filteredCarData:
            if car.model == filteredCar.model:
                return False
        return True
    
    while len(filteredCarData) < 6:
        car = next(carData)
        print(car)
        if innerLoopHelper(car):
            filteredCarData.append(car)

    returnList = []

    for car in filteredCarData:
        # getImages for each car
        car.images = getImgURLs(car.model + " " + str(car.year))
        #tidy up some headings while we're here
        car.model = car.model.capitalize()
        car.make = car.make.capitalize()

        #convert them all to lists
        returnList.append(list(car.__dict__.items()))

    print(filteredCarData)
    return returnList

def getSiteCounter():
    try:
        #download counter from aws
        s3.download_file(AWS_Bucket, AWS_Object, siteConterPath)
    except:
        print("AWS Connection not working, are your keys up to date?")


    #open counter file
    counterFile = open(siteConterPath, "r")

    #Read the current count
    count = counterFile.read()

    counterFile.close()

    return count


def setSiteCounter():
    try:
        #upload counter from aws
        s3.upload_file(siteConterPath, AWS_Bucket, AWS_Object)
    except:
        print("AWS Connection not working, are your keys up to date?")



def tickSiteCounter():
    
    count = int(getSiteCounter())

    #increase the count
    count += 1

    #open counter file
    counterFile = open(siteConterPath, "w")

    #write increase to file and upload
    counterFile.write(str(count))

    counterFile.close()

    setSiteCounter()

    print("Counter is: "+ str(count))

    return count



@app.route("/",methods = ['POST', 'GET'])
@app.route("/#CarPicker",methods = ['POST', 'GET'])
@app.route("/#Similar",methods = ['POST', 'GET'])
def index():
    form = SelectionForm()
    model = ""
    carData = ""
    similar = ""
    images = ""
    year = ""
    count = getSiteCounter()
    
    #increment site counter on gets
    if flask.request.method == 'GET':
        count = tickSiteCounter()

    if form.validate_on_submit():
        search = form.carModel.data
        form.carModel.data  = "" #reset the form
        count = tickSiteCounter() #increment site counter as as not all gets are caught correctly

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


    return render_template('index.html',carData=carData,form=form,model=model,images=images,similar=similar,count=count)


if __name__ == "__main__":
    app.run()
