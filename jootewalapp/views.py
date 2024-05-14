import jwt
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework import status as stus
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes, authentication_classes
import uuid
import datetime
import requests
from django.core.mail import get_connection
from django.template import Context
from django.template.loader import render_to_string, get_template
from django.core.mail import EmailMessage
from .serializer import *
from .queries import *
from .helpers import *


@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def user_login_f(request):
    try:
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.data['Email']
            password = serializer.data['Password']
            user_exists = user_login_q(email, password)
            print('user_exists ===== ', user_exists)

            if user_exists:
                json_data = {
                    'status_code': 200,
                    'status': 'Success',
                    'data': user_exists,
                    'message': 'Data Found Successfully',
                }
                return Response(json_data, status=stus.HTTP_200_OK)
            else:
                json_data = {
                    'status_code': 200,
                    'status': 'Success',
                    'Reason': 'Incorrect email/password',
                    'message': 'Data Not Found',
                }
                return Response(json_data, status=stus.HTTP_200_OK)
        else:
            json_data = {
                'status_code': 300,
                'status': 'Failed',
                'data': serializer.errors,
                'message': 'Please Enter All Fields'
            }
            return Response(json_data, status=stus.HTTP_300_MULTIPLE_CHOICES)
    except Exception as e:
        json_data = {
            'status_code': 400,
            'status': 'Failed',
            'Reason': e,
            'Remark': 'Landed in Exception',
        }
        raise APIException(json_data)
    

@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def user_register_f(request):
    try:
        serializer = UserProfileInsertSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.data['Email']
            email_exists = check_existing_email_q(email)
            if not email_exists:
                Data = {
                    'UserID': str(uuid.uuid4()),
                    'FirstName': serializer.data['FirstName'],
                    'LastName': serializer.data['LastName'],
                    'Email': serializer.data['Email'],
                    'Password': serializer.data['Password'],
                    'Phone': serializer.data['Phone'],
                    'Address': serializer.data['Address'],
                    'City': serializer.data['City'],
                    'Country': serializer.data['Country'],
                    'Pincode': serializer.data['Pincode'],
                    'Isdeleted': 0,
                    'CreatedAt': datetime.datetime.now()
                }
                insert = user_insert_q(list(Data.values()))
                if insert:
                    json_data = {
                        'status_code': 200,
                        'status': 'Success',
                        'data': '',
                        'message': 'Data Inserted Successfully',
                    }
                    return Response(json_data, status=stus.HTTP_200_OK)
                else:
                    json_data = {
                        'status_code': 200,
                        'status': 'Failed',
                        'data': '',
                        'message': 'Data Not Inserted',
                    }
                    return Response(json_data, status=stus.HTTP_200_OK)
            else:
                json_data = {
                    'status_code': 200,
                    'status': 'Failed',
                    'Reason': "Duplicate Email Entered",
                    'Remark': 'Email Already Exists',
                }
                return Response(json_data, status=stus.HTTP_200_OK)
        else:
            json_data = {
                'status_code': 300,
                'status': 'Failed',
                'data': serializer.errors,
                'message': 'Please Enter All Fields'
            }
            return Response(json_data, status=stus.HTTP_300_MULTIPLE_CHOICES)
    except Exception as e:
        json_data = {
            'status_code': 400,
            'status': 'Failed',
            'Reason': e,
            'Remark': 'Landed in Exception',
        }
        raise APIException(json_data)
    

