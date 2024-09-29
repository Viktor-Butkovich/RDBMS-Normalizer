CREATE TABLE CoffeeShopData (
    OrderID INT,
    Date DATE,
    PromocodeUsed LIST[VARCHAR],
    TotalCost FLOAT,
    TotalDrinkCost FLOAT,
    TotalFoodCost FLOAT,
    CustomerID INT,
    CustomerName VARCHAR,
    DrinkID INT,
    DrinkName VARCHAR,
    DrinkSize VARCHAR,
    DrinkQuantity INT,
    Milk VARCHAR,
    DrinkIngredient LIST[VARCHAR],
    DrinkAllergen LIST[VARCHAR],
    FoodID INT,
    FoodName VARCHAR,
    FoodQuantity INT,
    FoodIngredient LIST[VARCHAR],
    FoodAllergen LIST[VARCHAR],
    PRIMARY KEY (OrderID, DrinkID, FoodID)
);
INSERT INTO CoffeeShopData VALUES(1001, 6/30/2024, NULL, 7.25, 7.25, 0.00, 1, 'Alice Brown', 1, 'Caffe Latte', 'Grande', 1, 'ND', '[Espresso, Oat Milk]', '[Oat]', 0, 'NULL', 0, NULL, NULL);
INSERT INTO CoffeeShopData VALUES(1002, 6/30/2026, '[SUMMERFUN]', 9.98, 5.99, 3.99, 2, 'David Miller', 2, 'Iced Caramel Macchiato', 'Tall', 2, 'ND', '[Espresso, Vanilla Syrup, Milk, Ice]', '[Dairy, Nuts]', 3, 'Blueberry Muffin', 1, '[Flour, Sugar, Blueberries, Eggs]', '[Wheat, Egg]');
INSERT INTO CoffeeShopData VALUES(1002, 6/30/2026, '[SUMMERFUN]', 9.98, 5.99, 3.99, 2, 'David Miller', 3, 'Iced Matcha Latte', 'Grande', 1, 'ND', '[Matcha, Coconut Milk, Ice]', '[Nuts]', 3, 'Blueberry Muffin', 1, '[Flour, Sugar, Blueberries, Eggs]', '[Wheat, Egg]');
INSERT INTO CoffeeShopData VALUES(1003, 6/29/2024, '[SUMMERFUN, JUNEVIP]', 115.00, 115.00, 0.00, 3, 'Emily Garcia', 4, 'Vanilla Bean Frappuccino', 'Venti', 8, 'ND', '[Coffee, Ice, Vanilla Syrup, Soy Milk]', '[Nuts, Soy]', 0, 'NULL', 0, NULL, NULL);