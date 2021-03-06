from flask import Flask, render_template, redirect, jsonify

# Import our pymongo library, which lets us connect our Flask app to our Mongo database.
import pymongo
import scrapemars

# Create an instance of our Flask app.
app = Flask(__name__)

# Create connection variable
conn = 'mongodb://localhost:27017'

# Pass connection to the pymongo instance.
client = pymongo.MongoClient(conn)

# Connect to a database. Will create one if not already available.
mydb = client.marsDB

# Drops collection if available to remove duplicates
mydb.db.drop()

# Creates a collection in the database and inserts two documents



# Set route
@app.route("/")
def home():
    marsData = mydb.collection.find_one()
    print(marsData)
    return render_template("index.html", Mars_Info=marsData)



@app.route('/scrape')

def scrape():
    marsData = scrapemars.scrape_info
    print("test", marsData)
    mydb.collection.update({}, marsData, upsert=True)
    return redirect ("/")



if __name__ == "__main__":
    app.run(debug=True)

