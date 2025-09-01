--
-- File: database/seed_data.sql
--

-- Seed 10 sample users
INSERT INTO users (username, email, password_hash, full_name, shipping_address) VALUES
('juto-shogan', 'somtombonu53@gmail.com', 'hashed_pass_1', 'John Doe', '123 Main St, Anytown'),
('janesmith', 'jane.smith@example.com', 'hashed_pass_2', 'Jane Smith', '456 Oak Ave, Somewhere'),
('pete_jones', 'p.jones@example.com', 'hashed_pass_3', 'Peter Jones', '789 Pine Ln, Nowhere'),
('susan_williams', 's.williams@example.com', 'hashed_pass_4', 'Susan Williams', '101 Maple Rd, Elsewhere'),
('mark_taylor', 'm.taylor@example.com', 'hashed_pass_5', 'Mark Taylor', '202 Birch Blvd, Nowhereville'),
('lisa_brown', 'lisa.brown@example.com', 'hashed_pass_6', 'Lisa Brown', '303 Cedar Dr, Anyplace'),
('david_white', 'dave.white@example.com', 'hashed_pass_7', 'David White', '404 Redwood St, Somewhere'),
('maria_garcia', 'maria.g@example.com', 'hashed_pass_8', 'Maria Garcia', '505 Willow Ave, Anytown'),
('michael_kim', 'mike.k@example.com', 'hashed_pass_9', 'Michael Kim', '606 Ash Way, Elsewhere'),
('linda_davis', 'linda.d@example.com', 'hashed_pass_10', 'Linda Davis', '707 Poplar Pkwy, Somewhere');

-- Seed 10 sample products
INSERT INTO products (product_name, description, price, stock_quantity) VALUES
('Laptop Pro', 'A powerful laptop for professionals.', 1200.00, 50),
('Wireless Mouse', 'Ergonomic mouse with long battery life.', 25.50, 200),
('Mechanical Keyboard', 'RGB keyboard with clicky switches.', 99.99, 150),
('4K Monitor', 'Ultra-HD display with thin bezels.', 350.75, 75),
('Webcam', 'HD webcam for video conferencing.', 45.00, 100),
('USB-C Hub', 'Multiport adapter with HDMI and USB 3.0.', 65.00, 120),
('External SSD', '1TB portable high-speed storage.', 180.00, 80),
('Gaming Headset', 'Surround sound headset with mic.', 75.00, 90),
('Smartphone Stand', 'Adjustable stand for phones.', 20.00, 300),
('Portable Charger', '10000mAh power bank.', 40.00, 250);

-- Seed reviews
INSERT INTO reviews (product_id, user_id, rating, review_text) VALUES
((SELECT product_id FROM products WHERE product_name = 'Laptop Pro'), (SELECT user_id FROM users WHERE username = 'juto-shogan'), 5, 'Absolutely love this laptop! Fast and reliable.'),
((SELECT product_id FROM products WHERE product_name = 'Wireless Mouse'), (SELECT user_id FROM users WHERE username = 'janesmith'), 4, 'Comfortable and works great. Could be a little cheaper.'),
((SELECT product_id FROM products WHERE product_name = 'Mechanical Keyboard'), (SELECT user_id FROM users WHERE username = 'pete_jones'), 5, 'Best keyboard I have ever used. Typing is a joy.'),
((SELECT product_id FROM products WHERE product_name = '4K Monitor'), (SELECT user_id FROM users WHERE username = 'susan_williams'), 3, 'The picture is good, but the stand is a bit wobbly.'),
((SELECT product_id FROM products WHERE product_name = 'Webcam'), (SELECT user_id FROM users WHERE username = 'mark_taylor'), 4, 'Decent quality for video calls, but audio could be better.'),
((SELECT product_id FROM products WHERE product_name = 'USB-C Hub'), (SELECT user_id FROM users WHERE username = 'lisa_brown'), 5, 'Super handy, works with my laptop perfectly.'),
((SELECT product_id FROM products WHERE product_name = 'External SSD'), (SELECT user_id FROM users WHERE username = 'david_white'), 5, 'Blazing fast speeds! Highly recommend.'),
((SELECT product_id FROM products WHERE product_name = 'Gaming Headset'), (SELECT user_id FROM users WHERE username = 'maria_garcia'), 2, 'Mic quality is poor, not worth the price.'),
((SELECT product_id FROM products WHERE product_name = 'Smartphone Stand'), (SELECT user_id FROM users WHERE username = 'michael_kim'), 4, 'Cheap but does the job.'),
((SELECT product_id FROM products WHERE product_name = 'Portable Charger'), (SELECT user_id FROM users WHERE username = 'linda_davis'), 5, 'Charges my phone quickly and lasts long.');

-- Seed orders
INSERT INTO orders (user_id, total_amount, status) VALUES
((SELECT user_id FROM users WHERE username = 'juto-shogan'), 1225.50, 'completed'),
((SELECT user_id FROM users WHERE username = 'janesmith'), 350.75, 'shipped'),
((SELECT user_id FROM users WHERE username = 'pete_jones'), 99.99, 'pending'),
((SELECT user_id FROM users WHERE username = 'susan_williams'), 395.75, 'completed'),
((SELECT user_id FROM users WHERE username = 'mark_taylor'), 220.00, 'cancelled');

-- Seed order items
INSERT INTO order_items (order_id, product_id, quantity, price) VALUES
-- John Doe’s order (Laptop Pro + Mouse)
((SELECT order_id FROM orders WHERE user_id = (SELECT user_id FROM users WHERE username = 'juto-shogan') LIMIT 1), (SELECT product_id FROM products WHERE product_name = 'Laptop Pro'), 1, 1200.00),
((SELECT order_id FROM orders WHERE user_id = (SELECT user_id FROM users WHERE username = 'juto-shogan') LIMIT 1), (SELECT product_id FROM products WHERE product_name = 'Wireless Mouse'), 1, 25.50),

-- Jane Smith’s order (4K Monitor)
((SELECT order_id FROM orders WHERE user_id = (SELECT user_id FROM users WHERE username = 'janesmith') LIMIT 1), (SELECT product_id FROM products WHERE product_name = '4K Monitor'), 1, 350.75),

-- Peter Jones’s order (Mechanical Keyboard)
((SELECT order_id FROM orders WHERE user_id = (SELECT user_id FROM users WHERE username = 'pete_jones') LIMIT 1), (SELECT product_id FROM products WHERE product_name = 'Mechanical Keyboard'), 1, 99.99),

-- Susan Williams’s order (4K Monitor + Webcam)
((SELECT order_id FROM orders WHERE user_id = (SELECT user_id FROM users WHERE username = 'susan_williams') LIMIT 1), (SELECT product_id FROM products WHERE product_name = '4K Monitor'), 1, 350.75),
((SELECT order_id FROM orders WHERE user_id = (SELECT user_id FROM users WHERE username = 'susan_williams') LIMIT 1), (SELECT product_id FROM products WHERE product_name = 'Webcam'), 1, 45.00),

-- Mark Taylor’s cancelled order (External SSD + USB-C Hub)
((SELECT order_id FROM orders WHERE user_id = (SELECT user_id FROM users WHERE username = 'mark_taylor') LIMIT 1), (SELECT product_id FROM products WHERE product_name = 'External SSD'), 1, 180.00),
((SELECT order_id FROM orders WHERE user_id = (SELECT user_id FROM users WHERE username = 'mark_taylor') LIMIT 1), (SELECT product_id FROM products WHERE product_name = 'USB-C Hub'), 1, 40.00);
