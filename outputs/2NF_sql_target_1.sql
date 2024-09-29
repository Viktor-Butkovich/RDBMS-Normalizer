CREATE TABLE CoffeeShopPromocodeUsedData (
    OrderID INT,
    DrinkID INT,
    FoodID INT,
    PromocodeUsed VARCHAR,
    PRIMARY KEY (OrderID, DrinkID, FoodID, PromocodeUsed),
    FOREIGN KEY (DrinkID) REFERENCES CoffeeShopDrinkData(DrinkID),
    FOREIGN KEY (FoodID) REFERENCES CoffeeShopFoodData(FoodID),
    FOREIGN KEY (OrderID) REFERENCES CoffeeShopOrderData(OrderID)
);
INSERT INTO CoffeeShopPromocodeUsedData VALUES(1001, 1, 0, 'NONE');
INSERT INTO CoffeeShopPromocodeUsedData VALUES(1002, 2, 3, 'SUMMERFUN');
INSERT INTO CoffeeShopPromocodeUsedData VALUES(1002, 3, 3, 'SUMMERFUN');
INSERT INTO CoffeeShopPromocodeUsedData VALUES(1003, 4, 0, 'SUMMERFUN');
INSERT INTO CoffeeShopPromocodeUsedData VALUES(1003, 4, 0, 'JUNEVIP');

CREATE TABLE CoffeeShopDrinkIngredientData (
    OrderID INT,
    DrinkID INT,
    FoodID INT,
    DrinkIngredient VARCHAR,
    PRIMARY KEY (OrderID, DrinkID, FoodID, DrinkIngredient),
    FOREIGN KEY (DrinkID) REFERENCES CoffeeShopDrinkData(DrinkID),
    FOREIGN KEY (FoodID) REFERENCES CoffeeShopFoodData(FoodID),
    FOREIGN KEY (OrderID) REFERENCES CoffeeShopOrderData(OrderID)
);
INSERT INTO CoffeeShopDrinkIngredientData VALUES(1001, 1, 0, 'Espresso');
INSERT INTO CoffeeShopDrinkIngredientData VALUES(1001, 1, 0, 'Oat Milk');
INSERT INTO CoffeeShopDrinkIngredientData VALUES(1002, 2, 3, 'Espresso');
INSERT INTO CoffeeShopDrinkIngredientData VALUES(1002, 2, 3, 'Vanilla Syrup');
INSERT INTO CoffeeShopDrinkIngredientData VALUES(1002, 2, 3, 'Milk');
INSERT INTO CoffeeShopDrinkIngredientData VALUES(1002, 2, 3, 'Ice');
INSERT INTO CoffeeShopDrinkIngredientData VALUES(1002, 3, 3, 'Matcha');
INSERT INTO CoffeeShopDrinkIngredientData VALUES(1002, 3, 3, 'Coconut Milk');
INSERT INTO CoffeeShopDrinkIngredientData VALUES(1002, 3, 3, 'Ice');
INSERT INTO CoffeeShopDrinkIngredientData VALUES(1003, 4, 0, 'Coffee');
INSERT INTO CoffeeShopDrinkIngredientData VALUES(1003, 4, 0, 'Ice');
INSERT INTO CoffeeShopDrinkIngredientData VALUES(1003, 4, 0, 'Vanilla Syrup');
INSERT INTO CoffeeShopDrinkIngredientData VALUES(1003, 4, 0, 'Soy Milk');

CREATE TABLE CoffeeShopDrinkAllergenData (
    OrderID INT,
    DrinkID INT,
    FoodID INT,
    DrinkAllergen VARCHAR,
    PRIMARY KEY (OrderID, DrinkID, FoodID, DrinkAllergen),
    FOREIGN KEY (DrinkID) REFERENCES CoffeeShopDrinkData(DrinkID),
    FOREIGN KEY (FoodID) REFERENCES CoffeeShopFoodData(FoodID),
    FOREIGN KEY (OrderID) REFERENCES CoffeeShopOrderData(OrderID)
);
INSERT INTO CoffeeShopDrinkAllergenData VALUES(1001, 1, 0, 'Oat');
INSERT INTO CoffeeShopDrinkAllergenData VALUES(1002, 2, 3, 'Dairy');
INSERT INTO CoffeeShopDrinkAllergenData VALUES(1002, 2, 3, 'Nuts');
INSERT INTO CoffeeShopDrinkAllergenData VALUES(1002, 3, 3, 'Nuts');
INSERT INTO CoffeeShopDrinkAllergenData VALUES(1003, 4, 0, 'Nuts');
INSERT INTO CoffeeShopDrinkAllergenData VALUES(1003, 4, 0, 'Soy');

