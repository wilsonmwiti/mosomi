import random
from django.core.management.base import BaseCommand

from school.models import *
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
    # sms_models = [
    #     UserTopUp, MpesaPayments, Contact, Group, Outgoing, Sale, SalesPerson, Customer, User
    # ]
    #
    # for model in sms_models:
    #     print("Deleted all {}".format(model))
    #     model.objects.all().delete()
    pass

def seed_subject_groups():
    data = ['Compulsory', 'Group 2', 'Group 3', 'Group 4', 'Group 5']

    for d in data:
        SubjectGroup.objects.create(
            name=d
        )


def seed_subjects():
    subject_groups = SubjectGroup.objects.all()

    for group in subject_groups:
        if group.name == 'Compulsory':
            data = ['English', 'Kiswahili', 'Mathematics']
            for d in data:
                Subject.objects.create(
                    name=d,
                    subject_group=group
                )
        elif group.name == 'Group 2':
            data = ['Biology', 'Physics', 'Chemistry']
            for d in data:
                Subject.objects.create(
                    name=d,
                    subject_group=group
                )
        elif group.name == 'Group 3':
            data = ['History and Government', 'Geography', 'Christian Religious Education',
                    'Islamic Religious Education', 'Hindu Religious Education']
            for d in data:
                Subject.objects.create(
                    name=d,
                    subject_group=group
                )
        elif group.name == 'Group 4':
            data = ['Home Science', 'Art and Design', 'Computer Studies', 'Aviation']
            for d in data:
                Subject.objects.create(
                    name=d,
                    subject_group=group
                )
        elif group.name == 'Group 5':
            data = ['French', 'German', 'Arabic', 'Music', 'Business Studies']
            for d in data:
                Subject.objects.create(
                    name=d,
                    subject_group=group
                )


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
    seed_subject_groups()
    seed_subjects()
    pass
