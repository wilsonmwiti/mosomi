import math
from datetime import datetime

import requests
from django.contrib.auth import authenticate
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_200_OK, HTTP_400_BAD_REQUEST

from sms.models import Customer, OutgoingApi, From_Willinya, OutgoingApiNew, CustomerSubAccounts, OutgoingNew, Tag, \
    Inbox
from sms.utils import calculate_message_cost
from sms_api.models import DeliveryUrl
from sms_api.serializers import OutgoingSerializer
import logging

logging.basicConfig(filename="test.log", level=logging.DEBUG)


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def get_access_token(request):
    username = request.data.get("consumer_key")
    password = request.data.get("consumer_password")
    if username is None or password is None:
        return Response({'error': 'Please provide both consumer key and consumer password'}, status=HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)

    if not user:
        context = {
            'error': 'Invalid Credentials',
        }
        return Response(context, status=HTTP_404_NOT_FOUND)
    token, _ = Token.objects.get_or_create(user=user)

    context = {
        'token': token.key,
    }
    return Response(context, status=HTTP_200_OK)


@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def simple_sms(request):
    if request.data.get('message') and request.data.get('phone_number') and request.data.get('sender_name') \
            and request.data.get('unique_identifier'):
        message = request.data.get('message')
        phone_number = request.data.get('phone_number')
        sender_name = request.data.get('sender_name')
        # access_code = request.data.get('access_code')
        unique_identifier = request.data.get('unique_identifier')

        token = Token.objects.get(key=request.META.get('HTTP_AUTHORIZATION').split()[1])
        customer = Customer.objects.filter(user_ptr_id=token.user_id).first()

        if customer is not None:
            if customer.access_code != request.data.get('sender_name'):
                context = {
                    "response": "Error",
                    "response_message": "You do not own this sender name"
                }
                return Response(context, status=HTTP_200_OK)
            customer_code = f"{datetime.today().date()}{customer.id}"
            message_cost = calculate_message_cost(message)
            actual_phone_number = f"{254}{phone_number[-9:]}"
            if customer.credit >= message_cost:
                result = OutgoingNew.objects.create(
                    phone_number=actual_phone_number,
                    text_message=message,
                    access_code=sender_name,
                    customer_id=customer.id,
                    track_code=customer_code.replace('-', ''),
                    request_identifier=unique_identifier,
                    sent_time=datetime.today())
                remaining_credit = customer.credit - message_cost
                customer.credit = remaining_credit
                customer.save()
                s = OutgoingSerializer(result, many=False)
                context = {
                    'response': 'Success, your message has been queued for sending',
                    'text_message': s.data,
                    'credit_balance': remaining_credit
                }
                return Response(context, status=HTTP_200_OK)
            else:
                if customer.credit != -1:
                    customer.credit = -1
                    customer.save()
                    OutgoingNew.objects.create(
                        phone_number=customer.phone_number,
                        text_message=f'Dear {customer.email}, you have depleted your available credit. '
                                     f'Kindly top-up to continue using our bulk sms service',
                        access_code=customer.access_code,
                        customer_id=customer.id,
                        track_code=customer_code.replace('-', ''),
                        request_identifier=unique_identifier)
                    context = {
                        'error': 'error, insufficient credit balance'
                    }
                    return Response(context, status=HTTP_200_OK)
                else:    
                    context = {
                        'error': 'error, insufficient credit balance'
                    }
                    return Response(context, status=HTTP_200_OK)
        else:
            customer = CustomerSubAccounts.objects.filter(user_ptr_id=token.user_id).first().owner
            if customer.access_code != request.data.get('sender_name'):
                context = {
                    "response": "Error",
                    "response_message": "You do not own this sender name"
                }
                return Response(context, status=HTTP_200_OK)
            customer_code = f"{datetime.today().date()}{customer.id}"
            message_cost = calculate_message_cost(message)
            actual_phone_number = f"{254}{phone_number[-9:]}"
            if customer.credit >= message_cost:
                result = OutgoingNew.objects.create(
                    phone_number=actual_phone_number,
                    text_message=message,
                    access_code=customer.access_code,
                    customer_id=customer.id,
                    track_code=customer_code.replace('-', ''),
                    request_identifier=unique_identifier)
                remaining_credit = customer.credit - message_cost
                customer.credit = remaining_credit
                customer.save()
                s = OutgoingSerializer(result, many=False)
                context = {
                    'response': 'Success, your message has been queued for sending',
                    'text_message': s.data,
                    'credit_balance': remaining_credit
                }
                return Response(context, status=HTTP_200_OK)
            else:
                if customer.credit != -1:
                    customer.credit = -1
                    customer.save()
                    OutgoingNew.objects.create(
                        phone_number=customer.phone_number,
                        text_message=f'Dear {customer.email}, you have depleted your available credit. '
                                     f'Kindly top-up to continue using our bulk sms service',
                        access_code=customer.access_code,
                        customer_id=customer.id,
                        track_code=customer_code.replace('-', ''),
                        request_identifier=unique_identifier)
                    context = {
                        'error': 'error, insufficient credit balance'
                    }
                    return Response(context, status=HTTP_200_OK)
    else:
        context = {
            'error': 'error, ensure you have fields phone number, message, sender_name and a unique identifier in your request body'
        }
        return Response(context, status=HTTP_200_OK)


