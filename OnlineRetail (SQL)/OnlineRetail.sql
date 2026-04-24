CREATE DATABASE OnlineRetail;
USE OnlineRetail;

CREATE TABLE Customers (
    customer_id INT PRIMARY KEY,
    name VARCHAR(100),
    city VARCHAR(100)
);

CREATE TABLE Products (
    product_id INT PRIMARY KEY,
    name VARCHAR(100),
    category VARCHAR(100),
    price DECIMAL(10,2)
);

CREATE TABLE Orders (
    order_id INT PRIMARY KEY,
    customer_id INT,
    order_date DATE,
    FOREIGN KEY (customer_id) REFERENCES Customers(customer_id)
);

CREATE TABLE Order_Items (
    order_id INT,
    product_id INT,
    quantity INT,
    FOREIGN KEY (order_id) REFERENCES Orders(order_id),
    FOREIGN KEY (product_id) REFERENCES Products(product_id)
);

INSERT INTO Customers VALUES
(1, 'Amit', 'Hyderabad'),
(2, 'Ravi', 'Bangalore'),
(3, 'Sita', 'Chennai'),
(4, 'Neha', 'Delhi'),
(5, 'Arjun', 'Mumbai');

INSERT INTO Products VALUES
(101, 'Laptop', 'Electronics', 60000),
(102, 'Phone', 'Electronics', 20000),
(103, 'Shoes', 'Fashion', 3000),
(104, 'Watch', 'Accessories', 5000),
(105, 'Headphones', 'Electronics', 2500);

INSERT INTO Orders VALUES
(1001, 1, '2026-04-10'),
(1002, 2, '2026-04-15'),
(1003, 1, '2025-02-05'),
(1004, 3, '2026-03-20'),
(1005, 4, '2025-03-01');

INSERT INTO Order_Items VALUES
(1001, 101, 1),
(1001, 105, 2),
(1002, 102, 1),
(1003, 103, 2),
(1003, 104, 1),
(1004, 101, 1),
(1005, 105, 3);

--- Top-Selling Products ---
SELECT p.product_id, p.name, SUM(oi.quantity) AS total_sold
FROM Order_Items oi
JOIN Products p ON oi.product_id = p.product_id
GROUP BY p.product_id, p.name
ORDER BY total_sold DESC;

--- Most Valuable Customers ---
SELECT c.customer_id, c.name,
       SUM(p.price * oi.quantity) AS total_spent
FROM Customers c
JOIN Orders o ON c.customer_id = o.customer_id
JOIN Order_Items oi ON o.order_id = oi.order_id
JOIN Products p ON oi.product_id = p.product_id
GROUP BY c.customer_id, c.name
ORDER BY total_spent DESC;

--- Monthly revenue Calculation ---
SELECT DATE_FORMAT(o.order_date, '%Y-%m') AS month,
       SUM(p.price * oi.quantity) AS revenue
FROM Orders o
JOIN Order_Items oi ON o.order_id = oi.order_id
JOIN Products p ON oi.product_id = p.product_id
GROUP BY month
ORDER BY month;

--- Category-Wise Sales Analysis ---
SELECT p.category,
       SUM(oi.quantity) AS total_items_sold,
       SUM(p.price * oi.quantity) AS total_revenue
FROM Order_Items oi
JOIN Products p ON oi.product_id = p.product_id
GROUP BY p.category
ORDER BY total_revenue DESC;

--- Inactive Customers ---
SELECT c.customer_id, c.name
FROM Customers c
WHERE c.customer_id NOT IN (
    SELECT DISTINCT customer_id
    FROM Orders
    WHERE order_date >= DATE_SUB(CURDATE(), INTERVAL 2 MONTH)
);
