import json, jwt
from flask import Blueprint, request, jsonify, current_app, Response
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_restful import Api, Resource # used for REST API building
from datetime import datetime
from auth_middleware import token_required

from model.users import User, Stocks

user_api = Blueprint('user_api', __name__,
                   url_prefix='/api/users')


# API docs https://flask-restful.readthedocs.io/en/latest/api.html
api = Api(user_api)

class UserAPI:        
    class _CRUD(Resource):  # User API operation for Create, Read.  THe Update, Delete methods need to be implemeented
        # @token_required
        def post(self): # Create method
            ''' Read data for json body '''
            body = request.get_json()
            
            ''' Avoid garbage in, error checking '''
            # validate name
            name = body.get('name')
            if name is None or len(name) < 2:
                return {'message': f'Name is missing, or is less than 2 characters'}, 400
            # validate uid
            uid = body.get('uid')
            if uid is None or len(uid) < 2:
                return {'message': f'User ID is missing, or is less than 2 characters'}, 400
            # look for password and dob
            password = body.get('password')
            dob = body.get('dob')
            pnum = body.get('pnum')
            email = body.get('email')

            ''' Set up the email server functionality '''
            msg = Message('Welcome to Our Website', recipients=[email])
            msg.body = f'Hello {name}!\n\nThank you for signing up on Our Website. Please follow the instructions to complete your registration.'
            mail.send(msg)

            ''' #1: Key code block, setup USER OBJECT '''
            uo = User(name=name, uid=uid, password=password, pnum=pnum, email=email)
            
            ''' Additional garbage error checking '''
            # set password if provided
            if password is not None:
                uo.set_password(password)
            # convert to date type
            if dob is not None:
                try:
                    uo.dob = datetime.strptime(dob, '%Y-%m-%d').date()
                except:
                    return {'message': f'Date of birth format error {dob}, must be mm-dd-yyyy'}, 400
            
            if pnum is not None:
                try:
                    if pnum is None:
                        pnum = "123-456-7890"
                except:
                    return {'message': f'Phone number format error {pnum}, must be 10 digits'}, 400
            
            
            ''' #2: Key Code block to add user to database '''
            # create user in database
            user = uo.create()
            # success returns json of user
            if user:
                return jsonify(user.read())
            # failure returns error
            return {'message': f'Processed {name}, either a format error or User ID {uid} is duplicate'}, 400

        # @token_required
        def get(self): # Read Method , current_user
            users = User.query.all()    # read/extract all users from database
            json_ready = [user.read() for user in users]  # prepare output in json
            return jsonify(json_ready)  # jsonify creates Flask response object, more specific to APIs than json.dumps
        
        # @token_required
        def delete(self):
            ''' Read data from json body '''
            body = request.get_json()
            ''' Avoid garbage in, error checking '''
            # validate uid, name, and password
            uid = body.get('uid')
            password = body.get('password')
            if uid is None or len(uid) < 2:
                return {'message': f'User ID is missing, or is less than 2 characters'}, 400
            if password is None or len(password) < 2:
                return {'message': f'Password is missing, or is less than 2 characters'}, 400
            ''' Find user '''
            user = User.query.filter_by(_uid=uid).first()
            if user is None:
                return {'message': f'User {uid} not found'}, 400
            ''' Confirm Password Is Valid'''
            password = User.query.filter_by(password=password).first()
            if password is None:
                return {'message': f'Invalid password for user {uid}'}, 400
            ''' Delete user '''
            user.delete()
            return {'message': f'User {uid} deleted'}, 200
    
    class _Security(Resource):
        def post(self):
            try:
                body = request.get_json()
                if not body:
                    return {
                        "message": "Please provide user details",
                        "data": None,
                        "error": "Bad request"
                    }, 400
                ''' Get Data '''
                uid = body.get('uid')
                if uid is None:
                    return {'message': f'User ID is missing'}, 400
                password = body.get('password')
                
                ''' Find user '''
                user = User.query.filter_by(_uid=uid).first()
                if user is None or not user.is_password(password):
                    return {'message': f"Invalid user id or password"}, 400
                if user:
                    try:
                        token_payload = {
                            "_uid": user._uid,
                            "stockmoney": user._stockmoney
                        }
                        token = jwt.encode(
                            token_payload,
                            current_app.config["SECRET_KEY"],
                            algorithm="HS256"
                        )
                        print("this is token")
                        print (token)
                        resp = Response("Authentication for %s successful" % (user._uid))
                        resp.set_cookie("jwt", token,
                                max_age=3600,
                                secure=True,
                                httponly=False,
                                path='/',
                                samesite='None'  # This is the key part for cross-site requests

                                # domain="frontend.com"
                                )
                        return resp
                    except Exception as e:
                        current_app.logger.error('Error during authentication: %s', e)
                        return {'message': 'Internal server error'}, 500
                return {
                    "message": "Error fetching auth token!",
                    "data": None,
                    "error": "Unauthorized"
                }, 404
            except Exception as e:
                return {
                        "message": "Something went wrong!",
                        "error": str(e),
                        "data": None
                }, 500


            
    # building RESTapi endpoint
    api.add_resource(_CRUD, '/')
    api.add_resource(_Security, '/authenticate')
    