import random
import time

from django.shortcuts import HttpResponse, HttpResponseRedirect, redirect
from django.urls import reverse
from django.template import loader, Context
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout

from . import models
import hashlib
from . import Information
from hashlib import sha1
from Crypto.Signature import PKCS1_v1_5
from Crypto.PublicKey import RSA
import base64
from zeep import Client

# views code ...

####################################
####################################
"""       Bloger Views           """
####################################
####################################


def main(requests):

    """
    render main page
    """

    main_page = loader.get_template("InstaPay/main.html")

    return HttpResponse(main_page.render())


@csrf_exempt
def bloger_signup(requests):

    """
    Bloger SignUp to it's account
    """

    if requests.user.is_authenticated:

        # redirect to main page
        return HttpResponseRedirect(reverse('main'))

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
            return bloger_signup_form(requests, "???????? ???? ?????? ???????? ?????? ?????? ?????? ?????? ?????? !!!")

        # Check password
        if password != verify_password:

            # raised error because password and verify password don't match
            return bloger_signup_form(requests, "?????? ???????? ?? ?????? ???????? ???????????? ?????????? ????????????")

        # Check Phone number
        if (len(str(phone_number)) != 11) or (str(phone_number)[:2] != "09"):

            # raised error because phone number format is false
            return bloger_signup_form(requests, "???????? ?????????? ???????????? ???????????? ?????? ")

        # Check national code
        if len(str(national_code)) != 10:

            # raised error because of false format
            return bloger_signup_form(requests, "???? ?????? ???? ???????????? ???????? ???????? ??????")

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


def bloger_signup_form(requests, error_text="???????? ?????? ???????? ???? ???? ???????? ..."):

    """
    Bloger SignUp's form
    """

    if requests.user.is_authenticated:

        # redirect to main page
        return HttpResponseRedirect(reverse('main'))

    else:

        # render form login form page
        login_form_page = loader.get_template("InstaPay/SignUp_Form.html")

        context = {
            "error": error_text
        }

        return HttpResponse(login_form_page.render(context))


def bloger_verify_information(requests):

    """
    Verify Bloger's information (phone_number, address, password, ...)
    """

    # this requests method is POST and contain to keys (param_name, value, page_name, password)
    # param_name    :   it is one of the bloger's attribute that we want verify it
    # value         :   it is attribute's value that w want verify it

    param_name = requests.POST['param_name']
    value = requests.POST["value"]
    page_name = requests.POST["page_name"]

    # we must get password's hash
    password = requests.POST["password"]

    # get bloger's object
    bloger_list = models.Bloger.objects.all().filter(page_name=page_name)

    if len(bloger_list) > 0:

        bloger_obj = bloger_list[0]

        if bloger_obj.bloger_password_hashcode == password:

            # so we must verify data if it's correct we must return 1 else we must return 0

            if bloger_obj.verify_param(param_name) == value:

                # so our value verified
                return HttpResponse("1")

            else:

                # value didn't verified
                return HttpResponse("0")

        else:

            # this error mean's password is incorrect
            return HttpResponse("-2")

    else:

        # this return means we didn't have this user
        return HttpResponse("-1")


def bloger_edit_information_form(requests, error_text="?????????? ???? ???????? ?????????? ????????"):

    """
    edit Bloger's information form
    """

    if requests.user.is_authenticated and not requests.user.is_superuser:

        # render edit information form page
        edit_info_form_page = loader.get_template("InstaPay/Edit_Information_Form.html")

        page_name = requests.user.username
        bloger_list = models.Bloger.objects.all().filter(page_name=page_name)

        if len(bloger_list) > 0:

            bloger_obj = bloger_list[0]

            context = {

                "error": error_text,
                "name": bloger_obj.name,
                "last_name": bloger_obj.last_name,
                "page_name": bloger_obj.page_name,
                "phone_number": bloger_obj.phone_number,
                "address": bloger_obj.address,
                "email": bloger_obj.bloger_email,
                "national_code": bloger_obj.national_code,
                "bank_name": bloger_obj.bank_name,
                "bank_account_number": bloger_obj.bank_account_number,
                "shaba": bloger_obj.shaba,
                "password": bloger_obj.bloger_password_hashcode

            }

            return HttpResponse(edit_info_form_page.render(context))

        else:

            context = {

                "error": "???????????? ???? ?????? ???????????? ???????? ??????????"

            }
            return HttpResponse(edit_info_form_page.render(context))

    else:

        # redirect to main page
        return HttpResponseRedirect(reverse('main'))


@csrf_exempt
def bloger_edit_information(requests):

    """
    edit Bloger's information (phone_number, address, password, ...)
    """

    if requests.user.is_authenticated and not requests.user.is_superuser:

        # edit information
        # get information from requests
        requests_info = requests.POST

        # bloger information
        name = requests_info["name"]
        last_name = requests_info["last_name"]
        page_name = requests_info["page_name"]
        address = requests_info["address"]
        phone_number = requests_info["phone_number"]
        national_code = requests_info["national_code"]
        shaba = requests_info["shaba"]
        bank_account_number = requests_info["bank_account_number"]
        bank_name = requests_info["bank_name"]
        email = requests_info["email"]
        password = requests_info["password"]

        # here we will check some of above information and if them True we will edit data
        # else we will raised Error and redirect to Edit page form

        # Check Page Name
        bloger_list = models.Bloger.objects.all().filter(page_name=page_name)

        if len(bloger_list) != 1:

            # redirect to signup form page because someone previously registered with this page name
            return HttpResponseRedirect(reverse('bloger_edit_information_form', args=["?????? ?????? ?????? ???????? ?????????????? !!!"]))

        # Check Phone number
        if (len(str(phone_number)) != 11) or (str(phone_number)[:2] != "09"):

            # raised error because phone number format is false
            return HttpResponseRedirect(reverse("bloger_signup_form",args=[ "???????? ?????????? ???????????? ???????????? ?????? "]))

        # Check national code
        if len(str(national_code)) != 10:

            # raised error because of false format
            return HttpResponseRedirect(reverse(bloger_signup_form,args=[ "???? ?????? ???? ???????????? ???????? ???????? ??????"]))

        # after check above information in here we will edit information

        # get bloger's object
        user_name = requests.user.username
        bloger_obj = models.Bloger.objects.all().filter(page_name=user_name)[0]

        if bloger_obj.bloger_password_hashcode == password:

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
            bloger_obj.bloger_hashcode = str(hash(page_name) % 10 ** 8)

            # update user's user_name
            new_user = requests.user
            new_user.user_name = page_name
            new_user.save()

            # save bloger
            bloger_obj.save()

            return HttpResponseRedirect(reverse("bloger_edit_information_form", args=[ "???????????? ???? ???????????? ?????????? ????????"]))

        else:

            # if password is incorrect
            return HttpResponseRedirect(reverse("bloger_edit_information_form", args=[ "?????? ???????? ???????????? ???????? ?????? ?????? "]))

    else:

        # redirect to main page
        return HttpResponseRedirect(reverse('main'))


