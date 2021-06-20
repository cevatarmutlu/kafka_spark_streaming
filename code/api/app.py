from flask import Flask, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from src.model.Product import ProductView
import src.config as config

cfg = config.get('postgres')

DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{cfg['user']}:{cfg['password']}@{cfg['host']}:{cfg['port']}/{cfg['database']}"
db = SQLAlchemy(app)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})



@app.route('/<int:userid>', methods=['GET'])
def root(userid):
    
    products = db \
        .session \
        .query(ProductView.productid) \
        .filter(ProductView.userid == userid) \
        .order_by(ProductView.timestamp.asc()) \
        .limit(5) \
        .all()

    return jsonify({
        'userid': userid, 
        'viewed-products': [i.productid for i in products]
    })

if __name__ == '__main__':
    app.run(debug=DEBUG)