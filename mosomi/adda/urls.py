from django.urls import path

from adda import views

app_name = 'adda'
urlpatterns = [
    path('login', views.adda_login, name='login'),
    path('register', views.register, name='register'),
    path('verify/account', views.verify_account, name='verify_account'),


    path('dashboard', views.dashboard, name='dashboard'),
    path('challenges', views.challenges, name='challenges'),
    path('ideas/<int:challenge_id>', views.ideas, name='ideas'),
    path('create/challenge', views.create_challenge, name='create_challenge'),
    path('create/idea/<int:challenge_id>', views.create_idea, name='create_idea'),
    path('edit/idea/<int:idea_id>', views.edit_idea, name='edit_idea'),
    path('edit/challenge/<int:challenge_id>', views.edit_challenge, name='edit_challenge'),

    path('idea/comments/<int:idea_id>', views.comments, name='comments'),
    path('create/comment/<int:idea_id>', views.create_comment, name='create_comment')
]