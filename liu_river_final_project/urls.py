from django.contrib import admin
from django.contrib.auth.views import (
    LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView,
    PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
)
from django.urls import path, include, reverse_lazy
from django.views.generic import RedirectView, TemplateView
from proleague.views import signup

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('proleague.urls')),

    path(
        '',
        RedirectView.as_view(
            pattern_name='about_urlpattern',
            permanent=False
        )
    ),

    path(
        'login/',
        LoginView.as_view(template_name='proleague/login.html'),
        name='login_urlpattern'
    ),

    path(
        'signup/',
        signup,
        name='signup_urlpattern'
    ),

    path(
        'logout/',
        LogoutView.as_view(),
        name='logout_urlpattern'
    ),

    path(
        'password_change/',
        PasswordChangeView.as_view(
            success_url=reverse_lazy('password_change_done_urlpattern'),
            template_name='proleague/password_change_form.html'),
        name='password_change_urlpattern'
    ),

    path(
        'password_change/done/',
        PasswordChangeDoneView.as_view(
            template_name='proleague/password_change_done.html'
        ),
        name='password_change_done_urlpattern'
    ),

    path(
        'password_reset/',
        PasswordResetView.as_view(
            template_name='proleague/password_reset_form.html',
            email_template_name='proleague/password_reset_email.html'
        ),
        name='password_reset_urlpattern'
    ),

    path(
        'password_reset/done/',
        PasswordResetDoneView.as_view(
            template_name='proleague/password_reset_done.html'
        ),
        name='password_reset_done'
    ),

    path(
        'password_reset/<uidb64>/<token>/',
        PasswordResetConfirmView.as_view(
            template_name='proleague/password_reset_confirm.html',
        ),
        name='password_reset_confirm'
    ),

    path(
        'password_reset/complete/',
        PasswordResetCompleteView.as_view(
            template_name='proleague/password_reset_complete.html'
        ),
        name='password_reset_complete'
    ),

    path(
        'about/',
        TemplateView.as_view(template_name='proleague/about.html'),
        name='about_urlpattern'
    ),
]
