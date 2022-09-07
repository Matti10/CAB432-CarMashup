from flask import Flask
from flask import render_template
app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html',name="Lorem Ipsum")

@app.route("/hello/")
@app.route("/hello/<var>")
def helloFlask(var="DefaultValue"):
    return render_template('helloFromFlask.html',name=var)
    


if __name__ == "__main__":
    app.run()
