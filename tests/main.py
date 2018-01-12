from flask import Flask
from flask_sqlalchemy import Model, SQLAlchemy
from sqlalchemy_dst import DictionarySerializableModel

app = Flask(__name__)
app.config.from_object('tests.config')

ModelClass = type('ModelClass', (Model, DictionarySerializableModel), {})
db = SQLAlchemy(app, model_class=ModelClass)

if __name__ == '__main__':
    app.run(host=app.config['SERVER_HOST'], port=app.config['SERVER_PORT'])
