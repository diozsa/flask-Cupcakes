from crypt import methods
from ctypes import sizeof
from flask import Flask, request, render_template, jsonify
from models import db, connect_db, Cupcake

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['SECRET_KEY'] = "secretkey"

connect_db(app)

##################### ROUTES ######################

@app.route("/")
def home():
    """Home Page route"""
    return render_template("index.html")



@app.route("/api/cupcakes")
def list_cupcakes():
    """Lists all cupcakes from db
    Returns JSON formated data
    """
    cupcakes = [cupcake.serialize() for cupcake in Cupcake.query.all()]
    return jsonify(cupcakes=cupcakes)



@app.route("/api/cupcakes/<int:cupcake_id>")
def show_cupcake(cupcake_id):
    """Retrieves one cupcake based on its id
        Returns JSON formated data like
        {cupcake: [{id, flavor, rating, size, image}]}
    """
    cupcake = Cupcake.query.get_or_404(cupcake_id).serialize()
    return jsonify(cupcake=cupcake)



@app.route("/api/cupcakes", methods=['POST'])
def create_cupcake():
    """Creates cupcake,
        Returns JSON formated data like
        {cupcake: [{id, flavor, rating, size, image}]}
    """
    data = request.json
    cupcake = Cupcake(  flavor=data['flavor'],
                        size=data['size'],
                        rating=data['rating'],
                        image=data['image'] or None)

    db.session.add(cupcake)
    db.session.commit()

#POST returns a tuple of JSON data and status code 201
    return (jsonify(cupcake=cupcake.serialize()), 201)



@app.route("/api/cupcakes/<int:cupcake_id>", methods=["PATCH"])
def update_cupcake(cupcake_id):
    """Updates cupcake and return data in JSON format like
        {cupcake: [{id, flavor, rating, size, image}]}
    """
    data = request.json
    cupcake = Cupcake.query.get_or_404(cupcake_id)

    cupcake.flavor = data['flavor']
    cupcake.size = data['size']
    cupcake.ratin = data['rating']
    cupcake.image = data['image']

    db.session.add(cupcake)
    db.session.commit()

    return jsonify(cupcake=cupcake.serialize())



@app.route("/api/cupcakes/<int:cupcake_id>", methods=["DELETE"])
def delete_cupcake(cupcake_id):
    """Delete cupcake by ID and show confirmation
        Respond with JSON like {message: "Deleted"}
    """
    cupcake = Cupcake.query.get_or_404(cupcake_id)

    db.session.delete(cupcake)
    db.session.commit()

    return jsonify(message="Deleted")
