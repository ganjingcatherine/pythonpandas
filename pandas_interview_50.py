"""
50 Python/Pandas Coding Interview Questions
Covering: Filtering, Window Functions, GroupBy, Pivot, Statistical Calculations,
Merging, Reshaping, String Operations, DateTime, and Advanced Manipulation
"""

import pandas as pd
import numpy as np

# ============================================================
# SAMPLE DATA SETUP
# ============================================================

employees = pd.DataFrame({
    'emp_id': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    'name': ['Alice', 'Bob', 'Charlie', 'Diana', 'Eve', 'Frank', 'Grace', 'Hank', 'Ivy', 'Jack'],
    'department': ['Engineering', 'Engineering', 'Sales', 'Sales', 'HR', 'HR', 'Engineering', 'Sales', 'HR', 'Engineering'],
    'salary': [95000, 88000, 72000, 68000, 75000, 71000, 102000, 65000, 78000, 91000],
    'hire_date': pd.to_datetime(['2019-03-15', '2020-07-01', '2018-01-20', '2021-06-10', '2019-11-05',
                                  '2022-02-28', '2017-09-12', '2023-04-01', '2020-08-22', '2021-01-15']),
    'age': [32, 28, 45, 26, 38, 29, 50, 24, 35, 31],
    'rating': [4.5, 3.8, 4.2, 3.5, 4.8, 3.0, 4.9, 3.2, 4.1, 4.0],
    'bonus': [5000, 3000, 4000, 2000, 5500, 1500, 6000, 1000, 4500, 3500],
    'city': ['New York', 'San Francisco', 'New York', 'Chicago', 'San Francisco', 'Chicago', 'New York', 'Chicago', 'San Francisco', 'New York']
})

sales = pd.DataFrame({
    'sale_id': range(1, 21),
    'emp_id': [3, 4, 8, 3, 4, 8, 3, 4, 8, 3, 4, 8, 3, 4, 8, 3, 4, 8, 3, 4],
    'product': ['A', 'B', 'A', 'C', 'A', 'B', 'B', 'C', 'A', 'A', 'B', 'C', 'C', 'A', 'B', 'A', 'C', 'A', 'B', 'B'],
    'amount': [1200, 800, 1500, 2000, 950, 1100, 1800, 750, 1300, 1600, 900, 1400, 2200, 1050, 1700, 1900, 850, 1150, 1350, 1000],
    'quantity': [10, 5, 12, 8, 7, 9, 15, 4, 11, 13, 6, 10, 18, 8, 14, 16, 5, 9, 11, 7],
    'sale_date': pd.to_datetime([
        '2024-01-05', '2024-01-12', '2024-01-18', '2024-02-03', '2024-02-14',
        '2024-02-20', '2024-03-01', '2024-03-15', '2024-03-22', '2024-04-05',
        '2024-04-12', '2024-04-25', '2024-05-03', '2024-05-18', '2024-05-28',
        '2024-06-10', '2024-06-20', '2024-06-30', '2024-07-15', '2024-07-25'
    ]),
    'region': ['East', 'West', 'East', 'East', 'West', 'West', 'East', 'West', 'East', 'East',
               'West', 'West', 'East', 'West', 'East', 'East', 'West', 'East', 'East', 'West']
})

orders = pd.DataFrame({
    'order_id': range(101, 116),
    'customer': ['C1', 'C2', 'C1', 'C3', 'C2', 'C4', 'C1', 'C3', 'C5', 'C2', 'C4', 'C5', 'C1', 'C3', 'C2'],
    'amount': [250, 450, 300, 150, 500, 200, 350, 400, 100, 550, 275, 325, 600, 175, 425],
    'status': ['completed', 'completed', 'pending', 'completed', 'cancelled', 'completed', 'completed',
               'pending', 'completed', 'completed', 'cancelled', 'completed', 'pending', 'completed', 'completed'],
    'order_date': pd.to_datetime([
        '2024-01-10', '2024-01-15', '2024-02-05', '2024-02-12', '2024-02-20',
        '2024-03-01', '2024-03-10', '2024-03-18', '2024-04-02', '2024-04-15',
        '2024-04-22', '2024-05-05', '2024-05-15', '2024-05-25', '2024-06-10'
    ])
})

