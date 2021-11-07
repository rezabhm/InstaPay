from django.db import models
from uuid import uuid1
import time
import random

# Create your models here.

"""
models : 

    1. bloger model           ==> for create user and store user's information
    2. admin model          ==> admin information
    3. customer model       ==> customer information
    4. factor model         ==> for payment information
    5. product model        ==> for create product
    6. off code model       ==> for define disposable off code


models relation :

    1. bloger model:

                    - OneToMany with factor model
                    - OneToMany with product model
                    - OneToMany with off code model
                    - ManyToMany with customer model


    2. factor model:

                    - OneToMany with bloger model
                    - OneToMany with product model
                    - OneToMany with customer model
                    - OneToOne with off code model


    3. product model:

                    - OneToMany with bloger model
                    - OneToMany with factor model
                    - ManyToMany with customer model
                    - OneToMany with off code model


    4. customer model:

                    - OneToMany with bloger model
                    - OneToMany with factor model
                    - ManyToMany with product model
                    - OneToMany with off code model


    5. off code model:

                    - OneToMany with bloger model
                    - OneToOne with factor model
                    - OneToMany with product model
                    - OneToMany with customer model


"""


class Bloger(models.Model):
    """
    bloger's table's column name in database :

        1.  name
        2.  last name
        3.  instagram page's name
        4.  national code
        5.  address
        6.  phone number
        7.  email
        8.  bank account number
        9.  bank name
        10. bank account Shaba
        11. bloger's hashcode
        12. bloger's password hashcode

    bloger's relation :

        None

    """

    # bloger's name
    name = models.CharField(max_length=10)

    # bloger's last name
    last_name = models.CharField(max_length=10)

    # bloger's instagram page name
    page_name = models.CharField(max_length=25)

    # bloger's national code
    national_code = models.IntegerField()

    # bloger's address
    address = models.TextField()

    # bloger's phone number
    phone_number = models.CharField(max_length=12, help_text="09121234567")

    # bloger's email
    bloger_email = models.EmailField()

    # bloger's bank account number
    bank_account_number = models.CharField(max_length=30)

    # bloger's bank name
    bank_name = models.CharField(max_length=15)

    # bloger's shaba
    shaba = models.CharField(max_length=50)

    # bloger's hashcode
    bloger_hashcode = models.CharField(max_length=15, default=str(hash(page_name) % 10 ** 8))

    # bloger's password hashcode
    bloger_password_hashcode = models.CharField(max_length=128)

    # bloger's forgot password's code
    forgot_password_code = models.IntegerField(default=random.randint(100000, 999999))

    # bloger's forgot password's deadline
    forgot_password_code_deadline = models.FloatField(default=time.time()+300.0)

    # verify phone_number status
    verify_phone_number = models.BooleanField(default=False)

    def __str__(self):
        return str(self.page_name)

    def verify_param(self, param_name):

        """
        we have dict with verify_dict name .
        in this dict we have all of above attribute's value and return param_name value
        """

        verify_dict = {

            "name": self.name,
            "last_name": self.last_name,
            "page_name": self.page_name,
            "phone_number": self.phone_number,
            "address": self.address,
            "national_code": self.national_code,
            "bnak_account_number": self.bank_account_number,
            "bank_name": self.bank_name,
            "shaba": self.shaba,
            "email": self.bloger_email,
            "bloger_hashcode": self.bloger_hashcode,
            "password": self.bloger_password_hashcode,
            "forgot_password_code": self.forgot_password_code,
            "forgot_password_code_deadline": self.forgot_password_code_deadline

        }

        # return param_name's value
        try:
            return verify_dict[param_name]

        except:
            return False


class Product(models.Model):
    """
    product's table's column name in database :

        1.  product name
        2.  price
        3.  description
        4.  product image
        5.  number of product
        6.  purchase state
        7.  off code
        8.  off code deadline
        9.  field off product
        10. product's hashcode

    product's relation:

        1. foreign ==> bloger

    """

    # product name
    name = models.CharField(max_length=25)

    # product price
    price = models.IntegerField(help_text="تومان")

    # product description
    description = models.TextField()

    # product image
    # One To one relation with Image class.
    # relation code write in Image Class

    # number of product
    number = models.IntegerField()

    # purchase state if equal True it mean customer can buy it however it equal False Customer can't buy it
    purchase_state = models.BooleanField(default=True)

    # off code
    off_code = models.IntegerField(default=0)

    # off code deadline
    off_code_deadline = models.FloatField(default=time.time()+((3600.0 * 24.0 * 30.0) * time.time()))

    # category
    category = models.CharField(max_length=20)

    # product hashcode
    product_hashcode = models.CharField(max_length=128, default=str(hash(name) % 10 ** 8))

    # relation
    bloger = models.ForeignKey(Bloger, on_delete=models.CASCADE, default=None)

    # image
    image = models.ImageField(upload_to="InstaPay/Product_Image/", default=None)

    def __str__(self):
        return str(self.name)


