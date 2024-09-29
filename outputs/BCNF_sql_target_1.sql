CREATE TABLE CoffeeShopPromocodeUsedData (
    OrderID INT,
    PromocodeUsed VARCHAR,
    PRIMARY KEY (OrderID, PromocodeUsed),
    FOREIGN KEY (OrderID) REFERENCES CoffeeShopOrderData(OrderID)
);
INSERT INTO CoffeeShopPromocodeUsedData VALUES(1001, 'NONE');
INSERT INTO CoffeeShopPromocodeUsedData VALUES(1002, 'SUMMERFUN');
INSERT INTO CoffeeShopPromocodeUsedData VALUES(1003, 'SUMMERFUN');
INSERT INTO CoffeeShopPromocodeUsedData VALUES(1003, 'JUNEVIP');

CREATE TABLE CoffeeShopDrinkIngredientData (
    OrderID INT,
    DrinkID INT,
    DrinkIngredient VARCHAR,
    PRIMARY KEY (OrderID, DrinkID, DrinkIngredient),
    FOREIGN KEY (DrinkID) REFERENCES CoffeeShopDrinkData(DrinkID),
    FOREIGN KEY (OrderID) REFERENCES CoffeeShopOrderData(OrderID)
);
INSERT INTO CoffeeShopDrinkIngredientData VALUES(1001, 1, 'Espresso');
INSERT INTO CoffeeShopDrinkIngredientData VALUES(1001, 1, 'Oat Milk');
INSERT INTO CoffeeShopDrinkIngredientData VALUES(1002, 2, 'Espresso');
INSERT INTO CoffeeShopDrinkIngredientData VALUES(1002, 2, 'Vanilla Syrup');
INSERT INTO CoffeeShopDrinkIngredientData VALUES(1002, 2, 'Milk');
INSERT INTO CoffeeShopDrinkIngredientData VALUES(1002, 2, 'Ice');
INSERT INTO CoffeeShopDrinkIngredientData VALUES(1002, 3, 'Matcha');
INSERT INTO CoffeeShopDrinkIngredientData VALUES(1002, 3, 'Coconut Milk');
INSERT INTO CoffeeShopDrinkIngredientData VALUES(1002, 3, 'Ice');
INSERT INTO CoffeeShopDrinkIngredientData VALUES(1003, 4, 'Coffee');
INSERT INTO CoffeeShopDrinkIngredientData VALUES(1003, 4, 'Ice');
INSERT INTO CoffeeShopDrinkIngredientData VALUES(1003, 4, 'Vanilla Syrup');
INSERT INTO CoffeeShopDrinkIngredientData VALUES(1003, 4, 'Soy Milk');

CREATE TABLE CoffeeShopDrinkAllergenData (
    OrderID INT,
    DrinkID INT,
    DrinkAllergen VARCHAR,
    PRIMARY KEY (OrderID, DrinkID, DrinkAllergen),
    FOREIGN KEY (DrinkID) REFERENCES CoffeeShopDrinkData(DrinkID),
    FOREIGN KEY (OrderID) REFERENCES CoffeeShopOrderData(OrderID)
);
INSERT INTO CoffeeShopDrinkAllergenData VALUES(1001, 1, 'Oat');
INSERT INTO CoffeeShopDrinkAllergenData VALUES(1002, 2, 'Dairy');
INSERT INTO CoffeeShopDrinkAllergenData VALUES(1002, 2, 'Nuts');
INSERT INTO CoffeeShopDrinkAllergenData VALUES(1002, 3, 'Nuts');
INSERT INTO CoffeeShopDrinkAllergenData VALUES(1003, 4, 'Nuts');
INSERT INTO CoffeeShopDrinkAllergenData VALUES(1003, 4, 'Soy');

CREATE TABLE CoffeeShopFoodIngredientData (
    OrderID INT,
    FoodID INT,
    FoodIngredient VARCHAR,
    PRIMARY KEY (OrderID, FoodID, FoodIngredient),
    FOREIGN KEY (FoodID) REFERENCES CoffeeShopFoodData(FoodID),
    FOREIGN KEY (OrderID) REFERENCES CoffeeShopOrderData(OrderID)
);
INSERT INTO CoffeeShopFoodIngredientData VALUES(1001, 0, 'NONE');
INSERT INTO CoffeeShopFoodIngredientData VALUES(1003, 0, 'NONE');
INSERT INTO CoffeeShopFoodIngredientData VALUES(1002, 3, 'Flour');
INSERT INTO CoffeeShopFoodIngredientData VALUES(1002, 3, 'Sugar');
INSERT INTO CoffeeShopFoodIngredientData VALUES(1002, 3, 'Blueberries');
INSERT INTO CoffeeShopFoodIngredientData VALUES(1002, 3, 'Eggs');