def bloger_login_form(requests, error_text="???????? ?????? ?? ?????? ???????? ???? ???????? ????????"):

    """
    login form
    """

    if requests.user.is_authenticated:

        # redirect to main page
        return HttpResponseRedirect(reverse('main'))

    else:

        # render login form page
        login_form_page = loader.get_template("InstaPay/Login_Form.html")

        context = {

            "error": error_text

        }

        return HttpResponse(login_form_page.render(context))


@csrf_exempt
def bloger_login(requests):

    """
    Bloger login to it's account
    """

    if not requests.user.is_authenticated:

        # login to account
        user_name = requests.POST["page_name"]
        password = requests.POST["password"]

        # verify username and password
        user_obj = authenticate(requests, username=user_name, password=password)

        if user_obj:

            # login
            login(requests, user_obj)
            return HttpResponseRedirect(reverse('main'))

        else:

            # username or password is incorrect
            return HttpResponseRedirect(reverse("bloger_login_form",args= ["?????? ???????? ???? ?????? ?????? ???????????? ??????"]))

    else:

        # user login previously and just redirect to main page
        return HttpResponseRedirect(reverse('main'))


def bloger_logout(requests):

    """
    logout bloger
    """

    if requests.user.is_authenticated:

        # logout
        logout(requests)

    return HttpResponseRedirect(reverse('main'))


def bloger_forgot_password_form(requests, error_text="?????? ???? ???? ?????????? ???????????? ?????? ?????????? ?????? ???? ???????? ????????"):

    """
    forgot password form for change password
    """

    if requests.user.is_authenticated:

        # redirect to main page
        return HttpResponseRedirect(reverse('main'))

    else:

        # generate new code and send it to bloge

        # get page name from post request information
        page_name = requests.POST["page_name"]

        # get all of bloger list
        bloger_list = models.Bloger.objects.all().filter(page_name=page_name)

        # check user exist or not
        if len(bloger_list) == 0:

            # user's doesn't exist so we must redirect to signup page
            return HttpResponseRedirect(reverse("bloger_signup_form",
                                                args=[ "???????? ???????????? ?????????? ?????? ???????? . ???????? ?????? ?????? ????????"]))

        else:

            # we must generate verification code
            bloger_obj = bloger_list[0]

            # generate new code
            bloger_obj.forgot_password_code = random.randint(100000, 999999)

            # renew code's deadline
            bloger_obj.forgot_password_code_deadline = time.time() + 300.0

            # save bloger
            bloger_obj.save()
            phone_number = str(bloger_obj.phone_number)[4:-4]

            # load template
            forgot_password_form_html = loader.get_template("InstaPay/Forgot_Password_Form.html")

            context = Context({

                "error": error_text,
                "phone_number": phone_number,
                "page_name": page_name,
                "next_page": "change_password",

            })

            return HttpResponse(forgot_password_form_html.render(context))


@csrf_exempt
def bloger_forgot_password_verify(requests):

    """
    verify forgot password code
    """

    if requests.user.is_superuser:

        # redirect to main page
        return HttpResponseRedirect(reverse('main'))

    elif requests.user.is_authenticated:

        # in this condition user has logged in and try to verify it's sms

        # get post data
        request_inf = requests.POST

        page_name = request_inf["page_name"]

        # get bloger's list
        bloger_list = models.Bloger.objects.all().filter(page_name=page_name)

        if len(bloger_list) == 0:

            # user doesn't exist and must signup
            return HttpResponseRedirect(reverse("bloger_signup_form",args=[ "???????????? ????  ???????? ?????????? ?????????????? ???????? ?????? ?????? ????????"]))

        else:

            # get bloger object
            bloger_obj = bloger_list[0]

            # change verify_phone_number value to True
            bloger_obj.verify_phone_number = True
            bloger_obj.save()

            return HttpResponseRedirect(reverse('main'))

    else:

        # verify code and redirect to change password

        # get post data
        request_inf = requests.POST

        page_name = request_inf["page_name"]

        # get bloger's list
        bloger_list = models.Bloger.objects.all().filter(page_name=page_name)

        if len(bloger_list) == 0:

            # user doesn't exist and must signup
            return HttpResponseRedirect(reverse("bloger_signup_form",
                                                args=["???????????? ????  ???????? ?????????? ?????????????? ???????? ?????? ?????? ????????"]))

        else:

            # get bloger object
            bloger_obj = bloger_list[0]

            # get input code
            code = request_inf["code"]

            # get bloger code
            bloger_code = bloger_obj.forgot_password_code

            # check time
            code_deadline = bloger_obj.forgot_password_code_deadline

            if code_deadline < time.time():

                # user can't change password and we must send new code
                error_text = "???? ???? ?????? ???????? ???????? ?????? .???? ?????????? ?????????? ?????? ?????? ???????? ???? ???? ???? ???????? ????????"
                return HttpResponseRedirect(reverse("bloger_forgot_password_form", args=[error_text]))

            else:

                if bloger_code == code:

                    # code is correct and redirect to change_password view
                    password_hashcode = bloger_obj.bloger_password_hashcode
                    return HttpResponseRedirect(reverse("bloger_change_password_form",
                                                        args= [page_name, password_hashcode]))

                else:

                    # code is incorrect and must get it again
                    return HttpResponseRedirect(reverse("bloger_forgot_password_form",args=[ "???? ???? ???????? ???????? ????????"]))


