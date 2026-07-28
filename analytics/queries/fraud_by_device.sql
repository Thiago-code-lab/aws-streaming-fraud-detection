SELECT device_type, COUNT(*) AS suspicious_transactions
FROM fraud_assessments
WHERE risk_level IN ('medium', 'high')
GROUP BY device_type
ORDER BY suspicious_transactions DESC;
