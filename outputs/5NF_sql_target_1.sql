CREATE TABLE CoffeeShopDrinksOrderDataDecomposed1 (
    CustomerID INT,
    OrderID INT,
    PRIMARY KEY (CustomerID, OrderID),
    FOREIGN KEY (CustomerID, OrderID) REFERENCES CoffeeShopDrinksOrderData(CustomerID, OrderID)
);
INSERT INTO CoffeeShopDrinksOrderDataDecomposed1 VALUES(1, 1001);
INSERT INTO CoffeeShopDrinksOrderDataDecomposed1 VALUES(1, 1002);
INSERT INTO CoffeeShopDrinksOrderDataDecomposed1 VALUES(2, 1003);

CREATE TABLE CoffeeShopDrinksOrderDataDecomposed2 (
    Milk varchar,
    DrinkID INT,
    OrderID INT,
    PRIMARY KEY (Milk, DrinkID, OrderID),
    FOREIGN KEY (Milk, DrinkID, OrderID) REFERENCES CoffeeShopDrinksOrderData(Milk, DrinkID, OrderID)
);
INSERT INTO CoffeeShopDrinksOrderDataDecomposed2 VALUES('ND', 1, 1001);
INSERT INTO CoffeeShopDrinksOrderDataDecomposed2 VALUES('D', 1, 1001);
INSERT INTO CoffeeShopDrinksOrderDataDecomposed2 VALUES('D', 2, 1002);
INSERT INTO CoffeeShopDrinksOrderDataDecomposed2 VALUES('ND', 3, 1003);
INSERT INTO CoffeeShopDrinksOrderDataDecomposed2 VALUES('D', 3, 1003);
INSERT INTO CoffeeShopDrinksOrderDataDecomposed2 VALUES('ND', 4, 1003);