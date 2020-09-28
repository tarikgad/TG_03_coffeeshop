import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS
from werkzeug.exceptions import Forbidden, Unauthorized, BadRequest, NotFound

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,X-Requested-With,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
    response.headers.add('Access-Control-Allow-Credentials','true')
    return response
'''

'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''
#db_drop_and_create_all()

## ROUTES
'''
@TODO implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks',methods=['GET'])
def retrieve_drinks():
    selection = Drink.query.order_by(Drink.title).all()
    
    if len(selection) == 0:
        abort(404)
    
    drinks = []
    for d in selection:
        drinks.append(d.short())

    return jsonify({
      'success': True,
      'drinks': drinks
    })

'''
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks-detail',methods=['GET'])
@requires_auth('get:drinks-detail')
def retrieve_drinks_details(jwt):
    selection = Drink.query.order_by(Drink.title).all()

    if len(selection) == 0:
        abort(404)
    
    drinks = []
    for d in selection:
        drinks.append(d.long())

    return jsonify({
    'success': True,
    'drinks': drinks
    })


'''
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def add_drinks(jwt):
    body = request.get_json()
    req_title = body.get('title', None)
    req_recipe = body.get('recipe', None)
    
    if req_title == None or req_recipe == None:
        abort(404)
    
    check = Drink.query.filter_by(title=req_title).one_or_none()
    if check != None:
        raise AuthError({
            'code': 'invalid_data',
            'description': 'repeated title'
        },422)
    drink = Drink(title=req_title, recipe=json.dumps(req_recipe))
    drink.insert()
    
    return jsonify({
    'success': True,
    'drinks': drink.long()
    })


'''
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<int:drink_id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def update_drinks(jwt,drink_id):
    drink = Drink.query.filter_by(id=drink_id).one_or_none()
    
    if drink == None:
        abort(404)
    
    body = request.get_json()
    req_title = body.get('title', None)
    req_recipe = body.get('recipe', None)
    
    if req_title == None and req_recipe == None:
        abort(404)
    
    if req_title != None:
        check = Drink.query.filter_by(title=req_title).one_or_none()
        if check != None:
            raise AuthError({
                'code': 'invalid_data',
                'description': 'repeated title'
            },422)
        drink.title = req_title
    if req_recipe != None:
        drink.recipe = req_recipe
    drink.update()
    
    return jsonify({
    'success': True,
    'drinks': drink.long()
    })


'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<int:drink_id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drinks(jwt,drink_id):
    drink = Drink.query.filter_by(id=drink_id).one_or_none()
    
    if drink == None:
        abort(404)
    
    drink.delete()
    
    return jsonify({
    'success': True,
    'delete': drink_id
    })


## Error Handling
'''
Example error handling for unprocessable entity
'''
@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
                    "success": False, 
                    "error": 422,
                    "message": "unprocessable"
                    }), 422

'''
@TODO implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False, 
                    "error": 404,
                    "message": "resource not found"
                    }), 404
'''

'''
@TODO implement error handler for 404
    error handler should conform to general task above 
'''
#BadRequest
@app.errorhandler(400)
def bad_request(error):
    return jsonify({
                    "success": False, 
                    "error": 400,
                    "message": "bad request"
                    }), 400

#Unauthorized
@app.errorhandler(401)
def unauthorized(error):
    return jsonify({
                    "success": False, 
                    "error": 401,
                    "message": "unauthorized"
                    }), 401

#Forbidden
@app.errorhandler(403)
def forbidden(error):
    return jsonify({
                    "success": False, 
                    "error": 403,
                    "message": "forbidden"
                    }), 403

#NotFound
@app.errorhandler(404)
def not_found(error):
    return jsonify({
                    "success": False, 
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''
@TODO implement error handler for AuthError
    error handler should conform to general task above 
'''
def autherror_func(e):
    return jsonify({
        "success": False,
        "error": e.error['code'],
        "message": e.error['description']
    }), e.status_code

app.register_error_handler(AuthError,autherror_func)
