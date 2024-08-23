-- Create test_Customers table
CREATE TABLE test_Customers (
    CustomerID INT PRIMARY KEY IDENTITY(1,1),
    FirstName NVARCHAR(50),
    LastName NVARCHAR(50),
    Email NVARCHAR(100)
);

-- Create test_Invoices table
CREATE TABLE test_Invoices (
    InvoiceID INT PRIMARY KEY IDENTITY(1,1),
    CustomerID INT,
    InvoiceDate DATE,
    TotalAmount DECIMAL(10, 2),
    FOREIGN KEY (CustomerID) REFERENCES test_Customers(CustomerID)
);

-- Create test_Employees table
CREATE TABLE test_Employees (
    EmployeeID INT PRIMARY KEY IDENTITY(1,1),
    FirstName NVARCHAR(50),
    LastName NVARCHAR(50),
    Department NVARCHAR(50)
);

-- Create test_Timesheets table
CREATE TABLE test_Timesheets (
    TimesheetID INT PRIMARY KEY IDENTITY(1,1),
    EmployeeID INT,
    WorkDate DATE,
    HoursWorked DECIMAL(4, 2),
    FOREIGN KEY (EmployeeID) REFERENCES test_Employees(EmployeeID)
);

-- Insert sample data into test_Customers
INSERT INTO test_Customers (FirstName, LastName, Email)
VALUES 
    ('John', 'Doe', 'john.doe@example.com'),
    ('Jane', 'Smith', 'jane.smith@example.com'),
    ('Bob', 'Johnson', 'bob.johnson@example.com'),
    ('Alice', 'Williams', 'alice.williams@example.com'),
    ('Charlie', 'Brown', 'charlie.brown@example.com');

-- Insert sample data into test_Invoices
INSERT INTO test_Invoices (CustomerID, InvoiceDate, TotalAmount)
VALUES 
    (1, '2023-01-15', 1500.00),
    (1, '2023-02-20', 2000.00),
    (2, '2023-01-25', 1750.00),
    (3, '2023-02-10', 3000.00),
    (4, '2023-03-05', 2500.00),
    (5, '2023-03-15', 1800.00),
    (2, '2023-04-01', 2200.00),
    (3, '2023-04-10', 2800.00),
    (4, '2023-05-05', 3200.00),
    (5, '2023-05-20', 1900.00);

-- Insert sample data into test_Employees
INSERT INTO test_Employees (FirstName, LastName, Department)
VALUES 
    ('Michael', 'Scott', 'Management'),
    ('Dwight', 'Schrute', 'Sales'),
    ('Jim', 'Halpert', 'Sales'),
    ('Pam', 'Beesly', 'Reception'),
    ('Angela', 'Martin', 'Accounting');

-- Insert sample data into test_Timesheets
INSERT INTO test_Timesheets (EmployeeID, WorkDate, HoursWorked)
VALUES 
    (1, '2023-05-01', 8.00),
    (1, '2023-05-02', 7.50),
    (2, '2023-05-01', 8.00),
    (2, '2023-05-02', 8.00),
    (3, '2023-05-01', 7.75),
    (3, '2023-05-02', 8.00),
    (4, '2023-05-01', 8.00),
    (4, '2023-05-02', 7.25),
    (5, '2023-05-01', 8.00),
    (5, '2023-05-02', 8.00),
    (1, '2023-05-03', 8.00),
    (2, '2023-05-03', 8.25),
    (3, '2023-05-03', 7.50),
    (4, '2023-05-03', 8.00),
    (5, '2023-05-03', 7.75);