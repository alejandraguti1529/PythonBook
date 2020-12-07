from flask import Flask, jsonify, request 
from flask_pymongo import PyMongo
from flask import Response
import json

app= Flask(__name__)

app.config['MONGO_URI'] = 'mongodb://localhost:27017/Library'
app.config['MONGO_DBNAME'] = 'Library'

mongo = PyMongo(app)

@app.route('/Library', methods=['GET'])
def get_all_books():
    book = mongo.db.Book
    
    output = []

    for b in book.find():
        output.append({ 'name' : b['name'], 'author': b['author']})

    return jsonify({'result' : output})

@app.route('/Library/<name>', methods = ["PATCH"])
def update_book(name):
    book = mongo.db.Book
    myquery = { "name": name }
    newvalues = { "$set": { "author": request.form["author"] } }
    book.update_one(myquery, newvalues)
    return jsonify({'result' : "Book Updated"})

@app.route('/Library', methods = ["POST"])
def add_book():
    book = mongo.db.Book

    name = request.json['name']
    author = request.json['author']

    book_id = book.insert({'name':name, 'author':author})
    new_book = book.find_one({'_id' : book_id})

    output = {'name' : new_book['name'], 'author' : new_book['author']}

    return jsonify({'result' : output})

if __name__ == '__main__':
    app.run(debug=True)