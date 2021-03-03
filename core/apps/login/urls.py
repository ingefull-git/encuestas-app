from django.urls import path


from .views import registerPage, loginPage, logoutUser


app_name = 'login'

urlpatterns = [
    
    path('register', registerPage, name="register"),
    path('', loginPage, name="login"),
    path('logout', logoutUser, name="logout"),
]
