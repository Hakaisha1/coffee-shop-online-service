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


class Riwayat:
    def __init__(self, entries=None):
        # entries: list of dict (may be from existing JSON)
        self.entries = entries.copy() if entries else []

    def add_topup(self, customer, awal, jumlah, akhir):
        entry = {
            "jenis": "top up",
            "customer": customer,
            "saldo_awal": awal,
            "perubahan": jumlah,
            "saldo_akhir": akhir
        }
        self.entries.append(entry)

    def add_pembelian(self, customer, awal, total_belanja, akhir, pesanan_list):
        # pesanan_list: list of dict {menu, jumlah, subtotal}
        entry = {
            "jenis": "pembelian",
            "customer": customer,
            "saldo_awal": awal,
            "total_belanja": total_belanja,
            "saldo_akhir": akhir,
            "pesanan": pesanan_list
        }
        self.entries.append(entry)

    def get_for(self, customer):
        return [e for e in self.entries if e.get("customer") == customer]

    def to_list(self):
        return self.entries


class Customer:
    def __init__(self, nama):
        self.nama = nama
        self.file_json = "customer.json"
        self.data = self.load_data()

        # saldo as dict mapping name->amount (backwards compatible)
        self.saldo = self.data.get("saldo", {})
        # riwayat managed by Riwayat class
        self.riwayat = Riwayat(self.data.get("riwayat", []))

        # Jika customer baru → saldo mulai 0
        if self.nama not in self.saldo:
            self.saldo[self.nama] = 0
            self.simpan_data()

    # Load JSON
    def load_data(self):
        if not os.path.exists(self.file_json):
            return {"saldo": {}, "riwayat": []}
        with open(self.file_json, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                # kalau file rusak/ kosong, inisialisasi ulang
                return {"saldo": {}, "riwayat": []}

    def simpan_data(self):
        with open(self.file_json, "w") as f:
            json.dump({"saldo": self.saldo, "riwayat": self.riwayat.to_list()}, f, indent=4)

    # Top up saldo
    def top_up(self):
        print(f"\nSaldo Anda sekarang: Rp{self.saldo[self.nama]:,}")
        try:
            jumlah = int(input("Masukkan jumlah top up: Rp"))
            if jumlah > 0:
                saldo_awal = self.saldo[self.nama]
                self.saldo[self.nama] += jumlah
                saldo_akhir = self.saldo[self.nama]

                # catat riwayat via Riwayat class
                self.riwayat.add_topup(self.nama, saldo_awal, jumlah, saldo_akhir)
                # simpan kedua data (saldo + riwayat)
                self.simpan_data()

                print(f"Top up berhasil! Saldo Anda kini: Rp{self.saldo[self.nama]:,}")
            else:
                print("Jumlah harus lebih dari 0.")
        except ValueError:
            print("Masukkan angka yang valid.")

    # Bayar pakai saldo
    def bayar_pakai_saldo(self, total, daftar_pesanan):
        if self.saldo[self.nama] >= total:
            saldo_awal = self.saldo[self.nama]
            self.saldo[self.nama] -= total
            saldo_akhir = self.saldo[self.nama]

            # siapkan detail pesanan sebagai list of dict
            pesanan_list = [
                {"menu": item.nama, "jumlah": jumlah, "subtotal": subtotal}
                for item, jumlah, subtotal in daftar_pesanan
            ]

            # catat riwayat pembelian via Riwayat
            self.riwayat.add_pembelian(self.nama, saldo_awal, total, saldo_akhir, pesanan_list)
            # simpan data
            self.simpan_data()

            print("\nPembayaran berhasil menggunakan saldo!")
            print(f"Sisa saldo: Rp{self.saldo[self.nama]:,}")
            return True
        return False

    # Lihat riwayat 
    def lihat_riwayat(self):
        print("\n=== Riwayat Transaksi & Saldo ===")

        data = self.riwayat.get_for(self.nama)

        if not data:
            print("Belum ada riwayat.")
            return

        for i, transaksi in enumerate(data, 1):
            print(f"\n--- Transaksi {i} ---")

            jenis = transaksi.get("jenis", "pembelian")
            print(f"Jenis        : {jenis}")

            saldo_awal = transaksi.get("saldo_awal", 0)
            saldo_akhir = transaksi.get("saldo_akhir", saldo_awal)

            print(f"Saldo awal   : Rp{saldo_awal:,}")
            # jika top up
            if jenis == "top up":
                perubahan = transaksi.get("perubahan", 0)
                print(f"Top up       : Rp{perubahan:,}")
                print(f"Saldo akhir  : Rp{saldo_akhir:,}")
            # jika pembelian
            elif jenis == "pembelian":
                total_belanja = transaksi.get("total_belanja", 0)
                print(f"Total belanja: Rp{total_belanja:,}")
                print(f"Saldo akhir  : Rp{saldo_akhir:,}")
                print("Detail pesanan:")
                for item in transaksi.get("pesanan", []):
                    print(f" - {item.get('menu','?')} x{item.get('jumlah',0)} = Rp{item.get('subtotal',0):,}")
            else:
                # fallback untuk jenis yg tak dikenali
                print("Detail transaksi tidak dikenal.")
                print(f"Saldo akhir  : Rp{saldo_akhir:,}")

    # Cetak struk
    def cetak_struk(self, daftar_pesanan, total):
        print("\n===================================")
        print("               STRUK")
        print("===================================")
        print(f"Customer : {self.nama}")

        print("\nPesanan:")
        for item, jumlah, subtotal in daftar_pesanan:
            print(f"- {item.nama} x{jumlah} = Rp{subtotal:,}")

        print("\n-----------------------------------")
        print(f"TOTAL = Rp{total:,}")
        print("-----------------------------------")
        print("Terima kasih telah berkunjung!")
        print("===================================\n")

    # Proses pemesanan
    def buat_pesanan(self, daftar_menu):
        pesanan = Pesanan(self)

        print(f"\nSelamat datang, {self.nama}!")
        print(f"Saldo Anda: Rp{self.saldo[self.nama]:,}")
        print("\n=== Menu Restoran ===")
        for i, item in enumerate(daftar_menu, 1):
            print(f"{i}. {item}")

        while True:
            try:
                pilih = int(input("\nPilih menu (0 untuk selesai): "))
                if pilih == 0:
                    break
                if 1 <= pilih <= len(daftar_menu):
                    jumlah = int(input("Jumlah: "))
                    pesanan.tambah_item(daftar_menu[pilih - 1], jumlah)
                    print("Item ditambahkan!")
                else:
                    print("Menu tidak valid.")
            except ValueError:
                print("Masukkan angka valid.")

        if not pesanan.daftar_pesanan:
            print("Tidak ada pesanan.")
            return

        pesanan.tampilkan_pesanan()
        total = pesanan.total

        print(f"\nTotal tagihan: Rp{total:,}")
        print(f"Saldo Anda: Rp{self.saldo[self.nama]:,}")

        # Bayar pakai saldo
        if self.bayar_pakai_saldo(total, pesanan.daftar_pesanan):
            self.cetak_struk(pesanan.daftar_pesanan, total)
            return

        # Jika saldo kurang → wajib top up
        print("\nSaldo tidak cukup. Silakan top up.\n")
        self.top_up()

        # Coba bayar lagi
        if self.bayar_pakai_saldo(total, pesanan.daftar_pesanan):
            self.cetak_struk(pesanan.daftar_pesanan, total)
        else:
            print("Saldo tetap tidak cukup. Pesanan dibatalkan.")


# ============================
#  MAIN PROGRAM
# ============================
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

    while True:
        print("\n=== MENU UTAMA ===")
        print("1. Buat Pesanan")
        print("2. Lihat Riwayat")
        print("3. Top Up Saldo")
        print("0. Keluar")

        pilihan = input("Pilih menu: ")

        if pilihan == "1":
            pelanggan.buat_pesanan(daftar_menu)
        elif pilihan == "2":
            pelanggan.lihat_riwayat()
        elif pilihan == "3":
            pelanggan.top_up()
        elif pilihan == "0":
            print("Program selesai. Terima kasih!")
            break
        else:
            print("Pilihan tidak valid.")
