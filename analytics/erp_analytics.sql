-- name: Invoice portfolio by currency
SELECT
    invoice_type,
    currency,
    COUNT(*) AS invoice_count,
    ROUND(SUM(total_cents) / 100.0, 2) AS invoiced_amount,
    ROUND(SUM(balance_cents) / 100.0, 2) AS outstanding_amount,
    ROUND(100.0 * SUM(paid_cents) / NULLIF(SUM(total_cents), 0), 1) AS paid_percent
FROM v_invoice_balances
GROUP BY invoice_type, currency
ORDER BY invoice_type, currency;

-- name: Sales by customer region
SELECT
    c.region,
    i.currency,
    COUNT(*) AS invoice_count,
    ROUND(SUM(i.total_cents) / 100.0, 2) AS sales_amount,
    ROUND(SUM(i.functional_total_cents) / 100.0, 2) AS sales_usd
FROM invoices i
JOIN customers c ON c.customer_id = i.customer_id
WHERE i.invoice_type = 'SALES'
GROUP BY c.region, i.currency
ORDER BY sales_usd DESC;

-- name: Vendor spend by category
SELECT
    v.category,
    COUNT(*) AS invoice_count,
    ROUND(SUM(i.functional_total_cents) / 100.0, 2) AS spend_usd,
    ROUND(AVG(i.functional_total_cents) / 100.0, 2) AS average_invoice_usd
FROM invoices i
JOIN vendors v ON v.vendor_id = i.vendor_id
WHERE i.invoice_type = 'PURCHASE'
GROUP BY v.category
ORDER BY spend_usd DESC;

-- name: AR aging in functional currency
SELECT
    CASE
        WHEN date(due_date) >= date('2026-01-31') THEN 'Current'
        WHEN julianday('2026-01-31') - julianday(due_date) <= 30 THEN '1-30'
        WHEN julianday('2026-01-31') - julianday(due_date) <= 60 THEN '31-60'
        WHEN julianday('2026-01-31') - julianday(due_date) <= 90 THEN '61-90'
        ELSE '90+'
    END AS aging_bucket,
    COUNT(*) AS invoice_count,
    ROUND(SUM(balance_cents * exchange_rate_to_usd) / 100.0, 2) AS balance_usd
FROM v_invoice_balances b
JOIN invoices i USING (invoice_id)
WHERE invoice_type = 'SALES' AND balance_cents > 0
GROUP BY aging_bucket
ORDER BY CASE aging_bucket
    WHEN 'Current' THEN 1 WHEN '1-30' THEN 2 WHEN '31-60' THEN 3
    WHEN '61-90' THEN 4 ELSE 5 END;

-- name: Payment operations
SELECT
    payment_type,
    status,
    method,
    COUNT(*) AS payment_count,
    ROUND(SUM(functional_amount_cents) / 100.0, 2) AS amount_usd
FROM payments
GROUP BY payment_type, status, method
ORDER BY payment_type, status, amount_usd DESC;

-- name: Monthly invoice trend
SELECT
    substr(invoice_date, 1, 7) AS month,
    invoice_type,
    COUNT(*) AS invoice_count,
    ROUND(SUM(functional_total_cents) / 100.0, 2) AS amount_usd
FROM invoices
GROUP BY month, invoice_type
ORDER BY month, invoice_type;

-- name: Trial balance in functional currency
SELECT
    account_number,
    name,
    account_type,
    ROUND(debit_cents / 100.0, 2) AS debit_usd,
    ROUND(credit_cents / 100.0, 2) AS credit_usd,
    ROUND(net_debit_cents / 100.0, 2) AS net_debit_usd
FROM v_trial_balance
WHERE debit_cents <> 0 OR credit_cents <> 0
ORDER BY account_number;

-- name: Data quality and risk indicators
SELECT 'Invoices over 90 days past due' AS indicator, COUNT(*) AS records,
       ROUND(COALESCE(SUM(balance_cents * exchange_rate_to_usd), 0) / 100.0, 2) AS exposure_usd
FROM v_invoice_balances b JOIN invoices i USING (invoice_id)
WHERE balance_cents > 0
  AND julianday('2026-01-31') - julianday(due_date) > 90
UNION ALL
SELECT 'Failed payments', COUNT(*),
       ROUND(COALESCE(SUM(functional_amount_cents), 0) / 100.0, 2)
FROM payments WHERE status = 'FAILED'
UNION ALL
SELECT 'Customers on hold with open AR', COUNT(DISTINCT c.customer_id),
       ROUND(COALESCE(SUM(balance_cents * exchange_rate_to_usd), 0) / 100.0, 2)
FROM customers c
JOIN invoices i ON i.customer_id = c.customer_id
JOIN v_invoice_balances b ON b.invoice_id = i.invoice_id
WHERE c.status = 'ON_HOLD' AND balance_cents > 0;
