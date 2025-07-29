import mysql.connector


def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='RootPass123!',
        database='db_maintenance_alat'
    )
