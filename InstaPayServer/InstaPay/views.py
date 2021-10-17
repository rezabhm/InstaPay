from django.shortcuts import HttpResponse, HttpResponseRedirect
from django.template import loader, context
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

from . import models

import hashlib

# views code ...

####################################
####################################
"""       Bloger Views           """
####################################
####################################


@csrf_exempt
def bloger_signup(requests):

    """
    Bloger SignUp to it's account
    """

    if requests.user.is_authenticated:

        # redirect to main page
        main_page = loader.get_template("InstaPay/main.html")

        return HttpResponse(main_page.render())

    else:

        # create user
        # get information from requests
        requests_info = requests.POST

        # bloger information
        name = requests_info["name"]
        last_name = requests_info["last_name"]
        page_name = requests_info["page_name"]
        password = requests_info["password"]
        verify_password = requests_info["verify_password"]
        address = requests_info["address"]
        phone_number = requests_info["phone_number"]
        national_code = requests_info["national_code"]
        shaba = requests_info["shaba"]
        bank_account_number = requests_info["bank_account_number"]
        bank_name = requests_info["bank_name"]
        email = requests_info["email"]

        # here we will check some of above information and if them True we will create user
        # else we will raised Error and redirect to SignUp form page

        # Check Page Name
        bloger_list = models.Bloger.objects.all().filter(page_name=page_name)

        if len(bloger_list) > 0:

            # redirect to signup form page because someone previously registered with this page name
            return bloger_signup_form(requests, "قبلا با این آدرس بیج ثبت نام شده است !!!")

        # Check password
        if password != verify_password:

            # raised error because password and verify password don't match
            return bloger_signup_form(requests, "رمز عبور و رمز عبور تصدیقی برابر نیستند")

        # Check Phone number
        if (len(str(phone_number)) != 11) or (str(phone_number)[:2] != "09"):

            # raised error because phone number format is false
            return bloger_signup_form(requests, "فرمت شماره موبایل نادرست است ")

        # Check national code
        if len(str(national_code)) != 10:

            # raised error because of false format
            return bloger_signup_form(requests, "کد ملی را اشتباه وارد کرده اید")

        # after check above information in here we will create user

        # create user
        bloger_user = User.objects.create_user(page_name, email, password)
        bloger_user.save()

        # login user
        login(requests, bloger_user)

        # create new bloger object
        bloger_obj = models.Bloger()

        # set attribute
        bloger_obj.name = name
        bloger_obj.last_name = last_name
        bloger_obj.page_name = page_name
        bloger_obj.address = address
        bloger_obj.phone_number = phone_number
        bloger_obj.national_code = national_code
        bloger_obj.bloger_email = email
        bloger_obj.bank_name = bank_name
        bloger_obj.bank_account_number = bank_account_number
        bloger_obj.shaba = shaba
        bloger_obj.bloger_password_hashcode = hashlib.sha256(password.encode()).hexdigest()
        bloger_obj.bloger_hashcode = str(hash(page_name) % 10 ** 8)

        # save bloger
        bloger_obj.save()

        return HttpResponse("ok")


def bloger_signup_form(requests, error_text="کادر های خالی را بر کنید ..."):

    """
    Bloger SignUp's form
    """

    if requests.user.is_authenticated:

        # redirect to main page
        main_page = loader.get_template("InstaPay/main.html")

        return HttpResponse(main_page.render())

    else:

        # render form login form page
        login_form_page = loader.get_template("InstaPay/Login_Form.html")

        context = {
            "error": error_text
        }

        return HttpResponse(login_form_page.render(context))


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