stock_prices = pd.DataFrame({
    'date': pd.date_range('2024-01-01', periods=30, freq='B'),
    'ticker': ['AAPL'] * 15 + ['GOOG'] * 15,
    'close': [150 + np.random.randn() * 5 for _ in range(15)] + [140 + np.random.randn() * 4 for _ in range(15)],
    'volume': [np.random.randint(1000000, 5000000) for _ in range(30)]
})
np.random.seed(42)
stock_prices['close'] = [150 + np.random.randn() * 5 for _ in range(15)] + [140 + np.random.randn() * 4 for _ in range(15)]
stock_prices['volume'] = [np.random.randint(1000000, 5000000) for _ in range(30)]


# ============================================================
# SECTION 1: FILTERING & SELECTION (Q1-Q8)
# ============================================================

# ------ Q1: Basic Filtering ------
# Filter employees with salary > 80000 in the Engineering department.

def q1_filter_high_salary_eng(df):
    return df[(df['salary'] > 80000) & (df['department'] == 'Engineering')]

# ------ Q2: isin Filtering ------
# Select employees who work in either 'HR' or 'Sales' and have a rating >= 4.0.

def q2_filter_isin_rating(df):
    return df[(df['department'].isin(['HR', 'Sales'])) & (df['rating'] >= 4.0)]

# ------ Q3: String-Based Filtering ------
# Find employees whose name starts with a vowel (A, E, I, O, U).

def q3_filter_name_vowel(df):
    return df[df['name'].str[0].str.upper().isin(list('AEIOU'))]

# ------ Q4: Top N per Group ------
# Get the top 2 highest-paid employees in each department.

def q4_top_n_per_group(df):
    return df.groupby('department').apply(
        lambda x: x.nlargest(2, 'salary'), include_groups=False
    ).reset_index(level=0)

# ------ Q5: Filtering with query() ------
# Use .query() to find employees hired after 2020 with age < 30.

def q5_query_method(df):
    return df.query('hire_date > "2020-01-01" and age < 30')

# ------ Q6: Filter Rows Based on Another DataFrame ------
# Find employees who have made at least one sale (exist in sales table).

def q6_filter_by_another_df(employees_df, sales_df):
    active_sellers = sales_df['emp_id'].unique()
    return employees_df[employees_df['emp_id'].isin(active_sellers)]

# ------ Q7: Conditional Selection with np.where ------
# Create a new column 'level': 'Senior' if salary >= 80000, else 'Junior'.

def q7_conditional_column(df):
    df = df.copy()
    df['level'] = np.where(df['salary'] >= 80000, 'Senior', 'Junior')
    return df

# ------ Q8: Filter Using Between ------
# Find sales with amount between 1000 and 1500 (inclusive).

def q8_filter_between(df):
    return df[df['amount'].between(1000, 1500)]


# ============================================================
# SECTION 2: GROUPBY & AGGREGATION (Q9-Q18)
# ============================================================

# ------ Q9: Basic GroupBy ------
# Calculate the average salary and total bonus per department.

def q9_basic_groupby(df):
    return df.groupby('department').agg(
        avg_salary=('salary', 'mean'),
        total_bonus=('bonus', 'sum')
    ).reset_index()

# ------ Q10: Multiple Aggregations ------
# For each department, find min, max, mean, and std of salary.

def q10_multi_agg(df):
    return df.groupby('department')['salary'].agg(['min', 'max', 'mean', 'std']).reset_index()

