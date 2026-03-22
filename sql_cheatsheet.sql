/*
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  SQL DATA MANIPULATION CHEATSHEET — Interview Prep (Complete)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Covers: SELECT → FILTER → JOIN → GROUP → WINDOW → PIVOT → CTE → STATS
Each section: syntax → gotchas → dialect differences → interview tips
*/


-- ╔════════════════════════════════════════════════════════════════════╗
-- ║  PART A: FUNDAMENTALS                                             ║
-- ╚════════════════════════════════════════════════════════════════════╝


-- ════════════════════════════════════════════════════════════════════
-- A1. SELECT & BASIC CLAUSES — Execution Order
-- ════════════════════════════════════════════════════════════════════
/*
SQL EXECUTION ORDER (NOT the written order!):

  Written Order:         Execution Order:
  ─────────────         ─────────────────
  1. SELECT              5. SELECT        ← pick columns
  2. FROM                1. FROM/JOIN     ← get tables
  3. WHERE               2. WHERE         ← filter rows
  4. GROUP BY            3. GROUP BY      ← group rows
  5. HAVING              4. HAVING        ← filter groups
  6. ORDER BY            6. ORDER BY      ← sort
  7. LIMIT               7. LIMIT         ← cap output

  WHY THIS MATTERS:
  - You can't use a SELECT alias in WHERE (not computed yet)
  - You CAN use a SELECT alias in ORDER BY (computed before ORDER BY)
  - HAVING runs after GROUP BY, so it can reference aggregates
  - Table JOINs happen first, then WHERE filters the joined result
*/

-- Basic SELECT patterns
SELECT *                                  FROM table_name;
SELECT col1, col2                         FROM table_name;
SELECT DISTINCT col1                      FROM table_name;
SELECT col1 AS alias_name                 FROM table_name;
SELECT col1, col2, col1 + col2 AS total   FROM table_name;
SELECT COUNT(*) AS row_count              FROM table_name;


-- ════════════════════════════════════════════════════════════════════
-- A2. WHERE — Filtering Rows
-- ════════════════════════════════════════════════════════════════════
/*
┌────────────────────────┬──────────────────────────────────────────────┐
│ Operator               │ Example                                      │
├────────────────────────┼──────────────────────────────────────────────┤
│ =, !=, <>, <, >, <=,>=│ WHERE salary > 50000                         │
│ AND, OR, NOT           │ WHERE dept='A' AND salary > 50000            │
│ IN                     │ WHERE dept IN ('A', 'B', 'C')               │
│ NOT IN                 │ WHERE dept NOT IN ('A')                      │
│ BETWEEN                │ WHERE salary BETWEEN 50000 AND 90000        │
│ LIKE                   │ WHERE name LIKE 'A%'    -- starts with A    │
│                        │ WHERE name LIKE '%son'  -- ends with son    │
│                        │ WHERE name LIKE '_o%'   -- 2nd char is o    │
│ IS NULL / IS NOT NULL  │ WHERE manager_id IS NOT NULL                │
│ EXISTS                 │ WHERE EXISTS (SELECT 1 FROM ...)            │
│ Subquery               │ WHERE salary > (SELECT AVG(salary) FROM ..) │
└────────────────────────┴──────────────────────────────────────────────┘

GOTCHAS:
  - NULL = NULL → NULL (not TRUE). Always use IS NULL / IS NOT NULL
  - NOT IN with NULLs in the list → returns empty! Use NOT EXISTS instead
  - BETWEEN is INCLUSIVE on both ends
  - LIKE is case-sensitive in Postgres, case-insensitive in MySQL
    → Use ILIKE in Postgres for case-insensitive
  - % matches 0+ chars, _ matches exactly 1 char
*/


