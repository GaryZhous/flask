from flask import Flask, render_template, request, redirect, url_for
from flask_pymongo import PyMongo
from bson.json_util import dumps, loads

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb+srv://Gary:Garyzhou1201@local.judmzmz.mongodb.net/MCU"
mongo = PyMongo(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    search_query = request.form['searchQuery']
    results = mongo.db['MCU-Inventory'].find({"Name": search_query})
    return redirect(url_for('results', query=dumps(results)))

@app.route('/results')
def results():
    query_results = request.args.get('query')
    results = loads(query_results)
    return render_template('results.html', results=results)

@app.route('/list')
def list_all():
    results = mongo.db['MCU-Inventory'].find()
    return render_template('list.html', results=results)

@app.route('/add', methods=['GET', 'POST'])
def add_chip():
    if request.method == 'POST':
        new_chip = {
            "_id": request.form['_id'],
            "Name": request.form['Name'],
            "Memory": request.form['Memory'],
            "Tags": request.form['Tags'],
            "Status": request.form['Status'],
            "PS": request.form['PS'],
        }
        mongo.db['MCU-Inventory'].insert_one(new_chip)
        return redirect(url_for('home'))
    return render_template('add.html')

@app.route('/update/<id>', methods=['POST'])
def update_chip(id):
    updated_chip = {
        "Name": request.form['Name'],
        "Memory": request.form['Memory'],
        "Tags": request.form['Tags'],
        "Status": request.form['Status'],
        "PS": request.form['PS'],
    }
    mongo.db['MCU-Inventory'].update_one({"_id": id}, {"$set": updated_chip})
    return redirect(url_for('results', query=dumps(mongo.db['MCU-Inventory'].find())))

@app.route('/delete/<id>')
def delete_chip(id):
    mongo.db['MCU-Inventory'].delete_one({"_id": id})
    return redirect(url_for('results', query=dumps(mongo.db['MCU-Inventory'].find())))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)
