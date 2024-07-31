import pymysql

HOST = 'localhost'
USER = 'root'
PASSWORD = 'Dhavle@2427'
DATABASE = 'employee_data'

def connect_database():
    """Establish a connection to the database."""
    return pymysql.connect(host=HOST, user=USER, passwd=PASSWORD, database=DATABASE)

def create_table():
    """Create the 'data' table if it does not exist."""
    conn = connect_database()
    try:
        with conn.cursor() as cursor:
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS data (
                    Id VARCHAR(20) PRIMARY KEY,
                    Name VARCHAR(50),
                    Phone VARCHAR(15),
                    Role VARCHAR(50),
                    Gender VARCHAR(20),
                    Salary DECIMAL(10,2)
                )
            ''')
        conn.commit()
    finally:
        conn.close()

def insert(id, name, phone, role, gender, salary):
    """Insert a new employee into the 'data' table."""
    conn = connect_database()
    try:
        with conn.cursor() as cursor:
            cursor.execute('INSERT INTO data (Id, Name, Phone, Role, Gender, Salary) VALUES (%s, %s, %s, %s, %s, %s)', 
                           (id, name, phone, role, gender, salary))
        conn.commit()
    finally:
        conn.close()

def id_exists(id):
    """Check if an employee ID already exists in the 'data' table."""
    conn = connect_database()
    try:
        with conn.cursor() as cursor:
            cursor.execute('SELECT COUNT(*) FROM data WHERE Id = %s', (id,))
            result = cursor.fetchone()
        return result[0] > 0
    finally:
        conn.close()

def fetch_employees():
    """Fetch all employees from the 'data' table."""
    conn = connect_database()
    try:
        with conn.cursor() as cursor:
            cursor.execute('SELECT * FROM data')
            result = cursor.fetchall()
        return result
    finally:
        conn.close()

def search_employees(column, value):
    """Search employees by a specified column and value."""
    conn = connect_database()
    try:
        with conn.cursor() as cursor:
            query = f'SELECT * FROM data WHERE {column} LIKE %s'
            cursor.execute(query, ('%' + value + '%',))
            result = cursor.fetchall()
        return result
    finally:
        conn.close()

def update_employee(old_id, new_id, name, phone, role, gender, salary):
    """Update an employee's details."""
    conn = connect_database()
    try:
        with conn.cursor() as cursor:
            cursor.execute('''
                UPDATE data SET Id = %s, Name = %s, Phone = %s, Role = %s, Gender = %s, Salary = %s
                WHERE Id = %s
            ''', (new_id, name, phone, role, gender, salary, old_id))
        conn.commit()
    finally:
        conn.close()

def delete_employee(id):
    """Delete an employee by ID."""
    conn = connect_database()
    try:
        with conn.cursor() as cursor:
            cursor.execute('DELETE FROM data WHERE Id = %s', (id,))
        conn.commit()
    finally:
        conn.close()

def delete_all_employees():
    """Delete all employees from the 'data' table."""
    conn = connect_database()
    try:
        with conn.cursor() as cursor:
            cursor.execute('DELETE FROM data')
        conn.commit()
    finally:
        conn.close()

create_table()