-- ════════════════════════════════════════════════════════════════════
-- A3. ORDER BY & LIMIT
-- ════════════════════════════════════════════════════════════════════
/*
┌────────────────────────┬──────────────────────────────────────────────┐
│ Pattern                │ Syntax                                        │
├────────────────────────┼──────────────────────────────────────────────┤
│ Sort ascending         │ ORDER BY col ASC          -- default          │
│ Sort descending        │ ORDER BY col DESC                            │
│ Multi-column sort      │ ORDER BY dept ASC, salary DESC               │
│ Sort by position       │ ORDER BY 1, 2             -- col positions   │
│ Sort by expression     │ ORDER BY salary * 12 DESC                    │
│ NULLs first/last       │ ORDER BY col NULLS FIRST  -- Postgres        │
│ Limit rows             │ LIMIT 10                                     │
│ Offset + Limit         │ LIMIT 10 OFFSET 20        -- skip 20, get 10│
│ Top N (SQL Server)     │ SELECT TOP 10 * FROM ...                     │
│ Fetch (SQL Standard)   │ FETCH FIRST 10 ROWS ONLY                    │
└────────────────────────┴──────────────────────────────────────────────┘

DIALECT DIFFERENCES — LIMIT:
  MySQL/Postgres/SQLite: LIMIT 10 OFFSET 20
  SQL Server:            SELECT TOP 10 ... or OFFSET 20 ROWS FETCH NEXT 10 ROWS ONLY
  Oracle:                FETCH FIRST 10 ROWS ONLY  (12c+) or ROWNUM <= 10

GOTCHAS:
  - ORDER BY without LIMIT: result order is not guaranteed in some DBs
  - LIMIT without ORDER BY: which rows you get is non-deterministic
  - NULL values sort LAST in ASC by default (Postgres), FIRST in some DBs
*/


-- ════════════════════════════════════════════════════════════════════
-- A4. NULL HANDLING
-- ════════════════════════════════════════════════════════════════════
/*
┌────────────────────────┬──────────────────────────────────────────────┐
│ Function               │ Purpose                                      │
├────────────────────────┼──────────────────────────────────────────────┤
│ IS NULL                │ Check if value is NULL                       │
│ IS NOT NULL            │ Check if value is NOT NULL                   │
│ COALESCE(a, b, c)     │ Return first non-NULL argument               │
│ NULLIF(a, b)          │ Return NULL if a = b, else return a          │
│ IFNULL(a, b)          │ MySQL/SQLite: return b if a is NULL          │
│ NVL(a, b)             │ Oracle: same as IFNULL                       │
│ ISNULL(a, b)          │ SQL Server: same as IFNULL                   │
└────────────────────────┴──────────────────────────────────────────────┘

KEY NULL RULES:
  - NULL = NULL        → NULL (not TRUE)
  - NULL != anything   → NULL
  - NULL + 5           → NULL
  - NULL AND TRUE      → NULL
  - NULL OR TRUE       → TRUE
  - COUNT(*)           → counts all rows (including NULL)
  - COUNT(column)      → counts non-NULL values only
  - SUM/AVG/MIN/MAX    → ignore NULL values
  - GROUP BY           → groups NULLs together as one group

SAFE DIVISION:
  salary / NULLIF(hours, 0)   -- returns NULL instead of error when hours=0
*/


-- ╔════════════════════════════════════════════════════════════════════╗
-- ║  PART B: JOINS                                                     ║
-- ╚════════════════════════════════════════════════════════════════════╝

-- ════════════════════════════════════════════════════════════════════
-- B1. JOIN TYPES — Visual Reference
-- ════════════════════════════════════════════════════════════════════
/*
         Table A              Table B
       ┌─────────┐         ┌─────────┐
       │  1  2  3│         │  2  3  4│
       └─────────┘         └─────────┘

  INNER JOIN:       {2, 3}              -- only matching rows
  LEFT JOIN:        {1, 2, 3}           -- all of A + matches from B
  RIGHT JOIN:       {2, 3, 4}           -- matches from A + all of B
  FULL OUTER JOIN:  {1, 2, 3, 4}        -- all from both
  CROSS JOIN:       A × B (9 combos)    -- cartesian product
  SELF JOIN:        A joined to A       -- compare rows within same table

SYNTAX:
*/

-- Inner join
SELECT a.*, b.*
FROM table_a a
INNER JOIN table_b b ON a.key = b.key;

-- Left join (keep all from left)
SELECT a.*, b.*
FROM table_a a
LEFT JOIN table_b b ON a.key = b.key;

-- Full outer join (keep all from both)
SELECT a.*, b.*
FROM table_a a
FULL OUTER JOIN table_b b ON a.key = b.key;

-- Cross join (all combinations)
SELECT a.*, b.*
FROM table_a a
CROSS JOIN table_b b;

-- Self join (employee → manager)
SELECT e.name AS employee, m.name AS manager
FROM employees e
LEFT JOIN employees m ON e.manager_id = m.emp_id;