def bloger_change_password_form(requests, page_name, password_hashcode):

    """
    bloger change password

    NOTE:
        from url we can't access to this view .
        the only for access this view is above view .
    """

    if requests.user.is_superuser:

        # redirect to main page
        return HttpResponseRedirect(reverse('main'))

    else:

        # check password and page name
        bloger_obj = models.Bloger.objects.all().filter(page_name=page_name)[0]

        # get password_hashcode
        if password_hashcode == bloger_obj.bloger_password_hashcode:

            # user have access to change password
            change_password_form = loader.get_template("InstaPay/Change_Password_Form.html")

            context = Context({

                "page_name": page_name,
                "old_pass": password_hashcode

            })

            return HttpResponse(change_password_form.render(context))

        else:

            # password is incorrect
            return HttpResponseRedirect(reverse("bloger_login_form", args=[ "?????????????? ???????? ?????? ???????????? ??????."]))


@csrf_exempt
def bloger_change_password(requests):

    """
    change password in database
    """

    # get requests post information
    old_pass = requests.POST["old_pass"]
    new_pass = requests.POST["new_pass"]
    verify_new_pass = requests.POST["verify_new_pass"]
    page_name = requests.POST["page_name"]

    # get bloger objects
    bloger_obj = models.Bloger.objects.all().filter(page_name=page_name)[0]

    if bloger_obj.bloger_password_hashcode != old_pass:

        # user cant change password
        return HttpResponseRedirect(reverse('main'))

    else:

        # user have access to change password
        # check new_pass and verify_new_pass

        if new_pass != verify_new_pass:

            # redirect to previous page
            return HttpResponseRedirect(reverse("bloger_change_password_form", args=[page_name, old_pass]))

        else:

            # change password
            new_pass = hashlib.sha256(new_pass.encode()).hexdigest()
            bloger_obj.bloger_password_hashcode = new_pass
            bloger_obj.save()

            return HttpResponseRedirect(reverse("bloger_login_form", args=["???????????? ?????? ???????? ???? ?????????? ???????? ??????"]))


def create_product_form(requests):
    """
    create product form for get product information
    """

    if requests.user.is_authenticated and not requests.user.is_superuser:

        # return create product form
        product_form = loader.get_template("InstaPay/Create_Product.html")

        context = {

            "username": requests.user.username,

        }

        return HttpResponse(product_form.render(context))

    else:

        # redirect to main page
        return HttpResponseRedirect(reverse('main'))


@csrf_exempt
def create_product(requests):

    """
    create product and store it's image
    """

    if requests.user.is_authenticated and not requests.user.is_superuser:

        # get post data
        requests_inf = requests.POST

        # get bloger object
        bloger_obj = models.Bloger.objects.all().filter(page_name=requests.user.username)[0]

        # get information
        name = requests_inf["name"]
        price = requests_inf["price"]
        description = requests_inf["description"]
        number = requests_inf["number"]
        off_code = requests_inf["off_code"]
        off_code_deadline = requests_inf["off_code_deadline"]
        category = requests_inf["category"]
        image = requests.FILES.get('image')
        product_hashcode = str(hash(bloger_obj.page_name+name) % 10 ** 12)

        # set purchase_state value
        try:
            x = requests_inf["purchase_state"]
            purchase_state = True
        except:
            purchase_state = False

        # create product object
        prod = models.Product()

        # set attribute
        prod.name = name
        prod.price = price
        prod.description = description
        prod.number = number
        prod.purchase_state = purchase_state
        prod.off_code = off_code
        prod.off_code_deadline = off_code_deadline
        prod.category = category
        prod.image = image
        prod.bloger = bloger_obj
        prod.product_hashcode = product_hashcode

        # save product
        prod.save()

        return HttpResponseRedirect(reverse('Product_List'))

    else:

        # redirect to main page
        return HttpResponseRedirect(reverse('main'))


def product_list(requests):

    """
    return all of user's product
    """

    if requests.user.is_authenticated and not requests.user.is_superuser:

        # get product list
        prod_list = models.Product.objects.all().filter(bloger__page_name=requests.user.username)

        if len(prod_list) > 0:

            context = {

                "prod_len": True,
                'prod_list': prod_list,
                "super_user": False

            }

        else:

            context = {

                "prod_len": False,
                'prod_list': prod_list,
                "super_user": False

            }

        # load template
        prod_list_temp = loader.get_template("InstaPay/Product_List.html")

        return HttpResponse(prod_list_temp.render(context))

    elif requests.user.is_authenticated and requests.user.is_superuser:

        # get product list
        prod_list = models.Product.objects.all()

        if len(prod_list) > 0:

            cont = {

                "prod_len": True,
                'prod_list': prod_list,
                "super_user": True

            }

        else:

            cont = {

                "prod_len": False,
                'prod_list': prod_list,
                "super_user": True

            }

        # load template
        prod_list_temp = loader.get_template("InstaPay/Product_List.html")

        return HttpResponse(prod_list_temp.render(cont))

    else:

        return HttpResponseRedirect(reverse('main'))


def product_list_admin(requests, page_name):

    """
    return all of user's product
    """

    if requests.user.is_authenticated and requests.user.is_superuser:

        # get product list
        prod_list = models.Product.objects.all().filter(bloger__page_name=page_name)

        if len(prod_list) > 0:

            context = {

                "prod_len": True,
                'prod_list': prod_list,
                "super_user": True

            }

        else:

            context = {

                "prod_len": False,
                'prod_list': prod_list,
                "super_user": True

            }

        # load template
        prod_list_temp = loader.get_template("InstaPay/Product_List.html")

        return HttpResponse(prod_list_temp.render(context))

    else:

        # redirect to main page
        return HttpResponseRedirect(reverse('main'))


