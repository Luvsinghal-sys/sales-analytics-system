import sys
# Make sure we can find the utils folder
sys.path.append('utils')

from utils.file_handler import read_sales_data, parse_transactions, validate_and_filter
from utils.data_processor import generate_sales_report
from utils.api_handler import fetch_all_products, create_product_mapping, enrich_sales_data

def main():
    print("=========================================")
    print("        SALES ANALYTICS SYSTEM          ")
    print("=========================================\n")

    try:
        # 1. Read Data
        print("[1/10] Reading sales data...")
        raw_lines = read_sales_data('data/sales_data.txt')
        if not raw_lines: return
        print(f"✓ Successfully read {len(raw_lines)} lines")

        # 2. Parse and Clean
        print("\n[2/10] Parsing and cleaning data...")
        parsed_data = parse_transactions(raw_lines)
        print(f"✓ Parsed {len(parsed_data)} records")

        # 3. Filter Options (Ask User)
        print("\n[3/10] Filter Options Available:")
        print("Regions: North, South, East, West")
        
        do_filter = input("Do you want to filter data? (y/n): ").lower()
        region_choice = None
        if do_filter == 'y':
            region_choice = input("Enter region: ")

        # 4. Validate and Filter
        print("\n[4/10] Validating transactions...")
        clean_data, inv_count, summary = validate_and_filter(parsed_data, region=region_choice)
        print(f"✓ Valid: {len(clean_data)} | Invalid: {inv_count}")

        # 5. Analysis (Implicit in Report Generation)
        print("\n[5/10] Analyzing sales data...")
        print("✓ Analysis complete")

        # 6. API Integration
        print("\n[6/10] Fetching product data from API...")
        api_prods = fetch_all_products()
        print(f"✓ Fetched {len(api_prods)} products")
        mapping = create_product_mapping(api_prods)

        # 7. Enrich Data
        print("\n[7/10] Enriching sales data...")
        enriched = enrich_sales_data(clean_data, mapping)

        # 8. Save Enriched Data (Handled inside enrich_sales_data)
        print("\n[8/10] Saving enriched data...")

        # 9. Generate Report
        print("\n[9/10] Generating report...")
        generate_sales_report(clean_data, enriched)

        print("\n[10/10] Process Complete!")
        print("=========================================")

    except Exception as e:
        print(f"\nCRITICAL ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()