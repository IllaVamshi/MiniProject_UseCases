# Database Created 

CREATE DATABASE DigitalLibrary;
USE DigitalLibrary;

# Students Table

CREATE TABLE Students (
    StudentID INT PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(100),
    Email VARCHAR(100),
    JoinDate DATE,
    Status VARCHAR(20)
);

# Books Table

CREATE TABLE Books (
    BookID INT PRIMARY KEY AUTO_INCREMENT,
    Title VARCHAR(150),
    Author VARCHAR(100),
    Category VARCHAR(50)
);

# IssuedBooks Table

CREATE TABLE IssuedBooks (
    IssueID INT PRIMARY KEY AUTO_INCREMENT,
    StudentID INT,
    BookID INT,
    IssueDate DATE,
    ReturnDate DATE,
    FOREIGN KEY (StudentID) REFERENCES Students(StudentID),
    FOREIGN KEY (BookID) REFERENCES Books(BookID)
);

# Insert Students

INSERT INTO Students (Name, Email, JoinDate, Status) VALUES
('Ravi Kumar', 'ravi@gmail.com', '2021-06-15', 'Active'),
('Sneha Reddy', 'sneha@gmail.com', '2022-01-10', 'Active'),
('Arjun Patel', 'arjun@gmail.com', '2020-03-22', 'Active'),
('Meena Sharma', 'meena@gmail.com', '2019-07-05', 'Active'),
('Kiran Rao', 'kiran@gmail.com', '2018-11-30', 'Active');

# Insert Books

INSERT INTO Books (Title, Author, Category) VALUES
('The Alchemist', 'Paulo Coelho', 'Fiction'),
('A Brief History of Time', 'Stephen Hawking', 'Science'),
('Wings of Fire', 'A.P.J Abdul Kalam', 'Biography'),
('The Great Gatsby', 'F. Scott Fitzgerald', 'Fiction'),
('Sapiens', 'Yuval Noah Harari', 'History');

# Insert IssuedBooks

INSERT INTO IssuedBooks (StudentID, BookID, IssueDate, ReturnDate) VALUES
(1, 1, CURDATE() - INTERVAL 30 DAY, NULL),
(2, 2, CURDATE() - INTERVAL 5 DAY, NULL),
(3, 3, CURDATE() - INTERVAL 20 DAY, CURDATE() - INTERVAL 10 DAY),
(1, 4, CURDATE() - INTERVAL 15 DAY, NULL),
(4, 5, '2022-01-01', '2022-01-10'),
(5, 1, '2021-02-15', '2021-02-25');

# Overdue Books (Penalty Report)

SELECT 
    S.StudentID,
    S.Name,
    B.Title,
    I.IssueDate,
    DATEDIFF(CURDATE(), I.IssueDate) AS Days_Borrowed
FROM IssuedBooks I
JOIN Students S ON I.StudentID = S.StudentID
JOIN Books B ON I.BookID = B.BookID
WHERE I.ReturnDate IS NULL
AND DATEDIFF(CURDATE(), I.IssueDate) > 14;

# Popularity Index

SELECT 
    B.Category,
    COUNT(*) AS Total_Borrows
FROM IssuedBooks I
JOIN Books B ON I.BookID = B.BookID
GROUP BY B.Category
ORDER BY Total_Borrows DESC;

# Preview Inactive Students

SELECT * FROM Students
WHERE StudentID NOT IN (
    SELECT DISTINCT StudentID
    FROM IssuedBooks
    WHERE IssueDate >= DATE_SUB(CURDATE(), INTERVAL 3 YEAR)
);

# Mark Inactive Students (Final Safe Solution)

UPDATE Students
SET Status = 'Inactive'
WHERE StudentID NOT IN (
    SELECT DISTINCT StudentID
    FROM IssuedBooks
    WHERE IssueDate >= DATE_SUB(CURDATE(), INTERVAL 3 YEAR)
);

# Verify Final Data

SELECT * FROM Students;