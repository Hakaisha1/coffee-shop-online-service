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


class Customer:
    def __init__(self, nama):
        self.nama = nama
        self.file_json = "customer.json"
        self.data = self.load_data()

        # Data saldo & riwayat
        self.saldo = self.data.get("saldo", {})
        self.riwayat = self.data.get("riwayat", [])

        # Jika customer baru → saldo mulai 0
        if self.nama not in self.saldo:
            self.saldo[self.nama] = 0
            self.simpan_data()

    # Load JSON
    def load_data(self):
        if not os.path.exists(self.file_json):
            return {"saldo": {}, "riwayat": []}
        with open(self.file_json, "r") as f:
            return json.load(f)

    # Save JSON
    def simpan_data(self):
        with open(self.file_json, "w") as f:
            json.dump({"saldo": self.saldo, "riwayat": self.riwayat}, f, indent=4)

    # Top up saldo
    def top_up(self):
        print(f"\nSaldo Anda sekarang: Rp{self.saldo[self.nama]:,}")
        try:
            jumlah = int(input("Masukkan jumlah top up: Rp"))
            if jumlah > 0:
                saldo_awal = self.saldo[self.nama]
                self.saldo[self.nama] += jumlah
                self.simpan_data()

                # Catat riwayat top up
                self.riwayat.append({
                    "jenis": "top up",
                    "customer": self.nama,
                    "saldo_awal": saldo_awal,
                    "perubahan": jumlah,
                    "saldo_akhir": self.saldo[self.nama]
                })
                self.simpan_data()

                print(f"Top up berhasil! Saldo Anda kini: Rp{self.saldo[self.nama]:,}")
            else:
                print("Jumlah harus lebih dari 0.")
        except:
            print("Masukkan angka yang valid.")

    # Bayar pakai saldo
    def bayar_pakai_saldo(self, total, daftar_pesanan):
        if self.saldo[self.nama] >= total:
            saldo_awal = self.saldo[self.nama]
            self.saldo[self.nama] -= total
            self.simpan_data()

            # Catat riwayat pembelian
            self.riwayat.append({
                "jenis": "pembelian",
                "customer": self.nama,
                "saldo_awal": saldo_awal,
                "total_belanja": total,
                "saldo_akhir": self.saldo[self.nama],
                "pesanan": [
                    {
                        "menu": item.nama,
                        "jumlah": jumlah,
                        "subtotal": subtotal
                    }
                    for item, jumlah, subtotal in daftar_pesanan
                ]
            })
            self.simpan_data()

            print("\nPembayaran berhasil menggunakan saldo!")
            print(f"Sisa saldo: Rp{self.saldo[self.nama]:,}")
            return True
        return False

    # Lihat riwayat (format aman tidak error)
    def lihat_riwayat(self):
        print("\n=== Riwayat Transaksi & Saldo ===")

        data = [r for r in self.riwayat if r["customer"] == self.nama]

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
            print(f"Saldo akhir  : Rp{saldo_akhir:,}")

            if jenis == "top up":
                print(f"Top up       : Rp{transaksi.get('perubahan', 0):,}")

            if jenis == "pembelian":
                print(f"Total belanja: Rp{transaksi.get('total_belanja', 0):,}")
                print("Detail pesanan:")
                for item in transaksi.get("pesanan", []):
                    print(f" - {item['menu']} x{item['jumlah']} = Rp{item['subtotal']:,}")

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
            except:
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
