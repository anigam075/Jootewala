import os
import random
from urllib.parse import urlparse
import datetime
import pytz
from datetime import timedelta
from urllib.parse import unquote,quote

def get_filename_and_extension_from_url(url):
    parsed_url = urlparse(url)
    path = parsed_url.path
    filename = os.path.basename(path)
    filename_without_extension, file_extension = os.path.splitext(filename)
    return filename_without_extension, file_extension


def dictfetchall(cursor=''):
    # "Returns all rows from a cursor as a dict"
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]

def dictfetchone(cursor=''):
    # "Returns all rows from a cursor as a dict"
    desc = cursor.description
    print('\ndesc =========== > ', desc)
    return dict(zip([col[0] for col in desc], cursor.fetchone()))


def replace_null_with_empty_string_many(result):
    for dictionary in result:
        for i in dictionary:
            if dictionary[i] == 'NULL' or dictionary[i] == None or dictionary[i] == 'None' or dictionary[i] == 'null':
                dictionary[i] = ''
            elif type(dictionary[i]) == int:
                dictionary[i] = str(dictionary[i])
    return result


def replace_null_with_empty_string(dictionary):
    for i in dictionary:
        if dictionary[i] == 'NULL' or dictionary[i] == None or dictionary[i] == 'None' or dictionary[i] == 'null':
            dictionary[i] = ''
        elif type(dictionary[i]) == int:
            dictionary[i] = str(dictionary[i])
    return dictionary


def get_page(num1):
    if type(num1)== str:
        if num1.isdigit():
            num=int(num1)
            if num<=1:
                return 0
            else:
                return num-1
        else:
            return 0
    elif type(num1)== int:
        num=int(num1)
        if num<=1:
            return 0
        else:
            return num-1
    else:
        return 0


def get_file_size_in_megabytes(file_path):
   size = os.path.getsize(file_path)
   size_mb = size/(1024*1024)
   return f'{size_mb:.2f}'

def username(first_name, last_name):
    names = first_name + last_name
    first_letter = names[0][0]
    three_letters_surname = names[-1][:3]
    number = '{:03d}'.format(random.randrange(1, 999))
    username = (first_letter + three_letters_surname + number)
    return username