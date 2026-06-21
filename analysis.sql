SELECT Category, SUM(Sales) AS total_sales
FROM sales
GROUP BY Category;

SELECT State, SUM(Profit) AS total_profit
FROM sales
GROUP BY State;

SELECT Product_Name, SUM(Sales) AS total_sales
FROM sales
GROUP BY Product_Name
ORDER BY total_sales DESC;