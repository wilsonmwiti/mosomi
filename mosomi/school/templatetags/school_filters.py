import urllib
from random import randrange

from django import template
import json

from invoices.models import Service, Invoice
from school.models import *
from sms.models import *
from sms.utils import calculate_message_cost

register = template.Library()


@register.filter(name='return_item')
def return_item_at_index(list,index):
    return list[index]

#
@register.filter(name='get_fee_balance')
def get_fee_balance(args, student_id,):
    if args is None:
        return False
    else:
        print(args)
        arg_list = [arg.strip() for arg in args.split(',')]
        print(arg_list, student_id)
        student_fee = StudentFee.objects.filter(student_id=student_id, term_id=arg_list[0], form_id=arg_list[1])
        student_term = StudentTerm.objects.filter(student_id=student_id, is_current=True).first()
        if student_term:
            paid = 0
            for fee in student_fee:
                paid += fee.amount_paid
            return student_term.term.fee - paid
        else:
            paid = 0
            for fee in student_fee:
                paid += fee.amount_paid
            return 20000 - paid


@register.filter(name='get_list')
def get_list(student_id, class_id):
    return f"{student_id},{class_id}"


@register.filter(name='term_id')
def term_id(student_id):
    student_term = StudentTerm.objects.filter(student_id=student_id, is_current=True).first()
    if student_term:
        return student_term.term.id
    else:
        return 1


@register.filter(name='class_streams')
def class_streams(form_id):
    return Stream.objects.filter(form_id=form_id).count()


@register.filter(name='stream_students')
def stream_students(stream_id):
    students = StudentStream.objects.filter(stream_id=stream_id)
    return len(list(set(students)))


@register.filter(name='grade')
def per_subject_grading(score):
    print('score', score)
    score = float(score)
    grade = ''
    points = 0
    if 80 <= score <= 100:
        grade = 'A'
        points = 12
    elif 75 <= score <= 79.99:
        grade = 'A-'
        points = 11
    elif 70 <= score <= 74.99:
        grade = 'B+'
        points = 10
    elif 65 <= score <= 69.99:
        grade = 'B'
        points = 9
    elif 60 <= score <= 64.99:
        grade = 'B-'
        points = 8
    elif 55 <= score <= 59.99:
        grade = 'C+'
        points = 7
    elif 50 <= score <= 54.99:
        grade = 'C'
        points = 6
    elif 45 <= score <= 49.99:
        grade = 'C-'
        points = 5
    elif 40 <= score <= 44.99:
        grade = 'D+'
        points = 4
    elif 35 <= score <= 39.99:
        grade = 'D'
        points = 3
    elif 30 <= score <= 34.99:
        grade = 'D-'
        points = 2
    elif 0 <= score <= 29.99:
        grade = 'E'
        points = 1

    # grading = {}
    grading = grade
    # grading['points'] = points
    return grading


@register.filter(name='fee')
def term_year_fee(term_year_id):
    fee = Fee.objects.filter(term_year=term_year_id).first()
    if fee is not None:
        return fee.fee


@register.filter(name='term_year_id')
def term_year(term_id, year):
    term_year_id = TermYear.objects.filter(term_id=term_id, date__year=year).first().id
    return term_year_id