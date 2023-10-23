# coding: utf-8
from flask import Flask, request, render_template, redirect, url_for, session
from ping3 import ping
import database 
from flask_session import Session
from datetime import timedelta





app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Remplacez 'your_secret_key' par une cle secrete

from flask_bootstrap import Bootstrap
Bootstrap(app)

# Configuration de Flask-Session
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=1440)  # Duree de la session

# Initialisez l'extension Flask-Session

Session(app)



def ping_host(host):
    response_time = ping(host)
    if response_time is not None:
        return True  # Le point d'acces est fonctionnel
    else:
        return False  # Le point d'acces ne repond pas

def ping_and_update_db():
    connection = database.get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT ipadress FROM ipadress")
    addresses = cursor.fetchall()
    cursor.close()

    for address in addresses:
        ip = address['ipadress']
        response_time = ping_host(ip)

        if response_time:
            is_functional = True
            cursor = connection.cursor()
            cursor.execute("UPDATE ipadress SET operationnelle = %s WHERE ipadress = %s", (is_functional, ip))
            connection.commit()
            cursor.close()

        else:
            is_functional = False
            cursor = connection.cursor()
            cursor.execute("UPDATE ipadress SET operationnelle = %s WHERE ipadress = %s", (is_functional, ip))
            connection.commit()
            cursor.close()

def ipadress_db():
    connection = database.get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM ipadress")
    addresses = cursor.fetchall()
    cursor.close()

    return addresses

def info_users():
    connection = database.get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users")
    info_users = cursor.fetchall()
    cursor.close()

    return info_users



@app.route('/', methods=['GET', 'POST'])
def index():
    ping_and_update_db()
    database.get_db_connection()
    results = []
    if request.method == 'POST':
        hosts = request.form.get('hosts').split(',')
        for host in hosts:
            host = host.strip()
            result = ping_host(host)
            results.append({'host': host, 'result': result})
    return render_template('index.html', results=results)



