from mysql.connector import connect, Error

def get_connection():
    try:
        connection = connect(
            host="localhost",
            user="----",
            password="----",
            database="UserPasswordDb",
        )
        if connection.is_connected():
            print("Successfully connected to the database")
        return connection
    except Error as e:
        print(f"Connection error: {e}")
        return None

