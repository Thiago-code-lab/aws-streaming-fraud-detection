SELECT year, month, day, hour, COUNT(*) AS transactions
FROM fraud_assessments
GROUP BY year, month, day, hour
ORDER BY year, month, day, hour;
