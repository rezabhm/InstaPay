from django.contrib import admin
from django.urls import re_path

from . import views

# create your urls here.

"""

user urls :

    1. create user url
    2. verify user url
    3. verify information ( email , page name , password , ... ) url
    4. edit user information url
    5. send forgot password code url
    6. verify forgot password sent code url
    7. change password url

factor urls :

    1.  create factor url                                                            # customer
    2.  return list of user's factor url                                             # user
    3.  return list of user's factor order by date url                               # user
    4.  return list of all of factor url                                             # admin
    5.  return list of all of factor order by date url                               # admin
    6.  return list of all of factor order by user url                               # admin
    7.  return list of user's ordering url                                           # user
    8.  return list of user's ordering order by date url                             # user
    8.  return list all of ordering url                                              # admin
    9.  return list all of ordering order by date url                                # admin
    10. return list all of ordering order by user url                                # admin
    11. return list of user's payment-factor url                                     # user
    12. return list all of payment-factor url                                        # admin
    13. return list all of payment-factor order by date url                          # admin
    14. return list all of payment-factor order by user url                          # admin
    15. return excel for that include all of factor that we must pay to user url     # admin
        and convert payment-factor to not-payment-factor
    16. return list all of not-payment-factor url                                    # admin
    17. return list not-payment-factor order by user url                             # admin
    18. return list not-payment-factor order by date url                             # admin
    19. convert not-payment-factor to payment-factor url                             # admin
    20. return all of request's factor excel url                                     # admin
    21. get customer information url                                                 # customer
    22. return all of customer factor                                                # customer

NOTE : factor is factor that user has send product to customer
NOTE : ordering is factor that didn't send to customer
NOTE : payment-factor is factor that we must pay money to user
NOTE : Not-Payment-factor is factor that we had pay money to user

product urls :

    1.  create product url                                                           # user
    2.  edit product url                                                             # user
    3.  delete product url                                                           # user
    4.  create product url                                                           # admin
    5.  edit product url                                                             # admin
    6.  delete product url                                                           # admin
    7.  return list all of user's product url                                        # user
    8.  return list all of product url                                               # admin
    9.  return list all of product order by user url                                 # admin
    10. return list of product factor url                                            # user
    11. return list of product factor order by date url                              # user
    12. return list of product ordering url                                          # user
    13. return list of product ordering order by date url                            # user
    14. return list of product payment-factor url                                    # user
    15. return list of product payment-factor order by date url                      # user
    16. return list of product not-payment-factor url                                # user
    17. return list of product not-payment-factor order by date url                  # user
    18. return list of product factor url                                            # admin
    19. return list of product factor order by date url                              # admin
    20. return list of product ordering url                                          # admin
    21. return list of product ordering order by date url                            # admin
    22. return list of product payment-factor url                                    # admin
    23. return list of product payment-factor order by date url                      # admin
    24. return list of product not-payment-factor url                                # admin
    25. return list of product not-payment-factor order by date url                  # admin



    4. generate off code url
    5. get list of unused off code url
    6. get list of used off code url
    7. get all of off code url
    8. 




"""

My_app = 'InstaPay'

urlpatterns = [

    # Bloger Urls

    re_path(r'^bloger/SignUp/$', views.bloger_signup, name="Bloger_SignUp"),
    re_path(r'^bloger/SignUp/Form/$', views.bloger_signup_form, name="Bloger_SignUp_Form"),
    re_path(r'^bloger/verify/information/$', views.bloger_verify_information, name="Bloger_Verify_Information"),
    re_path(r'^bloger/edit/information/$', views.bloger_edit_information, name="Bloger_Edit_Information"),
    re_path(r'^bloger/edit/information/Form/$', views.bloger_edit_information_form, name="Bloger_Edit_Information_Form"),
    re_path(r'^bloger/login/Form/$', views.bloger_login_form, name="Bloger_LogIn_Form"),
    re_path(r'^bloger/login/$', views.bloger_login, name="Bloger_LogIn"),
    re_path(r'^bloger/logout/$', views.bloger_logout, name="Bloger_LogOut"),
    re_path(r'^bloger/forgot/password/Form/$', views.bloger_forgot_password_form, name="Bloger_Forgot_PassWord_Form"),
    re_path(r'^bloger/forgot/password/verify/$', views.bloger_forgot_password_verify,
            name="Bloger_Forgot_PassWord_Verify"),
    re_path(r'^bloger/change/password/$', views.bloger_change_password, name="Bloger_Change_PassWord"),

]
