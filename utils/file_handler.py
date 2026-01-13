import os

def read_sales_data(filename):
    """Reads sales data from file handling encoding issues"""
    encodings = ['utf-8', 'latin-1', 'cp1252']
    lines = []
    
    if not os.path.exists(filename):
        print(f"Error: File {filename} not found.")
        return []

    for encoding in encodings:
        try:
            with open(filename, 'r', encoding=encoding) as file:
                # Skip the header row
                next(file) 
                for line in file:
                    clean_line = line.strip()
                    if clean_line:  # Remove empty lines
                        lines.append(clean_line)
                return lines
        except (UnicodeDecodeError, StopIteration):
            continue
    return []

def parse_transactions(raw_lines):
    """Parses raw lines into clean list of dictionaries"""
    transactions = []
    parsed_count = 0
    
    for line in raw_lines:
        parsed_count += 1
        parts = line.split('|')
        
        # Skip rows with incorrect number of fields (Expected 8)
        if len(parts) != 8:
            continue
            
        try:
            # Handle commas in ProductName and Numeric fields
            prod_name = parts[3].replace(',', '')
            qty_str = parts[4].replace(',', '')
            price_str = parts[5].replace(',', '')
            
            # Create dictionary and convert types
            transaction = {
                'TransactionID': parts[0].strip(),
                'Date': parts[1].strip(),
                'ProductID': parts[2].strip(),
                'ProductName': prod_name.strip(),
                'Quantity': int(qty_str),
                'UnitPrice': float(price_str),
                'CustomerID': parts[6].strip(),
                'Region': parts[7].strip()
            }
            transactions.append(transaction)
        except ValueError:
            continue
            
    return transactions

def validate_and_filter(transactions, region=None, min_amount=None, max_amount=None):
    """Validates transactions and applies optional filters"""
    valid_list = []
    invalid_count = 0
    
    # Validation Logic
    for t in transactions:
        is_valid = (
            t['Quantity'] > 0 and 
            t['UnitPrice'] > 0 and
            t['TransactionID'].startswith('T') and
            t['ProductID'].startswith('P') and
            t['CustomerID'].startswith('C')
        )
        
        if is_valid:
            # Apply Filters
            amount = t['Quantity'] * t['UnitPrice']
            if region and t['Region'] != region:
                continue
            if min_amount and amount < min_amount:
                continue
            if max_amount and amount > max_amount:
                continue
            valid_list.append(t)
        else:
            invalid_count += 1
            
    summary = {
        'total_input': len(transactions),
        'invalid': invalid_count,
        'final_count': len(valid_list)
    }
    
    return valid_list, invalid_count, summary
