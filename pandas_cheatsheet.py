"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  PANDAS DATA MANIPULATION CHEATSHEET — Interview Prep (Complete)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Covers BASICS → INTERMEDIATE → ADVANCED patterns.
Each section: concept → syntax → gotchas → interview tips.
"""

import pandas as pd
import numpy as np


# ╔════════════════════════════════════════════════════════════════════════╗
# ║  PART A: FUNDAMENTALS — DataFrame Basics                             ║
# ╚════════════════════════════════════════════════════════════════════════╝


# ════════════════════════════════════════════════════════════════════════
# A1. CREATING DataFrames & Series
# ════════════════════════════════════════════════════════════════════════
"""
┌──────────────────────────┬──────────────────────────────────────────────┐
│ Pattern                  │ Syntax                                        │
├──────────────────────────┼──────────────────────────────────────────────┤
│ From dict                │ pd.DataFrame({'a': [1,2], 'b': [3,4]})       │
│ From list of dicts       │ pd.DataFrame([{'a':1,'b':2}, {'a':3,'b':4}]) │
│ From list of lists       │ pd.DataFrame([[1,2],[3,4]], columns=['a','b'])│
│ From CSV                 │ pd.read_csv('file.csv')                      │
│ From Excel               │ pd.read_excel('file.xlsx', sheet_name=0)     │
│ From SQL                 │ pd.read_sql('SELECT * FROM t', conn)         │
│ From clipboard           │ pd.read_clipboard()                          │
│ Series                   │ pd.Series([1,2,3], name='col')               │
│ Empty DataFrame          │ pd.DataFrame(columns=['a','b'])              │
│ Date range               │ pd.date_range('2024-01-01', periods=10)      │
│ Range index              │ pd.RangeIndex(start=0, stop=10, step=2)      │
└──────────────────────────┴──────────────────────────────────────────────┘

READ_CSV common params:
  pd.read_csv('f.csv',
      sep=',',              # delimiter
      header=0,             # row number for header (None if no header)
      names=['a','b'],      # custom column names
      index_col='id',       # set column as index
      usecols=['a','b'],    # read only these columns
      dtype={'a': int},     # force dtypes
      parse_dates=['date'], # auto-parse date columns
      na_values=['NA',''],  # treat these as NaN
      nrows=100,            # read only first 100 rows
      skiprows=5,           # skip first 5 rows
      encoding='utf-8'
  )
"""


# ════════════════════════════════════════════════════════════════════════
# A2. INSPECTING DATA
# ════════════════════════════════════════════════════════════════════════
"""
┌──────────────────────────┬──────────────────────────────────────────────┐
│ Pattern                  │ Syntax                                        │
├──────────────────────────┼──────────────────────────────────────────────┤
│ Shape                    │ df.shape               # (rows, cols)        │
│ Data types               │ df.dtypes                                    │
│ Info (types + non-null)  │ df.info()                                    │
│ First/Last rows          │ df.head(5) / df.tail(5)                      │
│ Random sample            │ df.sample(5) / df.sample(frac=0.1)           │
│ Column names             │ df.columns.tolist()                          │
│ Index                    │ df.index                                     │
│ Unique values            │ df['col'].unique()                           │
│ Number of unique         │ df['col'].nunique()                          │
│ Value counts             │ df['col'].value_counts()                     │
│                          │ df['col'].value_counts(normalize=True) # pct │
│ Describe (numeric)       │ df.describe()                                │
│ Describe (all)           │ df.describe(include='all')                   │
│ Memory usage             │ df.memory_usage(deep=True)                   │
│ Non-null count           │ df.count()                                   │
│ Check for NaN            │ df.isna().sum()                              │
│ Check duplicates         │ df.duplicated().sum()                        │
└──────────────────────────┴──────────────────────────────────────────────┘

INTERVIEW TIP:
  First thing in any data question: "Let me look at the shape,
  dtypes, and null counts." Shows structured thinking.
"""


# ════════════════════════════════════════════════════════════════════════
# A3. SELECTING & INDEXING
# ════════════════════════════════════════════════════════════════════════
"""
┌──────────────────────────┬──────────────────────────────────────────────┐
│ Pattern                  │ Syntax                                        │
├──────────────────────────┼──────────────────────────────────────────────┤
│ Single column            │ df['col']  or  df.col     # returns Series   │
│ Multiple columns         │ df[['col1', 'col2']]      # returns DataFrame│
│ By label (row + col)     │ df.loc[row_label, col_label]                 │
│ By position (row + col)  │ df.iloc[row_pos, col_pos]                    │
│ Row slice by label       │ df.loc['a':'c']           # inclusive both   │
│ Row slice by position    │ df.iloc[0:3]              # exclusive end    │
│ Single cell              │ df.at[row_label, 'col']   # fast scalar      │
│                          │ df.iat[row_pos, col_pos]  # fast scalar      │
│ Conditional rows         │ df.loc[df['col'] > 5]                        │
│ Conditional + col select │ df.loc[df['col'] > 5, ['a','b']]             │
│ Select dtypes            │ df.select_dtypes(include='number')            │
│                          │ df.select_dtypes(exclude='object')            │
└──────────────────────────┴──────────────────────────────────────────────┘

loc vs iloc:
  ┌──────┬─────────────────────────┬──────────────────────────┐
  │      │ loc                     │ iloc                      │
  ├──────┼─────────────────────────┼──────────────────────────┤
  │ Uses │ Labels / boolean mask   │ Integer positions          │
  │ End  │ INCLUSIVE               │ EXCLUSIVE                  │
  │ Best │ Named index, conditions │ Positional slicing         │
  └──────┴─────────────────────────┴──────────────────────────┘

