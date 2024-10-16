import conector_to_db
import functions


def main():
    # Отримання з'єднання з базою даних
    connection = conector_to_db.get_connection()
    
    if connection is None:
        print("Не вдалося підключитися до бази даних")
        return

    # Створення курсора для виконання SQL запитів
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM User")
    result = cursor.fetchall()

    for row in result:
        print(row)


    try:
        while True:
            print("\nMenu:")
            print("1. Create Account")
            print("2. Login")
            print("0. Exit")
            
            choice = input("Choose an option (1, 2, or 0): ")

            if choice == '1':
                userName, password = functions.inputUser(cursor)
                if userName and password:
                    functions.create_user(cursor, userName, password)
                    connection.commit()
            elif choice == '2':
                userName = functions.login(cursor)
                functions.is_password_expired(cursor, userName)
                if userName is not None:
                    functions.logmenu(cursor, userName)
                    connection.commit()

            elif choice == '0':
                print("Exiting the program.")
                break
            else:
                print("Invalid choice. Please try again.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Закриття з'єднання
        connection.commit()
        cursor.close()
        connection.close()


if __name__ == "__main__":
    main()
