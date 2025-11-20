# Kode bagian report
import json
from datetime import datetime
from typing import List, Dict
from collections import defaultdict

class DataLoader:
    def __init__(self, json_file: str="assets/database/data.json"):
        self.json_file = json_file
        self.data = {}

    def load_data(self) -> Dict:
        try:
            with open(self.json_file, 'r') as file:
                self.data = json.load(file)
            return self.data
        except FileNotFoundError:
            print(f"File {self.json_file} tidak bisa ditemukan.")
            return {}
        

class Report:
    def __init__(self, title:str):
        self.title = title
        self.report_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.content = {}
        self.data_loader = DataLoader()

    def generate(self):
        raise NotImplementedError("Subclasses harus mengimplementasikan metode generate().")
    
    def dictConverter(self):
        return {
            "title": self.title,
            "report_date": self.report_date,
            "content": self.content
        }

class SalesReport(Report):
    def __init__(self):
        super().__init__("Laporan Penjualan")
        self.total_sales = 0
        self.total_orders = 0

    def generate(self):
        print("Generating Sales Report")
        
        data = self.data_loader.load_data()
        transactions = data.get('transactions', [])
        
        if not transactions:
            self.content = {'message': 'Tidak ada data transaksi'}
            return self.content
        
        self.total_transactions = len(transactions)
        self.total_sales = sum(t.get('total_amount', 0) for t in transactions)
        

        product_count = defaultdict(lambda: {'quantity': 0, 'revenue': 0})
        for trans in transactions:
            for item in trans.get('items', []):
                product = item.get('product')
                qty = item.get('quantity', 0)
                price = item.get('price', 0)
                product_count[product]['quantity'] += qty
                product_count[product]['revenue'] += price * qty
        
        top_products = dict(sorted(
            product_count.items(), 
            key=lambda x: x[1]['quantity'], 
            reverse=True
        )[:5])
        
        avg_transaction = self.total_sales / self.total_transactions if self.total_transactions > 0 else 0
        
        self.content = {
            'total_penjualan': f"Rp {self.total_sales:,}",
            'total_transaksi': self.total_transactions,
            'rata_rata_per_transaksi': f"Rp {avg_transaction:,.0f}",
            'produk_terlaris': {
                name: {
                    'terjual': data['quantity'],
                    'pendapatan': f"Rp {data['revenue']:,}"
                } for name, data in top_products.items()
            }
        }
        
        print("Sales Report generated!")
        return self.content

        
class InventoryReport(Report):
    def __init__(self):
        super().__init__("Laporan Inventaris")
    
    def generate(self):
        print("Generating Inventory Report...")
        
        data = self.data_loader.load_data()
        products = data.get('products', [])
        
        if not products:
            self.content = {'message': 'Tidak ada data produk'}
            return self.content
        
        # Produk dengan stok menipis (< 10)
        low_stock = [p for p in products if p.get('stock', 0) < 10]
        
        # Total nilai inventaris
        total_inventory_value = sum(
            p.get('price', 0) * p.get('stock', 0) 
            for p in products
        )
        
        self.content = {
            'total_produk': len(products),
            'total_nilai_inventaris': f"Rp {total_inventory_value:,}",
            'produk_stok_menipis': len(low_stock),
            'detail_stok_menipis': low_stock,
            'semua_produk': products
        }
        
        print("Inventory Report generated!")
        return self.content

class CustomerReport(Report):
    def __init__(self):
        super().__init__("Laporan Pelanggan")

class EmployeeReport(Report):
    def __init__(self):
        super().__init__("Laporan Karyawan")

class ReportManager:
    pass