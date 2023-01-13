from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
import sqlite3
import random
import secrets



def loginPage(request):

    return render(request, 'cinema_manager/login.html')

def signUpPage(request):

    return render(request, 'cinema_manager/signup.html')

def signUp(request):

    username = request.POST['username']
    password = request.POST['password']
    fName = request.POST['fName']
    lName = request.POST['lName']

    user = User.objects.create_user(username=username, email=None, password=password)
    user.first_name = fName
    user.last_name = lName
    user.save()

    user = authenticate(username=username, password=password)

    login(request, user)

    return render(request, 'cinema_manager/home.html')

def logIn(request):

    username = request.POST['username']
    password = request.POST['password']

    user = authenticate(request, username=username, password=password)

    if user != None:
        login(request, user)
        return render(request, 'cinema_manager/home.html')

    else:
        return render(request, 'cinema_manager/login.html')

@login_required(login_url='loginPage')
def logOut(request):

    logout(request)

    return render(request, 'cinema_manager/home.html')

def home(request):

    con = sqlite3.connect('cinema_manager/database.db')
    cur = con.cursor()

    query = ''' SELECT Showing.id, Showing.date, Showing.time, Film.title, Screen.id 
                FROM Showing
                LEFT JOIN Film ON Showing.filmId = Film.id
                LEFT JOIN Screen ON Showing.screenId = Screen.id '''
    
    cur.execute(query)

    temp = cur.fetchall()
    headers = ['id', 'date', 'time', 'fName', 'sId']
    results = [{headers[i] : row[i] for i in range(5)} for row in temp]

    con.commit()
    cur.close()
    con.close()

    return render(request, 'cinema_manager/home.html', {'results':results})

@login_required(login_url='loginPage')
def registration(request):

    return render(request, 'cinema_manager/registration.html')

@login_required(login_url='loginPage')
def filmAddForm(request):

    return render(request, 'cinema_manager/filmAdd.html')

@login_required(login_url='loginPage')
def filmAdd(request):

    if request.method == 'POST':

        title = request.POST['title']
        rating = request.POST['rating']
        duration = request.POST['duration']
        description = request.POST['description']

        con = sqlite3.connect('cinema_manager/database.db')
        cur = con.cursor()

        query = ''' INSERT INTO Film(title, rating, duration, description) VALUES (?,?,?,?) '''
        values = (title, rating, duration, description)

        cur.execute(query, values)
        con.commit()

        cur.close()
        con.close()

        return render(request, 'cinema_manager/success.html')

@login_required(login_url='loginPage')
def filmView(request):

    con = sqlite3.connect('cinema_manager/database.db')
    cur = con.cursor()

    query = ''' SELECT * FROM Film ORDER BY title ASC'''
    
    cur.execute(query)

    temp = cur.fetchall()
    headers = ['id', 'title', 'rating', 'duration', 'description']
    results = [{headers[i] : row[i] for i in range(5)} for row in temp]

    con.commit()
    cur.close()
    con.close()

    return render(request, 'cinema_manager/filmView.html', {'results':results})

@login_required(login_url='loginPage')
def screenView(request):

    con = sqlite3.connect('cinema_manager/database.db')
    cur = con.cursor()

    query = ''' SELECT * FROM Screen'''
    
    cur.execute(query)

    temp = cur.fetchall()
    headers = ['id', 'capacity']
    results = [{headers[i] : row[i] for i in range(2)} for row in temp]

    con.commit()
    cur.close()
    con.close()

    return render(request, 'cinema_manager/screenView.html', {'results':results})

@login_required(login_url='loginPage')
def screenAddForm(request):

    return render(request, 'cinema_manager/screenAddForm.html')

@login_required(login_url='loginPage')
def screenAdd(request):

    if request.method == 'POST':

        capacity = request.POST['capacity']
        values = (int(capacity),)

        con = sqlite3.connect('cinema_manager/database.db')
        cur = con.cursor()

        query = ''' INSERT INTO Screen(capacity) VALUES (?) '''

        cur.execute(query, values)
        con.commit()

        cur.close()
        con.close()

    return render(request, 'cinema_manager/success.html')

