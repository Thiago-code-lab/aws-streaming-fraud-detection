SELECT rules_version, COUNT(*) AS processed_transactions, MIN(processed_at) AS first_processed_at, MAX(processed_at) AS last_processed_at
FROM fraud_assessments
GROUP BY rules_version;
