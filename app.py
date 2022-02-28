from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scraping

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

@app.route("/")
def index():
    #uses PyMongo to find the mars collection in our database which we will create
    #when we convert our jupyter scraping code to Python Script
    mars = mongo.db.mars.find_one()

    #Tells Flask to return an HTML template using an index.html file
    #mars=mars tells Python to use the "mars" collection in MongoDB
    return render_template("index.html", mars=mars)


#Define the route that Flask will be using
@app.route("/scrape")
def scrape():
    mars = mongo.db.mars

    #New variable to hold newly scraped data
    mars_data = scraping.scrape_all()

    #use data stored in mars_data. upsert=True tells Mongo to create a new document
    #if one doesn't already exist
    mars.update_one({}, {"$set":mars_data}, upsert=True)

    #redirect back to our homepage where we can see the updated content
    return redirect('/', code=302)

if __name__ == "__main__":
    app.run()