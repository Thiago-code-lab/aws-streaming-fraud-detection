SELECT state, COUNT(*) AS suspicious_transactions, SUM(amount) AS suspicious_amount
FROM fraud_assessments
WHERE risk_level IN ('medium', 'high')
GROUP BY state
ORDER BY suspicious_transactions DESC;
