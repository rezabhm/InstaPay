import random
import time

from django.shortcuts import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.template import loader, Context
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout

from . import models
from . import form
import hashlib

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


def bloger_edit_information_form(requests, error_text="قادیر را بروز رسانی کنید"):

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

                "error": "بلاگری با این مشخصات وجود ندارد"

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
            return HttpResponseRedirect(reverse('bloger_edit_information_form', args=["نام بیج شما صحیح نمیباشد !!!"]))

        # Check Phone number
        if (len(str(phone_number)) != 11) or (str(phone_number)[:2] != "09"):

            # raised error because phone number format is false
            return HttpResponseRedirect(reverse("bloger_signup_form",args=[ "فرمت شماره موبایل نادرست است "]))

        # Check national code
        if len(str(national_code)) != 10:

            # raised error because of false format
            return HttpResponseRedirect(reverse(bloger_signup_form,args=[ "کد ملی را اشتباه وارد کرده اید"]))

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

            return HttpResponseRedirect(reverse("bloger_edit_information_form", args=[ "مقادیر با موفقیت تغییر یافت"]))

        else:

            # if password is incorrect
            return HttpResponseRedirect(reverse("bloger_edit_information_form", args=[ "رمز عبور اشتباه وارد شده است "]))

    else:

        # redirect to main page
        return HttpResponseRedirect(reverse('main'))


def bloger_login_form(requests, error_text="آدرس بیج و رمز عبور را وارد کنید"):

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
            return HttpResponseRedirect(reverse("bloger_login_form",args= ["رمز عبور یا نام بیج اشتباه است"]))

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


def bloger_forgot_password_form(requests, error_text="کدی که به شماره موبایل زیر ارسال شده را وارد کنید"):

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
                                                args=[ "چنین کاربری موجود نمی باشد . لظفا ثبت نام کنید"]))

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
            return HttpResponseRedirect(reverse("bloger_signup_form",args=[ "کاربری با  آدرس موجود نمیباشد لطفا ثبت نام کنید"]))

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
                                                args=["کاربری با  آدرس موجود نمیباشد لطفا ثبت نام کنید"]))

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
                error_text = "کد را دیر وارد کرده اید .کد دیگری ارسال شده است لطفا آن کد را وارد کنید"
                return HttpResponseRedirect(reverse("bloger_forgot_password_form", args=[error_text]))

            else:

                if bloger_code == code:

                    # code is correct and redirect to change_password view
                    password_hashcode = bloger_obj.bloger_password_hashcode
                    return HttpResponseRedirect(reverse("bloger_change_password_form",
                                                        args= [page_name, password_hashcode]))

                else:

                    # code is incorrect and must get it again
                    return HttpResponseRedirect(reverse("bloger_forgot_password_form",args=[ "کد را صحیح وارد کنید"]))


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
            return HttpResponseRedirect(reverse("bloger_login_form", args=[ "اطلاعات وارد شده نادرست است."]))


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

            return HttpResponseRedirect(reverse("bloger_login_form", args=[ "موفقیت رمز عبور را تغییر داده اید"]))


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
    print("start this")

    if requests.user.is_authenticated and not requests.user.is_superuser:
        print("start 1")

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
        print("start 2")

        # get product list
        prod_list = models.Product.objects.all()

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
        print("start 3")

        return HttpResponseRedirect(reverse('main'))


def edit_product_form(requests):

    """
    return html for edit product
    """

    if requests.user.is_authenticated and not requests.user.is_superuser:

        # load template
        edit_temp = loader.get_template("InstaPay/Edit_Product.html")

        # we add user's username to form
        context = {

            "hidden_state": True,
            "username": requests.user.username

        }

        return HttpResponse(edit_temp.render(context))

    elif requests.user.is_authenticated and requests.user.is_superuser:

        # load template
        edit_temp = loader.get_template("InstaPay/Edit_Product.html")

        # we add user's username to form
        context = {

            "hidden_state": False,

        }


def edit_product(requests, product_hashcode):
    pass


def delete_product(requests, product_hashcode):
    pass


def product_buy(requests, product_hashcode):
    pass