# ------ Q11: GroupBy with Transform ------
# Add a column showing each employee's salary as a percentage of their department's total salary.

def q11_groupby_transform(df):
    df = df.copy()
    dept_total = df.groupby('department')['salary'].transform('sum')
    df['salary_pct_of_dept'] = (df['salary'] / dept_total * 100).round(2)
    return df

# ------ Q12: GroupBy Filter ------
# Keep only departments where the average salary exceeds 75000.

def q12_groupby_filter(df):
    return df.groupby('department').filter(lambda x: x['salary'].mean() > 75000)

# ------ Q13: Named Aggregation ------
# Per department: count employees, average rating, highest salary employee name.

def q13_named_agg(df):
    return df.groupby('department').agg(
        emp_count=('emp_id', 'count'),
        avg_rating=('rating', 'mean'),
        top_earner=('salary', 'idxmax')
    ).reset_index().assign(
        top_earner=lambda x: df.loc[x['top_earner'], 'name'].values
    )

# ------ Q14: GroupBy with Cumulative Sum ------
# Calculate cumulative sales amount per employee ordered by sale_date.

def q14_cumulative_sum(df):
    df = df.sort_values('sale_date')
    df['cum_amount'] = df.groupby('emp_id')['amount'].cumsum()
    return df

# ------ Q15: GroupBy Rank ------
# Rank employees within each department by salary (highest = rank 1).

def q15_groupby_rank(df):
    df = df.copy()
    df['salary_rank'] = df.groupby('department')['salary'].rank(ascending=False, method='dense').astype(int)
    return df

# ------ Q16: GroupBy with Value Counts ------
# Count the number of sales per product per region.

def q16_groupby_value_counts(df):
    return df.groupby(['region', 'product']).size().reset_index(name='sale_count')

# ------ Q17: Percentage of Group Total ------
# Calculate each sale's amount as a percentage of total sales for that product.

def q17_pct_of_group(df):
    df = df.copy()
    df['pct_of_product_total'] = (
        df['amount'] / df.groupby('product')['amount'].transform('sum') * 100
    ).round(2)
    return df

# ------ Q18: GroupBy with First/Last ------
# Get the first and last sale date per employee.

def q18_first_last(df):
    df = df.sort_values('sale_date')
    return df.groupby('emp_id').agg(
        first_sale=('sale_date', 'first'),
        last_sale=('sale_date', 'last'),
        total_sales=('sale_id', 'count')
    ).reset_index()


# ============================================================
# SECTION 3: WINDOW FUNCTIONS (Q19-Q26)
# ============================================================

# ------ Q19: Rolling Average ------
# Calculate 3-day rolling average of closing price per ticker.

def q19_rolling_avg(df):
    df = df.sort_values(['ticker', 'date'])
    df['rolling_3d_avg'] = df.groupby('ticker')['close'].transform(
        lambda x: x.rolling(3, min_periods=1).mean()
    )
    return df

# ------ Q20: Rolling Sum of Sales ------
# Calculate a 3-row rolling sum of amount per employee.

def q20_rolling_sum(df):
    df = df.sort_values(['emp_id', 'sale_date'])
    df['rolling_3_sum'] = df.groupby('emp_id')['amount'].transform(
        lambda x: x.rolling(3, min_periods=1).sum()
    )
    return df

# ------ Q21: Lag / Lead ------
# Add previous sale amount and next sale amount columns per employee.

def q21_lag_lead(df):
    df = df.sort_values(['emp_id', 'sale_date'])
    df['prev_amount'] = df.groupby('emp_id')['amount'].shift(1)
    df['next_amount'] = df.groupby('emp_id')['amount'].shift(-1)
    return df

# ------ Q22: Percent Change ------
# Calculate the percent change in closing price per ticker.

def q22_pct_change(df):
    df = df.sort_values(['ticker', 'date'])
    df['daily_return'] = df.groupby('ticker')['close'].pct_change().round(4)
    return df