GOTCHAS:
  - df['col'] returns a view (can cause SettingWithCopyWarning)
  - Use df.loc[mask, 'col'] = val  for safe assignment
  - df[0:5] works (positional slice) but df[0] does NOT (ambiguous)
  - at/iat are faster than loc/iloc for single values
"""


# ════════════════════════════════════════════════════════════════════════
# A4. ADDING, RENAMING & DROPPING COLUMNS
# ════════════════════════════════════════════════════════════════════════
"""
┌──────────────────────────┬──────────────────────────────────────────────┐
│ Pattern                  │ Syntax                                        │
├──────────────────────────┼──────────────────────────────────────────────┤
│ Add column               │ df['new'] = df['a'] + df['b']                │
│ Add with assign (chain)  │ df.assign(new=lambda x: x['a'] + x['b'])    │
│ Insert at position       │ df.insert(1, 'new', values)                  │
│ Rename columns           │ df.rename(columns={'old': 'new'})            │
│ Rename all               │ df.columns = ['a', 'b', 'c']                │
│ Lower case all cols      │ df.columns = df.columns.str.lower()          │
│ Drop column              │ df.drop(columns=['col1', 'col2'])            │
│ Drop rows                │ df.drop(index=[0, 1, 2])                    │
│ Reorder columns          │ df[['c', 'a', 'b']]                         │
│ Map/Replace values       │ df['col'].map({'a': 1, 'b': 2})             │
│                          │ df['col'].replace({'old': 'new'})            │
│ Clip values              │ df['col'].clip(lower=0, upper=100)           │
└──────────────────────────┴──────────────────────────────────────────────┘

assign() is great for method chaining:
  result = (df
      .assign(total = lambda x: x['price'] * x['qty'])
      .assign(tax   = lambda x: x['total'] * 0.1)
  )

map vs apply vs replace:
  map()     → Series only, element-wise, accepts dict/func/Series
  apply()   → Series or DataFrame, more flexible, slower
  replace() → exact value substitution, supports regex
"""


# ════════════════════════════════════════════════════════════════════════
# A5. SORTING & REINDEXING
# ════════════════════════════════════════════════════════════════════════
"""
┌──────────────────────────┬──────────────────────────────────────────────┐
│ Pattern                  │ Syntax                                        │
├──────────────────────────┼──────────────────────────────────────────────┤
│ Sort by column           │ df.sort_values('col', ascending=False)        │
│ Sort by multiple         │ df.sort_values(['a','b'], ascending=[T,F])   │
│ Sort by index            │ df.sort_index()                              │
│ Reset index              │ df.reset_index(drop=True)                    │
│ Set column as index      │ df.set_index('col')                          │
│ Reindex                  │ df.reindex(new_index, fill_value=0)          │
│ Nlargest / Nsmallest     │ df.nlargest(5, 'col') / df.nsmallest(5,'c') │
│ Shuffle rows             │ df.sample(frac=1).reset_index(drop=True)     │
└──────────────────────────┴──────────────────────────────────────────────┘

GOTCHAS:
  - sort_values returns a NEW DataFrame (not in-place by default)
  - reset_index(drop=True) → discard old index
  - reset_index(drop=False) → old index becomes a column
  - nlargest is faster than sort_values + head for large DataFrames
"""


# ════════════════════════════════════════════════════════════════════════
# A6. DATA TYPES & TYPE CONVERSION
# ════════════════════════════════════════════════════════════════════════
"""
┌──────────────────────────┬──────────────────────────────────────────────┐
│ Pattern                  │ Syntax                                        │
├──────────────────────────┼──────────────────────────────────────────────┤
│ Check types              │ df.dtypes                                    │
│ Convert type             │ df['col'].astype(int)                        │
│                          │ df['col'].astype('float64')                  │
│ To category              │ df['col'].astype('category')                 │
│ To datetime              │ pd.to_datetime(df['col'])                    │
│ To numeric (coerce err)  │ pd.to_numeric(df['col'], errors='coerce')   │
│ To string                │ df['col'].astype(str)                        │
│ Nullable int (with NaN)  │ df['col'].astype('Int64')  # capital I       │
│ Boolean                  │ df['col'].astype(bool)                       │
│ Infer better types       │ df.convert_dtypes()                          │
└──────────────────────────┴──────────────────────────────────────────────┘

COMMON TYPE HIERARCHY:
  object  → typically strings (catch-all)
  int64   → integers (no NaN allowed in standard int)
  float64 → floats (NaN allowed)
  bool    → True/False
  datetime64[ns]   → timestamps
  timedelta64[ns]  → time differences
  category         → categorical (saves memory)
  Int64 (nullable) → integers with NaN support

GOTCHAS:
  - Standard int columns with NaN auto-convert to float64
  - Use nullable Int64 (capital I) to keep ints with NaN
  - astype(int) fails on NaN → use errors='coerce' or fill first
  - pd.to_numeric with errors='coerce' turns bad values to NaN
"""


# ════════════════════════════════════════════════════════════════════════
# A7. MISSING DATA HANDLING
# ════════════════════════════════════════════════════════════════════════
"""
┌──────────────────────────┬──────────────────────────────────────────────┐
│ Pattern                  │ Syntax                                        │
├──────────────────────────┼──────────────────────────────────────────────┤
│ Detect NaN               │ df.isna() / df.isnull()     # same thing     │
│ Count NaN per column     │ df.isna().sum()                              │
│ Pct missing              │ df.isna().mean() * 100                       │
│ Any NaN in row           │ df.isna().any(axis=1)                        │
│ Drop rows with NaN       │ df.dropna()                                  │
│ Drop if specific col NaN │ df.dropna(subset=['col1','col2'])            │
│ Drop cols with NaN       │ df.dropna(axis=1)                            │
│ Drop if threshold        │ df.dropna(thresh=3)  # keep if ≥3 non-null  │
│ Fill with constant       │ df.fillna(0)                                 │
│ Fill with dict per col   │ df.fillna({'a': 0, 'b': 'unknown'})         │
│ Forward fill             │ df.ffill()  or  df.fillna(method='ffill')    │
│ Backward fill            │ df.bfill()  or  df.fillna(method='bfill')   │
│ Fill with column mean    │ df.fillna(df.mean(numeric_only=True))        │
│ Fill with group mean     │ df.groupby('g')['c'].transform(              │
│                          │     lambda x: x.fillna(x.mean()))            │
│ Interpolate              │ df['col'].interpolate(method='linear')       │
│ Replace specific value   │ df.replace(-999, np.nan)                     │
└──────────────────────────┴──────────────────────────────────────────────┘

