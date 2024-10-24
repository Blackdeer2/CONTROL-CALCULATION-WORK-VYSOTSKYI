import datetime
import hashlib
import uuid

MIN_PASSWORD_AGE_DAYS = 1
MAX_PASSWORD_AGE_DAYS = 30

def login(cursor, user_name, password):
    
    cursor.execute("SELECT CurrentPassword FROM User WHERE Name = %s", (user_name,))
    result = cursor.fetchone()
    
    if result is None:
        print("User does not exist.")
        return
    
    stored_password_hash = result[0]

    password_hash = hashlib.sha256(password.encode()).hexdigest()

    if password_hash == stored_password_hash:
        print("Login successful!")
        return user_name
    else:
        print("Invalid password. Please try again.")
        return None

def createNewPassword(cursor, userName, newPassword):

    oldPasswords = getPasswordsByUserName(cursor, userName)
    
    new_password_hash = hashlib.sha256(newPassword.encode()).hexdigest()

    for (oldPassword,) in oldPasswords:
        if new_password_hash == oldPassword:
             return "New password must not match any of the previous passwords."
            
        
    filepath = "..\\RR\\Source\\all.txt"
    check = checkByDictionary(newPassword, filepath)

    if check is False:
        return "Password is not secure."
        

    try:
        update_user_query = """
            UPDATE User
            SET CurrentPassword = %s, PasswordCreationDate = NOW()
            WHERE Name = %s
        """
        cursor.execute(update_user_query, (new_password_hash, userName))

        passwordId = str(uuid.uuid4())
        insert_password_query = """
            INSERT INTO Password (PasswordId, UserId, OldPassword, PasswordChangeDate)
            SELECT %s, UserId, %s, NOW()
            FROM User
            WHERE Name = %s
        """
        cursor.execute(insert_password_query, (passwordId, new_password_hash, userName))

        return "Password updated successfully."
    except Exception as e:
        print(f"An error occurred while updating the password: {e}")

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def create_user(cursor, username, password):

    user_id = str(uuid.uuid4())  
    creation_date = datetime.date.today()

    filepath = "..\\RR\\Source\\all.txt"
    check = checkByDictionary(password, filepath)

    if check is False:
        return

    cursor.execute(
        "INSERT INTO User (UserId, Name, PasswordCreationDate, CurrentPassword) VALUES (%s, %s, %s, %s)",
        (user_id, username, creation_date, hash_password(password)) 
    )

    password_id = str(uuid.uuid4())  
    cursor.execute(
        "INSERT INTO Password (PasswordId, UserId, OldPassword, PasswordChangeDate) VALUES (%s, %s, %s, %s)",
        (password_id, user_id, hash_password(password), creation_date)
    )
    return True
    
def getPasswordsByUserName(cursor, name):
    query = """
        SELECT p.OldPassword 
        FROM User u
        JOIN Password p ON u.UserId = p.UserId
        WHERE u.Name = %s
    """
    cursor.execute(query, (name,))
    result = cursor.fetchall()
    return result

def check_unique_username(cursor, name):
    query = """
        SELECT COUNT(*)
        FROM User u
        WHERE u.Name = %s
    """
    cursor.execute(query, (name,))
    result = cursor.fetchone()

    if result and result[0] == 0:
        return True
    else:
        return False
        
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
        with open(filepath, 'r', encoding="utf-8") as file:
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