from django.db import connection, connections
from .helpers import *
import psycopg2
import psycopg2.sql as sql


def check_existing_email_q(email):
    with connection.cursor() as cursor:
        cursor.execute("""SELECT * FROM public.user_data WHERE email = %s AND isdeleted=0 """,[email])
        resp = cursor.fetchall()
    return resp if resp else None


def user_insert_q(Data):
    with connection.cursor() as cursor:
        cursor.execute("""INSERT INTO public.user_data (user_uuid , first_name, last_name, email, password, phone, address, city, country, pincode, isdeleted, createdat) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING user_uuid""", Data)
        resp = dictfetchone(cursor)
    return resp

def user_login_q(email, password):
    with connection.cursor() as cursor:
        cursor.execute("""SELECT * FROM public.user_data WHERE email = %s AND password = %s AND isdeleted=0 """,[email, password])
        resp = cursor.fetchall()
    return resp if resp else None