-- ════════════════════════════════════════════════════════════════════
-- B2. ANTI-JOIN & SEMI-JOIN PATTERNS
-- ════════════════════════════════════════════════════════════════════
/*
ANTI-JOIN: rows in A that have NO match in B (SQL has no ANTI JOIN keyword)
*/

-- Method 1: NOT IN (watch for NULLs!)
SELECT * FROM a WHERE a.key NOT IN (SELECT key FROM b WHERE key IS NOT NULL);

-- Method 2: LEFT JOIN + IS NULL (safest, most common)
SELECT a.*
FROM table_a a
LEFT JOIN table_b b ON a.key = b.key
WHERE b.key IS NULL;

-- Method 3: NOT EXISTS (most portable, NULL-safe)
SELECT a.*
FROM table_a a
WHERE NOT EXISTS (SELECT 1 FROM table_b b WHERE b.key = a.key);

/*
SEMI-JOIN: rows in A that HAVE a match in B (no columns from B needed)
*/
-- Method 1: EXISTS
SELECT a.* FROM table_a a
WHERE EXISTS (SELECT 1 FROM table_b b WHERE b.key = a.key);

-- Method 2: IN
SELECT * FROM table_a WHERE key IN (SELECT key FROM table_b);

/*
GOTCHAS:
  - NOT IN with NULLs returns EMPTY RESULT SET! Always use NOT EXISTS
  - LEFT JOIN anti-join is often fastest on large datasets
  - SEMI-JOIN (EXISTS/IN) doesn't produce duplicates from B
  - JOIN can produce duplicates from B if B has multiple matches
*/


-- ╔════════════════════════════════════════════════════════════════════╗
-- ║  PART C: GROUP BY & AGGREGATION                                    ║
-- ╚════════════════════════════════════════════════════════════════════╝

-- ════════════════════════════════════════════════════════════════════
-- C1. AGGREGATE FUNCTIONS
-- ════════════════════════════════════════════════════════════════════
/*
┌────────────────────────┬──────────────────────────────────────────────┐
│ Function               │ Note                                         │
├────────────────────────┼──────────────────────────────────────────────┤
│ COUNT(*)               │ All rows including NULLs                     │
│ COUNT(col)             │ Non-NULL values only                         │
│ COUNT(DISTINCT col)    │ Unique non-NULL values                       │
│ SUM(col)               │ Total (ignores NULL)                         │
│ AVG(col)               │ Mean (ignores NULL — this can be misleading!)│
│ MIN(col) / MAX(col)    │ Works on numbers, strings, dates             │
│ GROUP_CONCAT / STRING_AGG │ Concatenate strings (dialect-specific)    │
│ ARRAY_AGG              │ Collect into array (Postgres)                │
│ VARIANCE / STDDEV      │ Statistical functions (not all dialects)     │
└────────────────────────┴──────────────────────────────────────────────┘

STRING AGGREGATION by dialect:
  SQLite:    GROUP_CONCAT(col, ',')
  MySQL:     GROUP_CONCAT(col ORDER BY col SEPARATOR ',')
  Postgres:  STRING_AGG(col, ',' ORDER BY col)
  BigQuery:  STRING_AGG(col, ',' ORDER BY col)
*/

-- Conditional aggregation (CASE inside aggregate)
SELECT department,
       COUNT(*) AS total,
       SUM(CASE WHEN salary > 80000 THEN 1 ELSE 0 END) AS high_earners,
       AVG(CASE WHEN salary > 80000 THEN salary END) AS avg_high_salary
FROM employees
GROUP BY department;

/*
WHERE vs HAVING:
  WHERE  → filters ROWS before grouping
  HAVING → filters GROUPS after aggregation

  -- "Departments where avg salary > 80K"
  SELECT department, AVG(salary) FROM employees
  GROUP BY department HAVING AVG(salary) > 80000;

  -- "Average salary of employees earning > 70K, per department"
  SELECT department, AVG(salary) FROM employees
  WHERE salary > 70000
  GROUP BY department;
*/


-- ════════════════════════════════════════════════════════════════════
-- C2. GROUPING SETS / ROLLUP / CUBE
-- ════════════════════════════════════════════════════════════════════
/*
For subtotals and grand totals (Postgres/MySQL 8+/BigQuery):

  ROLLUP(a, b)    → groups: (a,b), (a), ()
                     Hierarchical subtotals
  CUBE(a, b)      → groups: (a,b), (a), (b), ()
                     All possible subtotals
  GROUPING SETS   → custom combinations
*/

