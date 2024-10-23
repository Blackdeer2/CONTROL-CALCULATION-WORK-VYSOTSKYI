import DAL.conector_to_db as conector_to_db
from UI.main_UI import main_UI

import flet as ft

def main():
    connection = conector_to_db.get_connection()
    
    if connection is None:
        print("Не вдалося підключитися до бази даних")
        return
    cursor = connection.cursor()

    try:
        ft.app(lambda page: main_UI(page, cursor))
        cursor.execute("SELECT * FROM User")
        result = cursor.fetchall()

        for row in result:
            print(row)

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        connection.commit()
        cursor.close()
        connection.close()


if __name__ == "__main__":
   main()
