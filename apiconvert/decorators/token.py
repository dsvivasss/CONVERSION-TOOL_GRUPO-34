from flask import Flask, request, jsonify, make_response
import jwt

def token_required(func):
    def wrapper(self, *args, **kwargs):
        try:
            
            token = request.headers.get('Authorization').split(' ')[1]
            
            jwt.decode(token, options={'verify_signature': False, 'verify_aud': False, 'verify_nbf': False}, algorithms=["HS256"])
            
        except e:
            print(e)
            response = {
                'valid_token': False
            }
            return response, 401
        
        return func(self, *args, **kwargs) 
    return wrapper