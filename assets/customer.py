import json
import os

class MenuItem:
    def __init__(self, nama, harga):
        self.nama = nama
        self.harga = harga

    def __str__(self):
        return f"{self.nama} - Rp{self.harga:,}"


class Pesanan:
    def __init__(self, customer):
        self.customer = customer
        self.daftar_pesanan = []
        self.total = 0

    def tambah_item(self, item, jumlah):
        subtotal = item.harga * jumlah
        self.daftar_pesanan.append((item, jumlah, subtotal))
        self.total += subtotal

    def tampilkan_pesanan(self):
        print("\n=== Detail Pesanan ===")
        for item, jumlah, subtotal in self.daftar_pesanan:
            print(f"{item.nama} (x{jumlah}) = Rp{subtotal:,}")
        print(f"Total: Rp{self.total:,}")

    def hitung_total(self):
        return self.total


class Pembayaran:
    def __init__(self, pesanan):
        self.pesanan = pesanan

    def proses_pembayaran(self):
        total = self.pesanan.hitung_total()
        while True:
            try:
                bayar = int(input(f"Total tagihan Rp{total:,}. Masukkan jumlah bayar: Rp"))
                if bayar < total:
                    print("Uang tidak cukup. Silakan bayar sesuai total.")
                else:
                    print(f"Pembayaran berhasil! Kembalian Anda: Rp{bayar-total:,}")
                    return True
            except ValueError:
                print("Masukkan angka yang valid.")


class Customer:
    def __init__(self, nama):
        self.nama = nama
        self.file_json = "customer.json"  # DIGANTI DI SINI
        self.riwayat = self.load_riwayat()

    # Load riwayat dari file JSON
    def load_riwayat(self):
        if not os.path.exists(self.file_json):
            return []

        with open(self.file_json, "r") as f:
            data = json.load(f)
            return data.get("riwayat", [])

    # Simpan ulang ke JSON
    def simpan_riwayat(self):
        with open(self.file_json, "w") as f:
            json.dump({"riwayat": self.riwayat}, f, indent=4)

    # Tambahkan transaksi baru ke JSON
    def simpan_transaksi(self, daftar_pesanan, total):
        transaksi = {
            "customer": self.nama,
            "pesanan": [
                {
                    "menu": item.nama,
                    "jumlah": jumlah,
                    "subtotal": subtotal
                }
                for item, jumlah, subtotal in daftar_pesanan
            ],
            "total": total
        }

        self.riwayat.append(transaksi)
        self.simpan_riwayat()

    # Tampilkan riwayat transaksi
    def lihat_riwayat(self):
        data = [r for r in self.riwayat if r["customer"] == self.nama]

        print("\n=== Riwayat Pesanan Anda ===")
        if not data:
            print("Belum ada riwayat pesanan.")
            return

        for i, transaksi in enumerate(data, 1):
            print(f"\nTransaksi {i}: Total Rp{transaksi['total']:,}")
            for item in transaksi["pesanan"]:
                print(f" - {item['menu']} x{item['jumlah']} = Rp{item['subtotal']:,}")

    # Cetak struk setelah pembayaran
    def cetak_struk(self, daftar_pesanan, total):
        print("\n===================================")
        print("        STRUK")
        print("===================================")
        print(f"Customer : {self.nama}")

        print("\nPesanan:")
        for item, jumlah, subtotal in daftar_pesanan:
            print(f"- {item.nama} x{jumlah} = Rp{subtotal:,}")

        print("\n---------------------------------")
        print(f"TOTAL = Rp{total:,}")
        print("-----------------------------------")
        print("Terima kasih telah berkunjung!")
        print("===================================\n")

    # Proses membuat pesanan
    def buat_pesanan(self, daftar_menu):
        pesanan = Pesanan(self)

        print(f"\nSelamat datang, {self.nama}!")
        print("=== Menu Restoran ===")
        for i, item in enumerate(daftar_menu, 1):
            print(f"{i}. {item}")

        while True:
            try:
                pilih = int(input("\nPilih menu (nomor, 0 untuk selesai): "))
                if pilih == 0:
                    break
                if 1 <= pilih <= len(daftar_menu):
                    jumlah = int(input("Jumlah: "))
                    pesanan.tambah_item(daftar_menu[pilih - 1], jumlah)
                    print("Item ditambahkan!")
                else:
                    print("Menu tidak valid.")
            except ValueError:
                print("Masukkan angka yang valid.")

        if pesanan.daftar_pesanan:
            pesanan.tampilkan_pesanan()
            bayar = Pembayaran(pesanan)
            if bayar.proses_pembayaran():
                self.cetak_struk(pesanan.daftar_pesanan, pesanan.total)
                self.simpan_transaksi(pesanan.daftar_pesanan, pesanan.total)
        else:
            print("Tidak ada pesanan dibuat.")


if __name__ == "__main__":
    daftar_menu = [
        MenuItem("Espresso", 20000),
        MenuItem("Ice Cafe Latte", 25000),
        MenuItem("Cappucino", 23000),
        MenuItem("Matcha Latte", 27500),
        MenuItem("Butterscotch Coffee", 32000)
    ]

    nama = input("Masukkan nama customer: ")
    pelanggan = Customer(nama)

    print("\n1. Buat Pesanan")
    print("2. Lihat Riwayat Pesanan")
    pilihan = input("Pilih menu: ")

    if pilihan == "1":
        pelanggan.buat_pesanan(daftar_menu)
    elif pilihan == "2":
        pelanggan.lihat_riwayat()
    else:
        print("Pilihan tidak valid.")
