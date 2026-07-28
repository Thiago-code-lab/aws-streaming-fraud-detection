SELECT SUM(amount) AS total_suspicious_amount
FROM fraud_assessments
WHERE risk_level IN ('medium', 'high');