# ------ Q23: Expanding Window ------
# Calculate expanding (cumulative) mean of sales amount per employee.

def q23_expanding_mean(df):
    df = df.sort_values(['emp_id', 'sale_date'])
    df['expanding_mean'] = df.groupby('emp_id')['amount'].transform(
        lambda x: x.expanding().mean()
    )
    return df

# ------ Q24: Exponential Weighted Moving Average ------
# Calculate EWMA of close price with span=5 per ticker.

def q24_ewma(df):
    df = df.sort_values(['ticker', 'date'])
    df['ewma_5'] = df.groupby('ticker')['close'].transform(
        lambda x: x.ewm(span=5).mean()
    )
    return df

# ------ Q25: Difference from Group Mean (Z-Score-like) ------
# For each employee sale, compute how far the amount is from the employee's mean.

def q25_diff_from_mean(df):
    df = df.copy()
    df['mean_amount'] = df.groupby('emp_id')['amount'].transform('mean')
    df['std_amount'] = df.groupby('emp_id')['amount'].transform('std')
    df['z_score'] = ((df['amount'] - df['mean_amount']) / df['std_amount']).round(3)
    return df

# ------ Q26: Row Number Within Group ------
# Assign a row number to each sale per employee ordered by date.

def q26_row_number(df):
    df = df.sort_values(['emp_id', 'sale_date'])
    df['sale_seq'] = df.groupby('emp_id').cumcount() + 1
    return df


# ============================================================
# SECTION 4: PIVOT & RESHAPE (Q27-Q34)
# ============================================================

# ------ Q27: Pivot Table ------
# Create a pivot table: rows=region, columns=product, values=sum of amount.

def q27_pivot_table(df):
    return pd.pivot_table(df, values='amount', index='region', columns='product', aggfunc='sum', fill_value=0)

# ------ Q28: Pivot with Multiple Aggregations ------
# Pivot: rows=emp_id, columns=product, values=amount (sum and count).

def q28_pivot_multi_agg(df):
    return pd.pivot_table(df, values='amount', index='emp_id', columns='product',
                          aggfunc=['sum', 'count'], fill_value=0)

# ------ Q29: Melt (Unpivot) ------
# Given a wide DataFrame, melt it into long format.

def q29_melt():
    wide_df = pd.DataFrame({
        'employee': ['Alice', 'Bob', 'Charlie'],
        'Q1_sales': [10000, 12000, 8000],
        'Q2_sales': [11000, 13000, 9500],
        'Q3_sales': [10500, 11000, 10000],
        'Q4_sales': [12000, 14000, 11000]
    })
    return pd.melt(wide_df, id_vars='employee', var_name='quarter', value_name='sales')

# ------ Q30: Stack / Unstack ------
# Group sales by emp_id and product (sum amount), then unstack product to columns.

def q30_stack_unstack(df):
    grouped = df.groupby(['emp_id', 'product'])['amount'].sum()
    return grouped.unstack(fill_value=0)

# ------ Q31: Cross Tabulation ------
# Create a crosstab of department vs city showing employee counts.

def q31_crosstab(df):
    return pd.crosstab(df['department'], df['city'], margins=True)

# ------ Q32: Pivot then Flatten MultiIndex Columns ------
# Create a pivot and flatten the resulting MultiIndex columns into single-level names.

def q32_flatten_pivot(df):
    pivot = pd.pivot_table(df, values='amount', index='emp_id', columns='product',
                           aggfunc=['sum', 'mean'], fill_value=0)
    pivot.columns = ['_'.join(col).strip() for col in pivot.columns]
    return pivot.reset_index()

# ------ Q33: Transpose ------
# Show department-level statistics as columns (transposed).

def q33_transpose(df):
    stats = df.groupby('department').agg(
        avg_salary=('salary', 'mean'),
        avg_age=('age', 'mean'),
        headcount=('emp_id', 'count')
    )
    return stats.T

