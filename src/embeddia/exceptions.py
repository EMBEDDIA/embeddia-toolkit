from rest_framework.exceptions import APIException
from rest_framework import status

'''
default_detail - detailed message of the exception
default_code - code identifier of exception
'''

class ServiceFailedException(APIException):
    '''Raised when Service fails to process input.'''
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = ("Service failed.")
    default_code = 'service_failed'
