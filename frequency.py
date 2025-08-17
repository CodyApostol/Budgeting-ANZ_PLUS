import pandas as pd
import math

def frequency_count_avg(spendings, num_months):
    store_stats = {}
    count_sum = 0
    total_spent = 0.0

    for _, row in spendings.iterrows():
        store = row['Store']
        amount = float(row['Spending'])

        if store in store_stats:
            store_stats[store]['count'] += 1
            store_stats[store]['total_spent'] += amount
        else:
            store_stats[store] = {'count': 1, 'total_spent': amount}

        count_sum += 1
        total_spent += amount

    # Sort by total spent (descending)
    store_stats = dict(sorted(store_stats.items(), key=lambda x: x[1]['total_spent'], reverse=True))
    
    data = []
    outlier_count = 0
    outlier_total = 0.0

    for store, stats in store_stats.items():
        count_avg = stats['count'] / num_months
        total_spent_avg = stats['total_spent'] / num_months

        count_ceil = math.ceil(count_avg)
        total_spent_ceil = math.ceil(total_spent_avg * 100) / 100

        if count_ceil == 1:
            # Collect as outlier
            outlier_count += count_ceil
            outlier_total += total_spent_ceil
        else:
            data.append({
                'Store': store,
                'Count (avg/month)': count_ceil,
                'Avg Spent ($)': total_spent_ceil
            })

    # Add Outliers row if any
    if outlier_count > 0:
        data.append({
            'Store': 'Outliers',
            'Count (avg/month)': outlier_count,
            'Avg Spent ($)': round(outlier_total, 2)
        })

    # Add TOTAL row
    data.append({
        'Store': 'TOTAL',
        'Count (avg/month)': math.ceil(count_sum / num_months),
        'Avg Spent ($)': math.ceil((total_spent / num_months) * 100) / 100
    })
    
    df = pd.DataFrame(data)
    return df


import pandas as pd

def frequency_count(spendings):
    store_stats = {}
    count_sum = 0
    total_spent = 0.0

    for _, row in spendings.iterrows():
        store = row['Store']
        amount = float(row['Spending'])

        if store in store_stats:
            store_stats[store]['count'] += 1
            store_stats[store]['total_spent'] += amount
        else:
            store_stats[store] = {'count': 1, 'total_spent': amount}

        # Increment overall totals
        count_sum += 1
        total_spent += amount

    # Sort by count (descending)
    store_stats = dict(sorted(store_stats.items(), key=lambda x: x[1]['total_spent'], reverse=True))
    
    # Convert to DataFrame
    data = []
    for store, stats in store_stats.items():
        data.append({
            'Store': store,
            'Count': stats['count'],
            'Total Spent ($)': round(stats['total_spent'], 2)
        })
        
    # Add totals row
    data.append({
        'Store': 'TOTAL',
        'Count': count_sum,
        'Total Spent ($)': round(total_spent, 2)
    })

    df = pd.DataFrame(data)
    return df
