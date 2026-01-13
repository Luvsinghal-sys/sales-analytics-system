import requests

def fetch_all_products():
    """Fetches all products from DummyJSON API"""
    url = "https://dummyjson.com/products?limit=100"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        print("✓ Successfully fetched product data from API")
        return data.get('products', [])
    except Exception as e:
        print(f"✗ API Connection Error: {e}")
        return []

def create_product_mapping(api_products):
    """Creates a mapping of product IDs to info"""
    mapping = {}
    for prod in api_products:
        mapping[prod['id']] = {
            'title': prod.get('title'),
            'category': prod.get('category'),
            'brand': prod.get('brand'),
            'rating': prod.get('rating')
        }
    return mapping

def enrich_sales_data(transactions, product_mapping):
    """Enriches transaction data with API info"""
    enriched = []
    for t in transactions:
        # Logic to extract numeric ID (P101 -> 101)
        try:
            numeric_id = int(''.join(filter(str.isdigit, t['ProductID'])))
        except ValueError:
            numeric_id = None
            
        t_copy = t.copy() # Create a copy to handle updates safely
        if numeric_id in product_mapping:
            info = product_mapping[numeric_id]
            t_copy.update({
                'API_Category': info['category'],
                'API_Brand': info['brand'],
                'API_Rating': info['rating'],
                'API_Match': True
            })
        else:
            t_copy.update({
                'API_Category': None,
                'API_Brand': None,
                'API_Rating': None,
                'API_Match': False
            })
        enriched.append(t_copy)
    
    save_enriched_data(enriched)
    return enriched

def save_enriched_data(enriched_transactions, filename='data/enriched_sales_data.txt'):
    """Saves enriched transactions back to file"""
    header = "TransactionID|Date|ProductID|ProductName|Quantity|UnitPrice|CustomerID|Region|API_Category|API_Brand|API_Rating|API_Match"
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(header + "\n")
            for t in enriched_transactions:
                line = f"{t['TransactionID']}|{t['Date']}|{t['ProductID']}|{t['ProductName']}|{t['Quantity']}|{t['UnitPrice']}|{t['CustomerID']}|{t['Region']}|{t['API_Category']}|{t['API_Brand']}|{t['API_Rating']}|{t['API_Match']}"
                f.write(line + "\n")
        print(f"✓ Enriched data saved to: {filename}")
    except Exception as e:
        print(f"Error saving enriched data: {e}")
