CREATE DATABASE food;
SHOW VARIABLES LIKE 'local_infile';
CREATE TABLE providers (
    Provider_ID INT,
    Name VARCHAR(255),
    Type VARCHAR(100),
    Address VARCHAR(255),
    City VARCHAR(100),
    Contact VARCHAR(50)
);
use food;

LOAD DATA LOCAL INFILE 'D:/providers_cleaned.csv'
INTO TABLE providers
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

show tables;
select * from providers;

1. PROVIDERS BY CITY
SELECT City,
       COUNT(*) AS Total_Providers
FROM providers
GROUP BY City
ORDER BY Total_Providers DESC;

2. RECEIVERS BY CITY
SELECT City, 
       COUNT(*) AS Total_Receivers
FROM receivers_cleaned
GROUP BY City
ORDER BY Total_Receivers DESC;

3. MOST CONTRIBUTING FOOD PROVIDER TYPE
SELECT p.Type,
       SUM(f.Quantity) AS Total_Quantity_Donated
FROM providers p
JOIN food_cleaned f
ON p.Provider_ID = f.Provider_ID
GROUP BY p.Type
ORDER BY Total_Quantity_Donated DESC
LIMIT 10;

4. CONTACT INFORMATION OF FOOD PROVIDERS IN SPECIFIC CITY
SELECT Name,
       Contact,
       Address,
       City
FROM providers
WHERE City = 'Shannonside';

5. RECEIVERS WHO CLAIMED THE MOST FOOD
SELECT r.Name,
       SUM(f.Quantity) AS Total_Quantity_Claimed
FROM receivers_cleaned r
JOIN claims_cleaned c
ON r.Receiver_ID = c.Receiver_ID
JOIN food_cleaned f
ON c.Food_ID = f.Food_ID
GROUP BY r.Name
ORDER BY Total_Quantity_Claimed DESC
LIMIT 10;

6. TOTAL FOOD QUANTITY AVAILABLE FROM ALL PROVIDERS
SELECT p.Name,
       SUM(f.Quantity) AS Total_Quantity
FROM providers p
JOIN food_cleaned f
ON p.Provider_ID = f.Provider_ID
GROUP BY p.Name
ORDER BY Total_Quantity DESC;

7. CITY THAT HAS HIGHEST NUMBER OF FOOD LISTINGS
SELECT Location,
       COUNT(*) AS Total_Listings
FROM food_cleaned
GROUP BY Location
ORDER BY Total_Listings DESC
LIMIT 10;

8. MOST COMMONLY AVAILABLE FOOD TYPES
SELECT Food_Type,
       COUNT(*) AS Total
FROM food_cleaned
GROUP BY Food_Type
ORDER BY Total DESC;

9. FOOD CLAIMS THAT HAVE BEEN MADE FOR EACH FOOD ITEM
SELECT f.Food_Name,
       COUNT(c.Claim_ID) AS Total_Claims
FROM food_cleaned f
LEFT JOIN claims_cleaned c
ON f.Food_ID = c.Food_ID
GROUP BY f.Food_Name
ORDER BY Total_Claims DESC;

10. PROVIDER THAT HAS THE HIGHEST NUMBER OF SUCCESSFUL FOOD CLAIMS
SELECT p.Name,
       COUNT(c.Claim_ID) AS Successful_Claims
FROM providers p
JOIN food_cleaned f
ON p.Provider_ID = f.Provider_ID
JOIN claims_cleaned c
ON f.Food_ID = c.Food_ID
WHERE c.Status = 'Completed'
GROUP BY p.Name
ORDER BY Successful_Claims DESC
LIMIT 10;

11. PERCENTAGE OF FOOD CLAIMS THAT ARE COMPLETED ,PENDING OR CANCELED
SELECT Status,
       ROUND(COUNT(*) * 100.0 /
       (SELECT COUNT(*) FROM claims_cleaned),2) AS Percentage
FROM claims_cleaned
GROUP BY Status;

12. AVERAGE QUANTITY OF FOOD CLAIMED PER RECEIVER
SELECT c.Receiver_ID,
       ROUND(AVG(f.Quantity),2) AS Avg_Quantity
FROM claims_cleaned c
JOIN food_cleaned f
ON c.Food_ID = f.Food_ID
GROUP BY c.Receiver_ID
ORDER BY Avg_Quantity DESC;

13. MEAL TYPE THAT CLAIMED THE MOST
SELECT f.Meal_Type,
       COUNT(c.Claim_ID) AS Total_Claims
FROM food_cleaned f
JOIN claims_cleaned c
ON f.Food_ID = c.Food_ID
GROUP BY f.Meal_Type
ORDER BY Total_Claims DESC
LIMIT 10;

14. TOTAL QUANTITY OF FOOD DONATED BY EACH PROVIDER
SELECT p.Name,
       SUM(f.Quantity) AS Total_Donated
FROM providers p
JOIN food_cleaned f
ON p.Provider_ID = f.Provider_ID
GROUP BY p.Name
ORDER BY Total_Donated DESC;

15. PROVIDER TYPE VS TOTAL QUANTITY
SELECT Provider_Type,
       SUM(Quantity) AS Total_Quantity
FROM food_cleaned
GROUP BY Provider_Type
ORDER BY Total_Quantity DESC;

16. RECEIVER TYPE DISTRIBUTION
SELECT Type,
       COUNT(*) AS Total_Receivers
FROM receivers_cleaned
GROUP BY Type;

KPI
1. TOTAL FOOD LISTINGS
SELECT COUNT(*) AS Total_Food_Listings
FROM food_cleaned;

2. TOTAL FOOD QUANTITY AVAILABLE
SELECT SUM(Quantity) AS Total_Food_Quantity
FROM food_cleaned;

3. TOTAL PROVIDERS
SELECT COUNT(*) AS Total_Providers
FROM providers;

4. TOTAL RECEIVERS
SELECT COUNT(*) AS Total_Receivers
FROM receivers_cleaned;

5. TOTAL CLAIMS
SELECT COUNT(*) AS Total_Claims
FROM claims_cleaned;

