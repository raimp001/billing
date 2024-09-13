import os
import logging

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///medical_billing.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.urandom(24)
    COINBASE_COMMERCE_API_KEY = os.environ.get('COINBASE_COMMERCE_API_KEY')
    COINBASE_WALLET_CLIENT_ID = os.environ.get('COINBASE_WALLET_CLIENT_ID')
    COINBASE_WALLET_CLIENT_SECRET = os.environ.get('COINBASE_WALLET_CLIENT_SECRET')

    @staticmethod
    def init_app(app):
        logging.basicConfig(level=logging.INFO)
        logger = logging.getLogger(__name__)
        
        logger.info("Initializing configuration")
        logger.info(f"COINBASE_COMMERCE_API_KEY: {'set' if os.environ.get('COINBASE_COMMERCE_API_KEY') else 'not set'}")
        
        if os.environ.get('COINBASE_COMMERCE_API_KEY'):
            api_key = os.environ.get('COINBASE_COMMERCE_API_KEY')
            logger.info(f"COINBASE_COMMERCE_API_KEY length: {len(api_key)}")
            logger.info(f"COINBASE_COMMERCE_API_KEY first 5 chars: {api_key[:5]}")
            logger.info(f"COINBASE_COMMERCE_API_KEY last 5 chars: {api_key[-5:]}")
        else:
            logger.warning("COINBASE_COMMERCE_API_KEY is not set in the environment variables")
        
        logger.info(f"COINBASE_WALLET_CLIENT_ID: {'set' if os.environ.get('COINBASE_WALLET_CLIENT_ID') else 'not set'}")
        logger.info(f"COINBASE_WALLET_CLIENT_SECRET: {'set' if os.environ.get('COINBASE_WALLET_CLIENT_SECRET') else 'not set'}")

        app.logger.info("Configuration initialized")