-- ROLLUP: region subtotals + grand total
SELECT COALESCE(region, 'ALL') AS region,
       COALESCE(product, 'ALL') AS product,
       SUM(amount) AS total
FROM orders
GROUP BY ROLLUP(region, product);

-- GROUPING function: 1 if subtotal, 0 if real group
SELECT region, product,
       SUM(amount),
       GROUPING(region) AS is_region_subtotal,
       GROUPING(product) AS is_product_subtotal
FROM orders
GROUP BY ROLLUP(region, product);


-- ╔════════════════════════════════════════════════════════════════════╗
-- ║  PART D: WINDOW FUNCTIONS                                          ║
-- ╚════════════════════════════════════════════════════════════════════╝

-- ════════════════════════════════════════════════════════════════════
-- D1. WINDOW FUNCTION ANATOMY
-- ════════════════════════════════════════════════════════════════════
/*
  function_name(args) OVER (
      [PARTITION BY col1, col2]       -- like GROUP BY but keeps all rows
      [ORDER BY col3 ASC/DESC]        -- sort within partition
      [ROWS/RANGE frame_clause]       -- which rows to include
  )

  PARTITION BY = divide rows into groups (like GROUP BY but no reduction)
  ORDER BY     = sort within each partition
  Frame        = sliding window of rows for the calculation

  KEY DIFFERENCE from GROUP BY:
    GROUP BY  → reduces rows (1 row per group)
    OVER()    → keeps all rows (adds computed column)
*/


-- ════════════════════════════════════════════════════════════════════
-- D2. RANKING FUNCTIONS
-- ════════════════════════════════════════════════════════════════════
/*
┌────────────────────┬────────────┬──────────────────────────────────────┐
│ Function           │ Ties       │ Example: values 100, 90, 90, 80      │
├────────────────────┼────────────┼──────────────────────────────────────┤
│ ROW_NUMBER()       │ No ties    │ 1, 2, 3, 4                           │
│ RANK()             │ Gaps       │ 1, 2, 2, 4   ← skips 3              │
│ DENSE_RANK()       │ No gaps    │ 1, 2, 2, 3   ← no skip             │
│ NTILE(n)           │ N/A        │ Divides into n equal buckets         │
│ PERCENT_RANK()     │ 0 to 1     │ (rank-1)/(total-1)                   │
│ CUME_DIST()        │ 0 to 1     │ rank/total                           │
└────────────────────┴────────────┴──────────────────────────────────────┘

INTERVIEW CLASSIC — Top N per group:
*/
-- Second highest salary per department
WITH ranked AS (
    SELECT *, DENSE_RANK() OVER (
        PARTITION BY department ORDER BY salary DESC
    ) AS rnk
    FROM employees
)
SELECT * FROM ranked WHERE rnk = 2;


-- ════════════════════════════════════════════════════════════════════
-- D3. VALUE FUNCTIONS (LAG, LEAD, FIRST_VALUE, LAST_VALUE, NTH_VALUE)
-- ════════════════════════════════════════════════════════════════════
/*
┌────────────────────────┬──────────────────────────────────────────────┐
│ Function               │ Purpose                                      │
├────────────────────────┼──────────────────────────────────────────────┤
│ LAG(col, n, default)   │ Value n rows BEFORE current (default for     │
│                        │ first rows where no previous exists)         │
│ LEAD(col, n, default)  │ Value n rows AFTER current                   │
│ FIRST_VALUE(col)       │ First value in window frame                  │
│ LAST_VALUE(col)        │ Last value in window frame (⚠ frame!)        │
│ NTH_VALUE(col, n)      │ Nth value in window frame                    │
└────────────────────────┴──────────────────────────────────────────────┘

⚠ LAST_VALUE GOTCHA:
  Default frame is RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
  So LAST_VALUE = CURRENT ROW by default! Fix:
  LAST_VALUE(col) OVER (ORDER BY x
      ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING)
*/

-- Month-over-month comparison
SELECT month, revenue,
       LAG(revenue, 1) OVER (ORDER BY month)  AS prev_month,
       revenue - LAG(revenue, 1) OVER (ORDER BY month) AS delta
FROM monthly_revenue;


