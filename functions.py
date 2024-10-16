import datetime
import hashlib
import uuid

MIN_PASSWORD_AGE_DAYS = 1
MAX_PASSWORD_AGE_DAYS = 10


def inputUser(cursor):
    # Запит на ім'я користувача
    userName = input("Input user name: ")
    
    # Перевірка наявності користувача з таким ім'ям
    if user_exists(cursor, userName):
        print(f"User '{userName}' already exists. Please choose a different name.")
        return  # Завершити функцію, якщо ім'я користувача вже існує
    
    # Запит на пароль
    password = input("Input password: ")
    
    return userName, password

def login(cursor):
    # Запит на ім'я користувача
    userName = input("Enter your username: ")
    
    # Запит на пароль
    password = input("Enter your password: ")
    
    # Отримання хешу пароля з бази даних
    cursor.execute("SELECT CurrentPassword FROM User WHERE Name = %s", (userName,))
    result = cursor.fetchone()
    
    if result is None:
        print("User does not exist.")
        return
    
    stored_password_hash = result[0]

    # Хешування введеного пароля
    password_hash = hashlib.sha256(password.encode()).hexdigest()

    # Перевірка правильності пароля
    if password_hash == stored_password_hash:
        print("Login successful!")
        return userName
    else:
        print("Invalid password. Please try again.")
        return None

def createNewPassword(cursor, userName):
    # Введення нового пароля
    newPassword = input("Input new password: ")

    # Отримуємо всі старі паролі для користувача
    oldPasswords = getPasswordsByUserName(cursor, userName)
    
    # Перевіряємо, щоб новий пароль не збігався з попередніми
    new_password_hash = hashlib.sha256(newPassword.encode()).hexdigest()

    for (oldPassword,) in oldPasswords:
        if new_password_hash == oldPassword:
            print("New password must not match any of the previous passwords.")
            return

    # Якщо перевірка пройдена, оновлюємо пароль у базі даних
    try:
        # Оновлюємо поточний пароль у таблиці User
        update_user_query = """
            UPDATE User
            SET CurrentPassword = %s, PasswordCreationDate = NOW()
            WHERE Name = %s
        """
        cursor.execute(update_user_query, (new_password_hash, userName))

        passwordId = str(uuid.uuid4())
        # Додаємо новий запис у таблицю Password як старий пароль
        insert_password_query = """
            INSERT INTO Password (PasswordId, UserId, OldPassword, PasswordChangeDate)
            SELECT %s, UserId, %s, NOW()
            FROM User
            WHERE Name = %s
        """
        cursor.execute(insert_password_query, (passwordId, new_password_hash, userName))

        print("Password updated successfully.")
    except Exception as e:
        print(f"An error occurred while updating the password: {e}")

def user_exists(cursor, name):
    cursor.execute("SELECT COUNT(*) FROM User WHERE Name = %s", (name,))
    return cursor.fetchone()[0] > 0

def hash_password(password):
    """Функція для хешування пароля."""
    return hashlib.sha256(password.encode()).hexdigest()

def create_user(cursor, username, password):

    user_id = str(uuid.uuid4())  # Генерація унікального ID для користувача
    creation_date = datetime.date.today()

    filepath = "..\\RR\\Source\\all.txt"
    check = checkByDictionary(password, filepath)

    if check is False:
        return

    cursor.execute(
        "INSERT INTO User (UserId, Name, PasswordCreationDate, CurrentPassword) VALUES (%s, %s, %s, %s)",
        (user_id, username, creation_date, hash_password(password))  # Хешуємо пароль перед зберіганням
    )

    password_id = str(uuid.uuid4())  # Генерація унікального ID для пароля
    cursor.execute(
        "INSERT INTO Password (PasswordId, UserId, OldPassword, PasswordChangeDate) VALUES (%s, %s, %s, %s)",
        (password_id, user_id, hash_password(password), creation_date)  # Зберігаємо хеш пароля
    )
    print("Користувача та пароль успішно створено.")
    
def getPasswordsByUserName(cursor, name):
    # Виконуємо SQL-запит, який з'єднує таблиці User та Password за UserId
    query = """
        SELECT p.OldPassword 
        FROM User u
        JOIN Password p ON u.UserId = p.UserId
        WHERE u.Name = %s
    """
    cursor.execute(query, (name,))
    result = cursor.fetchall()
    
    # Повертаємо всі знайдені паролі для заданого імені користувача
    return result

def logmenu(cursor,userName):

    while True:
        print("\nMenu:")
            # Показуємо додаткове меню, якщо користувач увійшов
        print(f"Logged in as {userName}")
        print("1. Change Password")
        print("0. Logout")

        choice = input("Choose an option: ")

        if choice == '1':
            # Викликаємо функцію зміни пароля для увійшовшого користувача
            createNewPassword(cursor, userName)
        elif choice == '0':
            print("Logging out...")
            return
        else:
            print("Invalid choice. Please try again.")
            

def can_change_password(cursor, userName):
    cursor.execute("SELECT PasswordCreationDate FROM User WHERE Name = %s", (userName,))
    result = cursor.fetchone()
    if result:
        password_creation_date = result[0]
        days_since_creation = (datetime.datetime.now().date() - password_creation_date).days
        if days_since_creation < MIN_PASSWORD_AGE_DAYS:
            print(f"Password must be at least {MIN_PASSWORD_AGE_DAYS} days old before it can be changed.")
            return False
    return True

def is_password_expired(cursor, userName):
    cursor.execute("SELECT PasswordCreationDate FROM User WHERE Name = %s", (userName,))
    result = cursor.fetchone()
    if result:
        password_creation_date = result[0]
        days_since_creation = (datetime.datetime.now().date() - password_creation_date).days
        if days_since_creation > MAX_PASSWORD_AGE_DAYS:
            print(f"Password has expired. Please change your password.")
            return True
    return False

def checkByDictionary(password, filepath):
    try:
        with open(filepath, 'r') as file:
            for line in file:
                common_password = line.strip() 
                if password in common_password:
                    print("The password is too common and is not secure.")
                    return False
    except FileNotFoundError:
        print(f"The file at {filepath} was not found.")
        return False
    print("The password is secure.")
    return True