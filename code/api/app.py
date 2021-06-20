from flask import Flask, jsonify, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from model.Product import ProductView

# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123@localhost:5432/postgres'
db = SQLAlchemy(app)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})



@app.route('/', methods=['GET'])
def root():
    userid = request.args.get('userid')
    products = db.session.query(ProductView.productid).filter(ProductView.userid == userid).order_by(ProductView.timestamp.asc()).limit(5).all()

    return jsonify({'userid': userid, 'viewed-products': [i.productid for i in products]})

if __name__ == '__main__':
    app.run(debug=DEBUG)