@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def bulk_sms(request):
    if request.data.get('message') and request.data.get('phone_numbers') and \
            request.data.get('sender_name') and request.data.get('unique_identifier'):

        message = request.data.get('message')
        phone_numbers = request.data.getlist('phone_numbers')
        sender_name = request.data.get('sender_name')
        unique_identifier = request.data.get('unique_identifier')

        if len(message) <= 15:
            token = Token.objects.get(key=request.META.get('HTTP_AUTHORIZATION').split()[1])
            customer = Customer.objects.filter(user_ptr_id=token.user_id).first()
            if customer is not None:
                customer_code = f"{datetime.today().date()}{customer.id}"
                message_cost = calculate_message_cost(message) * len(phone_numbers)
                if customer.credit >= message_cost:
                    remaining_credit = customer.credit - message_cost
                    customer.credit = remaining_credit
                    customer.save()
                    outgoings = []
                    for phone_number in phone_numbers:
                        actual_phone_number = f"{254}{phone_number[-9:]}"
                        outgoings.append(OutgoingNew(
                            phone_number=actual_phone_number,
                            text_message=message,
                            access_code=sender_name,
                            customer_id=customer.id,
                            track_code=customer_code.replace('-', ''),
                            request_identifier=unique_identifier
                        ))
                        if len(outgoings) > 1000:
                            OutgoingNew.objects.bulk_create(outgoings)
                            outgoings.clear()
                    OutgoingNew.objects.bulk_create(outgoings)
                    outgoings.clear()
                    context = {
                        'response': 'Success, your messages have been queued for sending',
                        'unique_identifier': customer_code
                    }
                    return Response(context, status=HTTP_200_OK)
                else:
                    context = {
                        'error': 'error, insufficient credit balance'
                    }
                    return Response(context, status=HTTP_200_OK)
            else:
                customer = CustomerSubAccounts.objects.filter(user_ptr_id=token.user_id).first().owner
                customer_code = f"{datetime.today().date()}{customer.id}"
                message_cost = calculate_message_cost(message) * len(phone_numbers)
                if customer.credit >= message_cost:
                    remaining_credit = customer.credit - message_cost
                    customer.credit = remaining_credit
                    customer.save()

                    outgoings = []
                    for phone_number in phone_numbers:
                        actual_phone_number = f"{254}{phone_number[-9:]}"
                        outgoings.append(OutgoingNew(
                            phone_number=actual_phone_number,
                            text_message=message,
                            access_code=sender_name,
                            customer_id=customer.id,
                            track_code=customer_code.replace('-', ''),
                            request_identifier=unique_identifier
                        ))
                        if len(outgoings) > 1000:
                            OutgoingNew.objects.bulk_create(outgoings)
                            outgoings.clear()
                    OutgoingNew.objects.bulk_create(outgoings)
                    outgoings.clear()
                    context = {
                        'response': 'Success, your messages have been queued for sending',
                        'unique_identifier': customer_code
                    }
                    return Response(context, status=HTTP_200_OK)
                else:
                    context = {
                        'error': 'error, insufficient credit balance'
                    }
                    return Response(context, status=HTTP_200_OK)
        else:
            context = {
                'error': 'your request has exceeded the phone number field max limit of 15 phone numbers per request'
            }
            return Response(context, status=HTTP_200_OK)
    else:
        context = {
            'error': 'error, ensure you have fields phone numbers, message, sender_name and a unique identifier in your request body'
        }
        return Response(context, status=HTTP_200_OK)


