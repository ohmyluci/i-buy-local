import os
from sqlalchemy import Column, String, Integer
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import json

#database_name = "i_buy_local"
#database_path = "postgres://{}:{}@{}/{}".format('postgres','EresTonto','localhost:5432', database_name)
#database_path = os.environ.get('DATABASE_URL', database_path)
database_path = os.environ.get('DATABASE_URL')

db = SQLAlchemy()


'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()
    migrate = Migrate(app, db)


'''
db_drop_and_create_all()
    drops the database tables and starts fresh
    can be used to initialize a clean database
    !!NOTE you can change the database_filename variable to have multiple versions of a database
'''
def db_drop_and_create_all():
    db.drop_all()
    db.create_all()

'''
Business
a persistent business entity, extends the base SQLAlchemy Model
'''
class Business(db.Model):
    __tablename__ = 'businesses'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    address = db.Column(db.String(120), nullable=False)
    cif = db.Column(db.String(40), unique=True, nullable=False)
    phone = db.Column(db.String(20), unique=True, nullable=False)


    '''
    short()
        short form representation of the Business model
    '''
    def short(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'address': self.address,
        }

    '''
    long()
        long form representation of the Drink model
    '''
    def long(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'address': self.address,
            'cif': self.cif
        }

    '''
    insert()
        inserts a new model into a database
        the model must have a unique name
        the model must have a unique id or null id
        EXAMPLE
            business = Business(title=req_title, recipe=req_recipe)
            drink.insert()
    '''
    def insert(self):
        db.session.add(self)
        db.session.commit()

    '''
    delete()
        deletes a new model into a database
        the model must exist in the database
        EXAMPLE
            drink = Drink(title=req_title, recipe=req_recipe)
            drink.delete()
    '''
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    '''
    update()
        updates a new model into a database
        the model must exist in the database
        EXAMPLE
            business = Business.query.filter(business.id == id).one_or_none()
            business.title = 'Black Coffee'
            business.update()
    '''
    def update(self):
        db.session.commit()


    def __repr__(self):
        return json.dumps(self.long())


'''
Customer
a persistent customer entity, extends the base SQLAlchemy Model
'''
class Customer(db.Model):
    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    address = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), unique=True, nullable=False)

    '''
    short()
        short form representation of the business model
    '''
    def short(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone
        }

    '''
    long()
        long form representation of the business model
    '''
    def long(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'address': self.address
        }

    '''
    insert()
        inserts a new model into a database
        the model must have a unique name
        the model must have a unique id or null id
        EXAMPLE
            business = Business(title=req_title, recipe=req_recipe)
            drink.insert()
    '''
    def insert(self):
        db.session.add(self)
        db.session.commit()

    '''
    delete()
        deletes a new model into a database
        the model must exist in the database
        EXAMPLE
            drink = Drink(title=req_title, recipe=req_recipe)
            drink.delete()
    '''
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    '''
    update()
        updates a new model into a database
        the model must exist in the database
        EXAMPLE
            business = Business.query.filter(business.id == id).one_or_none()
            business.title = 'Black Coffee'
            business.update()
    '''
    def update(self):
        db.session.commit()


    def __repr__(self):
        return json.dumps(self.long())



'''
Products
a persistent customer entity, extends the base SQLAlchemy Model
'''
class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), unique=True, nullable=False)
    price = db.Column(db.Float, nullable=False)
    available = db.Column(db.Boolean, default=False, nullable=True)
    business_id = db.Column(db.Integer, db.ForeignKey('businesses.id'), nullable=False)

    '''
    short()
        short form representation of the customer model
    '''
    def short(self):
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'available': self.available,
            'business_id': self.business_id
        }

    '''
    long()
        long form representation of the business model
    '''
    def long(self):
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'available': self.available,
            'business_id': self.business_id
        }

    '''
    insert()
        inserts a new model into a database
        the model must have a unique name
        the model must have a unique id or null id
        EXAMPLE
            business = Business(title=req_title, recipe=req_recipe)
            drink.insert()
    '''
    def insert(self):
        db.session.add(self)
        db.session.commit()

    '''
    delete()
        deletes a new model into a database
        the model must exist in the database
        EXAMPLE
            drink = Drink(title=req_title, recipe=req_recipe)
            drink.delete()
    '''
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    '''
    update()
        updates a new model into a database
        the model must exist in the database
        EXAMPLE
            business = Business.query.filter(business.id == id).one_or_none()
            business.title = 'Black Coffee'
            business.update()
    '''
    def update(self):
        db.session.commit()


    def __repr__(self):
        return json.dumps(self.long())