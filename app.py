"""Flask app for Cupcakes"""

from flask import Flask, jsonify, request, render_template
from models import db, connect_db, Cupcake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcake'
app.config['SECRET_KEY'] = 'secret'
app.config['DEBUG'] = True
app.app_context().push()

connect_db(app)
db.create_all()

def serialize_cupcake(cupcake):
     return {
          "id": cupcake.id,
          "flavor": cupcake.flavor,
          "size": cupcake.size,
          "rating": cupcake.rating,
          "image": cupcake.image  
     }

@app.route("/", methods=["GET"])
def show_home():
     cupcakes = Cupcake.query.all()
     return render_template("/temp/home.html", cupcakes=cupcakes)

@app.route("/api/cupcakes", methods=["GET"])
def all_cupcakes():
     cupcakes = Cupcake.query.all()
     serialized = [serialize_cupcake(c) for c in cupcakes]

     return jsonify(cupcakes=serialized)

@app.route("/api/cupcakes/<cupcake_id>", methods=["GET"])
def list_single_cupcake(cupcake_id):
     
     cupcake = Cupcake.query.get_or_404(cupcake_id)
     serialized = serialize_cupcake(cupcake)

     return jsonify(cupcake=serialized)

@app.route("/api/cupcakes", methods=["POST"])
def create_cupcake():
     
     name = request.json["name"]
     flavor = request.json["flavor"]
     size = request.json["size"]
     rating = request.json["size"]
     image = request.json["image"]

     new_cupcake = Cupcake(name=name, flavor=flavor, size=size, rating=rating, image=image)

     db.session.add(new_cupcake)
     db.session.commit()

     serialized = serialize_cupcake(new_cupcake)

     return ( jsonify(cupcake=serialized), 201 )

@app.route("/api/cupcakes/<cupcake_id>", methods=["PATCH"])
def update_cupcake(id):
     cupcake = Cupcake.query.get_or_404(id)
     cupcake.name = request.json.get('name', cupcake.name)
     cupcake.flavor = request.json.get('flavor', cupcake.flavor)
     cupcake.size = request.json.get('size', cupcake.size)
     cupcake.rating = request.json.get('rating', cupcake.rating)
     cupcake.image = request.json.get('image', cupcake.image)

     db.session.commit()
     return jsonify(cupcake=cupcake.serialize())

@app.route("/api/cupcakes/<cupcake_id>", methods=["DELETE"])
def delete_cupcake(id):
     cupcake = Cupcake.query.get_or_404(id)
     db.session.delete(cupcake)
     db.session.commit()

     return jsonify(message="deleted")