INTERVIEW TIP:
  "How do you handle missing data?" is a VERY common behavioral question.
  Framework:
    1. Understand the pattern: random vs systematic missingness
    2. Decide: drop (if <5% and random) or impute
    3. Impute method depends on data type:
       - Numeric: mean (normal dist), median (skewed), interpolate (time series)
       - Categorical: mode, or 'Unknown' category
       - Time series: ffill/bfill or interpolate
    4. For modeling: consider indicator column for "was_missing"

GOTCHAS:
  - NaN != NaN (np.nan == np.nan → False). Use pd.isna() to check.
  - fillna does NOT modify in place by default
  - dropna thresh=N means: "keep row if it has at least N non-null values"
"""


# ════════════════════════════════════════════════════════════════════════
# A8. DUPLICATES
# ════════════════════════════════════════════════════════════════════════
"""
┌──────────────────────────┬──────────────────────────────────────────────┐
│ Pattern                  │ Syntax                                        │
├──────────────────────────┼──────────────────────────────────────────────┤
│ Check duplicates         │ df.duplicated()              # bool series    │
│ Count duplicates         │ df.duplicated().sum()                        │
│ Find duplicate rows      │ df[df.duplicated(keep=False)] # show ALL     │
│ Drop duplicates (first)  │ df.drop_duplicates(keep='first')             │
│ Drop duplicates (last)   │ df.drop_duplicates(keep='last')              │
│ Drop ALL duplicates      │ df[~df.duplicated(keep=False)]               │
│ Duplicates on subset     │ df.drop_duplicates(subset=['col1','col2'])   │
│ Count per value          │ df.groupby('col').size()                     │
│ Keep row with max value  │ df.sort_values('val', ascending=False)       │
│   among duplicates       │   .drop_duplicates(subset='key', keep='first')│
└──────────────────────────┴──────────────────────────────────────────────┘

KEEP parameter:
  'first' → keep first occurrence, mark rest as duplicate
  'last'  → keep last occurrence, mark rest as duplicate
  False   → mark ALL occurrences as duplicate (no keeping)

INTERVIEW TIP:
  "Remove duplicates but keep the one with the highest score"
  → Sort descending by score, then drop_duplicates(keep='first')
  OR use groupby + idxmax for more control
"""


# ╔════════════════════════════════════════════════════════════════════════╗
# ║  PART B: INTERMEDIATE — Core Manipulation Patterns                   ║
# ╚════════════════════════════════════════════════════════════════════════╝


# ════════════════════════════════════════════════════════════════════════
# B1. FILTERING & SELECTION (Advanced)
# ════════════════════════════════════════════════════════════════════════
"""
┌──────────────────────────┬────────────────────────────────────────────┐
│ Pattern                  │ Syntax                                     │
├──────────────────────────┼────────────────────────────────────────────┤
│ Boolean mask             │ df[df['col'] > val]                        │
│ Multiple conditions      │ df[(cond1) & (cond2)]       # & | ~       │
│ isin                     │ df[df['col'].isin([a, b])]                 │
│ between                  │ df[df['col'].between(lo, hi)]              │
│ String filter            │ df[df['col'].str.startswith('X')]          │
│                          │ df[df['col'].str.contains('pat', na=False)]│
│ query() method           │ df.query('col > 5 and col2 == "x"')       │
│ Top N per group          │ df.groupby('g').apply(                     │
│                          │     lambda x: x.nlargest(n, 'col'))        │
│ Conditional column       │ np.where(cond, val_true, val_false)        │
│                          │ np.select([c1,c2], [v1,v2], default)       │
│ Filter by another df     │ df[df['id'].isin(other['id'].unique())]    │
│ Anti-filter              │ df[~df['id'].isin(other['id'])]            │
└──────────────────────────┴────────────────────────────────────────────┘

np.where vs np.select:
  np.where  → 2 outcomes only (if/else)
  np.select → multiple conditions → multiple outcomes (if/elif/elif/else)

  df['grade'] = np.select(
      [df['score'] >= 90, df['score'] >= 80, df['score'] >= 70],
      ['A', 'B', 'C'],
      default='F'
  )

GOTCHAS:
  - Always wrap each condition in () with & | ~
  - .str methods return NaN for NaN values → use na=False
  - query() references column names directly, external vars with @var
  - nlargest/nsmallest keep duplicates by default (keep='all')
"""


# ════════════════════════════════════════════════════════════════════════
# B2. GROUPBY & AGGREGATION
# ════════════════════════════════════════════════════════════════════════
"""
┌──────────────────────────┬──────────────────────────────────────────────────┐
│ Pattern                  │ Syntax                                            │
├──────────────────────────┼──────────────────────────────────────────────────┤
│ Basic agg                │ df.groupby('g')['col'].mean()                     │
│ Multiple agg             │ .agg(['min','max','mean','std'])                   │
│ Named agg                │ .agg(new_name=('col','func'))                     │
│ Custom agg               │ .agg(lambda x: x.max() - x.min())                │
│ Transform (broadcast)    │ .groupby('g')['col'].transform('sum')             │
│ Filter groups            │ .groupby('g').filter(lambda x: x['c'].mean()>val) │
│ Cumulative sum           │ .groupby('g')['col'].cumsum()                     │
│ Rank in group            │ .groupby('g')['col'].rank(ascending=False)        │
│ Count per group          │ .groupby(['a','b']).size()                         │
│                          │ .groupby('a')['b'].value_counts()                 │
│ Pct of group total       │ col / groupby.transform('sum') * 100              │
│ First / Last             │ .agg(first=('col','first'), last=('col','last'))  │
│ Nth row                  │ .groupby('g').nth(0)                              │
│ Apply (flexible)         │ .groupby('g').apply(custom_func)                  │
└──────────────────────────┴──────────────────────────────────────────────────┘