-- ════════════════════════════════════════════════════════════════════
-- D4. FRAME CLAUSES — The Sliding Window
-- ════════════════════════════════════════════════════════════════════
/*
  ROWS BETWEEN <start> AND <end>

  Start/End options:
    UNBOUNDED PRECEDING  → from the very first row
    N PRECEDING          → N rows before current
    CURRENT ROW          → the current row
    N FOLLOWING          → N rows after current
    UNBOUNDED FOLLOWING  → to the very last row

  COMMON FRAMES:
  ┌──────────────────────────────────────┬───────────────────────────────┐
  │ Frame                                │ Use Case                      │
  ├──────────────────────────────────────┼───────────────────────────────┤
  │ ROWS BETWEEN UNBOUNDED PREC         │ Running total / cumulative    │
  │   AND CURRENT ROW                    │                               │
  │ ROWS BETWEEN 2 PREC AND CURRENT ROW │ 3-period moving average       │
  │ ROWS BETWEEN 1 PREC AND 1 FOLLOWING │ Centered moving average       │
  │ ROWS BETWEEN UNBOUNDED PREC         │ FIRST/LAST VALUE across all   │
  │   AND UNBOUNDED FOLLOWING            │                               │
  └──────────────────────────────────────┴───────────────────────────────┘

  ROWS vs RANGE:
    ROWS  → physical rows (exact N rows before/after)
    RANGE → logical range (all rows with same ORDER BY value)
    ROWS is usually what you want. RANGE is the DEFAULT (careful!).
*/