def edit_product_form(requests, product_hashcode):

    """
    return html for edit product
    """

    # only admin and bloger can access this page
    if not requests.user.is_authenticated:

        # return to main page
        return HttpResponseRedirect(reverse('main'))

    else:

        # at first we must show previous value and let them change it
        product_list_objects = models.Product.objects.all().filter(product_hashcode=product_hashcode)

        if len(product_list_objects) == 0:

            # return to main page because there is no product
            return HttpResponseRedirect(reverse('main'))

        else:

            username = requests.user.username

            # check user have access to change product information or not
            if username == product_list_objects[0].bloger.page_name or requests.user.is_superuser:

                # return product value
                context = {

                    "product": product_list_objects[0]

                }

                # get template
                edit_form = loader.get_template('InstaPay/Edit_Product.html')

                return HttpResponse(edit_form.render(context))

            else:

                # return main page
                return HttpResponseRedirect(reverse('main'))


@csrf_exempt
def edit_product(requests):

    """
    edit product
    """

    # only user can change product information
    if not requests.user.is_authenticated:

        # return to main page
        return HttpResponseRedirect(reverse('main'))

    else:

        request_inf = requests.POST
        username = requests.user.username

        product_objects_list = models.Product.objects.all().filter(product_hashcode=request_inf['product_hashcode'])

        if len(product_objects_list) == 0:

            # return to product list
            return HttpResponseRedirect(reverse('Product_List'))

        else:

            # check user have access or not
            prod = product_objects_list[0]

            if prod.bloger.page_name == username or requests.user.is_superuser:

                # have access

                # update information
                prod.name = request_inf['name']
                prod.price = request_inf['price']
                prod.description = request_inf['description']
                prod.number = request_inf['number']
                prod.off_code = request_inf['off_code']
                prod.off_code_deadline = request_inf['off_code_deadline']
                prod.category = request_inf['category']

                purchase_state = True if request_inf["purchase_state"] == "True" else False

                try:
                    x = request_inf['purchase_state_change']
                    purchase_state = not purchase_state
                except:
                    pass

                prod.purchase_state = purchase_state

                # save change's
                prod.save()

                return HttpResponseRedirect(reverse('Product_List'))

            else:

                # return to main page because don't have access
                return HttpResponseRedirect(reverse('main'))


def delete_product(requests, product_hashcode):

    """
    delete product
    """

    # only user can change
    if not requests.user.is_authenticated:

        # return to main page
        return HttpResponseRedirect(reverse('main'))

    else:

        username = requests.user.username

        product_objects_list = models.Product.objects.all().filter(product_hashcode=product_hashcode)

        if len(product_objects_list) == 0:

            # return to product list
            return HttpResponseRedirect(reverse('Product_List'))

        else:

            # check user have access or not
            prod = product_objects_list[0]

            if prod.bloger.page_name == username or requests.user.is_superuser:

                # delete object
                prod.delete()

                return HttpResponseRedirect(reverse('Product_List'))

            else:

                # return to main page
                return HttpResponseRedirect(reverse('main'))


def factor_list(requests, product_hashcode):

    """
    return all of product's factor
    """

    if requests.user.is_authenticated and not requests.user.is_superuser:

        # return factor list
        # get factor list

        factor_objects_list = models.Factor.objects.all().filter(product__product_hashcode=product_hashcode)

        if len(factor_objects_list) > 0:

            if requests.user.username == factor_objects_list[0].bloger.page_name:
                context = {

                    "len": True,
                    "superuser": True,
                    "factor": factor_objects_list

                }

            else:

                # redirect main page
                return HttpResponseRedirect(reverse('main'))

        else:

            context = {

                "len": False,
                "superuser": False,
                "factor": factor_objects_list

            }

        # get template
        factor_list_temp = loader.get_template("InstaPay/Factor_List_Product.html")

        return HttpResponse(factor_list_temp.render(context))

    elif requests.user.is_authenticated and requests.user.is_superuser:

        # return factor list
        # get factor list

        factor_objects_list = models.Factor.objects.all().filter(product__product_hashcode=product_hashcode)

        if len(factor_objects_list) > 0:

            context = {

                "len": True,
                "superuser": True,
                "factor": factor_objects_list

            }

        else:

            context = {

                "len": False,
                "superuser": True,
                "factor": factor_objects_list

            }

        # get template
        factor_list_temp = loader.get_template("InstaPay/Factor_List_Product.html")

        return HttpResponse(factor_list_temp.render(context))

    else:

        # redirect to main page
        return HttpResponseRedirect(reverse('main'))


def factor_list_ordering(requests, product_hashcode, ordering_state):

    """
    show ordering factor
    """

    ordering_state = True if str(ordering_state) == '1' else False

    if requests.user.is_authenticated and not requests.user.is_superuser:

        # return factor list
        # get factor list

        factor_objects_list = models.Factor.objects.all().filter(product__product_hashcode=product_hashcode).filter(
            factor_statement_ordering_factor=ordering_state)

        if len(factor_objects_list) > 0:

            if requests.user.username == factor_objects_list[0].bloger.page_name:
                context = {

                    "len": True,
                    "superuser": True,
                    "factor": factor_objects_list

                }

            else:

                # redirect main page
                return HttpResponseRedirect(reverse('main'))

        else:

            context = {

                "len": False,
                "superuser": False,
                "factor": factor_objects_list

            }

        # get template
        factor_list_temp = loader.get_template("InstaPay/Factor_List_Product.html")

        return HttpResponse(factor_list_temp.render(context))

    elif requests.user.is_authenticated and requests.user.is_superuser:

        # return factor list
        # get factor list

        factor_objects_list = models.Factor.objects.all().filter(product__product_hashcode=product_hashcode).filter(
            factor_statement_ordering_factor=ordering_state)

        if len(factor_objects_list) > 0:

            context = {

                "len": True,
                "superuser": True,
                "factor": factor_objects_list

            }

        else:

            context = {

                "len": False,
                "superuser": True,
                "factor": factor_objects_list

            }

        # get template
        factor_list_temp = loader.get_template("InstaPay/Factor_List_Product.html")

        return HttpResponse(factor_list_temp.render(context))

    else:

        # redirect to main page
        return HttpResponseRedirect(reverse('main'))


