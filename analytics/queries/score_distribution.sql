SELECT
  CASE
    WHEN risk_score < 35 THEN '00-34'
    WHEN risk_score < 70 THEN '35-69'
    ELSE '70-100'
  END AS score_range,
  COUNT(*) AS transactions
FROM fraud_assessments
GROUP BY 1
ORDER BY 1;
