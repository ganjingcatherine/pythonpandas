"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  50 SQL CODING INTERVIEW QUESTIONS — Data Manipulation
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Topics covered:
  • Filtering & WHERE clauses (Q1–Q8)
  • Window Functions (Q9–Q20)
  • GROUP BY & Aggregation (Q21–Q30)
  • Joins & Subqueries (Q31–Q38)
  • Pivot / Reshape / CASE (Q39–Q44)
  • Statistical & Advanced (Q45–Q50)

Each question includes:
  - Setup DDL + sample data (SQLite-compatible)
  - Problem statement
  - Expected output
  - Solution with explanation

Run:  python sql_interview_50.py          (executes all 50 in SQLite)
      python sql_interview_50.py --q 15   (run only question 15)
"""

import sqlite3
import textwrap
import sys


# ════════════════════════════════════════════════════════════════════════
# SHARED SETUP — tables reused across many questions
# ════════════════════════════════════════════════════════════════════════

SHARED_SETUP = """
-- employees table
CREATE TABLE IF NOT EXISTS employees (
    emp_id      INTEGER PRIMARY KEY,
    name        TEXT,
    department  TEXT,
    salary      INTEGER,
    hire_date   TEXT,       -- 'YYYY-MM-DD'
    manager_id  INTEGER
);
INSERT OR IGNORE INTO employees VALUES
    (1,  'Alice',   'Engineering', 95000,  '2020-01-15', NULL),
    (2,  'Bob',     'Engineering', 85000,  '2020-03-20', 1),
    (3,  'Carol',   'Engineering', 78000,  '2021-06-10', 1),
    (4,  'Dave',    'Sales',       72000,  '2019-02-05', NULL),
    (5,  'Eve',     'Sales',       91000,  '2020-04-18', 4),
    (6,  'Frank',   'Sales',       68000,  '2021-07-22', 4),
    (7,  'Grace',   'Marketing',   82000,  '2020-09-01', NULL),
    (8,  'Hank',    'Marketing',   75000,  '2021-11-15', 7),
    (9,  'Ivy',     'Engineering', 92000,  '2022-01-10', 1),
    (10, 'Jack',    'Marketing',   88000,  '2022-05-20', 7);

-- orders table
CREATE TABLE IF NOT EXISTS orders (
    order_id    INTEGER PRIMARY KEY,
    customer_id INTEGER,
    order_date  TEXT,
    amount      REAL,
    product     TEXT,
    region      TEXT
);
INSERT OR IGNORE INTO orders VALUES
    (1,  101, '2023-01-05', 250.00,  'Widget',  'East'),
    (2,  102, '2023-01-12', 450.00,  'Gadget',  'West'),
    (3,  101, '2023-02-08', 300.00,  'Widget',  'East'),
    (4,  103, '2023-02-14', 150.00,  'Gizmo',   'East'),
    (5,  102, '2023-03-01', 500.00,  'Gadget',  'West'),
    (6,  104, '2023-03-15', 200.00,  'Widget',  'South'),
    (7,  101, '2023-04-02', 350.00,  'Gizmo',   'East'),
    (8,  103, '2023-04-20', 275.00,  'Widget',  'East'),
    (9,  105, '2023-05-10', 600.00,  'Gadget',  'West'),
    (10, 102, '2023-05-25', 100.00,  'Gizmo',   'West'),
    (11, 101, '2023-06-15', 400.00,  'Widget',  'East'),
    (12, 104, '2023-06-28', 325.00,  'Gadget',  'South'),
    (13, 105, '2023-07-05', 550.00,  'Widget',  'West'),
    (14, 103, '2023-07-18', 175.00,  'Gizmo',   'East'),
    (15, 101, '2023-08-01', 450.00,  'Gadget',  'East');

-- daily_logins for streak / time-series questions
CREATE TABLE IF NOT EXISTS daily_logins (
    user_id    INTEGER,
    login_date TEXT
);
INSERT OR IGNORE INTO daily_logins VALUES
    (1, '2023-01-01'), (1, '2023-01-02'), (1, '2023-01-03'),
    (1, '2023-01-05'), (1, '2023-01-06'),
    (2, '2023-01-01'), (2, '2023-01-03'), (2, '2023-01-04'),
    (2, '2023-01-05'), (2, '2023-01-06'), (2, '2023-01-07'),
    (1, '2023-01-10'), (1, '2023-01-11'), (1, '2023-01-12'),
    (1, '2023-01-13');

-- student_scores for stats questions
CREATE TABLE IF NOT EXISTS student_scores (
    student_id INTEGER,
    subject    TEXT,
    score      INTEGER
);
INSERT OR IGNORE INTO student_scores VALUES
    (1, 'Math',    85), (1, 'Science', 90), (1, 'English', 78),
    (2, 'Math',    92), (2, 'Science', 88), (2, 'English', 95),
    (3, 'Math',    70), (3, 'Science', 75), (3, 'English', 80),
    (4, 'Math',    88), (4, 'Science', 92), (4, 'English', 85),
    (5, 'Math',    95), (5, 'Science', 85), (5, 'English', 90);

-- transactions for financial questions
CREATE TABLE IF NOT EXISTS transactions (
    txn_id      INTEGER PRIMARY KEY,
    account_id  INTEGER,
    txn_date    TEXT,
    txn_type    TEXT,    -- 'credit' or 'debit'
    amount      REAL
);
INSERT OR IGNORE INTO transactions VALUES
    (1,  1001, '2023-01-05', 'credit', 1000),
    (2,  1001, '2023-01-10', 'debit',   200),
    (3,  1001, '2023-02-01', 'credit',  500),
    (4,  1002, '2023-01-15', 'credit', 2000),
    (5,  1002, '2023-02-10', 'debit',   750),
    (6,  1002, '2023-03-01', 'credit',  300),
    (7,  1001, '2023-03-15', 'debit',   400),
    (8,  1003, '2023-01-20', 'credit', 1500),
    (9,  1003, '2023-02-15', 'debit',   600),
    (10, 1003, '2023-03-20', 'credit',  800);
