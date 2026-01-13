from datetime import datetime

# --- PART 2 FUNCTIONS ---

def calculate_total_revenue(transactions):
    return sum(t['Quantity'] * t['UnitPrice'] for t in transactions)

def region_wise_sales(transactions):
    regions = {}
    total_rev = calculate_total_revenue(transactions)
    for t in transactions:
        reg = t['Region']
        rev = t['Quantity'] * t['UnitPrice']
        if reg not in regions:
            regions[reg] = {'total_sales': 0.0, 'transaction_count': 0}
        regions[reg]['total_sales'] += rev
        regions[reg]['transaction_count'] += 1
    for reg in regions:
        regions[reg]['percentage'] = round((regions[reg]['total_sales'] / total_rev) * 100, 2)
    return dict(sorted(regions.items(), key=lambda x: x[1]['total_sales'], reverse=True))

def daily_sales_trend(transactions):
    days = {}
    for t in transactions:
        date = t['Date']
        if date not in days:
            days[date] = {'revenue': 0.0, 'transaction_count': 0, 'customers': set()}
        days[date]['revenue'] += t['Quantity'] * t['UnitPrice']
        days[date]['transaction_count'] += 1
        days[date]['customers'].add(t['CustomerID'])
    result = {}
    for date in sorted(days.keys()):
        result[date] = {
            'revenue': days[date]['revenue'],
            'transaction_count': days[date]['transaction_count'],
            'unique_customers': len(days[date]['customers'])
        }
    return result

def find_peak_sales_day(transactions):
    trend = daily_sales_trend(transactions)
    if not trend: return None
    peak_date = max(trend, key=lambda k: trend[k]['revenue'])
    return (peak_date, trend[peak_date]['revenue'], trend[peak_date]['transaction_count'])

def low_performing_products(transactions, threshold=10):
    products = {}
    for t in transactions:
        name = t['ProductName']
        if name not in products: products[name] = {'qty': 0, 'rev': 0.0}
        products[name]['qty'] += t['Quantity']
        products[name]['rev'] += t['Quantity'] * t['UnitPrice']
    low = [(n, d['qty'], d['rev']) for n, d in products.items() if d['qty'] < threshold]
    return sorted(low, key=lambda x: x[1])

def top_selling_products(transactions, n=5):
    products = {}
    for t in transactions:
        name = t['ProductName']
        if name not in products: products[name] = {'qty': 0, 'rev': 0.0}
        products[name]['qty'] += t['Quantity']
        products[name]['rev'] += t['Quantity'] * t['UnitPrice']
    sorted_p = sorted(products.items(), key=lambda x: x[1]['qty'], reverse=True)
    return [(k, v['qty'], v['rev']) for k, v in sorted_p[:n]]

def customer_analysis(transactions):
    customers = {}
    for t in transactions:
        cid = t['CustomerID']
        rev = t['Quantity'] * t['UnitPrice']
        if cid not in customers: customers[cid] = {'total_spent': 0.0, 'purchases': 0, 'items': set()}
        customers[cid]['total_spent'] += rev
        customers[cid]['purchases'] += 1
        customers[cid]['items'].add(t['ProductName'])
    result = {}
    for cid, data in customers.items():
        result[cid] = {
            'total_spent': round(data['total_spent'], 2),
            'purchase_count': data['purchases'],
            'avg_order_value': round(data['total_spent'] / data['purchases'], 2),
            'products_bought': list(data['items'])
        }
    return dict(sorted(result.items(), key=lambda x: x[1]['total_spent'], reverse=True))

# --- PART 4 REPORT GENERATION ---
def generate_sales_report(transactions, enriched_transactions, output_file='output/sales_report.txt'):
    total_rev = calculate_total_revenue(transactions)
    count = len(transactions)
    match_count = sum(1 for t in enriched_transactions if t.get('API_Match'))
    
    report = f"""=========================================
          SALES ANALYTICS REPORT
=========================================
Total Revenue:      ${total_rev:,.2f}
Total Transactions: {count}
API Success Rate:   {(match_count/count*100):.1f}%
=========================================
"""
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"✓ Report saved to: {output_file}")
    except Exception as e:
        print(f"Error generating report: {e}")
