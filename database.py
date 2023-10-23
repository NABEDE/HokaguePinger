import mysql.connector
from config import db_config



def get_db_connection():
    connection = mysql.connector.connect(**db_config)
    return connection






def fetch_ipadress_from_database():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor = connection.cursor(dictionary=True)

    # Exécutez votre requête SQL ici
    query = "SELECT * FROM ipadress"
    cursor.execute(query)

    # Récupérez les résultats
    results = cursor.fetchall()

    cursor.close()
    connection.close()

    return results


def fetch_ipadress_number_all():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor = connection.cursor(dictionary=True)

    # Exécutez votre requête SQL ici
    query = "SELECT count(*) FROM ipadress"
    cursor.execute(query)

    # Récupérez les résultats
    results = cursor.fetchone()

    cursor.close()
    connection.close()

    return results


def fetch_ipadress_number_function():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor = connection.cursor(dictionary=True)

    # Exécutez votre requête SQL ici
    query = "SELECT count(*) FROM ipadress WHERE operationnelle = 1"
    cursor.execute(query)

    # Récupérez les résultats
    results = cursor.fetchone()

    cursor.close()
    connection.close()

    return results


def fetch_ipadress_number_disfunction():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor = connection.cursor(dictionary=True)

    # Exécutez votre requête SQL ici
    query = "SELECT count(*) FROM ipadress WHERE operationnelle = 0"
    cursor.execute(query)

    # Récupérez les résultats
    results = cursor.fetchone()

    cursor.close()
    connection.close()

    return results