@app.route('/connexion', methods=['GET', 'POST'])
def login():
    ping_and_update_db()
    all_ip_adress = ipadress_db()
    session["allipadress"] = all_ip_adress
    all_number_ip = database.fetch_ipadress_number_all()

    function_number_ip = database.fetch_ipadress_number_function()
    disfunction_number_ip = database.fetch_ipadress_number_disfunction()

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        connection = database.get_db_connection()
        cursor = connection.cursor(dictionary=True)  # Utilisez dictionary=True pour obtenir un dictionnaire Python
        cursor.execute("SELECT * FROM users WHERE email = %s and password = md5(%s)", (email, password))
        user = cursor.fetchone()
        cursor.close()
        if user is not None:
            session['user'] = user 
            return render_template('dashboard.html',user = user, all_ip_adress= all_ip_adress,  all_number_ip =  all_number_ip, function_number_ip= function_number_ip, disfunction_number_ip= disfunction_number_ip)

        if session["user"] is not None:
            return render_template('dashboard.html',user = session["user"], all_ip_adress= all_ip_adress,  all_number_ip= all_number_ip, function_number_ip= function_number_ip, disfunction_number_ip=disfunction_number_ip)
    else:
        return render_template('index.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    ping_and_update_db()
    all_ip_adress = ipadress_db()
    session["allipadress"] = all_ip_adress
    all_number_ip = database.fetch_ipadress_number_all()
    function_number_ip = database.fetch_ipadress_number_function()
    disfunction_number_ip = database.fetch_ipadress_number_disfunction()
    if session["user"] is not None and session["allipadress"] is not None:
        return render_template('dashboard.html', user = session["user"], all_ip_adress = session["allipadress"],  all_number_ip=  all_number_ip, function_number_ip= function_number_ip, disfunction_number_ip= disfunction_number_ip)
    else:
        return render_template('index.html')


@app.route('/connexion/utilisateurs', methods=['GET', 'POST'])
def print_users():
    infos_users = info_users()
    all_number_ip = database.fetch_ipadress_number_all()
    function_number_ip = database.fetch_ipadress_number_function()
    disfunction_number_ip = database.fetch_ipadress_number_disfunction()
    all_ip_adress = ipadress_db()
    print(all_ip_adress)
    return render_template('users.html', user = session["user"],  all_number_ip=  all_number_ip, function_number_ip= function_number_ip, disfunction_number_ip= disfunction_number_ip, users = infos_users)
    




# Page de deconnexion
@app.route('/logout',methods = ['GET'])
def logout():
    session.pop('user', None)  # Supprimez l'utilisateur de la session
    return render_template('index.html')



@app.route('/connexion/ajouterip',methods = ['GET', 'POST'])
def addip():
    all_number_ip = database.fetch_ipadress_number_all()
    function_number_ip = database.fetch_ipadress_number_function()
    disfunction_number_ip = database.fetch_ipadress_number_disfunction()
    return render_template('addip.html', user = session["user"],  all_number_ip=  all_number_ip, function_number_ip= function_number_ip, disfunction_number_ip= disfunction_number_ip)



@app.route('/connexion/ajouterutilisateur', methods = ['GET', 'POST'])
def adduser():
    all_number_ip = database.fetch_ipadress_number_all()
    function_number_ip = database.fetch_ipadress_number_function()
    disfunction_number_ip = database.fetch_ipadress_number_disfunction()
    return render_template('adduser.html', user = session["user"],  all_number_ip= all_number_ip , function_number_ip= function_number_ip, disfunction_number_ip=disfunction_number_ip)


#la route pour ajoutef une adresse IP
@app.route('/connexion/ajouterip/ajouter', methods = ["GET", 'POST'])
def addip_o():
    all_number_ip = database.fetch_ipadress_number_all()
    function_number_ip = database.fetch_ipadress_number_function()
    disfunction_number_ip = database.fetch_ipadress_number_disfunction()
    if request.method == 'POST':
        ipadress = request.form['ipadress']
        nameip = request.form['nameip']
        operationnelle = True
        connection = database.get_db_connection()
        cursor = connection.cursor()
        cursor = connection.cursor(dictionary=True)

        #Une requete SQL pour voir l'adresse ip existe deja ou pas
        count_ip_query = "SELECT count(*) FROM ipadress WHERE ipadress = %s"
        cursor.execute(count_ip_query, (ipadress,))
        count_ip = cursor.fetchone()
        print(count_ip)
        if count_ip["count(*)"] == 0:
            # Utilisez une requete SQL d'INSERT pour ajouter une nouvelle adresse IP
            insert_query = "INSERT INTO ipadress (nameip, ipadress, operationnelle) VALUES (%s,%s,%s)"
            cursor.execute(insert_query, (nameip, ipadress, operationnelle))


            connection.commit()  # N'oubliez pas de commettre la transaction
            cursor.close()
            connection.close()
            if connection.commit:
                return render_template('addip.html', user = session["user"], message = "Enregistré avec succès",  all_number_ip= all_number_ip, function_number_ip= function_number_ip, disfunction_number_ip=disfunction_number_ip)
        else:
            cursor.close()
            connection.close()
            return render_template('addip.html', user = session["user"], message1 = "Cette adresse ip existe déjà",  all_number_ip= all_number_ip , function_number_ip= function_number_ip, disfunction_number_ip=disfunction_number_ip)



#La route pour ajouter les utilisateurs 
@app.route('/connexion/ajouterutilisateur/ajouter', methods = ["GET", 'POST'])
def adduser_o():
    all_number_ip = database.fetch_ipadress_number_all()
    function_number_ip = database.fetch_ipadress_number_function()
    disfunction_number_ip = database.fetch_ipadress_number_disfunction()
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        connection = database.get_db_connection()
        cursor = connection.cursor()
        cursor = connection.cursor(dictionary=True)

        #Une requete SQL pour voir l'utilisateur existe déjà ou pas
        count_user_query = "SELECT count(*) FROM users WHERE email = %s"
        cursor.execute(count_user_query, (email,))
        count_user = cursor.fetchone()

        if count_user["count(*)"] == 0:
            # Utilisez une requdte SQL d'INSERT pour ajouter une nouvelle adresse IP
            insert_query = "INSERT INTO users (username, email, password) VALUES (%s ,%s, md5(%s))"
            cursor.execute(insert_query, (username, email,password))

            connection.commit()  # N'oubliez pas de commettre la transaction
            cursor.close()
            connection.close()
            if connection.commit:
                return render_template('adduser.html', user = session["user"], message = "Enregistré avec succès",  all_number_ip= all_number_ip, function_number_ip= function_number_ip, disfunction_number_ip=disfunction_number_ip)
        
        else:
            cursor.close()
            connection.close()
            return render_template('adduser.html', user = session["user"], message1 = "Cet utilisateur existe déjà",  all_number_ip= all_number_ip, function_number_ip= function_number_ip, disfunction_number_ip=disfunction_number_ip)


@app.route('/supprimer_ip/<int:id>', methods=['GET'])
def supprimer_ip(id):
    all_number_ip = database.fetch_ipadress_number_all()
    function_number_ip = database.fetch_ipadress_number_function()
    disfunction_number_ip = database.fetch_ipadress_number_disfunction()
    # Vérifiez si l'ID est valide et existe dans la base de données
    if id is not None:
        connection = database.get_db_connection()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM ipadress WHERE id = %s", (id,))
        connection.commit()
        cursor.close()
        connection.close()
        # Redirigez l'utilisateur vers une page de confirmation ou autre

        all_ip_adress = ipadress_db()
        session["allipadress"] = all_ip_adress
        return render_template('dashboard.html', user = session["user"], all_ip_adress = session["allipadress"], message = "Supprimer avec succès",  all_number_ip= all_number_ip , function_number_ip= function_number_ip, disfunction_number_ip=disfunction_number_ip)
    else:
        # Gérez le cas où l'ID n'est pas valide
        all_ip_adress = ipadress_db()
        session["allipadress"] = all_ip_adress
        return render_template('dashboard.html', user = session["user"], all_ip_adress = session["allipadress"], message1 = "Ça n'a pas été supprimé",  all_number_ip= all_number_ip , function_number_ip= function_number_ip, disfunction_number_ip=disfunction_number_ip)

@app.route('/supprimer_user/<int:id>', methods=['GET'])
def supprimer_user(id):
    all_number_ip = database.fetch_ipadress_number_all()
    function_number_ip = database.fetch_ipadress_number_function()
    disfunction_number_ip = database.fetch_ipadress_number_disfunction()
    infos_users = info_users()
    # Vérifiez si l'ID est valide et existe dans la base de données
    if id is not None:
        connection = database.get_db_connection()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM users WHERE id = %s", (id,))
        connection.commit()
        cursor.close()
        connection.close()
        # Redirigez l'utilisateur vers une page de confirmation ou autre

        all_ip_adress = ipadress_db()
        session["allipadress"] = all_ip_adress
        return render_template('users.html', user = session["user"], all_ip_adress = session["allipadress"], message = "Supprimer avec succès",  all_number_ip= all_number_ip , function_number_ip= function_number_ip, disfunction_number_ip=disfunction_number_ip, users = infos_users)
    else:
        # Gérez le cas où l'ID n'est pas valide
        all_ip_adress = ipadress_db()
        session["allipadress"] = all_ip_adress
        return render_template('users.html', user = session["user"], all_ip_adress = session["allipadress"], message1 = "Ça n'a pas été supprimé",  all_number_ip= all_number_ip , function_number_ip= function_number_ip, disfunction_number_ip=disfunction_number_ip, users = infos_users)



if __name__ == '__main__':
    ping_and_update_db()
    app.run(debug=True)


