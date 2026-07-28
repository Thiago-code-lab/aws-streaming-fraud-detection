SELECT rule_id, COUNT(*) AS alerts
FROM fraud_assessments
CROSS JOIN UNNEST(triggered_rules) AS t(rule_id)
WHERE risk_level IN ('medium', 'high')
GROUP BY rule_id
ORDER BY alerts DESC;
