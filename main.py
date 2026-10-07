class CatatanTransaksi:
    def __init__(self, id_transaksi: str, total: float):
        self.id_transaksi = id_transaksi
        self.total = total

    def cetak_detail(self) -> str:
        return f"| Struk ID: {self.id_transaksi} | Total: Rp{self.total:,.2f}"


class MenuItem:
    def __init__(self, nama: str, harga_dasar: float, stok: int):
        self.nama = nama
        self._harga_dasar = harga_dasar
        self._stok = stok

    @property
    def harga(self) -> float:
        return self._harga_dasar

    @property
    def stok(self) -> int:
        return self._stok

    def info_menu(self) -> str:
        return f"Item: {self.nama} | Harga: Rp{self._harga_dasar:,.2f} | Stok: {self._stok}"


class Makanan(MenuItem):
    def __init__(self, nama: str, harga_dasar: float, stok: int, porsi: str):
        super().__init__(nama, harga_dasar, stok)
        self.porsi = porsi

    def info_menu(self) -> str:
        return f"[Makanan] {self.nama} ({self.porsi}) | Harga: Rp{self._harga_dasar:,.2f} | Stok: {self._stok}"


class Minuman(MenuItem):
    def __init__(self, nama: str, harga_dasar: float, stok: int, ukuran: str, ekstra_es: bool = False):
        super().__init__(nama, harga_dasar, stok)
        self.ukuran = ukuran
        self.ekstra_es = ekstra_es

    @property
    def harga(self) -> float:
        biaya_tambahan = 2000.0 if self.ukuran.lower() == "large" else 0.0
        return self._harga_dasar + biaya_tambahan

    def info_menu(self) -> str:
        es_str = "Dingin" if self.ekstra_es else "Normal"
        return f"[Minuman] {self.nama} ({self.ukuran}, {es_str}) | Harga: Rp{self.harga:,.2f} | Stok: {self._stok}"


class Pesanan:
    def __init__(self, id_pesanan: str, nama_pelanggan: str):
        self.id_pesanan = id_pesanan
        self.nama_pelanggan = nama_pelanggan
        self._daftar_item = []
        self.__kode_rahasia_dapur = f"KITCHEN-{id_pesanan}"
        self.__catatan = None

    def tambah_item(self, menu_item: MenuItem, jumlah: int):
        if jumlah <= 0:
            print(f"Jumlah pesanan {menu_item.nama} tidak valid!")
            return

        if menu_item.stok >= jumlah:
            menu_item._stok -= jumlah
            subtotal = menu_item.harga * jumlah
            self._daftar_item.append((menu_item, jumlah, subtotal))
            print(f"Berhasil menambah {jumlah}x {menu_item.nama} ke pesanan {self.id_pesanan}.")
        else:
            print(f"Stok {menu_item.nama} tidak mencukupi!")

    def hitung_total(self) -> float:
        return sum(subtotal for _, _, subtotal in self._daftar_item)

    def selesaikan_pesanan(self):
        total_bayar = self.hitung_total()
        self.__catatan = CatatanTransaksi(f"TRX-{self.id_pesanan}", total_bayar)

    def cetak_struk(self):
        print(f"\n==========================================")
        print(f"         STRUK PESANAN ({self.id_pesanan})")
        print(f"==========================================")
        print(f"Pelanggan: {self.nama_pelanggan}")
        for item, qty, sub in self._daftar_item:
            print(f"- {item.nama} x{qty} = Rp{sub:,.2f}")
        total = self.hitung_total()
        print(f"Total Tagihan: Rp{total:,.2f}")
        if self.__catatan:
            print(f"Status Transaksi: {self.__catatan.cetak_detail()}")
        print(f"==========================================\n")


class Karyawan:
    def __init__(self, nip: str, nama: str):
        self.nip = nip
        self.nama = nama


class RestoranManager:
    def __init__(self, nama_restoran: str):
        self.nama_restoran = nama_restoran
        self._daftar_karyawan = []

    def tambah_karyawan(self, karyawan: Karyawan):
        self._daftar_karyawan.append(karyawan)
        print(f"Karyawan {karyawan.nama} (NIP: {karyawan.nip}) berhasil didaftarkan ke {self.nama_restoran}.")

    def proses_pembayaran_via_kasir(self, kasir: Karyawan, pesanan: Pesanan):
        print(f"\n[Sistem Kasir] Kasir {kasir.nama} memproses pesanan {pesanan.id_pesanan}...")
        pesanan.selesaikan_pesanan()
        pesanan.cetak_struk()


if __name__ == "__main__":
    restoran = RestoranManager("McD Fast Food Mulawarman")

    karyawan1 = Karyawan("KAS-01", "Budi")
    karyawan2 = Karyawan("KAS-02", "Siti")

    restoran.tambah_karyawan(karyawan1)
    restoran.tambah_karyawan(karyawan2)

    makanan1 = Makanan("Ayam Goreng Spicy", 20000.0, 15, "Paket Jumbo")
    makanan2 = Makanan("Burger Keju", 25000.0, 10, "Reguler")

    minuman1 = Minuman("Coca Cola", 8000.0, 20, "Large", ekstra_es=True)
    minuman2 = Minuman("Teh Manis", 5000.0, 25, "Medium", ekstra_es=False)

    print("\n--- DAFTAR MENU RESTORAN ---")
    print(makanan1.info_menu())
    print(makanan2.info_menu())
    print(minuman1.info_menu())
    print(minuman2.info_menu())
    print("----------------------------\n")

    pesanan_budi = Pesanan("ORD-001", "Andi")

    pesanan_budi.tambah_item(makanan1, 2)
    pesanan_budi.tambah_item(minuman1, 1)

    restoran.proses_pembayaran_via_kasir(karyawan1, pesanan_budi)