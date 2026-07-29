PRAGMA foreign_keys = ON;

DROP VIEW IF EXISTS v_trial_balance;
DROP VIEW IF EXISTS v_invoice_balances;
DROP TABLE IF EXISTS journal_lines;
DROP TABLE IF EXISTS journal_entries;
DROP TABLE IF EXISTS payment_allocations;
DROP TABLE IF EXISTS payments;
DROP TABLE IF EXISTS invoice_lines;
DROP TABLE IF EXISTS invoices;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS gl_accounts;
DROP TABLE IF EXISTS vendors;
DROP TABLE IF EXISTS customers;

CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY,
    customer_code TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL,
    industry TEXT NOT NULL,
    region TEXT NOT NULL,
    country TEXT NOT NULL,
    currency TEXT NOT NULL CHECK (length(currency) = 3),
    credit_limit_cents INTEGER NOT NULL CHECK (credit_limit_cents >= 0),
    payment_terms_days INTEGER NOT NULL CHECK (payment_terms_days IN (15, 30, 45, 60)),
    status TEXT NOT NULL CHECK (status IN ('ACTIVE', 'ON_HOLD', 'INACTIVE')),
    created_date TEXT NOT NULL
);

CREATE TABLE vendors (
    vendor_id INTEGER PRIMARY KEY,
    vendor_code TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    region TEXT NOT NULL,
    country TEXT NOT NULL,
    currency TEXT NOT NULL CHECK (length(currency) = 3),
    payment_terms_days INTEGER NOT NULL CHECK (payment_terms_days IN (15, 30, 45, 60)),
    status TEXT NOT NULL CHECK (status IN ('ACTIVE', 'ON_HOLD', 'INACTIVE')),
    created_date TEXT NOT NULL
);

CREATE TABLE gl_accounts (
    account_id INTEGER PRIMARY KEY,
    account_number TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL,
    account_type TEXT NOT NULL
        CHECK (account_type IN ('ASSET', 'LIABILITY', 'EQUITY', 'REVENUE', 'EXPENSE')),
    normal_balance TEXT NOT NULL CHECK (normal_balance IN ('DEBIT', 'CREDIT')),
    parent_account_id INTEGER REFERENCES gl_accounts(account_id),
    is_active INTEGER NOT NULL DEFAULT 1 CHECK (is_active IN (0, 1))
);

CREATE TABLE products (
    product_id INTEGER PRIMARY KEY,
    sku TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    unit_price_cents INTEGER NOT NULL CHECK (unit_price_cents > 0),
    revenue_account_id INTEGER NOT NULL REFERENCES gl_accounts(account_id),
    expense_account_id INTEGER NOT NULL REFERENCES gl_accounts(account_id)
);

CREATE TABLE invoices (
    invoice_id INTEGER PRIMARY KEY,
    invoice_number TEXT NOT NULL UNIQUE,
    invoice_type TEXT NOT NULL CHECK (invoice_type IN ('SALES', 'PURCHASE')),
    customer_id INTEGER REFERENCES customers(customer_id),
    vendor_id INTEGER REFERENCES vendors(vendor_id),
    invoice_date TEXT NOT NULL,
    due_date TEXT NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('OPEN', 'PARTIAL', 'PAID', 'VOID')),
    currency TEXT NOT NULL CHECK (length(currency) = 3),
    exchange_rate_to_usd REAL NOT NULL CHECK (exchange_rate_to_usd > 0),
    subtotal_cents INTEGER NOT NULL CHECK (subtotal_cents >= 0),
    tax_cents INTEGER NOT NULL CHECK (tax_cents >= 0),
    total_cents INTEGER NOT NULL CHECK (total_cents = subtotal_cents + tax_cents),
    functional_total_cents INTEGER NOT NULL CHECK (functional_total_cents >= 0),
    description TEXT,
    CHECK (
        (invoice_type = 'SALES' AND customer_id IS NOT NULL AND vendor_id IS NULL)
        OR
        (invoice_type = 'PURCHASE' AND vendor_id IS NOT NULL AND customer_id IS NULL)
    ),
    CHECK (date(due_date) >= date(invoice_date)),
    CHECK (status <> 'VOID' OR total_cents = 0)
);

CREATE TABLE invoice_lines (
    invoice_line_id INTEGER PRIMARY KEY,
    invoice_id INTEGER NOT NULL REFERENCES invoices(invoice_id) ON DELETE CASCADE,
    line_number INTEGER NOT NULL CHECK (line_number > 0),
    product_id INTEGER REFERENCES products(product_id),
    description TEXT NOT NULL,
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    unit_price_cents INTEGER NOT NULL CHECK (unit_price_cents >= 0),
    line_amount_cents INTEGER NOT NULL
        CHECK (line_amount_cents = quantity * unit_price_cents),
    gl_account_id INTEGER NOT NULL REFERENCES gl_accounts(account_id),
    UNIQUE (invoice_id, line_number)
);

