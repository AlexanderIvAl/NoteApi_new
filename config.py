import os
from pathlib import Path
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin

BASE_DIR = Path(__file__).parent
security_definitions = {
    "basicAuth": {
        "type": "basic"
    }
}

class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', f"sqlite:///{BASE_DIR / 'base.db'}")
    TEST_DATABASE_URI = f"sqlite:///{BASE_DIR / 'test.db'}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Зачем эта настройка: https://flask-sqlalchemy-russian.readthedocs.io/ru/latest/config.html#id2
    DEBUG = True
    PORT = 5000
    SECRET_KEY = "My secret key =)"
    SQLALCHEMY_ECHO=True
    RESTFUL_JSON = {
        'ensure_ascii': False,
    }
    
    APISPEC_SPEC = APISpec(
            title='Notes Project',
            version='v1',
            plugins=[MarshmallowPlugin()],
            securityDefinitions=security_definitions,
            security=[],
            openapi_version='2.0.0',
    )
    
    APISPEC_SWAGGER_URL = '/swagger'  # URI API Doc JSON
    APISPEC_SWAGGER_UI_URL = '/swagger-ui'  # URI UI of API Doc
    LANGUAGES = ['en', 'ru']