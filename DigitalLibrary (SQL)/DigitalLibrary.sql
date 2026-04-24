create database DigitalLibrary;
use DigitalLibrary;

CREATE TABLE Students (
    StudentID INT PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(100) NOT NULL,
    Email VARCHAR(100) UNIQUE,
    JoinDate DATE NOT NULL,
    Status VARCHAR(20) DEFAULT 'Active'
);

CREATE TABLE Books (
    BookID INT PRIMARY KEY AUTO_INCREMENT,
    Title VARCHAR(150) NOT NULL,
    Author VARCHAR(100),
    Category VARCHAR(50)
);

CREATE TABLE IssuedBooks (
    IssueID INT PRIMARY KEY AUTO_INCREMENT,
    StudentID INT,
    BookID INT,
    IssueDate DATE NOT NULL,
    ReturnDate DATE,
    FOREIGN KEY (StudentID) REFERENCES Students(StudentID),
    FOREIGN KEY (BookID) REFERENCES Books(BookID)
);

INSERT INTO Students (Name, Email, JoinDate) VALUES
('Ravi Kumar', 'ravi@gmail.com', '2021-06-15'),
('Sneha Reddy', 'sneha@gmail.com', '2022-01-10'),
('Arjun Patel', 'arjun@gmail.com', '2020-03-22'),
('Meena Sharma', 'meena@gmail.com', '2019-07-05'),
('Kiran Rao', 'kiran@gmail.com', '2018-11-30');

INSERT INTO Books (Title, Author, Category) VALUES
('The Alchemist', 'Paulo Coelho', 'Fiction'),
('A Brief History of Time', 'Stephen Hawking', 'Science'),
('Wings of Fire', 'A.P.J Abdul Kalam', 'Biography'),
('The Great Gatsby', 'F. Scott Fitzgerald', 'Fiction'),
('Sapiens', 'Yuval Noah Harari', 'History');

INSERT INTO IssuedBooks (StudentID, BookID, IssueDate, ReturnDate) VALUES
(1, 1, '2026-03-20', NULL),
(2, 2, '2026-04-15', NULL),
(3, 3, '2026-03-25', '2026-04-05'),
(1, 4, '2026-04-01', NULL),
(4, 5, '2022-01-01', '2022-01-10'),
(5, 1, '2021-02-15', '2021-02-25');

--  Overdue Books ---
SELECT 
    S.StudentID,
    S.Name,
    B.Title,
    I.IssueDate,
    DATEDIFF(CURDATE(), I.IssueDate) AS Days_Borrowed,
    (DATEDIFF(CURDATE(), I.IssueDate) - 14) AS Overdue_Days
FROM IssuedBooks I
JOIN Students S ON I.StudentID = S.StudentID
JOIN Books B ON I.BookID = B.BookID
WHERE I.ReturnDate IS NULL
AND DATEDIFF(CURDATE(), I.IssueDate) > 14;

--- Most Borrowed Category ---
SELECT 
    B.Category,
    COUNT(*) AS Total_Borrows
FROM IssuedBooks I
JOIN Books B ON I.BookID = B.BookID
GROUP BY B.Category
ORDER BY Total_Borrows DESC;


SELECT *
FROM Students
WHERE StudentID NOT IN (
    SELECT DISTINCT StudentID
    FROM IssuedBooks
    WHERE IssueDate >= DATE_SUB(CURDATE(), INTERVAL 3 YEAR)
);

--- Inactive Students ---
SET SQL_SAFE_UPDATES = 0;

UPDATE Students
SET Status = 'Inactive'
WHERE StudentID NOT IN (
    SELECT DISTINCT StudentID
    FROM IssuedBooks
    WHERE IssueDate >= DATE_SUB(CURDATE(), INTERVAL 3 YEAR)
);

SET SQL_SAFE_UPDATES = 1;

SELECT * FROM Students;