# ------ Q34: Explode ------
# Given a column with lists, explode it into separate rows.

def q34_explode():
    df = pd.DataFrame({
        'employee': ['Alice', 'Bob', 'Charlie'],
        'skills': [['Python', 'SQL', 'Spark'], ['Java', 'Scala'], ['Python', 'R', 'SQL', 'Tableau']]
    })
    return df.explode('skills').reset_index(drop=True)


# ============================================================
# SECTION 5: STATISTICAL CALCULATIONS (Q35-Q42)
# ============================================================

# ------ Q35: Descriptive Statistics ------
# Generate full descriptive statistics for salary, include percentiles 10, 25, 50, 75, 90.

def q35_descriptive_stats(df):
    return df['salary'].describe(percentiles=[0.1, 0.25, 0.5, 0.75, 0.9])

# ------ Q36: Correlation Matrix ------
# Calculate correlation between salary, age, rating, and bonus.

def q36_correlation(df):
    return df[['salary', 'age', 'rating', 'bonus']].corr().round(3)

# ------ Q37: Quantile-Based Binning ------
# Categorize employees into salary quartiles (Q1, Q2, Q3, Q4).

def q37_quantile_bins(df):
    df = df.copy()
    df['salary_quartile'] = pd.qcut(df['salary'], q=4, labels=['Q1', 'Q2', 'Q3', 'Q4'])
    return df

# ------ Q38: Custom Binning ------
# Bin ages into categories: 'Young' (<30), 'Mid' (30-40), 'Senior' (>40).

def q38_custom_bins(df):
    df = df.copy()
    df['age_group'] = pd.cut(df['age'], bins=[0, 30, 40, 100], labels=['Young', 'Mid', 'Senior'])
    return df

# ------ Q39: Weighted Average ------
# Calculate quantity-weighted average price (amount/quantity) per product.

def q39_weighted_avg(df):
    df = df.copy()
    df['unit_price'] = df['amount'] / df['quantity']
    result = df.groupby('product').apply(
        lambda x: np.average(x['unit_price'], weights=x['quantity']), include_groups=False
    ).reset_index(name='weighted_avg_price')
    return result

# ------ Q40: Running Percentile Rank ------
# Assign percentile rank of each employee's salary within the entire company.

def q40_percentile_rank(df):
    df = df.copy()
    df['salary_percentile'] = df['salary'].rank(pct=True).round(2)
    return df

# ------ Q41: Covariance ------
# Calculate the covariance between salary and bonus.

def q41_covariance(df):
    return df[['salary', 'bonus']].cov()

# ------ Q42: Mode per Group ------
# Find the most common product sold per region.

def q42_mode_per_group(df):
    return df.groupby('region')['product'].agg(lambda x: x.mode().iloc[0]).reset_index(name='most_common_product')


# ============================================================
# SECTION 6: MERGING, JOINING & ADVANCED (Q43-Q50)
# ============================================================

# ------ Q43: Left Join with Aggregated Data ------
# Join employees with their total sales amount (left join to keep all employees).

def q43_left_join_agg(employees_df, sales_df):
    total_sales = sales_df.groupby('emp_id')['amount'].sum().reset_index(name='total_sales')
    return employees_df.merge(total_sales, on='emp_id', how='left').fillna({'total_sales': 0})

# ------ Q44: Anti Join ------
# Find employees who have never made a sale.

def q44_anti_join(employees_df, sales_df):
    sellers = sales_df['emp_id'].unique()
    return employees_df[~employees_df['emp_id'].isin(sellers)]

# ------ Q45: Self-Join for Pairwise Comparison ------
# Find all pairs of employees in the same department where one earns at least 20% more.

