import jwt
from flask import request, jsonify, make_response

from app.models.costum_user import CostumUser
from app import app

def token_required(function):
    def check_token(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return jsonify({'message': 'token missing'}, 401)
      
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = CostumUser.query.filter_by(public_id=data['id']).first
        except:
            
            return jsonify({'message': 'token not valid'}, 401)

        return function(current_user, *args, **kwargs)
  
    
    return check_token