from flask import Flask, request, jsonify, make_response
import jwt

def token_required(func):
    def wrapper(self, *args, **kwargs):
        try:
            
            token = request.headers.get('Authorization').split(' ')[1]
            
            jwt.decode(token, "secret", algorithms=["HS256"])
            
        except:
            response = {
                'valid_token': False
            }
            return response, 401
        
        return func(self, *args, **kwargs) 
    return wrapper