def q45_self_join(df):
    merged = df.merge(df, on='department', suffixes=('_a', '_b'))
    merged = merged[merged['emp_id_a'] < merged['emp_id_b']]
    merged = merged[merged['salary_a'] >= merged['salary_b'] * 1.2]
    return merged[['name_a', 'name_b', 'department', 'salary_a', 'salary_b']]

# ------ Q46: Concat with Deduplication ------
# Concatenate two DataFrames and remove duplicate rows.

def q46_concat_dedup():
    df1 = pd.DataFrame({'id': [1, 2, 3], 'value': ['a', 'b', 'c']})
    df2 = pd.DataFrame({'id': [3, 4, 5], 'value': ['c', 'd', 'e']})
    return pd.concat([df1, df2]).drop_duplicates().reset_index(drop=True)

# ------ Q47: Combine First (Fill NaN from another source) ------
# Fill missing values in one DataFrame using values from another.

def q47_combine_first():
    primary = pd.DataFrame({'A': [1, np.nan, 3, np.nan], 'B': [np.nan, 5, np.nan, 7]})
    backup = pd.DataFrame({'A': [10, 20, 30, 40], 'B': [50, 60, 70, 80]})
    return primary.combine_first(backup)

# ------ Q48: Consecutive Condition Detection ------
# Flag sales where an employee had 3 or more consecutive sales above 1200.

def q48_consecutive_condition(df):
    df = df.sort_values(['emp_id', 'sale_date']).copy()
    df['above_1200'] = (df['amount'] > 1200).astype(int)
    df['streak'] = df.groupby('emp_id')['above_1200'].transform(
        lambda x: x.groupby((x != x.shift()).cumsum()).cumsum()
    )
    df['hot_streak'] = df['streak'] >= 3
    return df

# ------ Q49: Year-over-Year / Period-over-Period Comparison ------
# Calculate month-over-month sales growth per employee.

def q49_mom_growth(df):
    df = df.copy()
    df['month'] = df['sale_date'].dt.to_period('M')
    monthly = df.groupby(['emp_id', 'month'])['amount'].sum().reset_index()
    monthly['prev_month_amount'] = monthly.groupby('emp_id')['amount'].shift(1)
    monthly['mom_growth_pct'] = ((monthly['amount'] - monthly['prev_month_amount']) / monthly['prev_month_amount'] * 100).round(2)
    return monthly

# ------ Q50: Dynamic Column Selection with Apply ------
# For each row, return the column name that has the maximum value among salary, bonus, and age.

def q50_dynamic_column(df):
    df = df.copy()
    cols = ['salary', 'bonus', 'age']
    df['max_field'] = df[cols].idxmax(axis=1)
    df['max_value'] = df[cols].max(axis=1)
    return df


# ============================================================
# RUNNER — Execute and display all solutions
# ============================================================

