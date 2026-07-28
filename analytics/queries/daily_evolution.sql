SELECT year, month, day, COUNT(*) AS transactions, SUM(CASE WHEN risk_level IN ('medium', 'high') THEN 1 ELSE 0 END) AS suspicious
FROM fraud_assessments
GROUP BY year, month, day
ORDER BY year, month, day;
