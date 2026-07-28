SELECT
  COUNT_IF(risk_level IN ('medium', 'high')) AS suspicious_transactions,
  COUNT(*) AS total_transactions,
  CAST(COUNT_IF(risk_level IN ('medium', 'high')) AS DOUBLE) / COUNT(*) AS estimated_fraud_rate
FROM fraud_assessments;
