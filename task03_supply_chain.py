import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from datetime import datetime

# 1. SETUP
script_dir = os.path.dirname(__file__)

def run_supply_chain_pipeline():
    # Try to find the file regardless of extension
    possible_files = ['supply_chain_data.xlsx', 'supply_chain_data.csv']
    file_path = None
    
    for f in possible_files:
        if os.path.exists(os.path.join(script_dir, f)):
            file_path = os.path.join(script_dir, f)
            break
            
    if not file_path:
        print(f"❌ Error: Could not find supply_chain_data file in {script_dir}")
        print("Please ensure the file is in the folder and named correctly.")
        return

    try:
        # 2. INGESTION BASED ON EXTENSION
        if file_path.endswith('.xlsx'):
            df = pd.read_excel(file_path)
        else:
            df = pd.read_csv(file_path, encoding='unicode_escape')
            
        df.columns = df.columns.str.strip().str.replace(' ', '_').str.lower()
        print(f"🚀 Ingested: {os.path.basename(file_path)}")

        # 3. OPERATIONAL KPIs
        # Delivery Efficiency = Lead Time vs Shipping Cost
        df['efficiency_score'] = df['lead_times'] / df['shipping_costs']
        
        # Identify High-Risk Suppliers (Defect rates above average)
        avg_defect = df['defect_rates'].mean()
        df['high_risk_supplier'] = df['defect_rates'] > avg_defect

        # 4. DASHBOARD VISUALIZATION
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        plt.subplots_adjust(hspace=0.4)

        # Plot 1: Lead Times (Bottleneck Identification)
        sns.barplot(x='lead_times', y='product_type', data=df, ax=axes[0, 0], palette='viridis')
        axes[0, 0].set_title('Product Lead Times (Supply Chain Speed)', fontweight='bold')

        # Plot 2: Cost Analysis
        sns.scatterplot(x='shipping_costs', y='lead_times', hue='shipping_carriers', data=df, ax=axes[0, 1])
        axes[0, 1].set_title('Logistics: Cost vs. Lead Time', fontweight='bold')

        # Plot 3: Supplier Risk (Defect Rates)
        sns.boxplot(x='defect_rates', y='supplier_name', data=df, ax=axes[1, 0], palette='magma')
        axes[1, 0].set_title('Supplier Quality Analysis', fontweight='bold')

        # Plot 4: Revenue vs Stock Levels
        sns.lineplot(x='stock_levels', y='revenue_generated', data=df, ax=axes[1, 1], color='red')
        axes[1, 1].set_title('Inventory: Stock Levels vs. Revenue', fontweight='bold')

        plt.suptitle("SUPPLY CHAIN & OPERATIONS ANALYTICS DASHBOARD", fontsize=20, fontweight='bold', y=0.95)

        # 5. REPORT EXPORT
        report_path = os.path.join(script_dir, 'Supply_Chain_Analysis_Report.txt')
        with open(report_path, 'w') as f:
            f.write("--- SUPPLY CHAIN FINAL REPORT ---\n")
            f.write(f"Average Defect Rate: {avg_defect:.2f}%\n")
            f.write(f"Most Efficient Carrier: {df.groupby('shipping_carriers')['efficiency_score'].mean().idxmin()}\n")
            f.write(f"Top Revenue Location: {df.groupby('location')['revenue_generated'].sum().idxmax()}\n")
        
        print(f"✅ Level 6 Task 3 Complete. Report: {report_path}")
        plt.show()

    except Exception as e:
        print(f"❌ Pipeline Failed: {e}")

if __name__ == "__main__":
    run_supply_chain_pipeline()