if __name__ == '__main__':
    print("=" * 70)
    print("  50 Pandas Interview Questions — Solutions")
    print("=" * 70)

    questions = [
        ("Q1: Filter high-salary Engineering employees", lambda: q1_filter_high_salary_eng(employees)),
        ("Q2: Filter HR/Sales with rating >= 4.0", lambda: q2_filter_isin_rating(employees)),
        ("Q3: Names starting with a vowel", lambda: q3_filter_name_vowel(employees)),
        ("Q4: Top 2 paid per department", lambda: q4_top_n_per_group(employees)),
        ("Q5: Query method — hired after 2020, age < 30", lambda: q5_query_method(employees)),
        ("Q6: Employees with at least one sale", lambda: q6_filter_by_another_df(employees, sales)),
        ("Q7: Conditional column (Senior/Junior)", lambda: q7_conditional_column(employees)),
        ("Q8: Sales amount between 1000-1500", lambda: q8_filter_between(sales)),
        ("Q9: Avg salary & total bonus per dept", lambda: q9_basic_groupby(employees)),
        ("Q10: Salary stats per department", lambda: q10_multi_agg(employees)),
        ("Q11: Salary as % of department total", lambda: q11_groupby_transform(employees)),
        ("Q12: Departments with avg salary > 75000", lambda: q12_groupby_filter(employees)),
        ("Q13: Named aggregation per department", lambda: q13_named_agg(employees)),
        ("Q14: Cumulative sales per employee", lambda: q14_cumulative_sum(sales.copy())),
        ("Q15: Salary rank within department", lambda: q15_groupby_rank(employees)),
        ("Q16: Sale count per product per region", lambda: q16_groupby_value_counts(sales)),
        ("Q17: Sale amount as % of product total", lambda: q17_pct_of_group(sales)),
        ("Q18: First and last sale per employee", lambda: q18_first_last(sales)),
        ("Q19: 3-day rolling avg close price", lambda: q19_rolling_avg(stock_prices.copy())),
        ("Q20: 3-row rolling sum of sale amount", lambda: q20_rolling_sum(sales.copy())),
        ("Q21: Lag and lead sale amounts", lambda: q21_lag_lead(sales.copy())),
        ("Q22: Daily return (pct change)", lambda: q22_pct_change(stock_prices.copy())),
        ("Q23: Expanding mean of sales", lambda: q23_expanding_mean(sales.copy())),
        ("Q24: EWMA of close price", lambda: q24_ewma(stock_prices.copy())),
        ("Q25: Z-score of sale amounts", lambda: q25_diff_from_mean(sales)),
        ("Q26: Row number within group", lambda: q26_row_number(sales.copy())),
        ("Q27: Pivot — sum of amount by region x product", lambda: q27_pivot_table(sales)),
        ("Q28: Pivot — sum and count", lambda: q28_pivot_multi_agg(sales)),
        ("Q29: Melt wide to long", lambda: q29_melt()),
        ("Q30: Stack/Unstack", lambda: q30_stack_unstack(sales)),
        ("Q31: Crosstab department vs city", lambda: q31_crosstab(employees)),
        ("Q32: Flatten MultiIndex pivot columns", lambda: q32_flatten_pivot(sales)),
        ("Q33: Transposed department stats", lambda: q33_transpose(employees)),
        ("Q34: Explode list column", lambda: q34_explode()),
        ("Q35: Descriptive statistics with percentiles", lambda: q35_descriptive_stats(employees)),
        ("Q36: Correlation matrix", lambda: q36_correlation(employees)),
        ("Q37: Salary quartile bins", lambda: q37_quantile_bins(employees)),
        ("Q38: Custom age bins", lambda: q38_custom_bins(employees)),
        ("Q39: Weighted average price per product", lambda: q39_weighted_avg(sales)),
        ("Q40: Percentile rank of salary", lambda: q40_percentile_rank(employees)),
        ("Q41: Covariance of salary and bonus", lambda: q41_covariance(employees)),
        ("Q42: Most common product per region", lambda: q42_mode_per_group(sales)),
        ("Q43: Left join employees with total sales", lambda: q43_left_join_agg(employees, sales)),
        ("Q44: Anti join — employees with no sales", lambda: q44_anti_join(employees, sales)),
        ("Q45: Self-join — salary 20%+ gap in same dept", lambda: q45_self_join(employees)),
        ("Q46: Concat with deduplication", lambda: q46_concat_dedup()),
        ("Q47: Combine first (fill NaN)", lambda: q47_combine_first()),
        ("Q48: Consecutive condition detection", lambda: q48_consecutive_condition(sales)),
        ("Q49: Month-over-month sales growth", lambda: q49_mom_growth(sales)),
        ("Q50: Dynamic column selection (idxmax)", lambda: q50_dynamic_column(employees)),
    ]

    for title, fn in questions:
        print(f"\n{'─' * 70}")
        print(f"  {title}")
        print(f"{'─' * 70}")
        result = fn()
        if isinstance(result, pd.DataFrame):
            print(result.to_string(max_rows=8))
        else:
            print(result)
