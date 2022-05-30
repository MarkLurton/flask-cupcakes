"""Flask app for Cupcakes"""
from flask import Flask, request, jsonify, render_template

from models import db, connect_db, Cupcake

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "letsgostros"

connect_db(app)

@app.route('/')
def show_home_page():
    """Render home page"""

    return render_template('index.html')

@app.route('/api/cupcakes')
def get_cupcakes():
    """Get all cupcakes"""

    cupcakes = [ cupcake.serialize() for cupcake in Cupcake.query.all()]

    return jsonify(cupcakes=cupcakes)

@app.route('/api/cupcakes/<int:id>')
def get_cupcake(id):
    """Get details on specific cupcake"""

    cupcake = Cupcake.query.get_or_404(id)

    return jsonify(cupcake=cupcake.serialize())

@app.route('/api/cupcakes', methods=['POST'])
def create_cupcake():
    """Create new cupcake"""
    flavor = request.json["flavor"]
    size = request.json["size"]
    rating = request.json["rating"]
    image = request.json["image"] if request.json["image"] else "https://tinyurl.com/demo-cupcake"

    cupcake = Cupcake(flavor=flavor, size=size, rating=rating, image=image)

    db.session.add(cupcake)
    db.session.commit()

    return (jsonify(cupcake=cupcake.serialize()), 201)

@app.route('/api/cupcakes/<id>', methods=['PATCH'])
def update_cupcake(id):
    """Update cupcake"""

    cupcake = Cupcake.query.get_or_404(id)

    cupcake.flavor = request.json.get("flavor", cupcake.flavor)
    cupcake.size = request.json.get("size", cupcake.size)
    cupcake.rating = request.json.get('rating', cupcake.rating)
    cupcake.image = request.json.get("image", cupcake.image)

    db.session.add(cupcake)
    db.session.commit()

    return (jsonify(cupcake=cupcake.serialize()), 200)

@app.route('/api/cupcakes/<id>', methods=['DELETE'])
def delete_cupcake(id):
    """Delete_cupcake"""

    cupcake = Cupcake.query.get_or_404(id)

    db.session.delete(cupcake)
    db.session.commit()

    return (jsonify(message="Deleted"), 200)