KEY DISTINCTION — agg vs transform vs apply vs filter:

  agg()       → returns ONE row per group (reduces)
  transform() → returns SAME shape as input (broadcasts group result back)
  apply()     → flexible: can return any shape (use for complex logic)
  filter()    → returns subset of ORIGINAL rows where group meets condition

  ┌─────────┐   agg()       ┌──────┐
  │ group 1 │ ──────────▶  │ 1 row│
  │ 5 rows  │               └──────┘
  └─────────┘
  ┌─────────┐  transform()  ┌─────────┐
  │ group 1 │ ──────────▶  │ group 1 │  (same 5 rows, each = group stat)
  │ 5 rows  │               │ 5 rows  │
  └─────────┘               └─────────┘

RANK method parameter:
  'average' → tied values get mean rank (default)
  'min'     → tied values get lowest rank (SQL-style RANK)
  'dense'   → like min but no gaps (SQL DENSE_RANK)
  'first'   → tied values ranked by position (SQL ROW_NUMBER)

GOTCHAS:
  - groupby drops NaN keys by default → use dropna=False
  - transform must return same-length series
  - .size() counts all rows; .count() excludes NaN
  - Named agg: .agg(name=('column', 'func')) — note the tuple
"""


# ════════════════════════════════════════════════════════════════════════
# B3. WINDOW FUNCTIONS
# ════════════════════════════════════════════════════════════════════════
"""
┌──────────────────────────┬────────────────────────────────────────────────┐
│ Pattern                  │ Syntax                                          │
├──────────────────────────┼────────────────────────────────────────────────┤
│ Rolling window           │ .rolling(n, min_periods=1).mean()                │
│ Rolling in group         │ .groupby('g')['c'].transform(                   │
│                          │     lambda x: x.rolling(3).mean())              │
│ Lag (previous row)       │ .groupby('g')['col'].shift(1)                   │
│ Lead (next row)          │ .groupby('g')['col'].shift(-1)                  │
│ Pct change               │ .groupby('g')['col'].pct_change()               │
│ Diff                     │ .groupby('g')['col'].diff()                     │
│ Expanding (cumulative)   │ .expanding(min_periods=1).mean()                │
│ EWMA                     │ .ewm(span=N).mean()                            │
│ Cumulative sum           │ .groupby('g')['col'].cumsum()                   │
│ Cumulative count         │ .groupby('g').cumcount()      # 0-indexed       │
│ Cumulative max/min       │ .groupby('g')['col'].cummax()                   │
└──────────────────────────┴────────────────────────────────────────────────┘

SQL ↔ PANDAS MAPPING:
  SQL                          │ Pandas
  ─────────────────────────────┼──────────────────────────────
  LAG(col, 1) OVER(...)        │ .shift(1)
  LEAD(col, 1) OVER(...)       │ .shift(-1)
  SUM() OVER(ROWS UNBOUNDED    │ .expanding().sum() or .cumsum()
    PRECEDING)                 │
  AVG() OVER(ROWS BETWEEN      │ .rolling(3).mean()
    2 PREC AND CURRENT ROW)    │
  ROW_NUMBER() OVER(PARTITION   │ .groupby('g').cumcount() + 1
    BY g ORDER BY col)          │
  RANK() OVER(...)              │ .rank(method='min')
  DENSE_RANK() OVER(...)        │ .rank(method='dense')
  PERCENT_RANK() OVER(...)      │ .rank(pct=True)
  NTILE(4)                      │ pd.qcut(..., 4, labels=False) + 1

GOTCHAS:
  - rolling/expanding need data SORTED first
  - rolling(3) returns NaN for first 2 rows unless min_periods=1
  - shift(1) = previous row, shift(-1) = next row
  - pct_change first row is always NaN
  - Always sort by date/order column before applying windows

CONSECUTIVE STREAK DETECTION (classic interview pattern):
  # 1. Boolean mask for condition
  mask = (df['amount'] > 1000).astype(int)
  # 2. Identify where streaks break → cumsum of inverted mask
  streak_id = (~mask.astype(bool)).cumsum()
  # 3. Cumulative count within each streak
  streak_len = mask.groupby(streak_id).cumsum()
"""


# ════════════════════════════════════════════════════════════════════════
# B4. PIVOT, RESHAPE & RESTRUCTURE
# ════════════════════════════════════════════════════════════════════════
"""
┌──────────────────────────┬──────────────────────────────────────────────┐
│ Pattern                  │ Syntax                                        │
├──────────────────────────┼──────────────────────────────────────────────┤
│ Pivot table              │ pd.pivot_table(df, values='v', index='r',     │
│                          │   columns='c', aggfunc='sum', fill_value=0)   │
│ Pivot (no agg, unique)   │ df.pivot(index='r', columns='c', values='v')  │
│ Melt (wide→long)         │ pd.melt(df, id_vars='id', var_name='var',     │
│                          │   value_name='val')                           │
│ Stack (cols→rows)        │ df.stack()                                    │
│ Unstack (rows→cols)      │ df.unstack(fill_value=0)                      │
│ Crosstab                 │ pd.crosstab(df['a'], df['b'], margins=True)   │
│ Transpose                │ df.T                                          │
│ Explode (list→rows)      │ df.explode('list_col')                        │
│ Flatten MultiIndex cols  │ ['_'.join(col) for col in df.columns]         │
│ Get dummies (one-hot)    │ pd.get_dummies(df, columns=['cat_col'])        │
└──────────────────────────┴──────────────────────────────────────────────┘