def factor_list_payment_to_bloger(requests, product_hashcode, payment_state=1):

    """
    show all of product's payment factor
    """

    payment_state = True if str(payment_state) == '1' else False

    if requests.user.is_authenticated and not requests.user.is_superuser:

        # return factor list
        # get factor list

        factor_objects_list = models.Factor.objects.all().filter(product__product_hashcode=product_hashcode).filter(
            factor_statement_payment_to_bloger=payment_state)

        if len(factor_objects_list) > 0:

            if requests.user.username == factor_objects_list[0].bloger.page_name:
                context = {

                    "len": True,
                    "superuser": True,
                    "factor": factor_objects_list

                }

            else:

                # redirect main page
                return HttpResponseRedirect(reverse('main'))

        else:

            context = {

                "len": False,
                "superuser": False,
                "factor": factor_objects_list

            }

        # get template
        factor_list_temp = loader.get_template("InstaPay/Factor_List_Product.html")

        return HttpResponse(factor_list_temp.render(context))

    elif requests.user.is_authenticated and requests.user.is_superuser:

        # return factor list
        # get factor list

        factor_objects_list = models.Factor.objects.all().filter(product__product_hashcode=product_hashcode).filter(
            factor_statement_payment_to_bloger=payment_state)

        if len(factor_objects_list) > 0:

            context = {

                "len": True,
                "superuser": True,
                "factor": factor_objects_list

            }

        else:

            context = {

                "len": False,
                "superuser": True,
                "factor": factor_objects_list

            }

        # get template
        factor_list_temp = loader.get_template("InstaPay/Factor_List_Product.html")

        return HttpResponse(factor_list_temp.render(context))

    else:

        # redirect to main page
        return HttpResponseRedirect(reverse('main'))


def factor(requests):

    """
    return all of factor
    """

    if requests.user.is_authenticated and not requests.user.is_superuser:

        # return factor list
        # get factor list

        factor_objects_list = models.Factor.objects.all().filter(bloger__page_name=requests.user.username)

        if len(factor_objects_list) > 0:

            if requests.user.username == factor_objects_list[0].bloger.page_name:
                context = {

                    "len": True,
                    "superuser": True,
                    "factor": factor_objects_list

                }

            else:

                # redirect main page
                return HttpResponseRedirect(reverse('main'))

        else:

            context = {

                "len": False,
                "superuser": False,
                "factor": factor_objects_list

            }

        # get template
        factor_list_temp = loader.get_template("InstaPay/Factor_List_Product.html")

        return HttpResponse(factor_list_temp.render(context))

    elif requests.user.is_authenticated and requests.user.is_superuser:

        # return factor list
        # get factor list

        factor_objects_list = models.Factor.objects.all()

        if len(factor_objects_list) > 0:

            context = {

                "len": True,
                "superuser": True,
                "factor": factor_objects_list

            }

        else:

            context = {

                "len": False,
                "superuser": True,
                "factor": factor_objects_list

            }

        # get template
        factor_list_temp = loader.get_template("InstaPay/Factor_List_Product.html")

        return HttpResponse(factor_list_temp.render(context))

    else:

        # redirect to main page
        return HttpResponseRedirect(reverse('main'))


def factor_ordering(requests, ordering_state):

    """
    return all of factor
    """

    ordering_state = True if str(ordering_state) == "1" else False

    if requests.user.is_authenticated and not requests.user.is_superuser:

        # return factor list
        # get factor list

        factor_objects_list = models.Factor.objects.all().filter(bloger__page_name=requests.user.username).filter(
            factor_statement_ordering_factor=ordering_state)

        if len(factor_objects_list) > 0:

            if requests.user.username == factor_objects_list[0].bloger.page_name:
                context = {

                    "len": True,
                    "superuser": True,
                    "factor": factor_objects_list

                }

            else:

                # redirect main page
                return HttpResponseRedirect(reverse('main'))

        else:

            context = {

                "len": False,
                "superuser": False,
                "factor": factor_objects_list

            }

        # get template
        factor_list_temp = loader.get_template("InstaPay/Factor_List_Product.html")

        return HttpResponse(factor_list_temp.render(context))

    elif requests.user.is_authenticated and requests.user.is_superuser:

        # return factor list
        # get factor list

        factor_objects_list = models.Factor.objects.all().filter(
            factor_statement_ordering_factor=ordering_state)

        if len(factor_objects_list) > 0:

            context = {

                "len": True,
                "superuser": True,
                "factor": factor_objects_list

            }

        else:

            context = {

                "len": False,
                "superuser": True,
                "factor": factor_objects_list

            }

        # get template
        factor_list_temp = loader.get_template("InstaPay/Factor_List_Product.html")

        return HttpResponse(factor_list_temp.render(context))

    else:

        # redirect to main page
        return HttpResponseRedirect(reverse('main'))


def factor_bloger_payment(requests, payment_state):

    """
    return all of payment factor
    """

    payment_state = True if str(payment_state) == "1" else False

    if requests.user.is_authenticated and not requests.user.is_superuser:

        # return factor list
        # get factor list

        factor_objects_list = models.Factor.objects.all().filter(bloger__page_name=requests.user.username).filter(
            factor_statement_payment_to_bloger=payment_state)

        if len(factor_objects_list) > 0:

            if requests.user.username == factor_objects_list[0].bloger.page_name:
                context = {

                    "len": True,
                    "superuser": True,
                    "factor": factor_objects_list

                }

            else:

                # redirect main page
                return HttpResponseRedirect(reverse('main'))

        else:

            context = {

                "len": False,
                "superuser": False,
                "factor": factor_objects_list

            }

        # get template
        factor_list_temp = loader.get_template("InstaPay/Factor_List_Product.html")

        return HttpResponse(factor_list_temp.render(context))

    elif requests.user.is_authenticated and requests.user.is_superuser:

        # return factor list
        # get factor list

        factor_objects_list = models.Factor.objects.all().filter(bloger__page_name=requests.user.username).filter(
            factor_statement_payment_to_bloger=payment_state)

        if len(factor_objects_list) > 0:

            context = {

                "len": True,
                "superuser": True,
                "factor": factor_objects_list

            }

        else:

            context = {

                "len": False,
                "superuser": True,
                "factor": factor_objects_list

            }

        # get template
        factor_list_temp = loader.get_template("InstaPay/Factor_List_Product.html")

        return HttpResponse(factor_list_temp.render(context))

    else:

        # redirect to main page
        return HttpResponseRedirect(reverse('main'))