@login_required(login_url='loginPage')
def showingView(request):

    con = sqlite3.connect('cinema_manager/database.db')
    cur = con.cursor()

    query = ''' SELECT Showing.id, Showing.date, Showing.time, Film.title, Screen.id 
                FROM Showing
                LEFT JOIN Film ON Showing.filmId = Film.id
                LEFT JOIN Screen ON Showing.screenId = Screen.id '''
    
    cur.execute(query)

    temp = cur.fetchall()
    headers = ['id', 'date', 'time', 'fName', 'sId']
    results = [{headers[i] : row[i] for i in range(5)} for row in temp]

    con.commit()
    cur.close()
    con.close()

    return render(request, 'cinema_manager/showingView.html', {'results':results})

@login_required(login_url='loginPage')
def showingAddForm(request):

    con = sqlite3.connect('cinema_manager/database.db')
    cur = con.cursor()

    query = '''SELECT DISTINCT title FROM Film ORDER BY title ASC'''

    cur.execute(query)
    titleData = cur.fetchall()

    query = '''SELECT DISTINCT id FROM Screen ORDER BY id ASC'''

    cur.execute(query)
    screenData = cur.fetchall()

    data = {
        'screen':screenData,
        'title':titleData
    }

    con.commit()
    cur.close()
    con.close()

    return render(request, 'cinema_manager/showingAddForm.html', data)

@login_required(login_url='loginPage')
def showingAdd(request):

    if request.method == 'POST':

        date = request.POST['date']
        time = request.POST['time']
        fName = request.POST['fName']
        sId = request.POST['sId']


        con = sqlite3.connect('cinema_manager/database.db')
        cur = con.cursor()

        query = '''SELECT id FROM Film WHERE title == ?'''
        values = (str(fName), )

        cur.execute(query, values)
        filmId = cur.fetchone()
        filmId = filmId[0]

        query = ''' INSERT INTO Showing(date, time, filmId, screenId) VALUES (?,?,?,?) '''
        values = (date, time, int(filmId), sId)

        cur.execute(query, values)
        con.commit()

        cur.close()
        con.close()


        return render(request, 'cinema_manager/success.html')

@login_required(login_url='loginPage')
def clubCreate(request):

    if request.method == 'POST':

        clubName = request.POST['clubName']
        clubAdd = request.POST['clubAdd']
        clubPhone = request.POST['clubPhone']
        repFirstName = request.POST['repFirstName']
        repLastName = request.POST['repLastName']
        repDob = request.POST['repDob']

        userId = random.randint(1000, 9999)
        password = secrets.token_urlsafe(5)

        con = sqlite3.connect('cinema_manager/database.db')
        cur = con.cursor()

        query = ''' SELECT * FROM Rep WHERE id = ? OR password = ?'''
        value = (userId, password)

        cur.execute(query, value)
        temp = cur.fetchall()

        loop = True
        while loop == True:
            if temp == []:

                query = ''' INSERT INTO Rep(firstName, lastName, dob, userId, password) VALUES (?,?,?,?,?) '''
                values = (repFirstName, repLastName, repDob, userId, password)

                cur.execute(query, values)

                repId = cur.lastrowid

                query = ''' INSERT INTO Club(name, address, phone, repId) VALUES (?,?,?,?) '''
                values = (clubName, clubAdd, clubPhone, repId)

                cur.execute(query, values)
                con.commit()

                cur.close()
                con.close()

                loop = False

            else: 
                userId = random.randint(1000, 9999)
                password = secrets.token_urlsafe(5)

        rep = {
            'id':userId,
            'pass':password
        }

        return render(request, 'cinema_manager/successClub.html', rep)