PIVOT vs PIVOT_TABLE:
  pivot()       → reshapes, NO aggregation, errors on duplicates
  pivot_table() → reshapes WITH aggregation, handles duplicates

MELT is the INVERSE of PIVOT:
  Wide:  id | Q1 | Q2 | Q3        Long:  id | quarter | value
                                          1  | Q1      | 100
  melt() ──────────────────▶             1  | Q2      | 200

STACK vs UNSTACK:
  stack()   → columns become inner row index level (wide → tall)
  unstack() → inner row index becomes columns (tall → wide)

GOTCHAS:
  - pivot() fails with duplicate index/column combos → use pivot_table()
  - fill_value in pivot_table to avoid NaN
  - explode() keeps index → reset_index(drop=True) if needed
  - After pivot, columns may be MultiIndex → flatten with join trick
"""


# ════════════════════════════════════════════════════════════════════════
# B5. STATISTICAL CALCULATIONS
# ════════════════════════════════════════════════════════════════════════
"""
┌──────────────────────────┬────────────────────────────────────────────────┐
│ Pattern                  │ Syntax                                          │
├──────────────────────────┼────────────────────────────────────────────────┤
│ Describe                 │ df['col'].describe(percentiles=[.1,.25,.5,.9])  │
│ Correlation              │ df[cols].corr()                                 │
│ Covariance               │ df[cols].cov()                                  │
│ Quantile binning         │ pd.qcut(df['col'], q=4, labels=[...])          │
│ Custom binning           │ pd.cut(df['col'], bins=[0,30,60,100])          │
│ Percentile rank          │ df['col'].rank(pct=True)                       │
│ Z-score                  │ (col - col.mean()) / col.std()                 │
│ Weighted average         │ np.average(vals, weights=wts)                   │
│ Mode                     │ df['col'].mode()                               │
│ Skewness / Kurtosis      │ df['col'].skew() / df['col'].kurt()            │
│ Variance                 │ df['col'].var()     # ddof=1 by default        │
│ Standard error           │ df['col'].sem()                                │
└──────────────────────────┴────────────────────────────────────────────────┘

QCUT vs CUT:
  qcut() → equal-FREQUENCY bins (same number of items per bin)
  cut()  → equal-WIDTH bins (same range per bin)

  Example: data = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    qcut(q=2) → each bin has 5 items:  [10-55] and [55-100]
    cut(bins=2) → equal range width:    [10-55] and [55-100]
    (happens to be same here but differs with skewed data)

GOTCHAS:
  - .corr() uses Pearson by default → method='spearman' for rank corr
  - .var() and .std() use ddof=1 (sample) by default → ddof=0 for population
  - qcut may fail if too many identical values → duplicates='drop'
  - mode() returns a Series (can have multiple modes)
"""


# ════════════════════════════════════════════════════════════════════════
# B6. MERGING, JOINING & COMBINING
# ════════════════════════════════════════════════════════════════════════
"""
┌──────────────────────────┬────────────────────────────────────────────────┐
│ Pattern                  │ Syntax                                          │
├──────────────────────────┼────────────────────────────────────────────────┤
│ Inner join               │ pd.merge(a, b, on='key', how='inner')           │
│ Left join                │ pd.merge(a, b, on='key', how='left')            │
│ Right join               │ pd.merge(a, b, on='key', how='right')           │
│ Outer join               │ pd.merge(a, b, on='key', how='outer')           │
│ Join on diff col names   │ pd.merge(a, b, left_on='x', right_on='y')      │
│ Join on index            │ a.join(b, on='key')  or  merge with             │
│                          │   left_index=True, right_index=True             │
│ Anti join (not in)       │ a[~a['key'].isin(b['key'])]                     │
│ Semi join (exists in)    │ a[a['key'].isin(b['key'])]                      │
│ Self join                │ pd.merge(df, df, on='col', suffixes=('_l','_r'))│
│ Cross join               │ pd.merge(a, b, how='cross')                     │
│ Concat (stack rows)      │ pd.concat([a, b], ignore_index=True)            │
│ Concat (side by side)    │ pd.concat([a, b], axis=1)                       │
│ Combine_first (fill NaN) │ a.combine_first(b)                              │
│ Update in place          │ a.update(b)                                     │
└──────────────────────────┴────────────────────────────────────────────────┘

SQL ↔ PANDAS JOIN MAPPING:
  SQL                     │ Pandas
  ────────────────────────┼────────────────────────
  INNER JOIN              │ how='inner' (default)
  LEFT JOIN               │ how='left'
  FULL OUTER JOIN         │ how='outer'
  CROSS JOIN              │ how='cross'
  WHERE NOT IN (subquery) │ ~isin()
  WHERE EXISTS (subquery) │ isin()

MERGE DIAGNOSTICS:
  validate='one_to_one'   → error if duplicate keys
  validate='one_to_many'  → error if left has dups
  indicator=True          → adds _merge column: left_only/right_only/both

GOTCHAS:
  - Merge on columns with NaN: NaN ≠ NaN → those rows won't match
  - Duplicate keys cause cartesian product (row explosion!)
  - suffixes=('_x','_y') default → rename for clarity
  - concat resets column alignment; use ignore_index=True for clean index
  - combine_first: takes values from caller, fills NaN from argument
