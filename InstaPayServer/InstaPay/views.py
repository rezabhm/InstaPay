from django.shortcuts import HttpResponse, HttpResponseRedirect
from django.template import loader, context

from . import models

# views code ...

####################################
####################################
"""       Bloger Views           """
####################################
####################################


def bloger_signup(requests):

    """
    Bloger login to it's account
    """
    pass


def bloger_verify(requests):

    """
    Verify Bloger's account
    """
    pass


def bloger_verify_information(requests):

    """
    Verify Bloger's information (phone_number, address, password, ...)
    """
    pass


def bloger_edit_information(requests):

    """
    edit Bloger's information (phone_number, address, password, ...)
    """
    pass


def bloger_forgot_password(requests):

    """
    forgot password view to login bloger
    """
    pass


def bloger_forgot_password_verify(requests):

    """
    verify forgot password code
    """
    pass


def bloger_change_password(requests):

    """
    bloger change password
    """
    pass
