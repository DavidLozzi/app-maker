from flask import Blueprint, request, jsonify
import boto3
from cognito_config import COGNITO_USER_POOL_ID, COGNITO_APP_CLIENT_ID

auth_bp = Blueprint('auth', __name__)

cognito_client = boto3.client('cognito-idp')

@auth_bp.route('/register', methods=['POST'])
def register_user():
    try:
        data = request.json
        email = data['email']
        password = data['password']
        response = cognito_client.sign_up(
            ClientId=COGNITO_APP_CLIENT_ID,
            Username=email,
            Password=password,
            UserAttributes=[
                {
                    'Name': 'email',
                    'Value': email
                }
            ]
        )
        return jsonify({'message': 'User registered successfully', 'user': response}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@auth_bp.route('/login', methods=['POST'])
def login_user():
    try:
        data = request.json
        email = data['email']
        password = data['password']
        response = cognito_client.initiate_auth(
            ClientId=COGNITO_APP_CLIENT_ID,
            AuthFlow='USER_PASSWORD_AUTH',
            AuthParameters={
                'USERNAME': email,
                'PASSWORD': password
            }
        )
        return jsonify({'message': 'Login successful', 'tokens': response['AuthenticationResult']}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400