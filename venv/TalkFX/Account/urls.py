from django.urls import path
from Account.views import (
    registration_view, logout_view,
    login_view, account_view,
    must_authenticate_view, home_screen_view,
    technical_analysis, fundamental_analysis,
    forex_quotes
)

app_name = 'Account'

urlpatterns = [
    path('', home_screen_view, name="home"),
    path('account/', account_view, name="account"),
    path('login/', login_view, name="login"),
    path('logout/', logout_view, name="logout"),
    path('must_authenticate/', must_authenticate_view, name="must_authenticate"),
    path('register/', registration_view, name="register"),
    path('technical_analysis/', technical_analysis, name="technical_analysis"),
    path('fundamental_analysis/', fundamental_analysis, name="fundamental_analysis"),
    path('forex_quotes/', forex_quotes, name="forex_quotes"),

]