@login_required(login_url='loginPage')
def viewClub(request):

    con = sqlite3.connect('cinema_manager/database.db')
    cur = con.cursor()

    query = ''' SELECT * FROM Club'''
    
    cur.execute(query)

    temp = cur.fetchall()
    headers = ['id', 'name', 'address', 'phone', 'repId']
    results = [{headers[i] : row[i] for i in range(5)} for row in temp]

    con.commit()
    cur.close()
    con.close()

    return render(request, 'cinema_manager/viewClub.html', {'results':results})

@login_required(login_url='loginPage')
def viewRep(request):

    con = sqlite3.connect('cinema_manager/database.db')
    cur = con.cursor()

    query = ''' SELECT * FROM Rep'''

    cur.execute(query)

    temp = cur.fetchall()
    headers = ['id', 'fName', 'lName', 'dob', 'userId', 'password']
    results = [{headers[i] : row[i] for i in range(6)} for row in temp]

    con.commit()
    cur.close()
    con.close()

    return render(request, 'cinema_manager/viewRep.html', {'results':results})

@login_required(login_url='loginPage')
def deleteClub(request):

    if request.method == 'POST':

        clubId = request.POST['cid']

        con = sqlite3.connect('cinema_manager/database.db')
        cur = con.cursor()

        query = ''' SELECT repId FROM Club WHERE id = ? '''
        value = (clubId,)

        cur.execute(query, value)
        temp = cur.fetchone()
        repId = temp[0]

        query = ''' DELETE FROM Club WHERE id = ? '''
        value = (clubId,)

        cur.execute(query, value)

        query = ''' DELETE FROM Rep WHERE id = ? '''
        value = (repId,)

        cur.execute(query, value)

        con.commit()
        cur.close()
        con.close()

        return render(request, 'cinema_manager/success.html')

@login_required(login_url='loginPage')
def deleteScreen(request):

    if request.method == 'POST':

        screenId = request.POST['sid']

        con = sqlite3.connect('cinema_manager/database.db')
        cur = con.cursor()

        query = ''' SELECT * 
                    FROM Screen 
                    WHERE EXISTS (SELECT * 
                                    FROM Showing 
                                    WHERE Showing.screenId = ? AND Screen.id = ?)'''
        values = (screenId, screenId)

        cur.execute(query, values)
        temp = cur.fetchall()
        print(temp)

        if temp != []:

            return render(request, 'cinema_manager/screenExist.html')

        else:
        
            query = ''' DELETE FROM Screen WHERE id = ?'''
            value = (screenId,)

            cur.execute(query, value)

            con.commit()
            cur.close()
            con.close()


        return render(request, 'cinema_manager/success.html')

@login_required(login_url='loginPage')
def deleteShowing(request):

    if request.method == 'POST':

        showingId = request.POST['sid']

        con = sqlite3.connect('cinema_manager/database.db')
        cur = con.cursor()

        query = ''' DELETE FROM Showing WHERE id = ? '''
        value = (showingId,)

        cur.execute(query, value)

        con.commit()
        cur.close()
        con.close()

        return render(request, 'cinema_manager/success.html')

@login_required(login_url='loginPage')    
def deleteFilm(request):

    if request.method == 'POST':

        filmId = request.POST['fid']

        con = sqlite3.connect('cinema_manager/database.db')
        cur = con.cursor()

        query = ''' SELECT * 
                    FROM Film 
                    WHERE EXISTS (SELECT * 
                                    FROM Showing 
                                    WHERE Showing.filmId = ? AND Film.id = ?)'''
        values = (filmId, filmId)

        cur.execute(query, values)
        temp = cur.fetchall()
        print(temp)

        if temp != []:

            return render(request, 'cinema_manager/showingExist.html')

        else:
        
            query = ''' DELETE FROM Film WHERE id = ?'''
            value = (filmId,)

            cur.execute(query, value)

            con.commit()
            cur.close()
            con.close()

        return render(request, 'cinema_manager/success.html')