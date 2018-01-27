# from flask import Flask
from flask import request
from flask import render_template
from flask import Flask, redirect, url_for, session
# from ClassConstract.py import ClassGenerator
from ClassConstract import ClassGenerator
from pprint import pprint
from flask import Flask, session
# import ClassConstract.py
app = Flask(__name__)
app.secret_key = 'aaaaaaaaaa'

# session['userID'] = "3"

DB = ClassGenerator()

@app.route('/hello/')
@app.route('/hello/<name>')
def helo(name=None):
  return render_template("hello.html", sk=name)


''' _______________
< My Movie List >
 ---------------
        \   ^__^
         \  (oo)\_______
            (__)\       )\/\
                ||----w |
                ||     ||
'''
@app.route('/mml.html', methods=["GET","POST"])
def mml():
 global DB
 films = DB.movies()
 myfilms = DB.mylist()
 lst = []
 for item in films.view():
  if item[3] == 0:
   lst.append(item)
 mylst = []
 for item in myfilms.view():
  #print("-------------myfilms")
  #print(item)
  if item[1] == session["userID"]:
   mylst.append(item)
 error = None
 print("Step 0")

 if request.method == "POST" and request.form['action'] == "edit":
  print("Step Edit")
  film = request.form['film']
  plan = request.form['plan']
  score = request.form['score']
  onListID = request.form['onListId']
  '''error = "Zmienieono film " + onListID + " " + plan + " " + score + "/5"'''
  error = "Zmienieono dane przy filmie: " + film
  return render_template("mml.html", error=error, lista=lst, mylist=mylst, wai = session["whoAmI"])

 if request.method == "POST" and request.form['action'] == "add":
  print("Step Add")
  idOfMovie = request.form['idOfMovie']
  movieToAdd = []
  for item in films.view():
   if item[0] == int(idOfMovie):
    movieToAdd.append(item)
  #print("Movie to add")
  #print ("_____________________________")
  #pprint(movieToAdd)
  #pprint(session["userID"])
  #print ("_____________________________")
  #print ("_____________________________")
  #print ("Movie to add")
  #pprint(movieToAdd[0][0])
  #pprint(movieToAdd[0][1])
  #print ("_____________________________")
  myfilms.add(session["userID"], movieToAdd[0][0], movieToAdd[0][1], 0, 0)
  return redirect(url_for('mml'))

 if request.method == "POST" and request.form['action'] == "del":
  #print("-------------------Step del")
  what = request.form['idDel']
  #print("-------------------Usun")
  #print(what)
  idOfMovie = request.form['idMov']
  movieToAdd = []
  for item in films.view():
      if item[0] == int(idOfMovie):
          movieToAdd.append(item)
  myfilms.remove(what)
  error = "Usunieto film z MyList"
  return redirect(url_for('mml'))
 if request.method == "POST" and request.form['action'] == "editmy":
  id = request.form['onListId']
  watch = request.form['plan']
  sco = request.form['score']
  lista = DB.mylist()
  dz = []
  for item in lista.view():
   if item[0] == int(id):
    dz = item
    print("----------------------good item")
    print(dz)
  print("----------------------update mylist")
  print(dz[1])
  print(dz[2])
  print(dz[3])
  print(watch)
  print(sco)
  print(dz[0])
  lista.change(dz[1], dz[2], dz[3], watch, sco, dz[0])
  return redirect(url_for('mml'))
 else:
  return render_template("mml.html", lista=lst, mylist=mylst, wai = session["whoAmI"])


''' _______________
< Logowanie >
 ---------------
        \   ^__^
         \  (oo)\_______
            (__)\       )\/\
                ||----w |
                ||     ||
'''

@app.route('/', methods=["GET","POST"])
@app.route('/index.html', methods=["GET","POST"])
def indexhtml():
 ''' Logowanie do systemu '''
 error = None
 global DB
 if request.method == "POST" and request.form['username'] != "" and request.form['password'] != "":
  user_name = request.form['username']
  user_pass = request.form['password']
  loginData = DB.user()
  print(DB.__dict__.keys())
  isset = loginData.isRegestrated(user_name, user_pass)
  print("-----------------------isset")
  print(isset)
  if not isset:
   error = "Brak uzytkownika"
   return render_template("index.html", error = error)			
  else:
   session["userID"] = isset[0][0]
   userData = DB.dane()
   for item in userData.view():
    print("userID: ")
    print(session["userID"])
    print("----------------------item login")
    print(item)
    if item[1] == session["userID"]:
     session['whoAmI'] = item[2] + " " + item[3]
  print(session['whoAmI'])
  return redirect(url_for('mml'))
 else:	
  return render_template("index.html")

