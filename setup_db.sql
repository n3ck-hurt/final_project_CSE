-- Create and populate the sari-sari_store database
CREATE DATABASE IF NOT EXISTS `sari-sari_store`;
USE `sari-sari_store`;

-- Fix 1: Correct product table structure
CREATE TABLE IF NOT EXISTS product (
    id INT AUTO_INCREMENT PRIMARY KEY,
    product_name VARCHAR(255) NOT NULL,
    category VARCHAR(50) NOT NULL,
    unit VARCHAR(20) NOT NULL,
    price DECIMAL(10, 2) DEFAULT 0.00,
    quantity INT DEFAULT 0,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Fix 2: Correct supplier table structure
CREATE TABLE IF NOT EXISTS supplier (
    id INT AUTO_INCREMENT PRIMARY KEY,
    supplier_name VARCHAR(255) NOT NULL,
    contact_number VARCHAR(20) NOT NULL,
    address TEXT NOT NULL,
    contact_person VARCHAR(255),
    phone VARCHAR(20),
    email VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Fix 3: Correct icecream table structure
CREATE TABLE IF NOT EXISTS icecream (
    id INT AUTO_INCREMENT PRIMARY KEY,
    flavor VARCHAR(255) NOT NULL,
    size VARCHAR(50) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    stock INT NOT NULL DEFAULT 0,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Clear existing data
TRUNCATE TABLE product;
ALTER TABLE product AUTO_INCREMENT = 1;

-- Insert product data (matches your INSERT statement)
INSERT INTO product (product_name, category, unit, price, quantity) VALUES
('Sachet Shampoo', 'Toiletries', 'sachet', 10.00, 100),
('Laundry Detergent', 'Toiletries', 'sachet', 15.00, 80),
('Bath Soap', 'Toiletries', 'piece', 20.00, 150),
('Toothpaste Sachet', 'Toiletries', 'sachet', 8.00, 120),
('Instant Noodles', 'Food', 'pack', 12.00, 200),
('Canned Sardines', 'Food', 'can', 25.00, 100),
('Canned Tuna', 'Food', 'can', 35.00, 80),
('Hotdog Pack', 'Food', 'pack', 50.00, 60),
('Bread Loaf', 'Food', 'piece', 40.00, 50),
('Bottled Water 500ml', 'Drinks', 'bottle', 15.00, 300),
('Soft Drink 1L', 'Drinks', 'bottle', 55.00, 150),
('Energy Drink', 'Drinks', 'can', 45.00, 100),
('Instant Coffee Sachet', 'Drinks', 'sachet', 10.00, 250),
('Sugar 1kg', 'Goods', 'bag', 60.00, 80),
('Rice 1kg', 'Goods', 'kg', 50.00, 200),
('Cooking Oil 500ml', 'Goods', 'bottle', 70.00, 90),
('Corned Beef Can', 'Food', 'can', 45.00, 70),
('Biscuits Small Pack', 'Snacks', 'pack', 25.00, 120),
('Potato Chips', 'Snacks', 'pack', 30.00, 100),
('Chocolate Bar', 'Snacks', 'piece', 35.00, 150);

-- Clear supplier data
TRUNCATE TABLE supplier;
ALTER TABLE supplier AUTO_INCREMENT = 1;

-- Insert supplier data (fixed column names)
INSERT INTO supplier (supplier_name, contact_number, address, contact_person, phone, email) VALUES
('ABC Distributors', '09123456789', 'Quezon City', 'Juan Dela Cruz', '09123456789', 'abc@distributors.com'),
('FreshFoods Supply Co.', '09987654321', 'Makati City', 'Maria Santos', '09987654321', 'freshfoods@supply.com'),
('Daily Essentials Trading', '09223334455', 'Pasig City', 'Pedro Reyes', '09223334455', 'daily@essentials.com'),
('Beverage Masters Inc.', '09112223344', 'Taguig City', 'Ana Torres', '09112223344', 'beverage@masters.com'),
('Snacks Unlimited', '09334445566', 'Caloocan City', 'Luis Gomez', '09334445566', 'snacks@unlimited.com'),
('GoodGoods Wholesale', '09175553322', 'Manila', 'Sofia Cruz', '09175553322', 'goodgoods@wholesale.com'),
('FastFood Products', '09556667788', 'Pasay City', 'Carlos Lim', '09556667788', 'fastfood@products.com'),
('TopChoice Retail Supply', '09443332211', 'Valenzuela City', 'Elena Tan', '09443332211', 'topchoice@retail.com'),
('Household Basics', '09221110099', 'Marikina City', 'Miguel Rivera', '09221110099', 'household@basics.com'),
('MegaDrinks Distributor', '09776655443', 'Mandaluyong City', 'Isabel Wong', '09776655443', 'megadrinks@distributor.com');

-- Clear icecream data
TRUNCATE TABLE icecream;
ALTER TABLE icecream AUTO_INCREMENT = 1;

-- Insert icecream data (added size column)
INSERT INTO icecream (flavor, size, price, stock, description) VALUES
('Selecta Super Thick Chocolate', '1.3L', 160.00, 12, 'Rich chocolate ice cream'),
('Selecta Very Strawberry', '1.3L', 160.00, 10, 'Fresh strawberry flavor'),
('Selecta Cookies & Cream', '1.3L', 165.00, 8, 'Cookies and cream delight'),
('Selecta Rocky Road', '1.3L', 170.00, 7, 'Chocolate with nuts and marshmallows'),
('Selecta Double Dutch', '1.3L', 165.00, 9, 'Double chocolate goodness'),
('Selecta Ube Keso', '1.3L', 165.00, 11, 'Ube and cheese combination'),
('Selecta Mango Graham', '1.3L', 175.00, 6, 'Mango with graham crackers'),
('Selecta Choco Mallow', '750ml', 85.00, 15, 'Chocolate with marshmallows'),
('Selecta Cookies & Cream', '750ml', 90.00, 14, 'Smaller cookies and cream'),
('Selecta Coffee Crumble', '750ml', 90.00, 12, 'Coffee flavor with crumbles'),
('Selecta Vanilla', '100ml Cup', 25.00, 35, 'Classic vanilla'),
('Selecta Chocolate', '100ml Cup', 25.00, 30, 'Classic chocolate'),
('Selecta Ube', '100ml Cup', 25.00, 28, 'Purple yam flavor'),
('Selecta Keso', '100ml Cup', 25.00, 25, 'Cheese flavor'),
('Selecta Cornetto Chocolate', 'Cone', 30.00, 40, 'Chocolate cone'),
('Selecta Cornetto Cookies & Cream', 'Cone', 30.00, 38, 'Cookies and cream cone'),
('Selecta Cornetto Black & White', 'Cone', 35.00, 32, 'Black and white chocolate cone'),
('Selecta Magnum Classic', '80ml Bar', 65.00, 22, 'Classic Magnum bar'),
('Selecta Magnum Almond', '80ml Bar', 70.00, 20, 'Magnum with almonds'),
('Selecta Magnum Infinity Chocolate', '80ml Bar', 75.00, 18, 'Infinite chocolate layers');

-- Verify the data
SELECT 'Database setup completed!' as message;
SELECT 'Products:' as table_name, COUNT(*) as count FROM product
UNION ALL
SELECT 'Suppliers:', COUNT(*) FROM supplier
UNION ALL
SELECT 'Ice Cream:', COUNT(*) FROM icecream;

-- Show sample data
SELECT 'Sample Products:' as '';
SELECT * FROM product LIMIT 5;

SELECT 'Sample Suppliers:' as '';
SELECT * FROM supplier LIMIT 5;

SELECT 'Sample Ice Cream:' as '';
SELECT * FROM icecream LIMIT 5;