import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import db_drop_and_create_all, setup_db, Business, Customer

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
  def get_businesses():
    businesses = Business.query.all()
    businesses_formatted = [business.short() for business in businesses]

    if len(businesses) == 0:
        abort(400)
    
    return jsonify({
      'success': True,
      'businesses' : businesses_formatted,
      'status': 200
    }), 200

  
  @app.route('/businesses/<int:id>')
  def get_business_by_id(id):
    business = Business.query.filter(Business.id == id).one_or_none()
    if business is None:
        abort(404)
  
    return jsonify({
      'success': True,
      'customer' : business.short(),
      'status': 200
    }), 200


  @app.route('/customers')
  def get_customer():
    customers = Customer.query.all()
    customers_formatted = [customer.short() for customer in customers]

    if len(customers) == 0:
        abort(400)
  
    return jsonify({
      'success': True,
      'customers' : customers_formatted,
      'status': 200
    }), 200

  

  @app.route('/customers/<int:id>')
  def get_customer_by_id(id):
    customer = Customer.query.filter(Customer.id == id).one_or_none()
    if customer is None:
        abort(404)
  
    return jsonify({
      'success': True,
      'customer' : customer.short(),
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

  return app

APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)
