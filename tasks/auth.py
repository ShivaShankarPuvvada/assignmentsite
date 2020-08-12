import jwt
from django.http import JsonResponse
from django.conf import settings
def authrize_user(jwt_token):
    if jwt_token:
            payload = jwt.decode(jwt_token.replace('Bearer ', ''), settings.JWT_SECRET,
                                 algorithm=['HS256'])
            return payload
def encode_jobseeker_id(user_id):
    payload={
    'user_id':user_id,
    }
    encoded = jwt.encode(payload, settings.JWT_SECRET, algorithm='HS256')
    return encoded.decode('utf-8')