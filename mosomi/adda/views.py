import random

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

from adda.forms import RegisrationForm, ChallengeForm, IdeaForm, CommentForm
from adda.models import *
from sms.models import Customer, OutgoingNew


def register(request):
    if request.method == "POST":
        customer_code = random.randint(10000, 99999)

        while Customer.objects.filter(customer_code=customer_code).count() > 0:
            customer_code = random.randint(10000, 99999)
        form = RegisrationForm(request.POST)

        if form.is_valid():
            if AddaUser.objects.filter(username=request.POST['email']).count() < 1:
                adda_user = form.save(commit=False)
                adda_user.first_name = request.POST['username']
                adda_user.username = request.POST['email']
                adda_user.verification_code = customer_code
                adda_user.is_active = False
                adda_user.save()

                phone_number = f"{254}{adda_user.phone_number.replace(' ', '')[-9:]}"
                OutgoingNew.objects.create(
                    phone_number=phone_number,
                    text_message="Your account has been created! We sent you a text message containing a verification code" + f"Verfication Code {adda_user.verification_code}",
                    service_id=6015152000175328,
                    access_code='ROBERMS_LTD',
                    customer_id=1,
                    track_code=customer_code)
                messages.success(request, 'Your account has been created! We sent you a text message containing a verification code')
                return redirect('adda:verify_account')
            else:
                messages.error(request, 'That Email Is Already Registered To Our System')
                return render(request, 'registration/register.html')
        else:
            print(form)
            return render(request, 'accounts/register.html', {'form': form})
    else:
        form = RegisrationForm()
        context = {
            'counties': County.objects.all()
        }
        return render(request, 'accounts/register.html', context, {'form': form})


def verify_account(request):
    if request.method == 'POST':
        if AddaUser.objects.filter(verification_code=request.POST['customer_code'], is_active=False).count() > 0:
            adda_user = AddaUser.objects.filter(verification_code=request.POST['customer_code']).first()
            adda_user.is_active = True
            adda_user.save()
            messages.success(request, f'Welcome {adda_user.first_name} your account is now active')
            return redirect('adda:login')
        else:
            messages.error(request, 'That code verification is not valid, please try again ')
            return render(request, 'accounts/verify_account.html')
    return render(request, 'accounts/verify_account.html')


def adda_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            if AddaUser.objects.filter(user_ptr_id=user.id).count() > 0:
                return redirect('adda:dashboard')
            else:
                messages.error(request, 'Invalid Email Or Password')
                return redirect('adda:login')
        else:
            messages.error(request, 'Invalid Email Or Password')
            return redirect('adda:login')
    return render(request, 'accounts/login.html')


def challenges(request):
    challenge_list = Challenge.objects.all()
    context = {
        'challenges': challenge_list,
        'adda_user': AddaUser.objects.filter(user_ptr_id=request.user.id).first()
    }
    return render(request, 'adda/challenges.html', context)


def create_challenge(request):
    if request.method == 'POST':
        form = ChallengeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Challenge Added Successfully')
            return redirect('adda:challenges')
        else:
            print(form)
    context = {
        'adda_user': AddaUser.objects.filter(user_ptr_id=request.user.id).first()
    }
    return render(request, 'adda/create_challenge.html', context)


def edit_challenge(request, challenge_id):
    challenge = Challenge.objects.get(id=challenge_id)
    if request.method == 'POST':
        form = ChallengeForm(request.POST, instance=challenge)
        if form.is_valid():
            form.save()
            messages.success(request, 'Challenge Updated Successfully')
            return redirect('adda:challenges')
    context = {
        'challenge': challenge
    }
    return render(request, 'adda/edit_challenge.html', context)


def ideas(request, challenge_id):
    idea_list = Idea.objects.filter(challenge_id=challenge_id)
    context = {
        'ideas': idea_list,
        'adda_user': AddaUser.objects.filter(user_ptr_id=request.user.id).first(),
        'challenge': Challenge.objects.get(id=challenge_id)
    }
    return render(request, 'adda/ideas.html', context)


def create_idea(request, challenge_id):
    if request.method == 'POST':
        form = IdeaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Challenge Idea Added Successfully')
            return redirect('adda:ideas', challenge_id)
        else:
            print(form)
    context = {
        'challenge': Challenge.objects.get(id=challenge_id),
        'adda_user': AddaUser.objects.filter(user_ptr_id=request.user.id).first()
    }
    return render(request, 'adda/create_idea.html', context)


def edit_idea(request, idea_id):
    idea = Idea.objects.get(id=idea_id)
    if request.method == 'POST':
        form = IdeaForm(request.POST, instance=idea)
        if form.is_valid():
            form.save()
            messages.success(request, 'Challenge Updated Successfully')
            return redirect('adda:challenges')
    context = {
        'idea': idea
    }
    return render(request, 'adda/edit_challenge.html', context)


def comments(request, idea_id):
    idea = Idea.objects.get(id=idea_id)

    context = {
        'idea': idea,
        'comments': Comment.objects.filter(idea_id=idea_id)
    }
    return render(request, 'adda/comments.html', context)


def create_comment(request, idea_id):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Idea Comment Added Successfully')
            return redirect('adda:comments', idea_id)
        else:
            print(form)
    context = {
        'idea': Idea.objects.get(id=idea_id)
    }
    return render(request, 'adda/create_comment.html', context)


def dashboard(request):
    return render(request, 'adda/dashboard.html')