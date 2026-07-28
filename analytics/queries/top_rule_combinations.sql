SELECT array_join(triggered_rules, ',') AS rule_combination, COUNT(*) AS transactions
FROM fraud_assessments
WHERE cardinality(triggered_rules) > 0
GROUP BY array_join(triggered_rules, ',')
ORDER BY transactions DESC
LIMIT 20;
