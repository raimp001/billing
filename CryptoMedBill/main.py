import os
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from models import db, Bill
from config import Config
import requests
from datetime import datetime
import logging
from bleach import clean
from coinbase_commerce import Client as CommerceClient

app = Flask(__name__)
app.config.from_object(Config)
Config.init_app(app)
db.init_app(app)
csrf = CSRFProtect(app)

logger = logging.getLogger(__name__)

def initialize_coinbase_client():
    api_key = os.environ.get('COINBASE_COMMERCE_API_KEY')
    if not api_key:
        logger.error("COINBASE_COMMERCE_API_KEY is not set in the environment variables.")
        return None

    try:
        client = CommerceClient(api_key=api_key)
        charges = client.charge.list()
        logger.info(f"Successfully connected to Coinbase Commerce API. Found {len(charges)} charges.")
        return client
    except Exception as e:
        logger.error(f"Error initializing Coinbase Commerce client: {str(e)}")
        return None

coinbase_commerce_client = initialize_coinbase_client()

@app.route('/')
def index():
    api_key_status = "valid" if coinbase_commerce_client else "invalid or not set"
    return render_template('index.html', api_key_status=api_key_status)

@app.route('/api/check_api_key')
def check_api_key():
    if coinbase_commerce_client:
        return jsonify({"status": "valid", "message": "API key is valid and working."})
    else:
        return jsonify({"status": "invalid", "message": "API key is invalid or not set. Please check your environment variables."})

@app.route('/api/submit_bill', methods=['POST'])
@csrf.exempt
def submit_bill():
    if not coinbase_commerce_client:
        return jsonify({"error": "Coinbase Commerce client is not initialized. Please check your API key."}), 500

    data = request.json
    logger.info(f"Received bill submission: {data}")

    try:
        charge = coinbase_commerce_client.charge.create(
            name='Medical Bill Payment',
            description=f"Payment for Patient ID: {data['patientId']}",
            pricing_type='fixed_price',
            local_price={
                'amount': data['amountUsd'],
                'currency': 'USD'
            }
        )
        logger.info(f"Coinbase charge created successfully: {charge['id']}")
        
        new_bill = Bill(
            patient_id=clean(data['patientId']),
            date=datetime.strptime(data['date'], '%Y-%m-%d').date(),
            visit_type=clean(data['visitType']),
            diagnosis=clean(data['diagnosis']),
            amount_usd=float(data['amountUsd']),
            payment_token=clean(data['paymentToken']),
            charge_id=charge['id'],
            payment_status='pending'
        )
        db.session.add(new_bill)
        db.session.commit()
        logger.info(f"Bill saved to database: {new_bill.id}")
        
        return jsonify({"message": "Bill submitted successfully", "charge_url": charge['hosted_url']}), 201
    except Exception as e:
        logger.error(f"Error submitting bill: {str(e)}")
        return jsonify({"error": f"An error occurred while submitting the bill: {str(e)}"}), 500

@app.route('/api/get_csrf_token', methods=['GET'])
def get_csrf_token():
    return jsonify({'csrf_token': csrf._get_csrf_token()})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    logger.info("Starting Flask application...")
    logger.info(f"COINBASE_COMMERCE_API_KEY status: {'Set' if os.environ.get('COINBASE_COMMERCE_API_KEY') else 'Not set'}")
    app.run(host='0.0.0.0', port=5000, debug=True)