CREATE TABLE CoffeeShopFoodAllergenData (
    OrderID INT,
    FoodID INT,
    FoodAllergen VARCHAR,
    PRIMARY KEY (OrderID, FoodID, FoodAllergen),
    FOREIGN KEY (FoodID) REFERENCES CoffeeShopFoodData(FoodID),
    FOREIGN KEY (OrderID) REFERENCES CoffeeShopOrderData(OrderID)
);
INSERT INTO CoffeeShopFoodAllergenData VALUES(1001, 0, 'NONE');
INSERT INTO CoffeeShopFoodAllergenData VALUES(1003, 0, 'NONE');
INSERT INTO CoffeeShopFoodAllergenData VALUES(1002, 3, 'Wheat');
INSERT INTO CoffeeShopFoodAllergenData VALUES(1002, 3, 'Egg');

CREATE TABLE CoffeeShopOrderData (
    OrderID INT,
    Date DATE,
    TotalCost FLOAT,
    TotalDrinkCost FLOAT,
    TotalFoodCost FLOAT,
    CustomerID INT,
    PRIMARY KEY (OrderID)
);
INSERT INTO CoffeeShopOrderData VALUES(1001, 6/30/2024, 7.25, 7.25, 0.00, 1);
INSERT INTO CoffeeShopOrderData VALUES(1002, 6/30/2026, 9.98, 5.99, 3.99, 2);
INSERT INTO CoffeeShopOrderData VALUES(1003, 6/29/2024, 115.00, 115.00, 0.00, 3);

CREATE TABLE CoffeeShopDrinkData (
    OrderID INT,
    DrinkID INT,
    DrinkSize VARCHAR,
    DrinkQuantity INT,
    Milk VARCHAR,
    PRIMARY KEY (OrderID, DrinkID),
    FOREIGN KEY (OrderID) REFERENCES CoffeeShopOrderData(OrderID)
);
INSERT INTO CoffeeShopDrinkData VALUES(1001, 1, 'Grande', 1, 'ND');
INSERT INTO CoffeeShopDrinkData VALUES(1002, 2, 'Tall', 2, 'ND');
INSERT INTO CoffeeShopDrinkData VALUES(1002, 3, 'Grande', 1, 'ND');
INSERT INTO CoffeeShopDrinkData VALUES(1003, 4, 'Venti', 8, 'ND');

CREATE TABLE CoffeeShopFoodData (
    OrderID INT,
    FoodID INT,
    FoodQuantity INT,
    PRIMARY KEY (OrderID, FoodID),
    FOREIGN KEY (OrderID) REFERENCES CoffeeShopOrderData(OrderID)
);
INSERT INTO CoffeeShopFoodData VALUES(1001, 0, 0);
INSERT INTO CoffeeShopFoodData VALUES(1002, 3, 1);
INSERT INTO CoffeeShopFoodData VALUES(1003, 0, 0);

CREATE TABLE CoffeeShopDrinkDrinkData (
    DrinkID INT,
    DrinkName VARCHAR,
    PRIMARY KEY (DrinkID),
    FOREIGN KEY (DrinkID) REFERENCES CoffeeShopDrinkData(DrinkID)
);
INSERT INTO CoffeeShopDrinkDrinkData VALUES(1, 'Caffe Latte');
INSERT INTO CoffeeShopDrinkDrinkData VALUES(2, 'Iced Caramel Macchiato');
INSERT INTO CoffeeShopDrinkDrinkData VALUES(3, 'Iced Matcha Latte');
INSERT INTO CoffeeShopDrinkDrinkData VALUES(4, 'Vanilla Bean Frappuccino');

CREATE TABLE CoffeeShopFoodFoodData (
    FoodID INT,
    FoodName VARCHAR,
    PRIMARY KEY (FoodID),
    FOREIGN KEY (FoodID) REFERENCES CoffeeShopFoodData(FoodID)
);
INSERT INTO CoffeeShopFoodFoodData VALUES(0, 'NULL');
INSERT INTO CoffeeShopFoodFoodData VALUES(3, 'Blueberry Muffin');

CREATE TABLE CoffeeShopOrderCustomerData (
    CustomerID INT,
    CustomerName VARCHAR,
    PRIMARY KEY (CustomerID),
    FOREIGN KEY (CustomerID) REFERENCES CoffeeShopOrderData(CustomerID)
);
INSERT INTO CoffeeShopOrderCustomerData VALUES(1, 'Alice Brown');
INSERT INTO CoffeeShopOrderCustomerData VALUES(2, 'David Miller');
INSERT INTO CoffeeShopOrderCustomerData VALUES(3, 'Emily Garcia');