"""


# ╔════════════════════════════════════════════════════════════════════════╗
# ║  PART C: ADVANCED PATTERNS & STRING/DATETIME                         ║
# ╚════════════════════════════════════════════════════════════════════════╝


# ════════════════════════════════════════════════════════════════════════
# C1. STRING OPERATIONS
# ════════════════════════════════════════════════════════════════════════
"""
┌──────────────────────────┬──────────────────────────────────────────────┐
│ Pattern                  │ Syntax                                        │
├──────────────────────────┼──────────────────────────────────────────────┤
│ Lowercase / Uppercase    │ df['c'].str.lower() / .str.upper()           │
│ Strip whitespace         │ df['c'].str.strip() / .lstrip() / .rstrip() │
│ Contains                 │ df['c'].str.contains('pat', na=False)        │
│ Starts/Ends with         │ df['c'].str.startswith('X')                  │
│ Split                    │ df['c'].str.split('_', expand=True)          │
│ Get nth element          │ df['c'].str.split('_').str[0]                │
│ Replace                  │ df['c'].str.replace('old', 'new', regex=F)   │
│ Regex extract            │ df['c'].str.extract(r'(\d+)')                │
│ Regex extract all        │ df['c'].str.extractall(r'(\d+)')             │
│ Length                   │ df['c'].str.len()                            │
│ Pad                      │ df['c'].str.pad(5, fillchar='0')             │
│ Zfill                    │ df['c'].str.zfill(5)                         │
│ Count occurrences        │ df['c'].str.count('pattern')                 │
│ Concatenate strings      │ df['c'].str.cat(sep=', ')                    │
│ Slice                    │ df['c'].str[0:5]                             │
│ Title case               │ df['c'].str.title()                          │
│ Find position            │ df['c'].str.find('sub')  # -1 if not found  │
└──────────────────────────┴──────────────────────────────────────────────┘

GOTCHAS:
  - All .str methods return NaN for NaN values
  - str.contains uses regex by default → regex=False for literal
  - str.replace also uses regex by default → regex=False for literal
  - str.extract needs a capture group () in the pattern
  - str.split(expand=True) returns DataFrame, False returns lists
"""


# ════════════════════════════════════════════════════════════════════════
# C2. DATETIME OPERATIONS
# ════════════════════════════════════════════════════════════════════════
"""
┌──────────────────────────┬──────────────────────────────────────────────┐
│ Pattern                  │ Syntax                                        │
├──────────────────────────┼──────────────────────────────────────────────┤
│ Parse to datetime        │ pd.to_datetime(df['col'])                    │
│ Custom format            │ pd.to_datetime(df['c'], format='%Y-%m-%d')   │
│ Year / Month / Day       │ df['d'].dt.year / .dt.month / .dt.day       │
│ Day of week (0=Mon)      │ df['d'].dt.dayofweek                        │
│ Day name                 │ df['d'].dt.day_name()                       │
│ Hour / Minute / Second   │ df['d'].dt.hour / .dt.minute                │
│ Quarter                  │ df['d'].dt.quarter                          │
│ Week of year             │ df['d'].dt.isocalendar().week                │
│ Days between             │ (df['d2'] - df['d1']).dt.days               │
│ Add timedelta            │ df['d'] + pd.Timedelta(days=7)              │
│ Date floor/ceil          │ df['d'].dt.floor('D') / .dt.ceil('H')      │
│ To period                │ df['d'].dt.to_period('M')  # monthly period │
│ Date range               │ pd.date_range('2024-01-01', periods=12,      │
│                          │   freq='MS')  # month start                 │
│ Resample (time-series)   │ df.set_index('d').resample('M').sum()       │
│ Rolling on time          │ df.set_index('d').rolling('7D').mean()      │
└──────────────────────────┴──────────────────────────────────────────────┘

COMMON FREQ STRINGS:
  'D'  → day          'B'  → business day    'W'  → week (Sunday)
  'MS' → month start  'M'  → month end       'QS' → quarter start
  'YS' → year start   'H'  → hour            'min' → minute

RESAMPLE vs GROUPBY:
  resample → for datetime index, time-aware (handles gaps, alignment)
  groupby  → for non-time grouping or when index is not datetime

  # Monthly sales totals (time-series)
  df.set_index('date').resample('M')['amount'].sum()

  # Same thing with groupby (less elegant)
  df.groupby(df['date'].dt.to_period('M'))['amount'].sum()

GOTCHAS:
  - to_datetime with errors='coerce' turns unparseable dates to NaT
  - dt accessor only works on datetime columns (not object/string)
  - resample requires DatetimeIndex → set_index('date') first
  - Timedelta arithmetic: datetime - datetime = timedelta
"""


# ════════════════════════════════════════════════════════════════════════
# C3. APPLY, MAP & VECTORIZATION
# ════════════════════════════════════════════════════════════════════════
"""
┌──────────────────────────┬──────────────────────────────────────────────┐
│ Pattern                  │ Syntax                                        │
├──────────────────────────┼──────────────────────────────────────────────┤
│ Element-wise (Series)    │ df['col'].apply(func)                        │
│ Row-wise (DataFrame)     │ df.apply(func, axis=1)                       │
│ Cell-wise (DataFrame)    │ df.map(func)          # pandas >= 2.1        │
│ Map with dict            │ df['col'].map({'a': 1, 'b': 2})             │
│ Map with Series          │ df['col'].map(lookup_series)                 │
│ Vectorized string        │ df['col'].str.upper()                        │
│ Vectorized numeric       │ df['col'] * 2 + df['col2']                  │
│ Vectorized conditional   │ np.where(cond, true_val, false_val)          │
│ Pipe (chain functions)   │ df.pipe(func1).pipe(func2, arg=val)         │
└──────────────────────────┴──────────────────────────────────────────────┘

