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
        self.jumlah_bayar = 0

    def proses_pembayaran(self):
        total = self.pesanan.hitung_total()
        while True:
            try:
                self.jumlah_bayar = int(input(f"Total tagihan Rp{total:,}. Masukkan jumlah bayar: Rp"))
                if self.jumlah_bayar < total:
                    print("Uang tidak cukup. Silakan bayar sesuai total.")
                else:
                    kembalian = self.jumlah_bayar - total
                    print(f"Pembayaran berhasil! Kembalian Anda: Rp{kembalian:,}")
                    break
            except ValueError:
                print("Masukkan nominal angka yang valid.")


class Customer:
    def __init__(self, nama):
        self.nama = nama
        self.pesanan = None

    def buat_pesanan(self, daftar_menu):
        self.pesanan = Pesanan(self)
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
                    self.pesanan.tambah_item(daftar_menu[pilih - 1], jumlah)
                    print("Item ditambahkan!")
                else:
                    print("Menu tidak valid.")
            except ValueError:
                print("Masukkan angka yang valid.")

        if self.pesanan.daftar_pesanan:
            self.pesanan.tampilkan_pesanan()
            bayar = Pembayaran(self.pesanan)
            bayar.proses_pembayaran()
        else:
            print("Tidak ada pesanan dibuat.")



if __name__ == "__main__":
    # Data menu awal
    daftar_menu = [
        MenuItem("Espresso", 20000),
        MenuItem("Ice Cafe Latte", 25000),
        MenuItem("Cappucino", 23000),
        MenuItem("Matcha Latte", 27500),
        MenuItem("Butterscotch Coffee", 32000)
    ]

    nama_customer = input("Masukkan nama customer: ")
    customer = Customer(nama_customer)
    customer.buat_pesanan(daftar_menu)
