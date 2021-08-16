import random
from django.core.management.base import BaseCommand
from sms.forms import *
from sms.models import *
from sms.utils import SDP

# python manage.py seed --mode=fresh
# python manage.py seed


class Command(BaseCommand):
    help = "seed database for testing and development."

    def add_arguments(self, parser):
        parser.add_argument('--mode', type=str, help="Mode")

    def handle(self, *args, **options):
        self.stdout.write('seeding data...')
        run_seed(self, options['mode'])
        self.stdout.write('done.')


def clear_data():
    """Deletes all the table data"""
    print("Delete all data instances")
    sms_models = [
        UserTopUp, MpesaPayments, Contact, Group, Outgoing, Sale, SalesPerson, Customer, User
    ]

    for model in sms_models:
        print("Deleted all {}".format(model))
        model.objects.all().delete()


def create_admin_customer_account():
    customer_code = random.randint(10000, 99999)
    while Customer.objects.filter(customer_code=customer_code).count() > 0:
        customer_code = random.randint(10000, 99999)
    admin_password = 'Roberms.2019'
    customer_data = {
        'username': 'Admin',
        'phone_number': '254704976963',
        'password1': admin_password,
        'password2': admin_password,
    }
    form = CustomerRegisrationForm(customer_data)
    if form.is_valid():
        sdp = SDP()
        customer = form.save(commit=False)
        customer.customer_code = customer_code
        customer.is_active = True
        customer.is_staff = True
        customer.email = form.cleaned_data.get('username')
        customer.set_password(admin_password)
        customer.save()
        response = sdp.send_sms_customized(service_id='6015152000175328', recipients=[customer.phone_number],
                                           message=f'Admin Account Created, Username = {customer.username}'
                                           f'password{admin_password}',
                                           sender_code='711037')
        print(f"Admin created: username {'Admin'} password {admin_password}")
    else:
        print('Review Form Details')


def create_roberms_admin():
    manager = Manager.objects.create(
        username='Roberms',
        email='admin@roberms.co.ke',
        password='Roberms.2019',
    )
    print(f"Username {manager.username}, Password Roberms.2019")


def run_seed(self, mode):
    """ Seed database based on mode
    :param mode: refresh / clear
    :return:
    """
    mode_clear = "fresh"
    # Clear data from tables
    if mode == mode_clear:
        clear_data()

    # Creating NEW DATA
    create_admin_customer_account()
    create_roberms_admin()
    pass