CREATE TABLE payments (
    payment_id INTEGER PRIMARY KEY,
    payment_number TEXT NOT NULL UNIQUE,
    payment_type TEXT NOT NULL CHECK (payment_type IN ('RECEIPT', 'DISBURSEMENT')),
    customer_id INTEGER REFERENCES customers(customer_id),
    vendor_id INTEGER REFERENCES vendors(vendor_id),
    payment_date TEXT NOT NULL,
    amount_cents INTEGER NOT NULL CHECK (amount_cents > 0),
    currency TEXT NOT NULL CHECK (length(currency) = 3),
    exchange_rate_to_usd REAL NOT NULL CHECK (exchange_rate_to_usd > 0),
    functional_amount_cents INTEGER NOT NULL CHECK (functional_amount_cents > 0),
    method TEXT NOT NULL CHECK (method IN ('ACH', 'WIRE', 'CHECK', 'CARD')),
    status TEXT NOT NULL CHECK (status IN ('CLEARED', 'PENDING', 'FAILED')),
    reference TEXT,
    CHECK (
        (payment_type = 'RECEIPT' AND customer_id IS NOT NULL AND vendor_id IS NULL)
        OR
        (payment_type = 'DISBURSEMENT' AND vendor_id IS NOT NULL AND customer_id IS NULL)
    )
);

CREATE TABLE payment_allocations (
    payment_id INTEGER NOT NULL REFERENCES payments(payment_id) ON DELETE CASCADE,
    invoice_id INTEGER NOT NULL REFERENCES invoices(invoice_id),
    allocated_cents INTEGER NOT NULL CHECK (allocated_cents > 0),
    PRIMARY KEY (payment_id, invoice_id)
);

CREATE TABLE journal_entries (
    journal_entry_id INTEGER PRIMARY KEY,
    journal_number TEXT NOT NULL UNIQUE,
    entry_date TEXT NOT NULL,
    source TEXT NOT NULL CHECK (source IN ('AR', 'AP', 'CASH', 'MANUAL', 'PAYROLL')),
    source_invoice_id INTEGER REFERENCES invoices(invoice_id),
    source_payment_id INTEGER REFERENCES payments(payment_id),
    description TEXT NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('POSTED', 'DRAFT', 'REVERSED')),
    created_by TEXT NOT NULL,
    CHECK (source_invoice_id IS NULL OR source_payment_id IS NULL)
);

CREATE TABLE journal_lines (
    journal_line_id INTEGER PRIMARY KEY,
    journal_entry_id INTEGER NOT NULL REFERENCES journal_entries(journal_entry_id) ON DELETE CASCADE,
    line_number INTEGER NOT NULL CHECK (line_number > 0),
    account_id INTEGER NOT NULL REFERENCES gl_accounts(account_id),
    debit_cents INTEGER NOT NULL DEFAULT 0 CHECK (debit_cents >= 0),
    credit_cents INTEGER NOT NULL DEFAULT 0 CHECK (credit_cents >= 0),
    memo TEXT,
    CHECK (
        (debit_cents > 0 AND credit_cents = 0)
        OR (credit_cents > 0 AND debit_cents = 0)
    ),
    UNIQUE (journal_entry_id, line_number)
);

CREATE INDEX idx_invoices_customer ON invoices(customer_id);
CREATE INDEX idx_invoices_vendor ON invoices(vendor_id);
CREATE INDEX idx_invoices_dates ON invoices(invoice_date, due_date);
CREATE INDEX idx_invoice_lines_invoice ON invoice_lines(invoice_id);
CREATE INDEX idx_payments_customer ON payments(customer_id);
CREATE INDEX idx_payments_vendor ON payments(vendor_id);
CREATE INDEX idx_payments_date ON payments(payment_date);
CREATE INDEX idx_allocations_invoice ON payment_allocations(invoice_id);
CREATE INDEX idx_journal_entries_date ON journal_entries(entry_date);
CREATE INDEX idx_journal_lines_entry ON journal_lines(journal_entry_id);
CREATE INDEX idx_journal_lines_account ON journal_lines(account_id);

CREATE VIEW v_invoice_balances AS
SELECT
    i.invoice_id,
    i.invoice_number,
    i.invoice_type,
    i.customer_id,
    i.vendor_id,
    i.invoice_date,
    i.due_date,
    i.status,
    i.currency,
    i.total_cents,
    COALESCE(SUM(CASE WHEN p.status = 'CLEARED' THEN pa.allocated_cents ELSE 0 END), 0)
        AS paid_cents,
    i.total_cents
        - COALESCE(SUM(CASE WHEN p.status = 'CLEARED' THEN pa.allocated_cents ELSE 0 END), 0)
        AS balance_cents
FROM invoices i
LEFT JOIN payment_allocations pa ON pa.invoice_id = i.invoice_id
LEFT JOIN payments p ON p.payment_id = pa.payment_id
GROUP BY i.invoice_id;

CREATE VIEW v_trial_balance AS
SELECT
    a.account_id,
    a.account_number,
    a.name,
    a.account_type,
    COALESCE(SUM(CASE WHEN je.status = 'POSTED' THEN jl.debit_cents ELSE 0 END), 0)
        AS debit_cents,
    COALESCE(SUM(CASE WHEN je.status = 'POSTED' THEN jl.credit_cents ELSE 0 END), 0)
        AS credit_cents,
    COALESCE(SUM(CASE WHEN je.status = 'POSTED'
        THEN jl.debit_cents - jl.credit_cents ELSE 0 END), 0) AS net_debit_cents
FROM gl_accounts a
LEFT JOIN journal_lines jl ON jl.account_id = a.account_id
LEFT JOIN journal_entries je ON je.journal_entry_id = jl.journal_entry_id
GROUP BY a.account_id;
