# Fictional ERP analytics report

Database: `fictional_erp.sqlite`  
Generated: 2026-07-29  
Functional currency: USD; transaction-currency totals remain grouped by currency.

## Invoice portfolio by currency

| invoice_type | currency | invoice_count | invoiced_amount | outstanding_amount | paid_percent |
| --- | --- | --- | --- | --- | --- |
| PURCHASE | AUD | 524 | 21986252.76 | 14377606.58 | 34.6 |
| PURCHASE | BRL | 770 | 34979894.3 | 22440225.52 | 35.8 |
| PURCHASE | CAD | 655 | 28326963.77 | 18088473.39 | 36.1 |
| PURCHASE | EUR | 866 | 37649271.69 | 24459374.24 | 35.0 |
| PURCHASE | GBP | 349 | 15827977.74 | 9955840.01 | 37.1 |
| PURCHASE | JPY | 463 | 21301808.11 | 15201199.61 | 28.6 |
| PURCHASE | MXN | 745 | 33862637.2 | 22761805.44 | 32.8 |
| PURCHASE | SGD | 387 | 16816842.47 | 11237392.8 | 33.2 |
| PURCHASE | USD | 827 | 37352133.55 | 24440972.52 | 34.6 |
| SALES | AUD | 1011 | 21925308.66 | 14298797.39 | 34.8 |
| SALES | BRL | 1750 | 38932100.63 | 25381737.73 | 34.8 |
| SALES | CAD | 1902 | 41901902.77 | 27886149.0 | 33.4 |
| SALES | EUR | 2494 | 53882326.09 | 35838874.12 | 33.5 |
| SALES | GBP | 1234 | 27170305.43 | 17745907.29 | 34.7 |
| SALES | JPY | 1256 | 28511764.25 | 18840626.55 | 33.9 |
| SALES | MXN | 1826 | 40174572.86 | 26928641.21 | 33.0 |
| SALES | SGD | 1090 | 24817692.92 | 16888852.89 | 31.9 |
| SALES | USD | 1851 | 40565255.73 | 26959295.64 | 33.5 |

## Sales by customer region

| region | currency | invoice_count | sales_amount | sales_usd |
| --- | --- | --- | --- | --- |
| Europe | EUR | 2494 | 53882326.09 | 58726475.01 |
| North America | USD | 1851 | 40565255.73 | 40521547.62 |
| Europe | GBP | 1234 | 27170305.43 | 34781564.31 |
| North America | CAD | 1902 | 41901902.77 | 30993585.58 |
| Asia Pacific | SGD | 1090 | 24817692.92 | 18631077.16 |
| Asia Pacific | AUD | 1011 | 21925308.66 | 14477584.09 |
| Latin America | BRL | 1750 | 38932100.63 | 7784823.46 |
| Latin America | MXN | 1826 | 40174572.86 | 2372088.41 |
| Asia Pacific | JPY | 1256 | 28511764.25 | 191090.85 |

## Vendor spend by category

| category | invoice_count | spend_usd | average_invoice_usd |
| --- | --- | --- | --- |
| Office Supplies | 768 | 21155773.3 | 27546.58 |
| Logistics | 667 | 20871681.93 | 31291.88 |
| Hardware | 755 | 20785616.65 | 27530.62 |
| Facilities | 630 | 20134235.46 | 31959.1 |
| Professional Services | 854 | 19478621.41 | 22808.69 |
| Cloud Services | 696 | 18931345.0 | 27200.21 |
| Marketing | 582 | 18249239.89 | 31356.08 |
| Insurance | 634 | 16234199.88 | 25605.99 |

## AR aging in functional currency

| aging_bucket | invoice_count | balance_usd |
| --- | --- | --- |
| Current | 80 | 824580.79 |
| 1-30 | 283 | 3372542.17 |
| 31-60 | 332 | 3817601.76 |
| 61-90 | 309 | 3368652.33 |
| 90+ | 10551 | 126880570.79 |

## Payment operations