PERFORMANCE HIERARCHY (fastest → slowest):
  1. Vectorized operations (numpy/pandas)    ← ALWAYS prefer
  2. .str / .dt accessor methods             ← good for string/date
  3. .apply() with simple function           ← OK for complex logic
  4. .itertuples()                           ← when apply won't work
  5. .iterrows()                             ← AVOID (very slow)

  Rule of thumb: if you can express it without apply, do it.
  apply is 10-100x slower than vectorized operations.

INTERVIEW TIP:
  If asked "how would you optimize this?" and you see iterrows/apply,
  the answer is almost always: replace with vectorized operations.
"""


# ════════════════════════════════════════════════════════════════════════
# C4. METHOD CHAINING & PIPE
# ════════════════════════════════════════════════════════════════════════
"""
Method chaining produces clean, readable data pipelines:

  result = (
      df
      .query('age > 25')
      .assign(
          salary_k = lambda x: x['salary'] / 1000,
          tax      = lambda x: x['salary'] * 0.3
      )
      .groupby('department')
      .agg(
          avg_salary = ('salary_k', 'mean'),
          headcount  = ('emp_id', 'count')
      )
      .sort_values('avg_salary', ascending=False)
      .reset_index()
      .rename(columns={'avg_salary': 'avg_salary_k'})
  )

CHAINABLE METHODS:
  .query()          .assign()         .sort_values()
  .rename()         .reset_index()    .set_index()
  .drop()           .dropna()         .fillna()
  .astype()         .pipe()           .groupby().agg()
  .merge()          .melt()           .explode()

NON-CHAINABLE (return non-DataFrame):
  .describe()   .info()   .value_counts()   .corr()
  → use these at the END of a chain

PIPE for custom functions in chains:
  def remove_outliers(df, col, n_std=3):
      return df[np.abs(df[col] - df[col].mean()) <= n_std * df[col].std()]

  result = df.pipe(remove_outliers, col='salary', n_std=2)
"""


# ╔════════════════════════════════════════════════════════════════════════╗
# ║  PART D: INTERVIEW DECISION TREE & QUICK REFERENCE                   ║
# ╚════════════════════════════════════════════════════════════════════════╝

"""
┌──────────────────────────────────────────────────────────────────────────┐
│                     INTERVIEW DECISION TREE                              │
│                  "What Pandas method do I use?"                           │
└──────────────────────────────────────────────────────────────────────────┘

  Q: "Per group, compute X"
     → groupby('g').agg(...)

  Q: "Add a column showing group-level stat for each row"
     → groupby('g')['col'].transform('stat')     # NOT agg

  Q: "Keep only groups where condition"
     → groupby('g').filter(lambda x: ...)

  Q: "Rank within group"
     → groupby('g')['col'].rank(method='dense')

  Q: "Running/moving calculation"
     → SORT first, then .rolling() or .expanding()

  Q: "Previous/next row value"
     → .shift(1) / .shift(-1)

  Q: "Wide to long"
     → pd.melt()

  Q: "Long to wide"
     → pd.pivot_table() or .unstack()

  Q: "Rows not in another table"
     → Anti-join: df[~df['key'].isin(other['key'])]

  Q: "Weighted average"
     → np.average(values, weights=weights)

  Q: "Bin into categories"
     → Equal frequency: pd.qcut()  |  Equal width: pd.cut()

  Q: "Consecutive events / streaks"
     → Boolean mask + cumsum trick for streak IDs

  Q: "Monthly/weekly aggregation on time series"
     → .set_index('date').resample('M').sum()

  Q: "Remove duplicates keeping best row"
     → sort_values + drop_duplicates(keep='first')

  Q: "Fill NaN with group mean"
     → groupby('g')['col'].transform(lambda x: x.fillna(x.mean()))

  Q: "One-hot encode categorical"
     → pd.get_dummies(df, columns=['col'])

  Q: "Split string column into multiple columns"
     → df['col'].str.split('_', expand=True)


┌──────────────────────────────────────────────────────────────────────────┐
│                   COMMON INTERVIEW QUESTION PATTERNS                     │
└──────────────────────────────────────────────────────────────────────────┘

  1. "Find the second highest salary per department"
     → groupby + rank(method='dense') + filter rank == 2

  2. "Find employees earning more than dept average"
     → transform('mean') then filter df[df['sal'] > df['dept_avg']]

  3. "Calculate month-over-month growth"
     → sort + groupby + shift + (current - prev) / prev

  4. "Find the most recent record per user"
     → sort_values('date').drop_duplicates('user', keep='last')
     → OR groupby('user')['date'].idxmax() + .loc[]

  5. "Detect gaps in sequential data"
     → diff() and find where diff > expected interval

  6. "Running total partitioned by category"
     → sort + groupby('cat').cumsum()

  7. "Compare each row to group median"
     → transform('median') then subtract

  8. "Combine overlapping date ranges"
     → sort + shift + cummax to detect overlaps + groupby to merge

  9. "Find top N per group with ties"
     → groupby + rank + filter <= N

  10. "Pivot report: rows=month, columns=category, values=sum"
      → pivot_table(values='amt', index='month', columns='cat', aggfunc='sum')