def change_ordering(requests, factor_id):

    """
    change factor ordering statement
    """

    if requests.user.is_authenticated and requests.user.is_superuser:

        # get factor list
        factor_objects_list_id = models.Factor.objects.all().filter(factor_id=int(factor_id))

        if len(factor_objects_list_id) > 0:

            # get factor
            fact = factor_objects_list_id[0]

            month_dict = {

                "Jan": 1,
                "Feb": 2,
                "Mar": 3,
                "Apr": 4,
                "May": 5,
                "Jun": 6,
                "Jul": 7,
                "Aug": 8,
                "Sep": 9,
                "Nov": 10,
                "Dec": 11,
                "Oct": 12,

            }

            if not fact.factor_statement_ordering_factor:

                change_time = time.ctime(time.time()).split(" ")

                fact.delivery_year = int(change_time[-1])
                fact.delivery_month = month_dict[change_time[1]]
                fact.delivery_day = int(change_time[2])
                fact.delivery_hours = int(change_time[3].split(':')[0])
                fact.delivery_minutes = int(change_time[3].split(':')[1])

            # change factor ordering statement
            fact.factor_statement_ordering_factor = not fact.factor_statement_ordering_factor

            fact.save()

        return HttpResponseRedirect(reverse('main'))

    elif requests.user.is_authenticated and not requests.user.is_superuser:

        # get factor list
        factor_objects_list_id = models.Factor.objects.all().filter(factor_id=int(factor_id)).filter(
            bloger__page_name=requests.user.username)

        if len(factor_objects_list_id) > 0:

            # get factor
            fact = factor_objects_list_id[0]

            month_dict = {

                "Jan": 1,
                "Feb": 2,
                "Mar": 3,
                "Apr": 4,
                "May": 5,
                "Jun": 6,
                "Jul": 7,
                "Aug": 8,
                "Sep": 9,
                "Nov": 10,
                "Dec": 11,
                "Oct": 12,

            }

            if not fact.factor_statement_ordering_factor:
                change_time = time.ctime(time.time()).split(" ")

                fact.delivery_year = int(change_time[-1])
                fact.delivery_month = month_dict[change_time[1]]
                fact.delivery_day = int(change_time[2])
                fact.delivery_hours = int(change_time[3].split(':')[0])
                fact.delivery_minutes = int(change_time[3].split(':')[1])

            # change factor ordering statement
            fact.factor_statement_ordering_factor = not fact.factor_statement_ordering_factor

            fact.save()

        return HttpResponseRedirect(reverse('main'))

    else:

        return HttpResponseRedirect(reverse('main'))


def change_payment(requests, factor_id):
    """
    change factor ordering statement
    """

    if requests.user.is_authenticated and requests.user.is_superuser:

        # get factor list
        factor_objects_list_id = models.Factor.objects.all().filter(factor_id=int(factor_id))

        if len(factor_objects_list_id) > 0:

            # get factor
            fact = factor_objects_list_id[0]

            month_dict = {

                "Jan": 1,
                "Feb": 2,
                "Mar": 3,
                "Apr": 4,
                "May": 5,
                "Jun": 6,
                "Jul": 7,
                "Aug": 8,
                "Sep": 9,
                "Nov": 10,
                "Dec": 11,
                "Oct": 12,

            }

            change_time = time.ctime(time.time()).split(" ")

            fact.bloger_payment_year = int(change_time[-1])
            fact.bloger_payment_month = month_dict[change_time[1]]
            fact.bloger_payment_day = int(change_time[2])
            fact.bloger_payment_hours = int(change_time[3].split(':')[0])
            fact.bloger_payment_minutes = int(change_time[3].split(':')[1])

            # change factor ordering statement
            fact.factor_statement_payment_to_bloger = not fact.factor_statement_payment_to_bloger

            fact.save()

        return HttpResponseRedirect(reverse('main'))

    elif requests.user.is_authenticated and not requests.user.is_superuser:

        # get factor list
        factor_objects_list_id = models.Factor.objects.all().filter(factor_id=int(factor_id)).filter(
            bloger__page_name=requests.user.username)

        if len(factor_objects_list_id) > 0:

            # get factor
            fact = factor_objects_list_id[0]

            month_dict = {

                "Jan": 1,
                "Feb": 2,
                "Mar": 3,
                "Apr": 4,
                "May": 5,
                "Jun": 6,
                "Jul": 7,
                "Aug": 8,
                "Sep": 9,
                "Nov": 10,
                "Dec": 11,
                "Oct": 12,

            }

            change_time = time.ctime(time.time()).split(" ")

            fact.bloger_payment_year = int(change_time[-1])
            fact.bloger_payment_month = month_dict[change_time[1]]
            fact.bloger_payment_day = int(change_time[2])
            fact.bloger_payment_hours = int(change_time[3].split(':')[0])
            fact.bloger_payment_minutes = int(change_time[3].split(':')[1])

            # change factor ordering statement
            fact.factor_statement_payment_to_bloger = not fact.factor_statement_payment_to_bloger

            fact.save()

        return HttpResponseRedirect(reverse('main'))

    else:

        return HttpResponseRedirect(reverse('main'))


def product_buy(requests, product_hashcode):

    """
    show product information redirect to buy product
    """

    # get product objects
    product_objects_list = models.Product.objects.all().filter(product_hashcode=product_hashcode)

    if len(product_hashcode) > 0:

        current_time = time.time()
        off_time = product_objects_list[0].off_code_deadline

        if off_time - current_time > 0:

            off_code_state = True
            price = product_objects_list[0].price * (1 - (product_objects_list[0].off_code / 100))

        else:

            off_code_state = False
            price = product_objects_list[0].price

        if product_objects_list[0].number >= 1 and product_objects_list[0].purchase_state:

            # product exist and we must return product's information
            context = {

                "prod": product_objects_list[0],
                "len": True,
                "product_len": True,
                "off_code_state": off_code_state,
                "off_price": price

            }

        else:

            # we don't have product
            context = {

                "prod": product_objects_list[0],
                "len": True,
                "product_len": False,
                "off_code_state": off_code_state,
                "off_price": price

            }

        # get product template
        product_temp = loader.get_template('InstaPay/Product.html')

        return HttpResponse(product_temp.render(context))

    else:

        # there is no product
        context = {

            "len": False

        }

        product_temp = loader.get_template('InstaPay/Product.html')

        return HttpResponse(product_temp.render(context))

