from db_engine import Session
from flask import Blueprint, request, g
from flask_restx import Namespace, fields, Resource
from authentication.hash_generator import HashGenerator
from models.User import User
from werkzeug.exceptions import BadRequest


api = Namespace('Registration', path='/users',
                description='New FilmFinder registration')

user = api.model('User', {
    'username': fields.String(description='First name of the user'),
    'yob': fields.Integer(description='Year of Birth of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='Password that will be used by the user when logging in to the service')
})

@api.route('')
class Users(Resource):
    description = '''\
    Creates a new user.
    Accepts the username, yob, email, and password of a new user.
    Rejects email that has been registered before.
    Hashes the password using bcrypt.
    Saves the new user attributes and the hashed password to the database.\
    '''
    @api.doc(security=[], description=description)
    @api.expect(user)
    @api.response(201, "Registration successful.")
    @api.response(400, "The parameters submitted are invalid or the provided email has been registered.")
    def post(self):
        # Get params
        username = request.json.get('username')
        yob = request.json.get('yob')
        email = request.json['email']
        password = request.json['password']

        session = Session()
        if session.query(User).filter(User.email == email).first():
            raise BadRequest

        hashed_password = HashGenerator(password).generate()
        new_user = User(username, email, hashed_password, yob)
        session.add(new_user)
        session.commit()

        # Put the current user id in global
        # g.userID = new_user.userID    #TODO: check if needed later.

        response = {'message': 'Registration successful.'}
        return response, 201