"""


# ════════════════════════════════════════════════════════════════════════
# RUNNABLE DEMO — all concepts in action
# ════════════════════════════════════════════════════════════════════════

def cheatsheet_demo():
    """Run this to see all major patterns in action."""
    np.random.seed(42)
    df = pd.DataFrame({
        'dept': ['A','A','A','B','B','B'],
        'name': ['Alice','Bob','Carol','Dave','Eve','Frank'],
        'salary': [90, 80, 70, 85, 95, 75],
        'score': [4.5, 3.8, 4.2, 3.9, 4.7, 3.5],
        'date': pd.to_datetime(['2023-01-15','2023-03-20','2023-06-10',
                                '2023-02-05','2023-04-18','2023-07-22'])
    })

    print("=" * 60)
    print("  Pandas Cheatsheet — Live Demo")
    print("=" * 60)

    print("\nOriginal DataFrame:")
    print(df, "\n")

    # A. BASICS
    print("─" * 60)
    print("A. BASICS")
    print("─" * 60)

    print("\n1. Shape & Types:")
    print(f"   Shape: {df.shape}, Dtypes: {dict(df.dtypes)}")

    print("\n2. Selecting columns:")
    print(df[['name', 'salary']].head(3))

    print("\n3. loc vs iloc:")
    print(f"   loc[0, 'name'] = {df.loc[0, 'name']}")
    print(f"   iloc[0, 1]     = {df.iloc[0, 1]}")

    print("\n4. Adding a column:")
    df['bonus'] = df['salary'] * 0.1
    print(df[['name', 'salary', 'bonus']].head(3))

    print("\n5. Sort by salary descending:")
    print(df.sort_values('salary', ascending=False)[['name', 'salary']].head(3))

    print("\n6. Value counts:")
    print(df['dept'].value_counts())

    # B. FILTERING
    print("\n" + "─" * 60)
    print("B. FILTERING")
    print("─" * 60)

    print("\n7. Filter salary > 80:")
    print(df[df['salary'] > 80][['name', 'salary']])

    print("\n8. np.where (conditional column):")
    df['level'] = np.where(df['salary'] >= 85, 'Senior', 'Junior')
    print(df[['name', 'salary', 'level']])

    # C. GROUPBY
    print("\n" + "─" * 60)
    print("C. GROUPBY & AGGREGATION")
    print("─" * 60)

    print("\n9. GroupBy agg:")
    print(df.groupby('dept').agg(avg_sal=('salary', 'mean'), count=('name', 'count')))

    print("\n10. Transform (broadcast dept mean):")
    df['dept_avg'] = df.groupby('dept')['salary'].transform('mean')
    print(df[['name', 'dept', 'salary', 'dept_avg']])

    print("\n11. Rank within group:")
    df['rank'] = df.groupby('dept')['salary'].rank(ascending=False, method='dense').astype(int)
    print(df[['name', 'dept', 'salary', 'rank']])

    # D. WINDOW FUNCTIONS
    print("\n" + "─" * 60)
    print("D. WINDOW FUNCTIONS")
    print("─" * 60)

    df_sorted = df.sort_values(['dept', 'date'])

    print("\n12. Shift (lag):")
    df_sorted['prev_sal'] = df_sorted.groupby('dept')['salary'].shift(1)
    print(df_sorted[['name', 'dept', 'salary', 'prev_sal']])

    print("\n13. Rolling 2-row mean:")
    df_sorted['rolling_2'] = df_sorted.groupby('dept')['salary'].transform(
        lambda x: x.rolling(2, min_periods=1).mean()
    )
    print(df_sorted[['name', 'dept', 'salary', 'rolling_2']])

    # E. PIVOT & RESHAPE
    print("\n" + "─" * 60)
    print("E. PIVOT & RESHAPE")
    print("─" * 60)

    sales = pd.DataFrame({
        'region': ['E','E','W','W','E','W'],
        'product': ['X','Y','X','Y','X','Y'],
        'amount': [100, 200, 150, 250, 120, 180]
    })

    print("\n14. Pivot table:")
    print(pd.pivot_table(sales, values='amount', index='region', columns='product', aggfunc='sum'))

    print("\n15. Melt (wide→long):")
    wide = pd.DataFrame({'id': [1, 2], 'Q1': [10, 20], 'Q2': [30, 40]})
    print(pd.melt(wide, id_vars='id', var_name='quarter', value_name='sales'))

    # F. STATISTICS
    print("\n" + "─" * 60)
    print("F. STATISTICS")
    print("─" * 60)

    print("\n16. Quantile binning:")
    df['sal_tier'] = pd.qcut(df['salary'], q=3, labels=['Low', 'Mid', 'High'])
    print(df[['name', 'salary', 'sal_tier']])

    print("\n17. Correlation:")
    print(df[['salary', 'score', 'bonus']].corr().round(2))

    # G. MERGING
    print("\n" + "─" * 60)
    print("G. MERGING")
    print("─" * 60)

    sellers = pd.DataFrame({'emp_id': [1, 3]})
    all_emp = pd.DataFrame({'emp_id': [1, 2, 3, 4], 'name': ['A', 'B', 'C', 'D']})

    print("\n18. Anti-join (employees with no sales):")
    print(all_emp[~all_emp['emp_id'].isin(sellers['emp_id'])])

    print("\n19. Left join:")
    extra = pd.DataFrame({'emp_id': [1, 3], 'total_sales': [5000, 3000]})
    print(pd.merge(all_emp, extra, on='emp_id', how='left').fillna(0))

    # H. STRING & DATETIME
    print("\n" + "─" * 60)
    print("H. STRING & DATETIME")
    print("─" * 60)

    print("\n20. String operations:")
    print(df['name'].str.upper().head(3))

    print("\n21. DateTime extraction:")
    df_sorted['month'] = df_sorted['date'].dt.month
    df_sorted['day_name'] = df_sorted['date'].dt.day_name()
    print(df_sorted[['name', 'date', 'month', 'day_name']])

    # I. MISSING DATA
    print("\n" + "─" * 60)
    print("I. MISSING DATA")
    print("─" * 60)

    df_na = pd.DataFrame({'a': [1, np.nan, 3, np.nan], 'b': [10, 20, np.nan, 40]})
    print("\n22. Original with NaN:")
    print(df_na)
    print(f"\n    NaN counts: {dict(df_na.isna().sum())}")
    print(f"    After fillna(0):\n{df_na.fillna(0)}")
    print(f"    After ffill:\n{df_na.ffill()}")

    print("\n" + "=" * 60)
    print("  Done! Use these patterns as building blocks.")
    print("=" * 60)


if __name__ == '__main__':
    cheatsheet_demo()