| payment_type | status | method | payment_count | amount_usd |
| --- | --- | --- | --- | --- |
| DISBURSEMENT | CLEARED | ACH | 1260 | 27142119.57 |
| DISBURSEMENT | CLEARED | WIRE | 555 | 11847925.16 |
| DISBURSEMENT | CLEARED | CHECK | 512 | 10565065.3 |
| DISBURSEMENT | CLEARED | CARD | 249 | 5245445.42 |
| DISBURSEMENT | FAILED | ACH | 45 | 953820.27 |
| DISBURSEMENT | FAILED | CHECK | 15 | 480863.79 |
| DISBURSEMENT | FAILED | WIRE | 15 | 382514.52 |
| DISBURSEMENT | FAILED | CARD | 8 | 250399.63 |
| DISBURSEMENT | PENDING | ACH | 95 | 2191886.05 |
| DISBURSEMENT | PENDING | CHECK | 42 | 897852.47 |
| DISBURSEMENT | PENDING | WIRE | 38 | 701311.21 |
| DISBURSEMENT | PENDING | CARD | 18 | 402553.56 |
| RECEIPT | CLEARED | ACH | 3195 | 34683796.14 |
| RECEIPT | CLEARED | CHECK | 1354 | 14763494.39 |
| RECEIPT | CLEARED | WIRE | 1321 | 14577340.71 |
| RECEIPT | CLEARED | CARD | 597 | 6185922.66 |
| RECEIPT | FAILED | ACH | 108 | 1354060.66 |
| RECEIPT | FAILED | WIRE | 43 | 484200.65 |
| RECEIPT | FAILED | CHECK | 31 | 396266.41 |
| RECEIPT | FAILED | CARD | 17 | 121731.38 |
| RECEIPT | PENDING | ACH | 248 | 3159141.31 |
| RECEIPT | PENDING | WIRE | 90 | 996739.03 |
| RECEIPT | PENDING | CHECK | 93 | 956605.65 |
| RECEIPT | PENDING | CARD | 51 | 691805.89 |

## Monthly invoice trend

| month | invoice_type | invoice_count | amount_usd |
| --- | --- | --- | --- |
| 2023-01 | PURCHASE | 135 | 4393222.91 |
| 2023-01 | SALES | 398 | 5809959.08 |
| 2023-02 | PURCHASE | 158 | 3744220.39 |
| 2023-02 | SALES | 373 | 5321624.76 |
| 2023-03 | PURCHASE | 157 | 4138025.75 |
| 2023-03 | SALES | 382 | 5254965.57 |
| 2023-04 | PURCHASE | 134 | 3917227.56 |
| 2023-04 | SALES | 388 | 5658292.2 |
| 2023-05 | PURCHASE | 148 | 3977468.61 |
| 2023-05 | SALES | 409 | 6367091.14 |
| 2023-06 | PURCHASE | 138 | 4036610.6 |
| 2023-06 | SALES | 388 | 5573670.59 |
| 2023-07 | PURCHASE | 156 | 5085510.85 |
| 2023-07 | SALES | 407 | 5591920.98 |
| 2023-08 | PURCHASE | 139 | 4010095.15 |
| 2023-08 | SALES | 429 | 6354949.18 |
| 2023-09 | PURCHASE | 161 | 4993910.82 |
| 2023-09 | SALES | 363 | 5375549.24 |
| 2023-10 | PURCHASE | 152 | 4804571.12 |
| 2023-10 | SALES | 414 | 5665173.97 |
| 2023-11 | PURCHASE | 151 | 4245587.57 |
| 2023-11 | SALES | 452 | 5889759.1 |
| 2023-12 | PURCHASE | 174 | 4938039.29 |
| 2023-12 | SALES | 405 | 6215072.12 |
| 2024-01 | PURCHASE | 150 | 4118547.2 |
| 2024-01 | SALES | 385 | 4911134.66 |
| 2024-02 | PURCHASE | 159 | 4090784.12 |
| 2024-02 | SALES | 409 | 5871753.9 |
| 2024-03 | PURCHASE | 150 | 4011612.38 |
| 2024-03 | SALES | 379 | 5793845.23 |
| 2024-04 | PURCHASE | 153 | 3968010.84 |
| 2024-04 | SALES | 406 | 5533262.45 |
| 2024-05 | PURCHASE | 139 | 4036163.15 |
| 2024-05 | SALES | 391 | 5487132.61 |
| 2024-06 | PURCHASE | 147 | 3890543.35 |
| 2024-06 | SALES | 370 | 5740025.28 |
| 2024-07 | PURCHASE | 178 | 5004292.29 |
| 2024-07 | SALES | 401 | 5923926.63 |
| 2024-08 | PURCHASE | 169 | 4831371.84 |
| 2024-08 | SALES | 405 | 5842778.0 |
| 2024-09 | PURCHASE | 152 | 4150432.68 |
| 2024-09 | SALES | 398 | 6021495.68 |
| 2024-10 | PURCHASE | 133 | 3619450.87 |
| 2024-10 | SALES | 414 | 6586175.57 |
| 2024-11 | PURCHASE | 155 | 4225816.32 |
| 2024-11 | SALES | 414 | 6160072.03 |
| 2024-12 | PURCHASE | 154 | 4063002.38 |
| 2024-12 | SALES | 439 | 6266472.73 |
| 2025-01 | PURCHASE | 156 | 4419181.21 |
| 2025-01 | SALES | 399 | 5788279.14 |
| 2025-02 | PURCHASE | 164 | 5369674.56 |
| 2025-02 | SALES | 399 | 5970036.56 |
| 2025-03 | PURCHASE | 161 | 4191867.92 |
| 2025-03 | SALES | 401 | 6108216.98 |
| 2025-04 | PURCHASE | 164 | 4428577.1 |
| 2025-04 | SALES | 405 | 6072989.91 |
| 2025-05 | PURCHASE | 156 | 3611600.41 |
| 2025-05 | SALES | 411 | 5798233.62 |
| 2025-06 | PURCHASE | 168 | 4459115.63 |
| 2025-06 | SALES | 392 | 5293676.6 |
| 2025-07 | PURCHASE | 168 | 4833862.11 |
| 2025-07 | SALES | 411 | 5976470.65 |
| 2025-08 | PURCHASE | 163 | 4416676.37 |
| 2025-08 | SALES | 379 | 5510613.47 |
| 2025-09 | PURCHASE | 171 | 5422786.8 |
| 2025-09 | SALES | 403 | 5536473.17 |
| 2025-10 | PURCHASE | 158 | 3885692.23 |
| 2025-10 | SALES | 375 | 5229718.7 |
| 2025-11 | PURCHASE | 153 | 3830116.15 |
| 2025-11 | SALES | 434 | 6352644.78 |
| 2025-12 | PURCHASE | 162 | 4677044.99 |
| 2025-12 | SALES | 386 | 5626380.21 |