-- Running total
SELECT order_date, amount,
       SUM(amount) OVER (ORDER BY order_date
           ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS running_total
FROM orders;

-- 3-period moving average
SELECT order_date, amount,
       AVG(amount) OVER (ORDER BY order_date
           ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) AS moving_avg_3
FROM orders;


-- ╔════════════════════════════════════════════════════════════════════╗
-- ║  PART E: CTEs, SUBQUERIES & PIVOTING                               ║
-- ╚════════════════════════════════════════════════════════════════════╝

-- ════════════════════════════════════════════════════════════════════
-- E1. CTEs (Common Table Expressions)
-- ════════════════════════════════════════════════════════════════════
/*
CTEs = named temporary result sets defined with WITH clause.

Benefits:
  - Readability: break complex queries into named steps
  - Reusability: reference the same CTE multiple times
  - Recursion: tree/graph traversal with RECURSIVE
*/

-- Chained CTEs
WITH step1 AS (
    SELECT department, AVG(salary) AS avg_sal
    FROM employees
    GROUP BY department
),
step2 AS (
    SELECT department, avg_sal,
           RANK() OVER (ORDER BY avg_sal DESC) AS dept_rank
    FROM step1
)
SELECT * FROM step2 WHERE dept_rank = 1;

-- Recursive CTE (hierarchical traversal)
WITH RECURSIVE hierarchy AS (
    -- Base case
    SELECT emp_id, name, manager_id, 1 AS level
    FROM employees
    WHERE manager_id IS NULL

    UNION ALL

    -- Recursive step
    SELECT e.emp_id, e.name, e.manager_id, h.level + 1
    FROM employees e
    JOIN hierarchy h ON e.manager_id = h.emp_id
)
SELECT * FROM hierarchy ORDER BY level, name;


-- ════════════════════════════════════════════════════════════════════
-- E2. SUBQUERY TYPES
-- ════════════════════════════════════════════════════════════════════
/*
┌────────────────────────┬──────────────────────────────────────────────┐
│ Type                   │ Example                                      │
├────────────────────────┼──────────────────────────────────────────────┤
│ Scalar (returns 1 val) │ WHERE salary > (SELECT AVG(salary) FROM ..) │
│ Column (returns col)   │ WHERE id IN (SELECT id FROM ...)            │
│ Table (returns table)  │ FROM (SELECT ... GROUP BY ...) AS sub       │
│ Correlated (refs outer)│ WHERE salary > (SELECT AVG(s) FROM e2       │
│                        │   WHERE e2.dept = e1.dept)                   │
│ Lateral (Postgres)     │ CROSS JOIN LATERAL (subquery using outer)   │
└────────────────────────┴──────────────────────────────────────────────┘

CTE vs Subquery:
  CTE       → more readable, reusable, supports recursion
  Subquery  → inline, sometimes optimized differently
  In most modern DBs, performance is equivalent.
*/


-- ════════════════════════════════════════════════════════════════════
-- E3. PIVOT & UNPIVOT
-- ════════════════════════════════════════════════════════════════════
/*
Standard SQL doesn't have PIVOT. Use CASE + aggregate:
*/

-- PIVOT: rows → columns
SELECT region,
       SUM(CASE WHEN product = 'Widget' THEN amount ELSE 0 END) AS Widget,
       SUM(CASE WHEN product = 'Gadget' THEN amount ELSE 0 END) AS Gadget,
       SUM(CASE WHEN product = 'Gizmo'  THEN amount ELSE 0 END) AS Gizmo
FROM orders
GROUP BY region;

-- UNPIVOT: columns → rows (using UNION ALL)
SELECT id, 'Math'    AS subject, math_score    AS score FROM wide_scores
UNION ALL
SELECT id, 'Science' AS subject, science_score AS score FROM wide_scores
UNION ALL
SELECT id, 'English' AS subject, english_score AS score FROM wide_scores;

-- CROSSTAB: frequency counts
SELECT region,
       COUNT(CASE WHEN product = 'Widget' THEN 1 END) AS widget_count,
       COUNT(CASE WHEN product = 'Gadget' THEN 1 END) AS gadget_count,
       COUNT(CASE WHEN product = 'Gizmo'  THEN 1 END) AS gizmo_count
FROM orders
GROUP BY region;


-- ╔════════════════════════════════════════════════════════════════════╗
-- ║  PART F: DATE & STRING FUNCTIONS                                    ║
-- ╚════════════════════════════════════════════════════════════════════╝

-- ════════════════════════════════════════════════════════════════════
-- F1. DATE FUNCTIONS (dialect comparison)
-- ════════════════════════════════════════════════════════════════════
/*
┌─────────────────────┬──────────────────┬──────────────────┬──────────────────┐
│ Operation           │ Postgres          │ MySQL             │ BigQuery          │
├─────────────────────┼──────────────────┼──────────────────┼──────────────────┤
│ Current date        │ CURRENT_DATE      │ CURDATE()         │ CURRENT_DATE()    │
│ Current timestamp   │ NOW()             │ NOW()             │ CURRENT_TIMESTAMP │
│ Extract year        │ EXTRACT(YEAR FROM │ YEAR(d)           │ EXTRACT(YEAR      │
│                     │   d)              │                   │   FROM d)         │
│ Truncate to month   │ DATE_TRUNC('month'│ DATE_FORMAT(d,    │ DATE_TRUNC(d,     │
│                     │  , d)             │  '%Y-%m-01')      │   MONTH)          │
│ Add interval        │ d + INTERVAL '7  │ DATE_ADD(d,       │ DATE_ADD(d,       │
│                     │   days'           │  INTERVAL 7 DAY)  │  INTERVAL 7 DAY)  │
│ Days between        │ d2 - d1           │ DATEDIFF(d2, d1)  │ DATE_DIFF(d2,d1,  │
│                     │                   │                   │   DAY)            │
│ Format              │ TO_CHAR(d,        │ DATE_FORMAT(d,    │ FORMAT_DATE(      │
│                     │  'YYYY-MM')       │  '%Y-%m')         │  '%Y-%m', d)      │
│ Parse string        │ TO_DATE('2023-01' │ STR_TO_DATE(s,    │ PARSE_DATE(       │
│                     │  ,'YYYY-MM')      │  '%Y-%m-%d')      │  '%Y-%m-%d', s)   │
└─────────────────────┴──────────────────┴──────────────────┴──────────────────┘

SQLite date functions:
  DATE('now')                          -- current date
  STRFTIME('%Y-%m', date_col)          -- format / truncate
  JULIANDAY(d2) - JULIANDAY(d1)       -- days between
  DATE(d, '+7 days')                   -- add interval
*/


-- ════════════════════════════════════════════════════════════════════
-- F2. STRING FUNCTIONS (dialect comparison)
-- ════════════════════════════════════════════════════════════════════
/*
┌─────────────────────┬──────────────────────────────────────────────────┐
│ Operation           │ Standard / Postgres                               │
├─────────────────────┼──────────────────────────────────────────────────┤
│ Concatenate         │ 'a' || 'b'   or   CONCAT('a', 'b')              │
│ Length              │ LENGTH(s)    or   CHAR_LENGTH(s)                 │
│ Uppercase           │ UPPER(s)                                         │
│ Lowercase           │ LOWER(s)                                         │
│ Trim                │ TRIM(s)   LTRIM(s)   RTRIM(s)                    │
│ Substring           │ SUBSTRING(s, start, length)                      │
│                     │ SUBSTR(s, start, length)     -- SQLite/Oracle     │
│ Position            │ POSITION('sub' IN s)         -- Postgres          │
│                     │ INSTR(s, 'sub')              -- MySQL/SQLite      │
│ Replace             │ REPLACE(s, 'old', 'new')                         │
│ Left / Right        │ LEFT(s, n)  /  RIGHT(s, n)                       │
│ Pad                 │ LPAD(s, len, '0')  /  RPAD(s, len, ' ')         │
│ Split (Postgres)    │ SPLIT_PART(s, delimiter, n)                      │
│ Regex (Postgres)    │ s ~ 'pattern'   /   REGEXP_MATCHES(s, pat)      │
│ Regex (MySQL)       │ s REGEXP 'pattern'                               │
└─────────────────────┴──────────────────────────────────────────────────┘
*/


-- ╔════════════════════════════════════════════════════════════════════╗
-- ║  PART G: ADVANCED PATTERNS                                          ║
-- ╚════════════════════════════════════════════════════════════════════╝

-- ════════════════════════════════════════════════════════════════════
-- G1. CONSECUTIVE STREAK DETECTION
-- ════════════════════════════════════════════════════════════════════
/*
Classic interview question: find consecutive login days.

Technique: date - ROW_NUMBER = constant for consecutive dates
*/
WITH numbered AS (
    SELECT user_id, login_date,
           login_date - ROW_NUMBER() OVER (
               PARTITION BY user_id ORDER BY login_date
           ) * INTERVAL '1 day' AS grp    -- Postgres syntax
    FROM daily_logins
),
streaks AS (
    SELECT user_id, grp,
           COUNT(*) AS streak_len,
           MIN(login_date) AS start_date,
           MAX(login_date) AS end_date
    FROM numbered
    GROUP BY user_id, grp
)
SELECT user_id, MAX(streak_len) AS max_streak
FROM streaks
GROUP BY user_id;


-- ════════════════════════════════════════════════════════════════════
-- G2. GAPS AND ISLANDS
-- ════════════════════════════════════════════════════════════════════
/*
Find gaps in sequential data (missing IDs, date gaps, etc.)
*/
-- Using LEAD to find gaps
SELECT order_id AS gap_start,
       LEAD(order_id) OVER (ORDER BY order_id) AS gap_end,
       LEAD(order_id) OVER (ORDER BY order_id) - order_id AS gap_size
FROM orders
WHERE LEAD(order_id) OVER (ORDER BY order_id) - order_id > 1;

-- Islands: find contiguous groups
WITH islands AS (
    SELECT val,
           val - ROW_NUMBER() OVER (ORDER BY val) AS island_id
    FROM my_table
)
SELECT MIN(val) AS island_start, MAX(val) AS island_end, COUNT(*) AS island_size
FROM islands
GROUP BY island_id;


-- ════════════════════════════════════════════════════════════════════
-- G3. MEDIAN (no built-in in most dialects)
-- ════════════════════════════════════════════════════════════════════

-- Postgres (simplest)
SELECT PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY salary) AS median
FROM employees;