CREATE TABLE CoffeeShopFoodIngredientData (
    OrderID INT,
    DrinkID INT,
    FoodID INT,
    FoodIngredient VARCHAR,
    PRIMARY KEY (OrderID, DrinkID, FoodID, FoodIngredient),
    FOREIGN KEY (DrinkID) REFERENCES CoffeeShopDrinkData(DrinkID),
    FOREIGN KEY (FoodID) REFERENCES CoffeeShopFoodData(FoodID),
    FOREIGN KEY (OrderID) REFERENCES CoffeeShopOrderData(OrderID)
);
INSERT INTO CoffeeShopFoodIngredientData VALUES(1001, 1, 0, 'NONE');
INSERT INTO CoffeeShopFoodIngredientData VALUES(1003, 4, 0, 'NONE');
INSERT INTO CoffeeShopFoodIngredientData VALUES(1002, 2, 3, 'Flour');
INSERT INTO CoffeeShopFoodIngredientData VALUES(1002, 2, 3, 'Sugar');
INSERT INTO CoffeeShopFoodIngredientData VALUES(1002, 2, 3, 'Blueberries');
INSERT INTO CoffeeShopFoodIngredientData VALUES(1002, 2, 3, 'Eggs');
INSERT INTO CoffeeShopFoodIngredientData VALUES(1002, 3, 3, 'Flour');
INSERT INTO CoffeeShopFoodIngredientData VALUES(1002, 3, 3, 'Sugar');
INSERT INTO CoffeeShopFoodIngredientData VALUES(1002, 3, 3, 'Blueberries');
INSERT INTO CoffeeShopFoodIngredientData VALUES(1002, 3, 3, 'Eggs');

CREATE TABLE CoffeeShopFoodAllergenData (
    OrderID INT,
    DrinkID INT,
    FoodID INT,
    FoodAllergen VARCHAR,
    PRIMARY KEY (OrderID, DrinkID, FoodID, FoodAllergen),
    FOREIGN KEY (DrinkID) REFERENCES CoffeeShopDrinkData(DrinkID),
    FOREIGN KEY (FoodID) REFERENCES CoffeeShopFoodData(FoodID),
    FOREIGN KEY (OrderID) REFERENCES CoffeeShopOrderData(OrderID)
);
INSERT INTO CoffeeShopFoodAllergenData VALUES(1001, 1, 0, 'NONE');
INSERT INTO CoffeeShopFoodAllergenData VALUES(1003, 4, 0, 'NONE');
INSERT INTO CoffeeShopFoodAllergenData VALUES(1002, 2, 3, 'Wheat');
INSERT INTO CoffeeShopFoodAllergenData VALUES(1002, 2, 3, 'Egg');
INSERT INTO CoffeeShopFoodAllergenData VALUES(1002, 3, 3, 'Wheat');
INSERT INTO CoffeeShopFoodAllergenData VALUES(1002, 3, 3, 'Egg');

CREATE TABLE CoffeeShopOrderData (
    OrderID INT,
    Date DATE,
    TotalCost FLOAT,
    TotalDrinkCost FLOAT,
    TotalFoodCost FLOAT,
    CustomerID INT,
    CustomerName VARCHAR,
    PRIMARY KEY (OrderID)
);
INSERT INTO CoffeeShopOrderData VALUES(1001, 6/30/2024, 7.25, 7.25, 0.00, 1, 'Alice Brown');
INSERT INTO CoffeeShopOrderData VALUES(1002, 6/30/2026, 9.98, 5.99, 3.99, 2, 'David Miller');
INSERT INTO CoffeeShopOrderData VALUES(1003, 6/29/2024, 115.00, 115.00, 0.00, 3, 'Emily Garcia');

CREATE TABLE CoffeeShopDrinkData (
    OrderID INT,
    DrinkID INT,
    DrinkName VARCHAR,
    DrinkSize VARCHAR,
    DrinkQuantity INT,
    Milk VARCHAR,
    PRIMARY KEY (OrderID, DrinkID),
    FOREIGN KEY (OrderID) REFERENCES CoffeeShopOrderData(OrderID)
);
INSERT INTO CoffeeShopDrinkData VALUES(1001, 1, 'Caffe Latte', 'Grande', 1, 'ND');
INSERT INTO CoffeeShopDrinkData VALUES(1002, 2, 'Iced Caramel Macchiato', 'Tall', 2, 'ND');
INSERT INTO CoffeeShopDrinkData VALUES(1002, 3, 'Iced Matcha Latte', 'Grande', 1, 'ND');
INSERT INTO CoffeeShopDrinkData VALUES(1003, 4, 'Vanilla Bean Frappuccino', 'Venti', 8, 'ND');

CREATE TABLE CoffeeShopFoodData (
    OrderID INT,
    FoodID INT,
    FoodName VARCHAR,
    FoodQuantity INT,
    PRIMARY KEY (OrderID, FoodID),
    FOREIGN KEY (OrderID) REFERENCES CoffeeShopOrderData(OrderID)
);
INSERT INTO CoffeeShopFoodData VALUES(1001, 0, 'NULL', 0);
INSERT INTO CoffeeShopFoodData VALUES(1002, 3, 'Blueberry Muffin', 1);
INSERT INTO CoffeeShopFoodData VALUES(1003, 0, 'NULL', 0);