## Trial balance in functional currency

| account_number | name | account_type | debit_usd | credit_usd | net_debit_usd |
| --- | --- | --- | --- | --- | --- |
| 1010 | Operating Bank Account | ASSET | 9344451.65 | 7513428.8 | 1831022.85 |
| 1100 | Accounts Receivable | ASSET | 28355578.28 | 9344451.65 | 19011126.63 |
| 1300 | Prepaid Expenses | ASSET | 1715880.49 | 0.0 | 1715880.49 |
| 1410 | Accumulated Depreciation | ASSET | 0.0 | 3758245.0 | -3758245.0 |
| 2000 | Accounts Payable | LIABILITY | 7513428.8 | 20272997.43 | -12759568.63 |
| 2100 | Accrued Expenses | LIABILITY | 0.0 | 6358321.0 | -6358321.0 |
| 2110 | Accrued Payroll | LIABILITY | 0.0 | 16977635.0 | -16977635.0 |
| 2200 | Sales Tax Payable | LIABILITY | 0.0 | 5796092.75 | -5796092.75 |
| 2500 | Long-Term Debt | LIABILITY | 0.0 | 3974522.0 | -3974522.0 |
| 4010 | Software Revenue | REVENUE | 0.0 | 6069074.58 | -6069074.58 |
| 4020 | Hardware Revenue | REVENUE | 0.0 | 7228774.3 | -7228774.3 |
| 4030 | Services Revenue | REVENUE | 0.0 | 6344627.84 | -6344627.84 |
| 4040 | Support Revenue | REVENUE | 0.0 | 6344158.81 | -6344158.81 |
| 5010 | Software Hosting Costs | EXPENSE | 2953919.4 | 0.0 | 2953919.4 |
| 5020 | Hardware Costs | EXPENSE | 2204269.43 | 0.0 | 2204269.43 |
| 5030 | Services Delivery Costs | EXPENSE | 2260712.22 | 0.0 | 2260712.22 |
| 5100 | Payroll Expense | EXPENSE | 16977635.0 | 0.0 | 16977635.0 |
| 5200 | Rent and Facilities | EXPENSE | 1866133.94 | 0.0 | 1866133.94 |
| 5310 | Advertising Expense | EXPENSE | 1943240.26 | 0.0 | 1943240.26 |
| 5510 | Professional Fees | EXPENSE | 5508233.07 | 0.0 | 5508233.07 |
| 5520 | Insurance Expense | EXPENSE | 2523212.96 | 0.0 | 2523212.96 |
| 5530 | Office Supplies Expense | EXPENSE | 2653841.66 | 0.0 | 2653841.66 |
| 5600 | Depreciation Expense | EXPENSE | 3758245.0 | 0.0 | 3758245.0 |
| 5700 | Interest Expense | EXPENSE | 3974522.0 | 0.0 | 3974522.0 |
| 5900 | Income Tax Expense | EXPENSE | 3427150.0 | 0.0 | 3427150.0 |
| 5990 | Other Expense | EXPENSE | 3001875.0 | 0.0 | 3001875.0 |

## Data quality and risk indicators

| indicator | records | exposure_usd |
| --- | --- | --- |
| Invoices over 90 days past due | 14597 | 219258355.58 |
| Failed payments | 282 | 4423857.31 |
| Customers on hold with open AR | 52 | 5948086.33 |
