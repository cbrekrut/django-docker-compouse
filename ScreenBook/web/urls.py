from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('', views.index, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path("account/", views.account_view, name="account"),
    path('account/password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('account/password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('ajax/filter-apps/', views.filter_apps_ajax, name='filter_apps_ajax'),
    path('app/<slug:slug>/', views.app_detail, name='app_detail'),
    path('submit-review/', views.submit_review, name='submit_review'),
    path('submit-feedback/', views.submit_feedback, name='submit_feedback'),
    path('start-payment/', views.start_payment, name='start_payment'),
    path('payment-webhook/', views.payment_webhook, name='payment_webhook'),
]
