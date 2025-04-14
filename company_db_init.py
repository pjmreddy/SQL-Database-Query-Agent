import sqlite3
import os
from pathlib import Path

def initialize_company_database():
    current_dir = Path(__file__).parent
    db_path = current_dir / "company.db"
    
    if db_path.exists():
        os.remove(db_path)
        print(f"Existing database removed at {db_path}")
    
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    
    cursor.execute("""
    CREATE TABLE EMPLOYEES(
        EMPLOYEE_ID INTEGER PRIMARY KEY,
        FIRST_NAME VARCHAR(50),
        LAST_NAME VARCHAR(50),
        EMAIL VARCHAR(100),
        PHONE VARCHAR(20),
        DEPARTMENT_ID INTEGER,
        POSITION VARCHAR(50),
        SALARY DECIMAL(10,2)
    )
    """)
    
    cursor.execute("""
    CREATE TABLE DEPARTMENTS(
        DEPARTMENT_ID INTEGER PRIMARY KEY,
        DEPARTMENT_NAME VARCHAR(50),
        LOCATION VARCHAR(100),
        MANAGER_ID INTEGER,
        BUDGET DECIMAL(15,2)
    )
    """)
    
    cursor.execute("""
    CREATE TABLE PROJECTS(
        PROJECT_ID INTEGER PRIMARY KEY,
        PROJECT_NAME VARCHAR(100),
        START_DATE DATE,
        END_DATE DATE,
        BUDGET DECIMAL(15,2),
        DEPARTMENT_ID INTEGER,
        STATUS VARCHAR(20)
    )
    """)
    
    cursor.execute("""
    CREATE TABLE CLIENTS(
        CLIENT_ID INTEGER PRIMARY KEY,
        CLIENT_NAME VARCHAR(100),
        CONTACT_PERSON VARCHAR(100),
        EMAIL VARCHAR(100),
        PHONE VARCHAR(20),
        ADDRESS VARCHAR(200),
        INDUSTRY VARCHAR(50)
    )
    """)
    
    cursor.execute("""
    CREATE TABLE INVENTORY(
        ITEM_ID INTEGER PRIMARY KEY,
        ITEM_NAME VARCHAR(100),
        CATEGORY VARCHAR(50),
        QUANTITY INTEGER,
        UNIT_PRICE DECIMAL(10,2),
        SUPPLIER VARCHAR(100),
        LAST_RESTOCK_DATE DATE
    )
    """)
    
    employees_data = [
        (1, "John", "Smith", "john.smith@company.com", "555-1234", 1, "Software Engineer", 85000.00),
        (2, "Sarah", "Johnson", "sarah.j@company.com", "555-2345", 1, "Senior Developer", 95000.00),
        (3, "Michael", "Brown", "m.brown@company.com", "555-3456", 2, "Marketing Specialist", 65000.00),
        (4, "Emily", "Davis", "emily.d@company.com", "555-4567", 3, "HR Manager", 78000.00),
        (5, "David", "Wilson", "d.wilson@company.com", "555-5678", 4, "Financial Analyst", 72000.00),
        (6, "Jessica", "Taylor", "j.taylor@company.com", "555-6789", 5, "Inventory Manager", 68000.00)
    ]
    
    for employee in employees_data:
        cursor.execute(
            "INSERT INTO EMPLOYEES (EMPLOYEE_ID, FIRST_NAME, LAST_NAME, EMAIL, PHONE, DEPARTMENT_ID, POSITION, SALARY) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            employee
        )
    
    # Insert sample data for DEPARTMENTS
    departments_data = [
        (1, "Engineering", "Building A, Floor 2", 2, 1500000.00),
        (2, "Marketing", "Building B, Floor 1", 3, 750000.00),
        (3, "Human Resources", "Building A, Floor 1", 4, 500000.00),
        (4, "Finance", "Building C, Floor 3", 5, 1200000.00),
        (5, "Operations", "Building B, Floor 2", 6, 900000.00)
    ]
    
    for department in departments_data:
        cursor.execute(
            "INSERT INTO DEPARTMENTS (DEPARTMENT_ID, DEPARTMENT_NAME, LOCATION, MANAGER_ID, BUDGET) VALUES (?, ?, ?, ?, ?)",
            department
        )
    
    # Insert sample data for PROJECTS
    projects_data = [
        (1, "Website Redesign", "2023-01-15", "2023-06-30", 120000.00, 1, "Completed"),
        (2, "Mobile App Development", "2023-03-01", "2023-09-30", 200000.00, 1, "In Progress"),
        (3, "Q3 Marketing Campaign", "2023-07-01", "2023-09-30", 75000.00, 2, "In Progress"),
        (4, "Employee Training Program", "2023-02-15", "2023-05-15", 35000.00, 3, "Completed"),
        (5, "Financial Audit", "2023-04-01", "2023-04-30", 50000.00, 4, "Completed"),
        (6, "Inventory System Upgrade", "2023-08-01", "2023-12-31", 90000.00, 5, "Planned")
    ]
    
    for project in projects_data:
        cursor.execute(
            "INSERT INTO PROJECTS (PROJECT_ID, PROJECT_NAME, START_DATE, END_DATE, BUDGET, DEPARTMENT_ID, STATUS) VALUES (?, ?, ?, ?, ?, ?, ?)",
            project
        )
    
    # Insert sample data for CLIENTS
    clients_data = [
        (1, "TechCorp Inc.", "Robert Chen", "r.chen@techcorp.com", "555-7890", "123 Tech Blvd, San Francisco, CA", "Technology"),
        (2, "Global Retail Ltd.", "Amanda Lewis", "a.lewis@globalretail.com", "555-8901", "456 Market St, New York, NY", "Retail"),
        (3, "HealthPlus", "Dr. James Wilson", "j.wilson@healthplus.org", "555-9012", "789 Medical Dr, Chicago, IL", "Healthcare"),
        (4, "EduSmart", "Patricia Moore", "p.moore@edusmart.edu", "555-0123", "321 Campus Rd, Boston, MA", "Education"),
        (5, "GreenEnergy Co.", "Thomas Green", "t.green@greenenergy.com", "555-1234", "567 Solar Ave, Austin, TX", "Energy")
    ]
    
    for client in clients_data:
        cursor.execute(
            "INSERT INTO CLIENTS (CLIENT_ID, CLIENT_NAME, CONTACT_PERSON, EMAIL, PHONE, ADDRESS, INDUSTRY) VALUES (?, ?, ?, ?, ?, ?, ?)",
            client
        )
    
    # Insert sample data for INVENTORY
    inventory_data = [
        (1, "Laptop", "Electronics", 25, 1200.00, "TechSuppliers Inc.", "2023-03-15"),
        (2, "Office Desk", "Furniture", 15, 350.00, "Office Furnishings Ltd.", "2023-02-10"),
        (3, "Printer", "Electronics", 10, 450.00, "TechSuppliers Inc.", "2023-04-20"),
        (4, "Office Chair", "Furniture", 30, 175.00, "Office Furnishings Ltd.", "2023-02-10"),
        (5, "Paper Reams", "Office Supplies", 100, 5.50, "Stationery Plus", "2023-05-05"),
        (6, "Ink Cartridges", "Office Supplies", 40, 35.00, "Stationery Plus", "2023-05-05"),
        (7, "Server", "Electronics", 3, 3500.00, "TechSuppliers Inc.", "2023-01-25")
    ]
    
    for item in inventory_data:
        cursor.execute(
            "INSERT INTO INVENTORY (ITEM_ID, ITEM_NAME, CATEGORY, QUANTITY, UNIT_PRICE, SUPPLIER, LAST_RESTOCK_DATE) VALUES (?, ?, ?, ?, ?, ?, ?)",
            item
        )
    
    # Commit changes and close connection
    connection.commit()
    connection.close()
    
    print(f"Company database successfully created at {db_path} with sample data")

if __name__ == "__main__":
    initialize_company_database()