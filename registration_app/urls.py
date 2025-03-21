from django.urls import path
from .views import *
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('registration-form/', registration_form, name='registration-form'),
    path('register/', registration_form, name='register'),  # Add this line
    path('login/', login_view, name='login'),  # Use login_view here
    path('partners/', partners, name='partners'),
    path('partners_copy/', partners_copy, name='partners_copy'),
    path('landing/', landing_page, name='landing'),
    path('land', land, name='land_test'),

    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),  # Add this line
    path('company/<int:company_id>/', company_landing_page, name='company_landing'),
    path('forgot-password/', forgot_password, name='forgot_password'),
    path('reset/<uidb64>/<token>/', reset_password, name='reset_password'),
    path('companies/', company_list, name='company_list'),
    path('companies/new/', company_create, name='company_create'),
    path('companies/<int:pk>/edit/',company_update, name='company_update'),
    path('companies/<int:pk>/delete/', company_delete, name='company_delete'),
    path('admin_login/', superuser_login, name='admin_login'),

    path('create_news/', create_news, name='create_news'),
    # path('news/', news_list, name='news_list'),
    path('news/<int:news_id>/', news_page, name='news_page'),
    path('create_event/', create_event, name='create_event'),
    path('event/', event_list, name='event_list'),
    path('event/<int:event_id>/', event_page, name='event_page'),
    # path('register/', views.registration_form, name='register'),
    path('news_list/', news_list, name='news_list'),
    path('news/create/', news_create, name='news_create'),
    path('news/<int:news_id>/', news_page, name='news_page'),
    path('news/<int:news_id>/edit/', news_update, name='news_update'),
    path('news/<int:news_id>/delete/', news_delete, name='news_delete'),

    # events
    path('events_list/', event_list, name='event_list'),
    path('events/create/',event_create, name='event_create'),
    path('events/<int:event_id>/',event_detail, name='event_detail'),
    path('events/<int:event_id>/edit/', event_update, name='event_update'),
    path('events/<int:event_id>/delete/', event_delete, name='event_delete'),
    path('events/', event_list1, name='event_list1'),

    path('admin_page/', admin_page, name='admin_page'),
    path('', new_index1, name='new_index'),
    path('meetings/', meetings, name='meetings'),
    path('about/', about, name='about'),
    path('home2/', home2, name='home2'),
    path('events1/', events, name='events1'),
    path('l1/', l1, name='l1'),
    path('news1/', news_new, name='news_new'),
    path('partners1/', partners_new, name='partners_new'),
]


