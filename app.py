import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import db_drop_and_create_all, setup_db, Business, Customer
from auth import AuthError, requires_auth

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  CORS(app)

  setup_db(app)
  
  # db_drop_and_create_all()

  @app.route('/')
  def hello():
      return "OK"


  @app.route('/businesses')
  @requires_auth('get:businesses')
  def get_businesses(payload):
    businesses = Business.query.all()
    businesses_formatted = [business.short() for business in businesses]

    if len(businesses) == 0:
        abort(404)
    
    return jsonify({
      'success': True,
      'businesses' : businesses_formatted,
      'status': 200
    }), 200

  
  @app.route('/businesses/<int:id>')
  @requires_auth('get:business-detail')
  def get_business_by_id(payload, id):
    business = Business.query.filter(Business.id == id).one_or_none()
    if business is None:
        abort(404)
  
    return jsonify({
      'success': True,
      'customer' : business.long(),
      'status': 200
    }), 200


  @app.route('/customers')
  @requires_auth('get:customers')
  def get_customer(payload):
    customers = Customer.query.all()
    customers_formatted = [customer.long() for customer in customers]

    if len(customers) == 0:
        abort(400)
  
    return jsonify({
      'success': True,
      'customers' : customers_formatted,
      'status': 200
    }), 200

  

  @app.route('/customers/<int:id>')
  @requires_auth('get:customers-detail')
  def get_customer_by_id(payload, id):
    customer = Customer.query.filter(Customer.id == id).one_or_none()
    if customer is None:
        abort(404)
  
    return jsonify({
      'success': True,
      'customer' : customer.long(),
      'status': 200
    }), 200


  @app.route('/businesses', methods=['POST'])
  @requires_auth('post:business')
  def post_business(payload):
    body = request.get_json()
    id = body.get('id', None)
    name = body.get('name', None)
    address = body.get('address', None)
    phone = body.get('phone', None)
    cif = body.get('cif', None)
    email = body.get('email', None)

    try:
      if id is None:
        business = Business(name=name, address=address, phone=phone, cif=cif, email=email)
      else:
        business = Business(id=id, name=name, address=address, phone=phone, cif=cif, email=email)
      business.insert()
    except:
      abort(422)
        
    return jsonify({
      'success': True,
      'business' : business.long(),
      'status': 200
    }), 200


  @app.route('/businesses', methods=['PATCH'])
  @requires_auth('post:business')
  def patch_business(payload):
    body = request.get_json()
    id = body.get('id', None)
    name = body.get('name', None)
    address = body.get('address', None)
    phone = body.get('phone', None)
    cif = body.get('cif', None)
    email = body.get('email', None)

    try:
      business = Business.query.filter(Business.id == id).one_or_none()
      if name is not None:
        business.name = name
      if address is not None:
        business.address = address
      if phone is not None:
        business.phone = phone
      if cif is not None:
        business.cif = cif
      if email is not None:
        business.email = email
      business.insert()
    except:
      abort(422)
        
    return jsonify({
      'success': True,
      'business' : business.long(),
      'status': 200
    }), 200



  @app.route('/businesses/<int:id>', methods=['DELETE'])
  @requires_auth('delete:business')
  def delete_business(,payolad, id):
    business = Business.query.filter(Business.id == id).one_or_none()

    if business is None:
      abort(404)
    else:
      business.delete()

    return jsonify({
      'success': True,
      'business' : id,
      'status': 200
    }), 200


  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
        'success': False,
        'error': 404,
        'message': "Resource Not Found"
    }), 404


  @app.errorhandler(400)
  def bad_request(error):
      return jsonify({
          'success': False,
          'error': 400,
          'message': "Bad Request"
      }), 400
  

  @app.errorhandler(422)
  def unprocessable_entity(error):
      return jsonify({
        'success': False,
        'error': 422,
        'message': "Unprocessable Entity"
      }), 422


  @app.errorhandler(405)
  def not_allowed(error):
      return jsonify({
        'success': False,
        'error': 405,
        'message': "Method Not Allowed"
      }), 405

  
  @app.errorhandler(AuthError)
  def auth_error(error):
    return jsonify({
        'success': False,
        'error': error.status_code,
        'message': error.error['description']
    }), error.status_code

  return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