@csrf_exempt
def create_factor(requests, product_hashcode):

    """
    create factor and create bank gateway token for buy
    """

    print(requests.POST.dict())

    # superuser can't buy product
    if requests.user.is_authenticated and requests.user.is_superuser:

        # return to main page
        return HttpResponseRedirect(reverse('main'))

    else:

        # get post data

        product_hashcode = requests.POST['product_hashcode']
        price = int(float(requests.POST['price']))
        name = requests.POST['name']
        lastname = requests.POST['lastname']
        phone_number = requests.POST['phone_number']
        postal_code = requests.POST['postal_code']
        bank = requests.POST['bank']
        address = requests.POST['address']
        number_of_product = int(requests.POST['number_of_product'])

        try:
            email_field = requests.POST['email']
        except:
            email_field = None

        # get product object
        product_obj = models.Product.objects.all().filter(product_hashcode=product_hashcode)[0]

        if int(product_obj.number) - int(number_of_product) < 0:

            # you cant buy anything
            # redirect to product_hashcode
            return HttpResponseRedirect(reverse('Product_Buy', args=[product_hashcode]))

        elif not product_obj.purchase_state:

            # you cant buy anything
            # redirect to product_hashcode
            return HttpResponseRedirect(reverse('Product_Buy', args=[product_hashcode]))

        else:

            # get bloger object
            bloger_obj = product_obj.bloger

            # get customer object
            customer_objects_list = models.Customer.objects.all().filter(phone_number=phone_number)

            if len(customer_objects_list) > 0:

                # get object
                customer_obj = customer_objects_list[0]

            else:

                # create object
                #print(str(phone_number))
                #customer_obj = product_obj.customer_set.create(phone_number=str(phone_number))

                customer_obj = models.Customer(phone_number=phone_number)

                customer_obj.name = name
                customer_obj.last_name = lastname
                customer_obj.customer_email = email_field
                customer_obj.address = address
                customer_obj.bloger = bloger_obj
                customer_obj.postal_code = postal_code

                # save object
                customer_obj.save()
                customer_obj.product.add(product_obj)

            # create factor objects
            factor_obj = models.Factor()
            factor_obj.price = int(float(price))
            factor_obj.number_of_product = int(number_of_product)
            factor_obj.bloger_payment_bank = bank

            factor_obj.bloger = bloger_obj
            factor_obj.product = product_obj
            factor_obj.customer = customer_obj

            # save factor
            factor_obj.save()

            # start create pending objects
            # split pending process to Sadad and Saman Bank
            if bank == 'saman':

                # we must start saman process

                # create pending object
                pending_obj = models.Pending()

                # set param
                pending_obj.amount = price * number_of_product
                pending_obj.cellNUM = str(phone_number)
                pending_obj.merchantID = Information.saman_terminalID
                pending_obj.bank = bank
                pending_obj.pendingID = factor_obj.factor_id
                pending_obj.redirect_url = Information.domain + str(product_hashcode) + "/Verify/saman/"

                # relation
                pending_obj.factor = factor_obj

                # save pending objects
                pending_obj.save()

                """
                SamanPending model
                """

                # create SamanPending objects
                saman_pending_obj = models.SamanPending()

                # set param
                saman_pending_obj.terminalID = Information.saman_terminalID
                saman_pending_obj.pendingID = factor_obj.factor_id
                saman_pending_obj.multiplex_shaba = bloger_obj.shaba

                # relation
                saman_pending_obj.pending = pending_obj

                # save object
                saman_pending_obj.save()

                # show factor to user and redirect to bank portal
                # get template
                factor_temp = loader.get_template('InstaPay/Factor.html')

                context = {

                    "factor": factor_obj,
                    'factor_time': time.ctime(factor_obj.create_time),
                    "final_price": number_of_product * price,
                    "customer": customer_obj,
                    "product": product_obj,
                    "pending": pending_obj,
                    "saman_pending": saman_pending_obj,
                    'saman_state': True,

                }

                return HttpResponse(factor_temp.render(context))

            elif bank == 'pasargad':

                # start pasargad portal process

                # create pending object
                pending_obj = models.Pending()

                # set param
                pending_obj.amount = price * number_of_product
                pending_obj.cellNUM = str(phone_number)
                pending_obj.merchantID = Information.pasargad_merchantCode
                pending_obj.bank = bank
                pending_obj.pendingID = factor_obj.factor_id
                pending_obj.redirect_url = Information.domain + str(product_hashcode) + "/Verify/pasargad/"

                # relation
                pending_obj.factor = factor_obj

                # save pending objects
                pending_obj.save()

                """
                pasargad pending model
                """

                # create pasargad models object
                pasargad_pending_obj = models.PasargadPending()

                # set param
                pasargad_pending_obj.pendingID = int(factor_obj.factor_id)
                pasargad_pending_obj.merchantCode = int(Information.pasargad_merchantCode)
                pasargad_pending_obj.terminalID = int(Information.pasargad_termianlID)
                pasargad_pending_obj.amount = number_of_product * price
                pasargad_pending_obj.redirectAddress = Information.domain + str(product_hashcode) + "/Verify/pasargad/"

                # create invoice date

                month_dict = {

                    "Jan": '01',
                    "Feb": '02',
                    "Mar": '03',
                    "Apr": '04',
                    "May": '05',
                    "Jun": '06',
                    "Jul": '07',
                    "Aug": '08',
                    "Sep": '09',
                    "Nov": '10',
                    "Dec": '11',
                    "Oct": '12',

                }

                cur_time = time.ctime(time.time()).split(' ')
                cur_year = cur_time[-1]
                cur_month = month_dict[cur_time[1]]
                cur_day = '0' + str(cur_time[2]) if len(cur_time[2]) < 2 else cur_time[2]
                cur_hour = cur_time[3]

                inv_date = '{0}/{1}/{2} {3}'.format(cur_year, cur_month, cur_day, cur_hour)

                # set inv date param
                pasargad_pending_obj.invoiceDate = inv_date

                # create time stamp
                cur_time = time.ctime(time.time()+5.0).split(' ')
                cur_year = cur_time[-1]
                cur_month = month_dict[cur_time[1]]
                cur_day = '0' + str(cur_time[2]) if len(cur_time[2]) < 2 else cur_time[2]
                cur_hour = cur_time[3]

                tm_stmp = '{0}/{1}/{2} {3}'.format(cur_year, cur_month, cur_day, cur_hour)

                # set time stamp param
                pasargad_pending_obj.timeStamp = tm_stmp

                # create sign data
                x = '#{0}#{1}#{2}#{3}#{4}#{5}#{6}#{7}#'.format(

                    str(Information.pasargad_merchantCode),
                    str(Information.pasargad_termianlID),
                    str(factor_obj.factor_id),
                    str(inv_date),
                    str(number_of_product * price),
                    Information.domain + str(product_hashcode) + "/Verify/pasargad/",
                    str(1003),
                    str(tm_stmp)

                )

                sign_data = sha1(x.encode())

                import os
                print(os.listdir('InstaPay'))
                # import private key
                with open('InstaPay/privateKey', 'r') as fd:
                    private_key = RSA.importKey(fd.read())

                signer = PKCS1_v1_5.new(private_key)

                # sign data with private key
                sign_data = signer.sign(sign_data)

                # convert to base64
                sign_data = base64.b64decode(sign_data)

                # set sign data param
                pasargad_pending_obj.signData = sign_data

                # save model
                pasargad_pending_obj.save()

                # show factor to user and redirect to bank portal
                # get template
                factor_temp = loader.get_template('InstaPay/Factor.html')

                context = {

                    "factor": factor_obj,
                    'factor_time': time.ctime(factor_obj.create_time),
                    "final_price": number_of_product * price,
                    "customer": customer_obj,
                    "product": product_obj,
                    "pending": pending_obj,
                    "pasargad_pending": pasargad_pending_obj,
                    'saman_state': False,

                }

                return HttpResponse(factor_temp.render(context))

            elif bank == 'zarinPal':

                # start ZarinPal portal process

                # create pending object
                pending_obj = models.Pending()

                # set param
                pending_obj.amount = price * number_of_product
                pending_obj.cellNUM = str(phone_number)
                pending_obj.merchantID = Information.zarinPal_merchantCode
                pending_obj.bank = bank
                pending_obj.pendingID = factor_obj.factor_id
                pending_obj.redirect_url = Information.domain + str(product_hashcode) + '/' + \
                                           str(factor_obj.factor_id) + "/Verify/zarinPal/"

                # relation
                pending_obj.factor = factor_obj

                # save pending objects
                pending_obj.save()

                """ start session """
                client = Client(Information.ZARINPAL_WEBSERVICE)

                # start first layer connection
                result = client.service.PaymentRequest(

                    Information.zarinPal_merchantCode,
                    number_of_product * price,
                    str(product_hashcode)+"@"+str(factor_obj.factor_id),
                    customer_obj.customer_email,
                    customer_obj.phone_number,
                    Information.domain + str(product_hashcode) + '/' + str(factor_obj.factor_id) + "/Verify/zarinPal/"

                )

                if result.Status == 100:

                    # create zarinPal pending
                    zarinpal_pending_obj = models.ZarinPalPending()

                    zarinpal_pending_obj.pendingID = factor_obj.factor_id
                    zarinpal_pending_obj.customer_email = customer_obj.customer_email
                    zarinpal_pending_obj.description = str(product_hashcode)+"@"+str(factor_obj.factor_id)
                    zarinpal_pending_obj.status = result.Status

                    # relation
                    zarinpal_pending_obj.pendingID = pending_obj

                    # save object
                    zarinpal_pending_obj.save()

                    return redirect('https://www.zarinpal.com/pg/StartPay/' + result.Authority)

                else:

                    # create zarinPal pending
                    zarinpal_pending_obj = models.ZarinPalPending()

                    zarinpal_pending_obj.pendingID = factor_obj.factor_id
                    zarinpal_pending_obj.customer_email = customer_obj.customer_email
                    zarinpal_pending_obj.description = str(product_hashcode)+"@"+str(factor_obj.factor_id)
                    zarinpal_pending_obj.status = result.Status

                    # relation
                    zarinpal_pending_obj.pendingID = pending_obj

                    # save object
                    zarinpal_pending_obj.save()

                    # redirect to product_hashcode
                    return HttpResponseRedirect(reverse('Product_Buy'))

