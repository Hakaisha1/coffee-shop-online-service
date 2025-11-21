# Kode bagian logistik
import json

class Barang:
    def __init__(self, nama, stok, harga, kadaluarsa=None):
        self.nama = nama
        self.stok = stok
        self.harga = harga
        self.kadaluarsa = kadaluarsa

    def tambah_stok(self, jumlah):
        self.stok += jumlah

    def kurangi_stok(self, jumlah):
        if jumlah <= self.stok:
            self.stok -= jumlah
        else:
            print("Stok tidak cukup!")

    def info(self):
        kadaluarsa = self.kadaluarsa if self.kadaluarsa else "Tidak ada"
        return (
            f"Nama: {self.nama} | Stok: {self.stok} | Harga: {self.harga} | "
            f"Kadaluarsa: {kadaluarsa}"
        )
    


class supplier:
    def __init__(self, nama, kontak):
        self.nama = nama
        self.kontak = kontak

    def info(self):
        return f"Supplier: {self.nama} | Kontak: {self.kontak}"



class TransaksiPembelian:
    def __init__(self, supplier, barang, jumlah, tanggal):
        self.supplier = supplier #class supplier
        self.barang = barang    #class barang
        self.jumlah = jumlah
        self.tanggal = tanggal

    def proses(self):
        self.barang.tambah_stok(self.jumlah)  #method di class barang

    def info(self):
        return (
            f"Transaksi Pembelian: {self.jumlah} {self.barang.nama} "
            f"dari {self.supplier.nama} pada {self.tanggal}"
        )
    


class Gudang:
    def __init__(self):
        self.daftar_barang = []

    def tambah_barang(self, barang):
        self.daftar_barang.append(barang)

    def cari_barang(self, nama):
        hasil = []
        for barang in self.daftar_barang:
            if nama.lower() in barang.nama.lower():
                hasil.append(barang)
        return hasil

    def hapus_barang(self, nama):
        for barang in self.daftar_barang:
            if barang.nama.lower() == nama.lower():
                self.daftar_barang.remove(barang)
                print(f"{nama} berhasil dihapus.")
                return
        print("Barang tidak ditemukan.")


    def simpan_json(self, logistik):
        data = []
        for b in self.daftar_barang:
            data.append({
                "nama": b.nama,
                "stok": b.stok,
                "harga": b.harga,
                "kadaluarsa": b.kadaluarsa
            })

        with open(logistik, "w") as f:
            json.dump(data, f, indent=4)

    def muat_json(self, logistik):
        with open(logistik, "r") as f:
            data = json.load(f)

        self.daftar_barang = []
        for item in data:
            barang = Barang(
                item["nama"],
                item["stok"],
                item["harga"],
                item["kadaluarsa"]
            )
            self.daftar_barang.append(barang)

            


    def tampilkan_semua_barang(self):
        for barang in self.daftar_barang:
            print(barang.info())



class LogistikManager:
    def __init__(self, gudang):
        self.gudang = gudang
        self.riwayat_transaksi = []

    def beli_barang(self, supplier, barang, jumlah, tanggal):
        transaksi = TransaksiPembelian(supplier, barang, jumlah, tanggal)
        transaksi.proses()
        self.riwayat_transaksi.append(transaksi)
        print("Transaksi berhasil diproses.")

    def tampilkan_riwayat(self):
        for trx in self.riwayat_transaksi:
            print(trx.info())



g = Gudang()


# Muat JSON jika ada
try:
    g.muat_json("assets/database/logistik.json")
except FileNotFoundError:
    print("File JSON tidak ada, akan dibuat nanti.")

# Simpan JSON
g.simpan_json("assets/database/logistik.json")


# Menu interaktif
# if __name__ == "__main__":
#     while True:
#         print("\n" + "="*50)
#         print("SISTEM MANAJEMEN LOGISTIK KOPI")
#         print("="*50)
#         print("1. Tampilkan semua barang")
#         print("2. Cari barang")
#         print("3. Tambah barang baru")
#         print("4. Hapus barang")
#         print("5. Keluar")
#         print("="*50)
        
#         pilihan = input("Pilih menu (1-5): ").strip()
        
#         if pilihan == "1":
#             print("\n--- Daftar Barang ---")
#             g.tampilkan_semua_barang()
            
#         elif pilihan == "2":
#             nama = input("Masukkan nama barang yang dicari: ").strip()
#             hasil = g.cari_barang(nama)
#             if hasil:
#                 print(f"\nHasil pencarian untuk '{nama}':")
#                 for barang in hasil:
#                     print(barang.info())
#             else:
#                 print(f"Barang '{nama}' tidak ditemukan.")
                
#         elif pilihan == "3":
#             nama = input("Nama barang: ").strip()
#             stok = int(input("Stok: "))
#             harga = int(input("Harga: "))
#             kadaluarsa = input("Tanggal kadaluarsa (YYYY-MM-DD) atau kosongkan: ").strip()
            
#             barang_baru = Barang(nama, stok, harga, kadaluarsa if kadaluarsa else None)
#             g.tambah_barang(barang_baru)
#             print(f" Barang '{nama}' berhasil ditambahkan!")
            
#             # Simpan ke JSON
#             g.simpan_json("assets/database/logistik.json")
#             print(" Data tersimpan ke JSON.")
            
#         elif pilihan == "4":
#             nama = input("Masukkan nama barang yang akan dihapus: ").strip()
#             g.hapus_barang(nama)
            
#             # Simpan ke JSON
#             g.simpan_json("assets/database/logistik.json")
#             print(" Data tersimpan ke JSON.")
            
#         elif pilihan == "5":
#             print("\nTerima kasih! Program ditutup.")
#             break
            
#         else:
#             print(" Pilihan tidak valid! Silakan coba lagi.")