class Customer(models.Model):
    """
    customer's table's column name in database :

        1. phone number
        2. address
        3. email
        4. postal code
        5. name
        6. last name

    customer relation :

        1. foreign ==> bloger
        2. Many    ==> product

    """

    # customer phone number
    phone_number = models.CharField(max_length=12, help_text="09121234567")

    # address
    address = models.TextField()

    # email
    customer_email = models.EmailField(null=True)

    # postal code
    postal_code = models.CharField(max_length=25)

    # name
    name = models.CharField(max_length=12)

    # last name
    last_name = models.CharField(max_length=12)

    # relation
    bloger = models.ForeignKey(Bloger, on_delete=models.CASCADE)
    product = models.ManyToManyField(Product, default=None)

    def __str__(self):
        return str(self.phone_number)


class OffCode(models.Model):
    """
    off code table's column name in database:

        1. off code id
        2. off number
        3. deadline time
        4. generating time
        5. using statement

    off code relation :

        1. foreign ==> bloger
        2. foreign ==> product
        3. foreign ==> customer

    """

    # off code id
    off_code_id = models.CharField(max_length=50, default=str(int(uuid1().int)))

    # off number
    off_number = models.IntegerField()

    # deadline
    deadline = models.FloatField(default=time.time() + (15 * 60.0))

    # generating time
    generating_time = models.FloatField(default=time.time())

    # using statement . if equal True this off code is useless however equal False code is useful
    using = models.BooleanField(default=False)

    # relation
    bloger = models.ForeignKey(Bloger, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.off_number)


class Factor(models.Model):
    """
    factor's table's column name in database:

        1.  factor id
        2.  year payment
        3.  month payment
        4.  day payment
        5.  hours payment
        6.  minutes payment
        7.  factor statement (ordering / factor)
        8.  factor statement (payment_factor / not_payment_factor)
        9.  price
        10. number of product
        11. delivery year
        12. delivery month
        13. delivery day
        14. delivery hours
        15. delivery minutes
        16. bloger payment year
        17. bloger payment month
        18. bloger payment day
        19. bloger payment hours
        20. bloger payment minutes
        21. bloger payment bank
        22. bloger payment serial

    factor's relation :

        1. foreign ==> bloger
        2. foreign ==> customer
        3. foreign ==> product
        4. one     ==> off code

    """

    # factor id
    factor_id = models.IntegerField(default=uuid1().int)

    # customer payment date time
    customer_payment_year = models.IntegerField()
    customer_payment_month = models.IntegerField()
    customer_payment_day = models.IntegerField()
    customer_payment_hours = models.IntegerField()
    customer_payment_minutes = models.IntegerField()

    # bloger deliver product (True) , not deliver (False)
    factor_statement_ordering_factor = models.BooleanField(default=False)

    # factor statement (payment_to_bloger = True / not_payment_to_bloger = False)
    factor_statement_payment_to_bloger = models.BooleanField(default=False)

    # factor price for one product
    price = models.IntegerField(help_text="تومان")

    # number of product that sold
    number_of_product = models.IntegerField(default=1)

    # payment date time
    delivery_year = models.IntegerField(null=True)
    delivery_month = models.IntegerField(null=True)
    delivery_day = models.IntegerField(null=True)
    delivery_hours = models.IntegerField(null=True)
    delivery_minutes = models.IntegerField(null=True)

    #  bloger payment date time
    bloger_payment_year = models.IntegerField(null=True)
    bloger_payment_month = models.IntegerField(null=True)
    bloger_payment_day = models.IntegerField(null=True)
    bloger_payment_hours = models.IntegerField(null=True)
    bloger_payment_minutes = models.IntegerField(null=True)

    # bloger payment bank
    bloger_payment_bank = models.CharField(max_length=15, null=True)

    # bloger payment serial
    bloger_payment_serial = models.CharField(max_length=50, null=True)

    # relation
    bloger = models.ForeignKey(Bloger, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    off_code = models.OneToOneField(OffCode, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return str(self.factor_id)


###########################################################
###########################################################
"""                  Additional class                   """
###########################################################
###########################################################
