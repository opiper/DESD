from django.urls import path
from cinema_manager import views

urlpatterns = [
    path("", views.home, name="home"),
    path("registration", views.registration, name="registration"),
    path("filmAdd", views.filmAdd, name="filmAdd"),
    path("filmAddForm", views.filmAddForm, name="filmAddForm"),
    path("filmView", views.filmView, name="filmView"),
    path("screenView", views.screenView, name="screenView"),
    path("screenAddForm", views.screenAddForm, name="screenAddForm"),
    path("screenAdd", views.screenAdd, name="screenAdd"),
    path("showingView", views.showingView, name="showingView"),
    path("showingAdd", views.showingAdd, name="showingAdd"),
    path("showingAddForm", views.showingAddForm, name="showingAddForm"),
    path("clubCreate", views.clubCreate, name="clubCreate"),
    path("viewclub", views.viewClub, name="viewClub"),
    path("viewRep", views.viewRep, name="viewRep"),
    path("deleteClub", views.deleteClub, name="deleteClub"),
    path("deleteScreen", views.deleteScreen, name="deleteScreen"),
    path("deleteShowing", views.deleteShowing, name="deleteShowing"),
    path("deleteFilm", views.deleteFilm, name="deleteFilm"),
    path("loginPage", views.loginPage, name="loginPage"),
    path("logIn", views.logIn, name="logIn"),
    path("logOut", views.logOut, name="logOut"),
    path("signUp", views.signUp, name="signUp"),
    path("signUpPage", views.signUpPage, name="signUpPage"),
]