''' _______________
< Rejestracja >
 ---------------
        \   ^__^
         \  (oo)\_______
            (__)\       )\/\
                ||----w |
                ||     ||
'''
@app.route('/rej.html', methods=["GET","POST"])
def rejhtml():
 error = None
 global DB
 NewUser = DB.user()
 NewUserData = DB.dane()
 if request.method == "POST" and request.form['login'] != "" and request.form['pass'] != "":
  user_name = request.form['login']
  user_pass = request.form['pass']
  user_imie = request.form['imie']
  user_nazw = request.form['nazw']
  user_email = request.form['email']
  isset = NewUser.isRegestrated(user_name, user_pass)
  if not isset:
   NewUser.add(user_name, user_pass)
   user = DB.user()
   id = 0;
   item = user.view()[-1]
   id = item[0]
   print("-----------------id add")
   print(id)
   NewUserData.add(id, user_imie, user_nazw, user_email)
   session['userID']=id
   session['whoAmI']=user_imie + " " + user_nazw
   return redirect(url_for('mml'))
  else:
   return render_template("rej.html", error = "Istnieje taki uzytkownik,")
 else:
   error="Uzupelnij pola"
   return render_template("rej.html", error=error)


''' _______________
< Profil >
 ---------------
        \   ^__^
         \  (oo)\_______
            (__)\       )\/\
                ||----w |
                ||     ||
'''
@app.route('/prof.html', methods=["GET","POST"])
def profilehtml():
 error = None
 global DB
 data = DB.dane()
 inputy = []
 for item in data.view():
  if item[1] == session['userID']:
   inputy = item
 if request.method == "POST" and request.form['action'] == "chpass":
  user_pass = request.form['chpass']
  haslo = DB.user()
  dane = []
  for item in haslo.view():
   if item[0] == session['userID']:
    dane = item
    print("-----------------zmiana hasla")
    print(item)
  haslo.change(item[1], user_pass, item[0])
  error = "Zmienieono haslo"
  return render_template("prof.html", error=error, chedycja = inputy)
 if request.method == "POST" and request.form['action'] == "chdata":
  data = DB.dane()
  zmien = []
  for item in data.view():
   if item[1] == session['userID']:
    zmien = item
    print("---------------------zmien")
    print(zmien[0])
  user_name = request.form['chname']
  user_nazw = request.form['chnazw']
  user_mail = request.form['chmail']
  data.change(session['userID'], user_name, user_nazw, user_mail, zmien[0])
  session['whoAmI'] = user_name + " " + user_nazw
  return redirect(url_for('profilehtml'))
 else:
  return render_template("prof.html", chedycja = inputy)


''' _______________
< Edycja filmow >
 ---------------
        \   ^__^
         \  (oo)\_______
            (__)\       )\/\
                ||----w |
                ||     ||
'''
@app.route('/mov.html', methods=["GET","POST"])
def movhtml():
 error = None
 global DB
 films = DB.movies()
 lst = []
 for item in films.view():
  if item[3] == 0:
   lst.append(item)
 if request.method == "POST" and request.form['action'] == "add":
  film = request.form['film']
  kat = request.form['kat']
  films.add(film, kat, 0)
  return redirect(url_for('movhtml'))
 if request.method == "POST" and request.form['action'] == "del":
  what = request.form['idOfMovie']
  films.remove(what)
  return redirect(url_for('movhtml'))
 if request.method == "POST" and request.form['action'] == "edit":
  film = request.form['film']
  kat = request.form['kat']
  what = request.form['idOfMovie']
  films.change(film, kat, 0, what)
  return redirect(url_for('movhtml'))
 else:
  return render_template('mov.html', lista = lst)


''' _______________
< Serwer >
 ---------------
        \   ^__^
         \  (oo)\_______
            (__)\       )\/\
                ||----w |
                ||     ||
'''
if __name__ == '__main__':
 app.run(host='127.0.0.1', port=81, debug=True)