-- Standard SQL approach
WITH ordered AS (
    SELECT salary,
           ROW_NUMBER() OVER (ORDER BY salary) AS rn,
           COUNT(*) OVER () AS total
    FROM employees
)
SELECT AVG(salary) AS median
FROM ordered
WHERE rn IN ((total + 1) / 2, (total + 2) / 2);


-- ════════════════════════════════════════════════════════════════════
-- G4. WEIGHTED AVERAGE
-- ════════════════════════════════════════════════════════════════════

-- Weighted average = SUM(value * weight) / SUM(weight)
SELECT SUM(score * weight) * 1.0 / SUM(weight) AS weighted_avg
FROM scores_with_weights;


-- ════════════════════════════════════════════════════════════════════
-- G5. DEDUPLICATION
-- ════════════════════════════════════════════════════════════════════

-- Keep first occurrence of each duplicate
WITH ranked AS (
    SELECT *,
           ROW_NUMBER() OVER (
               PARTITION BY email
               ORDER BY created_at ASC    -- keep earliest
           ) AS rn
    FROM users
)
SELECT * FROM ranked WHERE rn = 1;

-- Delete duplicates (keep one)
DELETE FROM users
WHERE id NOT IN (
    SELECT MIN(id) FROM users GROUP BY email
);


-- ╔════════════════════════════════════════════════════════════════════╗
-- ║  PART H: INTERVIEW DECISION TREE                                    ║
-- ╚════════════════════════════════════════════════════════════════════╝
/*
┌──────────────────────────────────────────────────────────────────────────┐
│                     SQL INTERVIEW DECISION TREE                          │
│                  "What SQL construct do I use?"                           │
└──────────────────────────────────────────────────────────────────────────┘

  Q: "Per group, compute X"
     → GROUP BY + aggregate (SUM, AVG, COUNT, etc.)

  Q: "Add a column showing group stat for each row"
     → Window function: SUM/AVG() OVER(PARTITION BY ...)

  Q: "Filter on aggregated results"
     → GROUP BY + HAVING (not WHERE)

  Q: "Rank within group"
     → RANK/DENSE_RANK/ROW_NUMBER() OVER(PARTITION BY ... ORDER BY ...)

  Q: "Top N per group"
     → CTE with RANK/DENSE_RANK + WHERE rnk <= N

  Q: "Running/cumulative total"
     → SUM() OVER(ORDER BY ... ROWS UNBOUNDED PRECEDING)

  Q: "Moving average"
     → AVG() OVER(ORDER BY ... ROWS BETWEEN N PRECEDING AND CURRENT ROW)

  Q: "Previous/next row value"
     → LAG(col, 1) / LEAD(col, 1) OVER(ORDER BY ...)

  Q: "Rows to columns"
     → SUM(CASE WHEN col='X' THEN val END) pattern (manual PIVOT)

  Q: "Columns to rows"
     → UNION ALL pattern (manual UNPIVOT)

  Q: "Rows not in another table"
     → LEFT JOIN + WHERE IS NULL  or  NOT EXISTS

  Q: "Rows in both tables"
     → INNER JOIN  or  EXISTS

  Q: "All combinations"
     → CROSS JOIN

  Q: "Consecutive sequences"
     → date - ROW_NUMBER() trick for streak detection

  Q: "Median"
     → PERCENTILE_CONT(0.5) or ROW_NUMBER middle-row trick

  Q: "Weighted average"
     → SUM(val * weight) / SUM(weight)

  Q: "Deduplicate"
     → ROW_NUMBER() OVER(PARTITION BY dup_cols ORDER BY ...) + WHERE rn=1

  Q: "Break complex query into steps"
     → CTEs (WITH clause)

  Q: "Tree / hierarchy traversal"
     → WITH RECURSIVE

  Q: "Conditional column"
     → CASE WHEN ... THEN ... ELSE ... END

  Q: "Avoid division by zero"
     → col / NULLIF(divisor, 0)

  Q: "Replace NULL with default"
     → COALESCE(col, default_value)


┌──────────────────────────────────────────────────────────────────────────┐
│               TOP 10 INTERVIEW PATTERNS — Quick Reference                │
└──────────────────────────────────────────────────────────────────────────┘

1. Second highest salary per department
   → DENSE_RANK() OVER(PARTITION BY dept ORDER BY salary DESC)
     + WHERE rnk = 2

2. Employees above department average
   → Window: salary > AVG(salary) OVER(PARTITION BY dept)
   → Subquery: salary > (SELECT AVG(salary) ... WHERE dept = ...)

3. Month-over-month growth
   → CTE: monthly totals → LAG for previous month → calculate %

4. Consecutive login streaks
   → date - ROW_NUMBER() = constant for consecutive dates

5. Running balance
   → SUM(CASE credit/debit) OVER(PARTITION BY account ORDER BY date)

6. Find duplicates
   → GROUP BY + HAVING COUNT(*) > 1
   → Or ROW_NUMBER to identify specific duplicate rows

7. Anti-join (not in another table)
   → LEFT JOIN + WHERE IS NULL

8. Pivot report
   → SUM(CASE WHEN category='X' THEN amount END) for each category

9. Weighted average
   → SUM(value * weight) / SUM(weight)

10. Hierarchical query
    → WITH RECURSIVE (Postgres, MySQL 8+, SQLite)
*/
