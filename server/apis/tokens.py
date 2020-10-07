from flask import Blueprint, request, g
from flask_restx import Namespace, fields, Resource
from authentication.credentials_authenticator import CredentialsAuthenticator


api = Namespace('Authentication', path='/tokens',
                description='User authentication and JWT token creation')

credential = api.model('Credential', {
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='Password that the user specified when registering to the platform')
})

@api.route('')
class Tokens(Resource):
    description = '''\
    Authenticates a user based on submitted credentials.
    Upon successful authentication, \
    creates a JWT token to be used in subsequent requests by the user.
    '''
    @api.doc(security=[], description=description)
    @api.expect(credential)
    @api.response(201, "User authenticated. JWT token sucessfully created.")
    @api.response(401, "The credentials provided are incorrect.")
    def post(self):
        '''
        Authenticates a user and creates a JWT token for the user
        '''
        email = request.json['email']
        password = request.json['password']
        authenticator = CredentialsAuthenticator(email, password)
        user, token = authenticator.authenticate()

        # Analytics here
        status_code = 201
        # record = Recorder('login', status_code)
        # record.recordUsage()

        response = {
            'message': 'Login successful. Token is successfully created.',
            'email': user.email,
            'token': token
        }

        return response, status_code