@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def register_urls(request):
    token = Token.objects.get(key=request.META.get('HTTP_AUTHORIZATION').split()[1])
    customer = Customer.objects.filter(user_ptr_id=token.user_id).first()
    if customer is not None:
        if request.data.get('delivery_url'):
            delivery_url, created = DeliveryUrl.objects.update_or_create(
                customer_id=customer.id, defaults={'delivery_url': request.data.get('delivery_url')}
            )
            context = {
                'response': 'Success, Delivery Url Registration Successful',
                'url': delivery_url.delivery_url
            }
            return Response(context, status=HTTP_200_OK)
        else:
            context = {
                'error': 'Ensure You Have A Delivery Url Field In Your Request Body'
            }
            return Response(context, status=HTTP_200_OK)
    else:
        customer = CustomerSubAccounts.objects.filter(user_ptr_id=token.user_id).first().owner
        if request.data.get('delivery_url'):
            # if not DeliveryUrl.objects.filter(customer_id=customer.id).count() > 0:
            delivery_url, created = DeliveryUrl.objects.update_or_create(
                customer_id=customer.id, defaults={'delivery_url': request.data.get('delivery_url')}
            )
            context = {
                'response': 'Success, Delivery Url Registration Successful',
                'url': delivery_url.delivery_url
            }
            return Response(context, status=HTTP_200_OK)
        else:
            context = {
                'error': 'Ensure You Have A Delivery Url Field In Your Request Body'
            }
            return Response(context, status=HTTP_200_OK)


