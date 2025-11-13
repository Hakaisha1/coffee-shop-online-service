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

class InventoryReport(Report):
    def __init__(self):
        super().__init__("Laporan Inventaris")

class CustomerReport(Report):
    def __init__(self):
        super().__init__("Laporan Pelanggan")

class EmployeeReport(Report):
    def __init__(self):
        super().__init__("Laporan Karyawan")

class ReportManager:
    pass