@csrf_exempt
def bank_url(requests):

    """
    waiting for bank portal
    """

    # load template
    bank_temp = loader.get_template('InstaPay/Bank.html')

    # get bank type
    bank = requests.POST['bank']

    if bank == 'saman':

        context = {

            'bank': bank,
            'amount': requests.POST['Amount'],
            'terminalID': requests.POST['TerminalID'],
            'resNum': requests.POST['ResNum'],
            'redirectUrl': requests.POST['RedirectUrl'],
            'cellNum': requests.POST['CellNumber']

        }

    else:

        context = {

            'bank': bank,
            'amount': requests.POST['amount'],
            'terminalID': requests.POST['terminalCode'],
            'resNum': requests.POST['invoiceNumber'],
            'redirectUrl': requests.POST['redirectAddress'],
            'merchantCode': requests.POST['merchantCode'],
            'invoiceDate': requests.POST['invoiceDate'],
            'action': requests.POST['action'],
            'timeStamp': requests.POST['timeStamp'],
            'sign': requests.POST['sign'],

        }

    return HttpResponse(bank_temp.render(context))


def verify_factor_pasargad(requests, product_hashcode):

    return HttpResponse("verify product" + str(product_hashcode))


def verify_factor_saman(requests, product_hashcode):
    return HttpResponse("verify product" + str(product_hashcode))


def verify_factor_zarinpal(requests):
    return HttpResponse('verify zarinpal')
