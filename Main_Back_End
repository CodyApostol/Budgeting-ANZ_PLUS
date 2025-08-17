from parser import parse_statement
from frequency import frequency_count_avg
from frequency import frequency_count
import pandas as pd

statements = [
]

num_months = len(statements)
dfs = []

for statement in statements:
    dfs.append(parse_statement(statement))

df = pd.concat(dfs, ignore_index=True)

store_stats_avg = frequency_count_avg(df, num_months)
store_stats_avg.to_csv("store_frequency_avg_amt.csv", index=False)

total_store_stats = frequency_count(df)
total_store_stats.to_csv("store_frequency_amt.csv", index=False)



print(total_store_stats)
print(store_stats_avg)