@api_view(["POST"])
@permission_classes((IsAuthenticated,))
@csrf_exempt
def receive_message_count(request):
    message_cost = request.data.get('message_cost')
    track_code = request.data.get('track_code')

    message = From_Willinya(
        message_cost=message_cost,
        track_code=track_code
    )
    if message.save():
        context = {
            "message": "success",
            "details": "received"
        }
        return Response(context, status=HTTP_200_OK)
    else:
        context = {
            "message": "error",
        }
        return Response(context, status=HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes((AllowAny,))
def get_credit_balance(request):
    if request.META.get('HTTP_AUTHORIZATION') is not None:
        token = Token.objects.get(key=request.META.get('HTTP_AUTHORIZATION').split()[1])
        customer = Customer.objects.filter(user_ptr_id=token.user_id).first()

        if customer is not None:
            context = {
                'response': 'Success',
                'credit_balance': customer.credit
            }
            return Response(context, status=HTTP_200_OK)
        else:
            customer = CustomerSubAccounts.objects.filter(user_ptr_id=token.user_id).first().owner
            context = {
                'response': 'Success, Delivery Url Registration Successful',
                'credit_balance': customer.credit

            }
            return Response(context, status=HTTP_200_OK)
    else:
        context = {
            'authentication': 'Authentication required',
        }
        return Response(context, status=HTTP_200_OK)


@api_view(["GET"])
@permission_classes((AllowAny,))
@csrf_exempt
def generate_credit_sample_request(request):
    url = "http://roberms.co.ke/sms/v1/credit/balance"
    headers = {
        "Authorization": "Token 77488299e17f9b33520f1183e37841f1abd4bce5"
    }
    response = requests.get(url=url, headers=headers)
    print(response.text)
    return Response(response.text, status=HTTP_200_OK)


@api_view(["GET"])
@permission_classes((AllowAny,))
@csrf_exempt
def generate_sample_request(request):
    url = "http://roberms.co.ke/sms/v1/roberms/send/simple/sms"
    body = {
        "message": "Simple Message",
        "phone_numbers": "0111979693",
        "sender_name": "ROBERMS_LTD",
        # "access_code": "123456",
        "unique_identifier": "unique_identifier"
    }
    headers = {
        "Authorization": "Token 77488299e17f9b33520f1183e37841f1abd4bce5"
    }
    response = requests.post(url=url, json=body, headers=headers)
    print(response.text)
    return Response(response.text, status=HTTP_200_OK)


def send_reply_to_bidco(request):
    tags = Tag.objects.filter(customer_id=105)
    url = ''
    headers = ''
    messages = {}
    for tag in tags:
        inbox_messages = Inbox.objects.filter(tag_id=tag.id, pushed=False)
        tag_messages = []
        for m in inbox_messages:
            single_message = {
                'tag': tag.hashtag,
                'phone_number': m.phone_number,
                'message': m.message,
            }
            tag_messages.append(single_message)
            m.pushed = True
            m.save()
        messages[tag.hashtag] = tag_messages
        tag_messages.clear()
    requests.post(url=url, headers=headers, data=messages)


@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def willinya_simple_sms(request):
    if request.data.get('message') and request.data.get('phone_number') and request.data.get('sender_name') \
            and request.data.get('unique_identifier'):
        message = request.data.get('message')
        phone_number = request.data.get('phone_number')
        sender_name = request.data.get('sender_name')
        # access_code = request.data.get('access_code')
        unique_identifier = request.data.get('unique_identifier')

        token = Token.objects.get(key=request.META.get('HTTP_AUTHORIZATION').split()[1])
        customer = Customer.objects.filter(user_ptr_id=token.user_id).first()

        if customer is not None:
            customer_code = f"{datetime.today().date()}{customer.id}"
            message_cost = calculate_message_cost(message)
            actual_phone_number = f"{254}{phone_number[-9:]}"
            if customer.credit >= message_cost:
                result = OutgoingNew.objects.create(
                    phone_number=actual_phone_number,
                    text_message=message,
                    access_code=sender_name,
                    customer_id=customer.id,
                    track_code=customer_code.replace('-', ''),
                    request_identifier=unique_identifier,
                    sent_time=datetime.today())
                remaining_credit = customer.credit - message_cost
                customer.credit = remaining_credit
                customer.save()
                s = OutgoingSerializer(result, many=False)
                context = {
                    'response': 'Success, your message has been queued for sending',
                    'text_message': s.data,
                    'credit_balance': remaining_credit
                }
                return Response(context, status=HTTP_200_OK)
            else:
                if customer.credit != -1:
                    customer.credit = -1
                    customer.save()
                    OutgoingNew.objects.create(
                        phone_number=customer.phone_number,
                        text_message=f'Dear {customer.email}, you have depleted your available credit. '
                                     f'Kindly top-up to continue using our bulk sms service',
                        access_code=customer.access_code,
                        customer_id=customer.id,
                        track_code=customer_code.replace('-', ''),
                        request_identifier=unique_identifier)
                    context = {
                        'error': 'error, insufficient credit balance'
                    }
                    return Response(context, status=HTTP_200_OK)
                else:
                    context = {
                        'error': 'error, insufficient credit balance'
                    }
                    return Response(context, status=HTTP_200_OK)
    else:
        context = {
            'error': 'error, ensure you have fields phone number, message, sender_name and a unique identifier in your request body'
        }
        return Response(context, status=HTTP_200_OK)


def send_usage(c):
    import requests
    url = "https://sms.procom.co.ke/sms/v1/company/credit/usage"
    company_id = 1

    body = {
        'company_id': company_id,
        'credits': c
    }
    response = requests.post(url=url, data=body)
    logging.info(" "+response.text)