"""


# ════════════════════════════════════════════════════════════════════════
# QUESTIONS
# ════════════════════════════════════════════════════════════════════════

QUESTIONS = [

    # ──────────────────────────────────────────────────────────────────
    # SECTION 1: FILTERING & WHERE (Q1–Q8)
    # ──────────────────────────────────────────────────────────────────

    {
        "id": 1,
        "title": "Basic WHERE with multiple conditions",
        "difficulty": "Easy",
        "category": "Filtering",
        "problem": """
            Find all employees in Engineering who earn more than 80000.
        """,
        "expected": "Bob (85000), Alice (95000), Ivy (92000)",
        "solution": """
            SELECT name, salary
            FROM employees
            WHERE department = 'Engineering'
              AND salary > 80000
            ORDER BY salary;
        """,
        "explanation": """
            Basic AND filtering. Always check if question asks for
            specific ordering. Here ORDER BY is optional but good practice.
        """
    },
    {
        "id": 2,
        "title": "IN and NOT IN filtering",
        "difficulty": "Easy",
        "category": "Filtering",
        "problem": """
            Find all orders for products that are NOT 'Widget'.
        """,
        "expected": "Orders for Gadget and Gizmo",
        "solution": """
            SELECT order_id, product, amount
            FROM orders
            WHERE product NOT IN ('Widget')
            ORDER BY order_id;
        """,
        "explanation": """
            NOT IN filters out matching values. Watch for NULL gotcha:
            if the list contains NULL, NOT IN returns empty! Use NOT EXISTS instead.
        """
    },
    {
        "id": 3,
        "title": "BETWEEN for date range filtering",
        "difficulty": "Easy",
        "category": "Filtering",
        "problem": """
            Find all orders placed in Q1 2023 (Jan–Mar).
        """,
        "expected": "Orders 1-6",
        "solution": """
            SELECT order_id, order_date, amount
            FROM orders
            WHERE order_date BETWEEN '2023-01-01' AND '2023-03-31'
            ORDER BY order_date;
        """,
        "explanation": """
            BETWEEN is inclusive on both ends. For dates, make sure the
            end date covers the full day (use '2023-03-31' not '2023-03-30').
        """
    },
    {
        "id": 4,
        "title": "LIKE pattern matching",
        "difficulty": "Easy",
        "category": "Filtering",
        "problem": """
            Find employees whose names start with a vowel (A, E, I, O, U).
        """,
        "expected": "Alice, Eve, Ivy",
        "solution": """
            SELECT name, department
            FROM employees
            WHERE name LIKE 'A%'
               OR name LIKE 'E%'
               OR name LIKE 'I%'
               OR name LIKE 'O%'
               OR name LIKE 'U%'
            ORDER BY name;
        """,
        "explanation": """
            LIKE with % wildcard. Some dialects support REGEXP or
            SIMILAR TO for more complex patterns. Alternative:
            WHERE SUBSTR(name, 1, 1) IN ('A','E','I','O','U')
        """
    },
    {
        "id": 5,
        "title": "Filtering with NULL handling",
        "difficulty": "Easy",
        "category": "Filtering",
        "problem": """
            Find all employees who DO have a manager (manager_id is not null).
        """,
        "expected": "Bob, Carol, Eve, Frank, Hank, Ivy, Jack",
        "solution": """
            SELECT name, manager_id
            FROM employees
            WHERE manager_id IS NOT NULL
            ORDER BY name;
        """,
        "explanation": """
            NULL requires IS NULL / IS NOT NULL. Never use = NULL or != NULL,
            because NULL = NULL evaluates to NULL (not TRUE).
        """
    },
    {
        "id": 6,
        "title": "Subquery in WHERE — filter by aggregate",
        "difficulty": "Medium",
        "category": "Filtering",
        "problem": """
            Find employees whose salary is above the company-wide average.
        """,
        "expected": "Alice (95000), Eve (91000), Ivy (92000), Jack (88000)",
        "solution": """
            SELECT name, salary
            FROM employees
            WHERE salary > (SELECT AVG(salary) FROM employees)
            ORDER BY salary DESC;
        """,
        "explanation": """
            Scalar subquery in WHERE. The inner query computes one value
            (the average), then the outer query filters against it.
            Alternative: use a CTE or window function.
        """
    },
    {
        "id": 7,
        "title": "EXISTS — correlated subquery filter",
        "difficulty": "Medium",
        "category": "Filtering",
        "problem": """
            Find customers who have placed at least one order above $400.
        """,
        "expected": "customer_ids: 101, 102, 105",
        "solution": """
            SELECT DISTINCT customer_id
            FROM orders o1
            WHERE EXISTS (
                SELECT 1 FROM orders o2
                WHERE o2.customer_id = o1.customer_id
                  AND o2.amount > 400
            )
            ORDER BY customer_id;
        """,
        "explanation": """
            EXISTS is often faster than IN for large datasets because it
            short-circuits. Here we could also use:
            SELECT DISTINCT customer_id FROM orders WHERE amount > 400
        """
    },
    {
        "id": 8,
        "title": "HAVING — filter on aggregated results",
        "difficulty": "Easy",
        "category": "Filtering",
        "problem": """
            Find customers who have placed more than 3 orders.
        """,
        "expected": "customer_id 101 (5 orders), 102 (3 orders), 103 (3 orders) — only 101",
        "solution": """
            SELECT customer_id, COUNT(*) AS order_count
            FROM orders
            GROUP BY customer_id
            HAVING COUNT(*) > 3
            ORDER BY order_count DESC;
        """,
        "explanation": """
            WHERE filters rows BEFORE grouping.
            HAVING filters groups AFTER aggregation.
            Cannot use column alias in HAVING in some dialects.
        """
    },

    # ──────────────────────────────────────────────────────────────────
    # SECTION 2: WINDOW FUNCTIONS (Q9–Q20)
    # ──────────────────────────────────────────────────────────────────

    {
        "id": 9,
        "title": "ROW_NUMBER — assign sequential rank",
        "difficulty": "Medium",
        "category": "Window",
        "problem": """
            Assign a row number to each employee within their department,
            ordered by salary descending.
        """,
        "expected": "Each dept's highest paid = row 1",
        "solution": """
            SELECT name, department, salary,
                   ROW_NUMBER() OVER (
                       PARTITION BY department
                       ORDER BY salary DESC
                   ) AS row_num
            FROM employees
            ORDER BY department, row_num;
        """,
        "explanation": """
            ROW_NUMBER: unique sequential integer, no ties.
            PARTITION BY = grouping, ORDER BY = sort within partition.
        """
    },
    {
        "id": 10,
        "title": "RANK vs DENSE_RANK — handling ties",
        "difficulty": "Medium",
        "category": "Window",
        "problem": """
            Rank all employees by salary. Show both RANK and DENSE_RANK
            to illustrate the difference. (For demo, we'll see the gap behavior.)
        """,
        "expected": "RANK skips numbers after ties, DENSE_RANK does not",
        "solution": """
            SELECT name, salary,
                   RANK()       OVER (ORDER BY salary DESC) AS rnk,
                   DENSE_RANK() OVER (ORDER BY salary DESC) AS dense_rnk
            FROM employees
            ORDER BY salary DESC;
        """,
        "explanation": """
            RANK:       1, 2, 2, 4 (skips 3)
            DENSE_RANK: 1, 2, 2, 3 (no gap)
            ROW_NUMBER: 1, 2, 3, 4 (always unique)
        """
    },
    {
        "id": 11,
        "title": "Top N per group — second highest salary per department",
        "difficulty": "Medium",
        "category": "Window",
        "problem": """
            Find the employee with the second highest salary in each department.
        """,
        "expected": "Engineering: Bob/Ivy (2nd), Sales: Frank or someone, Marketing: someone",
        "solution": """
            WITH ranked AS (
                SELECT name, department, salary,
                       DENSE_RANK() OVER (
                           PARTITION BY department
                           ORDER BY salary DESC
                       ) AS rnk
                FROM employees
            )
            SELECT name, department, salary
            FROM ranked
            WHERE rnk = 2;
        """,
        "explanation": """
            Classic top-N-per-group pattern:
            1. Use window function to rank within group
            2. Filter in outer query (can't filter window in WHERE directly)
            Use DENSE_RANK to handle ties gracefully.
        """
    },
    {
        "id": 12,
        "title": "LAG — previous row value",
        "difficulty": "Medium",
        "category": "Window",
        "problem": """
            For each order by customer 101, show the previous order amount
            and the difference from the previous order.
        """,
        "expected": "Each row shows current amount, prev amount, and delta",
        "solution": """
            SELECT order_id, order_date, amount,
                   LAG(amount, 1) OVER (ORDER BY order_date) AS prev_amount,
                   amount - LAG(amount, 1) OVER (ORDER BY order_date) AS delta
            FROM orders
            WHERE customer_id = 101
            ORDER BY order_date;
        """,
        "explanation": """
            LAG(col, n) looks n rows BACK. First row has NULL for LAG.
            LEAD(col, n) looks n rows FORWARD.
            Optional 3rd arg: default value for NULL.
        """
    },
    {
        "id": 13,
        "title": "LEAD — next row value for gap detection",
        "difficulty": "Medium",
        "category": "Window",
        "problem": """
            For user 1's logins, find gaps: show each login date and the
            next login date. Flag rows where the gap is more than 1 day.
        """,
        "expected": "Gaps on 2023-01-03→01-05 and 2023-01-06→01-10",
        "solution": """
            SELECT login_date,
                   LEAD(login_date) OVER (ORDER BY login_date) AS next_login,
                   JULIANDAY(LEAD(login_date) OVER (ORDER BY login_date))
                     - JULIANDAY(login_date) AS days_gap,
                   CASE
                       WHEN JULIANDAY(LEAD(login_date) OVER (ORDER BY login_date))
                            - JULIANDAY(login_date) > 1
                       THEN 'GAP'
                       ELSE 'OK'
                   END AS status
            FROM daily_logins
            WHERE user_id = 1
            ORDER BY login_date;
        """,
        "explanation": """
            LEAD looks at the next row. Combine with date arithmetic
            to detect gaps in sequential data. JULIANDAY is SQLite-specific;
            use DATEDIFF in MySQL/Postgres.
        """
    },
    {
        "id": 14,
        "title": "Running total — cumulative sum",
        "difficulty": "Medium",
        "category": "Window",
        "problem": """
            Calculate a running total of order amounts, ordered by date.
        """,
        "expected": "Cumulative sum grows with each row",
        "solution": """
            SELECT order_id, order_date, amount,
                   SUM(amount) OVER (
                       ORDER BY order_date
                       ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
                   ) AS running_total
            FROM orders
            ORDER BY order_date;
        """,
        "explanation": """
            SUM() OVER(ORDER BY ...) with ROWS UNBOUNDED PRECEDING
            gives a running total. This is the default frame for ORDER BY,
            so you can often omit the ROWS clause.
        """
    },
    {
        "id": 15,
        "title": "Moving average — rolling window",
        "difficulty": "Medium",
        "category": "Window",
        "problem": """
            Calculate a 3-order moving average of amounts for each order.
        """,
        "expected": "Each row shows average of current + 2 preceding orders",
        "solution": """
            SELECT order_id, order_date, amount,
                   ROUND(AVG(amount) OVER (
                       ORDER BY order_date
                       ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
                   ), 2) AS moving_avg_3
            FROM orders
            ORDER BY order_date;
        """,
        "explanation": """
            ROWS BETWEEN 2 PRECEDING AND CURRENT ROW = window of 3 rows.
            First row only has itself; second has 2 rows; third onward has 3.
            Use RANGE instead of ROWS for value-based windows.
        """
    },
    {
        "id": 16,
        "title": "Percent of total — ratio to group",
        "difficulty": "Medium",
        "category": "Window",
        "problem": """
            For each order, show what percentage of the region's total
            that order represents.
        """,
        "expected": "Each row: amount / SUM for that region * 100",
        "solution": """
            SELECT order_id, region, amount,
                   SUM(amount) OVER (PARTITION BY region) AS region_total,
                   ROUND(amount * 100.0 / SUM(amount) OVER (PARTITION BY region), 1)
                       AS pct_of_region
            FROM orders
            ORDER BY region, order_id;
        """,
        "explanation": """
            SUM() OVER(PARTITION BY region) without ORDER BY = total for
            the entire partition (no running sum). Dividing gives percentage.
        """
    },
    {
        "id": 17,
        "title": "NTILE — divide into quartiles",
        "difficulty": "Medium",
        "category": "Window",
        "problem": """
            Divide employees into 4 salary quartiles across the company.
        """,
        "expected": "Each employee assigned quartile 1-4",
        "solution": """
            SELECT name, salary,
                   NTILE(4) OVER (ORDER BY salary) AS quartile
            FROM employees
            ORDER BY salary;
        """,
        "explanation": """
            NTILE(n) divides rows into n roughly equal buckets.
            Useful for percentile analysis. If 10 rows / 4 buckets,
            first 2 buckets get 3 rows, last 2 get 2 rows.
        """
    },
    {
        "id": 18,
        "title": "FIRST_VALUE / LAST_VALUE",
        "difficulty": "Medium",
        "category": "Window",
        "problem": """
            For each employee, show the highest and lowest salary
            in their department (using window functions, not subquery).
        """,
        "expected": "Each row shows dept min and max salary",
        "solution": """
            SELECT name, department, salary,
                   FIRST_VALUE(salary) OVER (
                       PARTITION BY department ORDER BY salary DESC
                   ) AS dept_max,
                   FIRST_VALUE(salary) OVER (
                       PARTITION BY department ORDER BY salary ASC
                   ) AS dept_min
            FROM employees
            ORDER BY department, salary DESC;
        """,
        "explanation": """
            FIRST_VALUE gets the first value in the window frame.
            For LAST_VALUE, beware the default frame (RANGE BETWEEN
            UNBOUNDED PRECEDING AND CURRENT ROW) — you need
            ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING.
            Using FIRST_VALUE with reversed ORDER BY is safer.
        """
    },
    {
        "id": 19,
        "title": "Consecutive login streaks",
        "difficulty": "Hard",
        "category": "Window",
        "problem": """
            Find the longest consecutive login streak for each user.
        """,
        "expected": "User 1: 4 days (Jan 10-13), User 2: 5 days (Jan 3-7)",
        "solution": """
            WITH numbered AS (
                SELECT user_id, login_date,
                       DATE(login_date, '-' || (ROW_NUMBER() OVER (
                           PARTITION BY user_id ORDER BY login_date
                       ) - 1) || ' days') AS grp
                FROM daily_logins
            ),
            streaks AS (
                SELECT user_id, grp,
                       COUNT(*) AS streak_len,
                       MIN(login_date) AS streak_start,
                       MAX(login_date) AS streak_end
                FROM numbered
                GROUP BY user_id, grp
            )
            SELECT user_id, MAX(streak_len) AS longest_streak,
                   streak_start, streak_end
            FROM streaks
            GROUP BY user_id
            ORDER BY user_id;
        """,
        "explanation": """
            Classic streak detection:
            1. Subtract row_number from date → consecutive dates get same group value
            2. Group by that computed group
            3. Count within each group = streak length
            This works because if dates are consecutive (1,2,3) and row numbers
            are (1,2,3), then date - row_num = constant.
        """
    },
    {
        "id": 20,
        "title": "Month-over-month growth rate",
        "difficulty": "Medium",
        "category": "Window",
        "problem": """
            Calculate month-over-month revenue growth percentage.
        """,
        "expected": "Each month's total and % change from previous month",
        "solution": """
            WITH monthly AS (
                SELECT STRFTIME('%Y-%m', order_date) AS month,
                       SUM(amount) AS revenue
                FROM orders
                GROUP BY STRFTIME('%Y-%m', order_date)
            )
            SELECT month, revenue,
                   LAG(revenue) OVER (ORDER BY month) AS prev_revenue,
                   ROUND((revenue - LAG(revenue) OVER (ORDER BY month))
                         * 100.0 / LAG(revenue) OVER (ORDER BY month), 1)
                       AS growth_pct
            FROM monthly
            ORDER BY month;
        """,
        "explanation": """
            Pattern: aggregate to desired granularity first (CTE),
            then apply LAG for comparison. Growth = (current - prev) / prev * 100.
        """
    },

    # ──────────────────────────────────────────────────────────────────
    # SECTION 3: GROUP BY & AGGREGATION (Q21–Q30)
    # ──────────────────────────────────────────────────────────────────

    {
        "id": 21,
        "title": "Basic GROUP BY with multiple aggregates",
        "difficulty": "Easy",
        "category": "GroupBy",
        "problem": """
            For each department, find the average salary, min salary,
            max salary, and employee count.
        """,
        "expected": "3 rows (one per dept) with 4 aggregate columns",
        "solution": """
            SELECT department,
                   COUNT(*)        AS emp_count,
                   ROUND(AVG(salary), 0) AS avg_salary,
                   MIN(salary)     AS min_salary,
                   MAX(salary)     AS max_salary
            FROM employees
            GROUP BY department
            ORDER BY avg_salary DESC;
        """,
        "explanation": """
            Multiple aggregates in one GROUP BY. All non-aggregated columns
            in SELECT must appear in GROUP BY (SQL standard).
        """
    },
    {
        "id": 22,
        "title": "GROUP BY with HAVING — filter groups",
        "difficulty": "Easy",
        "category": "GroupBy",
        "problem": """
            Find regions where total order amount exceeds $1000.
        """,
        "expected": "East and West regions",
        "solution": """
            SELECT region, SUM(amount) AS total_amount
            FROM orders
            GROUP BY region
            HAVING SUM(amount) > 1000
            ORDER BY total_amount DESC;
        """,
        "explanation": """
            HAVING filters AFTER aggregation (unlike WHERE which filters before).
            Common interview question: "What's the difference between WHERE and HAVING?"
        """
    },
    {
        "id": 23,
        "title": "GROUP BY multiple columns",
        "difficulty": "Easy",
        "category": "GroupBy",
        "problem": """
            Find the total sales per region per product.
        """,
        "expected": "Grid of region × product with totals",
        "solution": """
            SELECT region, product,
                   SUM(amount)  AS total_sales,
                   COUNT(*)     AS num_orders
            FROM orders
            GROUP BY region, product
            ORDER BY region, product;
        """,
        "explanation": """
            Grouping by multiple columns creates a cross-tabulation.
            This is the raw data you'd pivot for a matrix view.
        """
    },
    {
        "id": 24,
        "title": "Conditional aggregation — CASE inside aggregate",
        "difficulty": "Medium",
        "category": "GroupBy",
        "problem": """
            For each account, calculate total credits, total debits,
            and net balance in a single query.
        """,
        "expected": "One row per account with credits, debits, and net",
        "solution": """
            SELECT account_id,
                   SUM(CASE WHEN txn_type = 'credit' THEN amount ELSE 0 END) AS total_credits,
                   SUM(CASE WHEN txn_type = 'debit'  THEN amount ELSE 0 END) AS total_debits,
                   SUM(CASE WHEN txn_type = 'credit' THEN amount ELSE -amount END) AS net_balance
            FROM transactions
            GROUP BY account_id
            ORDER BY account_id;
        """,
        "explanation": """
            CASE inside SUM/COUNT is the SQL equivalent of conditional aggregation.
            This avoids multiple self-joins or subqueries.
            Pattern: SUM(CASE WHEN condition THEN value ELSE 0 END)
        """
    },
    {
        "id": 25,
        "title": "COUNT DISTINCT — unique values per group",
        "difficulty": "Easy",
        "category": "GroupBy",
        "problem": """
            For each region, count the number of distinct customers
            and distinct products ordered.
        """,
        "expected": "Per region: unique customer and product counts",
        "solution": """
            SELECT region,
                   COUNT(DISTINCT customer_id) AS unique_customers,
                   COUNT(DISTINCT product)     AS unique_products,
                   COUNT(*)                    AS total_orders
            FROM orders
            GROUP BY region
            ORDER BY region;
        """,
        "explanation": """
            COUNT(DISTINCT col) counts unique non-null values.
            COUNT(*) counts all rows including nulls.
            COUNT(col) counts non-null values only.
        """
    },
    {
        "id": 26,
        "title": "GROUP BY with date truncation",
        "difficulty": "Medium",
        "category": "GroupBy",
        "problem": """
            Calculate monthly order totals and order counts.
        """,
        "expected": "One row per month with sum and count",
        "solution": """
            SELECT STRFTIME('%Y-%m', order_date) AS month,
                   COUNT(*)    AS num_orders,
                   SUM(amount) AS total_revenue,
                   ROUND(AVG(amount), 2) AS avg_order_value
            FROM orders
            GROUP BY STRFTIME('%Y-%m', order_date)
            ORDER BY month;
        """,
        "explanation": """
            Date truncation varies by dialect:
              SQLite:    STRFTIME('%Y-%m', date_col)
              Postgres:  DATE_TRUNC('month', date_col)
              MySQL:     DATE_FORMAT(date_col, '%Y-%m')
              BigQuery:  FORMAT_DATE('%Y-%m', date_col)
        """
    },
    {
        "id": 27,
        "title": "Percentage of total using GROUP BY + subquery",
        "difficulty": "Medium",
        "category": "GroupBy",
        "problem": """
            Show each department's total salary as a percentage of
            the company's total salary spend.
        """,
        "expected": "Each dept with its % of total",
        "solution": """
            SELECT department,
                   SUM(salary) AS dept_total,
                   ROUND(SUM(salary) * 100.0 /
                         (SELECT SUM(salary) FROM employees), 1) AS pct_of_total
            FROM employees
            GROUP BY department
            ORDER BY pct_of_total DESC;
        """,
        "explanation": """
            Scalar subquery (SELECT SUM(salary) FROM employees) computes
            the grand total. Alternative: use a window function
            SUM(salary) OVER() for the grand total.
        """
    },
    {
        "id": 28,
        "title": "GROUPING SETS / ROLLUP simulation",
        "difficulty": "Medium",
        "category": "GroupBy",
        "problem": """
            Show order totals by region, by product, AND grand total
            in a single result (simulate ROLLUP).
        """,
        "expected": "Subtotals per region, per product, and a grand total row",
        "solution": """
            -- SQLite doesn't support ROLLUP, so we UNION ALL
            SELECT region AS grouping_key, 'region' AS group_type,
                   SUM(amount) AS total
            FROM orders GROUP BY region

            UNION ALL

            SELECT product, 'product',
                   SUM(amount)
            FROM orders GROUP BY product

            UNION ALL

            SELECT 'ALL', 'grand_total',
                   SUM(amount)
            FROM orders

            ORDER BY group_type, grouping_key;
        """,
        "explanation": """
            In Postgres/MySQL/BigQuery, use:
              GROUP BY ROLLUP(region, product)  — hierarchical subtotals
              GROUP BY CUBE(region, product)    — all combinations
              GROUP BY GROUPING SETS(...)       — custom combinations
            SQLite doesn't support these, so UNION ALL is the workaround.
        """
    },
    {
        "id": 29,
        "title": "GROUP BY with string aggregation",
        "difficulty": "Medium",
        "category": "GroupBy",
        "problem": """
            For each customer, list all distinct products they've ordered
            as a comma-separated string.
        """,
        "expected": "customer 101: 'Gadget,Gizmo,Widget'",
        "solution": """
            SELECT customer_id,
                   GROUP_CONCAT(DISTINCT product ORDER BY product) AS products_ordered,
                   COUNT(DISTINCT product) AS num_products
            FROM orders
            GROUP BY customer_id
            ORDER BY customer_id;
        """,
        "explanation": """
            String aggregation varies by dialect:
              SQLite:    GROUP_CONCAT(col, separator)
              Postgres:  STRING_AGG(col, ',' ORDER BY col)
              MySQL:     GROUP_CONCAT(col ORDER BY col SEPARATOR ',')
              BigQuery:  STRING_AGG(col, ',' ORDER BY col)
        """
    },
    {
        "id": 30,
        "title": "Find rows matching max aggregate — correlated approach",
        "difficulty": "Medium",
        "category": "GroupBy",
        "problem": """
            Find the employee with the highest salary in each department
            (without using window functions).
        """,
        "expected": "Alice (Eng), Eve (Sales), Jack (Marketing)",
        "solution": """
            SELECT e.name, e.department, e.salary
            FROM employees e
            WHERE e.salary = (
                SELECT MAX(e2.salary)
                FROM employees e2
                WHERE e2.department = e.department
            )
            ORDER BY e.department;
        """,
        "explanation": """
            Correlated subquery: inner query references outer query's row.
            Runs once per outer row. Window function approach (RANK) is
            often cleaner but interviewers may ask for both approaches.
        """
    },

    # ──────────────────────────────────────────────────────────────────
    # SECTION 4: JOINS & SUBQUERIES (Q31–Q38)
    # ──────────────────────────────────────────────────────────────────

    {
        "id": 31,
        "title": "INNER JOIN — employees with their managers",
        "difficulty": "Easy",
        "category": "Joins",
        "problem": """
            Show each employee's name alongside their manager's name.
            Exclude employees with no manager.
        """,
        "expected": "7 rows (employees who have a manager_id)",
        "solution": """
            SELECT e.name AS employee,
                   m.name AS manager
            FROM employees e
            INNER JOIN employees m ON e.manager_id = m.emp_id
            ORDER BY e.name;
        """,
        "explanation": """
            Self-join: joining a table to itself. Use aliases (e, m)
            to distinguish the two references. INNER JOIN excludes
            rows with no match (employees without managers).
        """
    },
    {
        "id": 32,
        "title": "LEFT JOIN — include all employees even without manager",
        "difficulty": "Easy",
        "category": "Joins",
        "problem": """
            Show all employees with their manager name.
            Show NULL for employees without a manager.
        """,
        "expected": "10 rows, managers Alice/Dave/Grace show NULL manager",
        "solution": """
            SELECT e.name AS employee,
                   e.department,
                   COALESCE(m.name, 'No Manager') AS manager
            FROM employees e
            LEFT JOIN employees m ON e.manager_id = m.emp_id
            ORDER BY e.department, e.name;
        """,
        "explanation": """
            LEFT JOIN keeps ALL rows from left table.
            COALESCE(value, default) replaces NULL with a default.
            Use LEFT JOIN when you want to preserve all records from
            the primary table.
        """
    },
    {
        "id": 33,
        "title": "Anti-join — find customers with no orders in July",
        "difficulty": "Medium",
        "category": "Joins",
        "problem": """
            Find customers who placed orders in 2023 but NOT in July 2023.
        """,
        "expected": "Customers who ordered in 2023 but skipped July",
        "solution": """
            SELECT DISTINCT customer_id
            FROM orders
            WHERE customer_id NOT IN (
                SELECT DISTINCT customer_id
                FROM orders
                WHERE order_date BETWEEN '2023-07-01' AND '2023-07-31'
            )
            ORDER BY customer_id;
        """,
        "explanation": """
            Anti-join pattern: find rows in A that have no match in B.
            Three equivalent approaches:
              1. NOT IN (subquery)
              2. LEFT JOIN + WHERE b.key IS NULL
              3. NOT EXISTS (correlated subquery)
            NOT EXISTS is safest with NULLs.
        """
    },
    {
        "id": 34,
        "title": "CROSS JOIN — generate all combinations",
        "difficulty": "Medium",
        "category": "Joins",
        "problem": """
            Generate a report showing every combination of region and product,
            with actual sales (0 if no orders exist for that combination).
        """,
        "expected": "All region×product combos including gaps filled with 0",
        "solution": """
            WITH regions AS (SELECT DISTINCT region FROM orders),
                 products AS (SELECT DISTINCT product FROM orders)
            SELECT r.region, p.product,
                   COALESCE(SUM(o.amount), 0) AS total_sales
            FROM regions r
            CROSS JOIN products p
            LEFT JOIN orders o ON o.region = r.region AND o.product = p.product
            GROUP BY r.region, p.product
            ORDER BY r.region, p.product;
        """,
        "explanation": """
            CROSS JOIN generates all combinations (cartesian product).
            LEFT JOIN + COALESCE fills in 0 for missing combos.
            This is equivalent to a pivot table with fill_value=0.
        """
    },
    {
        "id": 35,
        "title": "CTE (Common Table Expression) — chained logic",
        "difficulty": "Medium",
        "category": "Joins",
        "problem": """
            Find the department with the highest average salary, then
            list all employees in that department.
        """,
        "expected": "Engineering department employees",
        "solution": """
            WITH dept_avg AS (
                SELECT department, AVG(salary) AS avg_sal
                FROM employees
                GROUP BY department
            ),
            top_dept AS (
                SELECT department
                FROM dept_avg
                ORDER BY avg_sal DESC
                LIMIT 1
            )
            SELECT e.name, e.salary
            FROM employees e
            JOIN top_dept t ON e.department = t.department
            ORDER BY e.salary DESC;
        """,
        "explanation": """
            CTEs (WITH clauses) break complex queries into readable steps.
            Each CTE can reference previous CTEs. Think of them as
            named temporary result sets.
        """
    },
    {
        "id": 36,
        "title": "Self-join — find employee pairs in same department",
        "difficulty": "Medium",
        "category": "Joins",
        "problem": """
            Find all pairs of employees in the same department
            where one earns at least $10,000 more than the other.
        """,
        "expected": "Pairs like (Alice, Carol) in Engineering",
        "solution": """
            SELECT e1.name AS higher_paid,
                   e2.name AS lower_paid,
                   e1.department,
                   e1.salary - e2.salary AS salary_gap
            FROM employees e1
            JOIN employees e2
                ON e1.department = e2.department
               AND e1.salary >= e2.salary + 10000
               AND e1.emp_id != e2.emp_id
            ORDER BY salary_gap DESC;
        """,
        "explanation": """
            Self-join with inequality condition. The e1.emp_id != e2.emp_id
            prevents pairing an employee with themselves. The salary
            condition ensures we only get meaningful gaps.
        """
    },
    {
        "id": 37,
        "title": "Subquery in FROM — derived table",
        "difficulty": "Medium",
        "category": "Joins",
        "problem": """
            Find the average of each department's max salary.
            (What's the average "top salary" across departments?)
        """,
        "expected": "Single number: average of each dept's max",
        "solution": """
            SELECT ROUND(AVG(max_sal), 0) AS avg_of_dept_maxes
            FROM (
                SELECT department, MAX(salary) AS max_sal
                FROM employees
                GROUP BY department
            ) dept_maxes;
        """,
        "explanation": """
            Subquery in FROM (derived table) is useful when you need
            to aggregate an aggregation. You can't nest aggregate
            functions directly (AVG(MAX(salary)) is invalid).
        """
    },
    {
        "id": 38,
        "title": "UNION vs UNION ALL — combining result sets",
        "difficulty": "Easy",
        "category": "Joins",
        "problem": """
            Combine two lists: employees earning > 90K AND employees
            hired before 2020. Some may appear in both lists.
            Show with and without duplicates.
        """,
        "expected": "UNION removes dups, UNION ALL keeps them",
        "solution": """
            -- UNION: removes duplicates
            SELECT name, 'high_earner' AS reason FROM employees WHERE salary > 90000
            UNION
            SELECT name, 'early_hire'  AS reason FROM employees WHERE hire_date < '2020-01-01';
        """,
        "explanation": """
            UNION = combine + deduplicate (slower, sorts internally)
            UNION ALL = combine, keep all rows (faster)
            Rule: use UNION ALL unless you specifically need dedup.
            All SELECTs must have same number & compatible types of columns.
        """
    },

    # ──────────────────────────────────────────────────────────────────
    # SECTION 5: PIVOT / RESHAPE / CASE (Q39–Q44)
    # ──────────────────────────────────────────────────────────────────

    {
        "id": 39,
        "title": "Manual pivot with CASE — rows to columns",
        "difficulty": "Medium",
        "category": "Pivot",
        "problem": """
            Create a pivot: rows = region, columns = product,
            values = total sales amount.
        """,
        "expected": "Matrix with regions as rows, products as columns",
        "solution": """
            SELECT region,
                   SUM(CASE WHEN product = 'Widget' THEN amount ELSE 0 END) AS Widget,
                   SUM(CASE WHEN product = 'Gadget' THEN amount ELSE 0 END) AS Gadget,
                   SUM(CASE WHEN product = 'Gizmo'  THEN amount ELSE 0 END) AS Gizmo,
                   SUM(amount) AS Total
            FROM orders
            GROUP BY region
            ORDER BY region;
        """,
        "explanation": """
            SQL standard doesn't have PIVOT keyword (except SQL Server).
            Use SUM(CASE WHEN ... THEN ... ELSE 0 END) pattern.
            This is the SQL equivalent of pandas pivot_table().
        """
    },
    {
        "id": 40,
        "title": "Unpivot — columns to rows",
        "difficulty": "Medium",
        "category": "Pivot",
        "problem": """
            Given student_scores (student_id, Math, Science, English as separate rows),
            they're already in long format. But if we had wide format, show the unpivot.
            Create a summary: for each subject, show avg and max score.
        """,
        "expected": "3 rows: Math, Science, English with stats",
        "solution": """
            SELECT subject,
                   ROUND(AVG(score), 1) AS avg_score,
                   MAX(score)           AS max_score,
                   MIN(score)           AS min_score,
                   COUNT(*)             AS num_students
            FROM student_scores
            GROUP BY subject
            ORDER BY avg_score DESC;
        """,
        "explanation": """
            If data were in wide format (columns: math_score, sci_score, eng_score),
            unpivot using UNION ALL:
              SELECT id, 'Math' AS subject, math_score FROM wide
              UNION ALL
              SELECT id, 'Science', sci_score FROM wide
              UNION ALL ...
            Postgres: UNNEST / LATERAL. BigQuery: UNPIVOT keyword.
        """
    },
    {
        "id": 41,
        "title": "CASE for bucketing / categorization",
        "difficulty": "Easy",
        "category": "Pivot",
        "problem": """
            Categorize employees into salary tiers:
            <70K = 'Junior', 70-85K = 'Mid', 85-95K = 'Senior', >95K = 'Staff+'
        """,
        "expected": "Each employee with their tier label",
        "solution": """
            SELECT name, salary,
                   CASE
                       WHEN salary < 70000  THEN 'Junior'
                       WHEN salary <= 85000 THEN 'Mid'
                       WHEN salary <= 95000 THEN 'Senior'
                       ELSE 'Staff+'
                   END AS tier
            FROM employees
            ORDER BY salary;
        """,
        "explanation": """
            CASE WHEN is evaluated top-to-bottom; first match wins.
            Order your conditions from most specific to least specific.
            This is the SQL equivalent of pd.cut() or np.select().
        """
    },
    {
        "id": 42,
        "title": "Pivot with COUNT — frequency table / crosstab",
        "difficulty": "Medium",
        "category": "Pivot",
        "problem": """
            Create a crosstab: for each region, count the number of
            orders per product.
        """,
        "expected": "Matrix of counts: region × product",
        "solution": """
            SELECT region,
                   SUM(CASE WHEN product = 'Widget' THEN 1 ELSE 0 END) AS Widget_orders,
                   SUM(CASE WHEN product = 'Gadget' THEN 1 ELSE 0 END) AS Gadget_orders,
                   SUM(CASE WHEN product = 'Gizmo'  THEN 1 ELSE 0 END) AS Gizmo_orders,
                   COUNT(*) AS total_orders
            FROM orders
            GROUP BY region
            ORDER BY region;
        """,
        "explanation": """
            Same CASE pivot pattern but with COUNT/SUM of 1s instead of values.
            This creates a frequency table (crosstab).
            Equivalent to pd.crosstab(df.region, df.product).
        """
    },
    {
        "id": 43,
        "title": "COALESCE and NULLIF — null handling expressions",
        "difficulty": "Easy",
        "category": "Pivot",
        "problem": """
            Show employee name and their manager's name.
            Display 'Top Level' for employees with no manager.
            Also handle potential division by zero safely.
        """,
        "expected": "Top Level for Alice, Dave, Grace",
        "solution": """
            SELECT e.name,
                   COALESCE(m.name, 'Top Level') AS manager_name,
                   e.salary,
                   -- Safe division: if dept count is 0, return NULL instead of error
                   e.salary * 1.0 / NULLIF(
                       (SELECT COUNT(*) FROM employees e2
                        WHERE e2.department = e.department), 0
                   ) AS salary_per_dept_member
            FROM employees e
            LEFT JOIN employees m ON e.manager_id = m.emp_id
            ORDER BY e.name;
        """,
        "explanation": """
            COALESCE(a, b, c) → returns first non-NULL argument
            NULLIF(a, b) → returns NULL if a = b, else returns a
            NULLIF is the standard way to prevent division by zero:
              x / NULLIF(y, 0) → returns NULL instead of error when y=0
        """
    },
    {
        "id": 44,
        "title": "Recursive CTE — hierarchical data",
        "difficulty": "Hard",
        "category": "Pivot",
        "problem": """
            Show the full management chain for each employee
            (employee → manager → manager's manager → ...).
        """,
        "expected": "Carol → Alice → (none); Frank → Dave → (none)",
        "solution": """
            WITH RECURSIVE mgmt_chain AS (
                -- Base case: start with each employee
                SELECT emp_id, name, manager_id,
                       name AS chain, 0 AS depth
                FROM employees

                UNION ALL

                -- Recursive case: join to manager
                SELECT mc.emp_id, mc.name, e.manager_id,
                       mc.chain || ' → ' || e.name, mc.depth + 1
                FROM mgmt_chain mc
                JOIN employees e ON mc.manager_id = e.emp_id
            )
            SELECT name, chain AS management_chain, depth
            FROM mgmt_chain
            WHERE manager_id IS NULL  -- terminal condition: reached top
            ORDER BY name;
        """,
        "explanation": """
            Recursive CTE has two parts:
            1. Base (anchor) query: starting rows
            2. Recursive query: JOIN to itself until no more matches
            Use for: org charts, bill of materials, graph traversal.
            Always include a termination condition (max depth or NULL check).
        """
    },

    # ──────────────────────────────────────────────────────────────────
    # SECTION 6: STATISTICAL & ADVANCED (Q45–Q50)
    # ──────────────────────────────────────────────────────────────────

    {
        "id": 45,
        "title": "Median calculation (no built-in median function)",
        "difficulty": "Hard",
        "category": "Statistics",
        "problem": """
            Calculate the median salary across all employees.
        """,
        "expected": "Median of [68K,72K,75K,78K,82K,85K,88K,91K,92K,95K] = 83,500",
        "solution": """
            WITH ordered AS (
                SELECT salary,
                       ROW_NUMBER() OVER (ORDER BY salary) AS rn,
                       COUNT(*) OVER () AS total
                FROM employees
            )
            SELECT ROUND(AVG(salary), 0) AS median_salary
            FROM ordered
            WHERE rn IN (
                (total + 1) / 2,
                (total + 2) / 2
            );
        """,
        "explanation": """
            For odd count: middle element. For even count: average of two middle.
            (total+1)/2 and (total+2)/2 handles both cases:
              Odd (n=5):  (5+1)/2=3, (5+2)/2=3 → same row
              Even (n=10): (10+1)/2=5, (10+2)/2=6 → average of row 5 & 6
            Postgres: PERCENTILE_CONT(0.5). BigQuery: APPROX_QUANTILES.
        """
    },
    {
        "id": 46,
        "title": "Percentile / Quartile assignment",
        "difficulty": "Medium",
        "category": "Statistics",
        "problem": """
            Assign each student's Math score to a percentile bucket
            (top 25%, 25-50%, 50-75%, bottom 25%).
        """,
        "expected": "Each student with their percentile tier",
        "solution": """
            WITH ranked AS (
                SELECT student_id, score,
                       PERCENT_RANK() OVER (ORDER BY score) AS pct_rank
                FROM student_scores
                WHERE subject = 'Math'
            )
            SELECT student_id, score, ROUND(pct_rank * 100, 1) AS percentile,
                   CASE
                       WHEN pct_rank >= 0.75 THEN 'Top 25%'
                       WHEN pct_rank >= 0.50 THEN '25-50%'
                       WHEN pct_rank >= 0.25 THEN '50-75%'
                       ELSE 'Bottom 25%'
                   END AS tier
            FROM ranked
            ORDER BY score DESC;
        """,
        "explanation": """
            PERCENT_RANK() = (rank - 1) / (total_rows - 1), range [0, 1].
            CUME_DIST() = rank / total_rows, range (0, 1].
            NTILE(4) divides into equal groups but doesn't give percentile value.
        """
    },
    {
        "id": 47,
        "title": "Year-over-year comparison with self-join",
        "difficulty": "Medium",
        "category": "Statistics",
        "problem": """
            Compare each employee's salary to the average salary of
            employees hired in the same year. Show if above or below average.
        """,
        "expected": "Each employee with their hire-year average and comparison",
        "solution": """
            WITH year_avg AS (
                SELECT STRFTIME('%Y', hire_date) AS hire_year,
                       AVG(salary) AS avg_salary
                FROM employees
                GROUP BY STRFTIME('%Y', hire_date)
            )
            SELECT e.name, e.salary,
                   STRFTIME('%Y', e.hire_date) AS hire_year,
                   ROUND(ya.avg_salary, 0) AS year_avg,
                   ROUND(e.salary - ya.avg_salary, 0) AS diff,
                   CASE
                       WHEN e.salary > ya.avg_salary THEN 'Above'
                       WHEN e.salary < ya.avg_salary THEN 'Below'
                       ELSE 'At Average'
                   END AS comparison
            FROM employees e
            JOIN year_avg ya ON STRFTIME('%Y', e.hire_date) = ya.hire_year
            ORDER BY hire_year, e.salary DESC;
        """,
        "explanation": """
            Join to a pre-aggregated CTE is cleaner than correlated subquery.
            Pattern: aggregate first in CTE, then join back for row-level comparison.
        """
    },
    {
        "id": 48,
        "title": "Running balance — cumulative credit/debit",
        "difficulty": "Hard",
        "category": "Statistics",
        "problem": """
            For each account, show a running balance after each transaction
            (credits add, debits subtract).
        """,
        "expected": "Running balance per account ordered by date",
        "solution": """
            SELECT account_id, txn_date, txn_type, amount,
                   SUM(CASE WHEN txn_type = 'credit' THEN amount ELSE -amount END)
                       OVER (
                           PARTITION BY account_id
                           ORDER BY txn_date
                           ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
                       ) AS running_balance
            FROM transactions
            ORDER BY account_id, txn_date;
        """,
        "explanation": """
            Combine CASE with window SUM for conditional running totals.
            This is a very common financial/accounting SQL pattern.
            Partition by account so each account has its own running balance.
        """
    },
    {
        "id": 49,
        "title": "Find gaps in sequences",
        "difficulty": "Hard",
        "category": "Statistics",
        "problem": """
            Find missing order_ids in the orders table
            (gaps in the sequence from 1 to max).
        """,
        "expected": "No gaps in our sample (1-15), but show the pattern",
        "solution": """
            WITH RECURSIVE all_ids AS (
                SELECT 1 AS id
                UNION ALL
                SELECT id + 1 FROM all_ids WHERE id < (SELECT MAX(order_id) FROM orders)
            )
            SELECT a.id AS missing_order_id
            FROM all_ids a
            LEFT JOIN orders o ON a.id = o.order_id
            WHERE o.order_id IS NULL
            ORDER BY a.id;
        """,
        "explanation": """
            Generate a complete sequence with recursive CTE,
            then LEFT JOIN to actual data and find NULLs.
            Alternative: use LEAD to check if next_id - current_id > 1.
            In Postgres: generate_series(1, max_id) is simpler.
        """
    },
    {
        "id": 50,
        "title": "Weighted average and advanced aggregation",
        "difficulty": "Hard",
        "category": "Statistics",
        "problem": """
            Calculate a weighted average score for each student,
            where Math has weight 3, Science weight 2, English weight 1.
            Then rank students by weighted average.
        """,
        "expected": "Weighted averages and final ranking",
        "solution": """
            WITH weights AS (
                SELECT 'Math' AS subject, 3 AS weight
                UNION ALL SELECT 'Science', 2
                UNION ALL SELECT 'English', 1
            ),
            weighted AS (
                SELECT s.student_id,
                       SUM(s.score * w.weight) AS weighted_sum,
                       SUM(w.weight)           AS total_weight,
                       ROUND(SUM(s.score * w.weight) * 1.0 / SUM(w.weight), 1)
                           AS weighted_avg
                FROM student_scores s
                JOIN weights w ON s.subject = w.subject
                GROUP BY s.student_id
            )
            SELECT student_id, weighted_avg,
                   RANK() OVER (ORDER BY weighted_avg DESC) AS rank
            FROM weighted
            ORDER BY rank;
        """,
        "explanation": """
            Weighted average = SUM(value * weight) / SUM(weight).
            Use a weights table (CTE or actual table) to join.
            This pattern is common in GPA calculations, survey scoring,
            and composite metric generation.
        """
    },
]


# ════════════════════════════════════════════════════════════════════════
# RUNNER — execute questions against SQLite
# ════════════════════════════════════════════════════════════════════════

def run_question(conn, q, verbose=True):
    """Execute a single question and print results."""
    cursor = conn.cursor()
    if verbose:
        print(f"\n{'═' * 70}")
        print(f"  Q{q['id']:02d}. {q['title']}")
        print(f"  Difficulty: {q['difficulty']}  |  Category: {q['category']}")
        print(f"{'═' * 70}")
        print(f"\n  PROBLEM: {textwrap.dedent(q['problem']).strip()}")
        print(f"\n  EXPECTED: {q['expected']}")
        print(f"\n  SOLUTION:")
        for line in textwrap.dedent(q['solution']).strip().split('\n'):
            print(f"    {line}")
        print(f"\n  RESULT:")

    try:
        # Handle queries with UNION (may have multiple statements conceptually)
        sql = textwrap.dedent(q['solution']).strip()
        # Remove comments for execution
        lines = [l for l in sql.split('\n') if not l.strip().startswith('--')]
        clean_sql = '\n'.join(lines).strip().rstrip(';')

        cursor.execute(clean_sql)
        rows = cursor.fetchall()
        if rows:
            # Get column names
            cols = [desc[0] for desc in cursor.description]
            if verbose:
                # Print header
                header = ' | '.join(f'{c:>15}' for c in cols)
                print(f"    {header}")
                print(f"    {'─' * len(header)}")
                for row in rows[:15]:  # limit display
                    vals = ' | '.join(f'{str(v):>15}' for v in row)
                    print(f"    {vals}")
                if len(rows) > 15:
                    print(f"    ... ({len(rows)} total rows)")
        else:
            if verbose:
                print("    (no results)")
    except Exception as e:
        if verbose:
            print(f"    ERROR: {e}")

    if verbose:
        print(f"\n  EXPLANATION: {textwrap.dedent(q['explanation']).strip()}")

    return True


def main():
    """Run all questions or a specific one."""
    conn = sqlite3.connect(':memory:')
    conn.execute("PRAGMA foreign_keys = ON")
    conn.executescript(SHARED_SETUP)

    # Parse args
    target_q = None
    if len(sys.argv) > 1:
        if sys.argv[1] == '--q' and len(sys.argv) > 2:
            target_q = int(sys.argv[2])
        elif sys.argv[1] == '--list':
            print("\n  50 SQL Interview Questions — Table of Contents\n")
            for q in QUESTIONS:
                print(f"  Q{q['id']:02d}. [{q['difficulty']:6s}] [{q['category']:10s}] {q['title']}")
            conn.close()
            return
        elif sys.argv[1] == '--help':
            print("""
Usage:
  python sql_interview_50.py           Run all 50 questions
  python sql_interview_50.py --q 15    Run only question 15
  python sql_interview_50.py --list    Show table of contents
  python sql_interview_50.py --help    Show this help
            """)
            conn.close()
            return

    print("━" * 70)
    print("  50 SQL CODING INTERVIEW QUESTIONS")
    print("━" * 70)

    if target_q:
        q = next((q for q in QUESTIONS if q['id'] == target_q), None)
        if q:
            run_question(conn, q)
        else:
            print(f"  Question {target_q} not found. Use --list to see available questions.")
    else:
        # Print summary first
        categories = {}
        for q in QUESTIONS:
            cat = q['category']
            categories[cat] = categories.get(cat, 0) + 1
        print("\n  Categories:")
        for cat, count in categories.items():
            print(f"    {cat:15s}: {count} questions")
        print(f"    {'TOTAL':15s}: {len(QUESTIONS)} questions\n")

        passed = 0
        for q in QUESTIONS:
            try:
                run_question(conn, q)
                passed += 1
            except Exception as e:
                print(f"  Q{q['id']:02d} FAILED: {e}")

        print(f"\n{'━' * 70}")
        print(f"  Results: {passed}/{len(QUESTIONS)} questions executed successfully")
        print(f"{'━' * 70}")

    conn.close()


if __name__ == '__main__':
    main()
