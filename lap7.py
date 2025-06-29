from sqlalchemy import create_engine, Column, Integer, String, UniqueConstraint
from sqlalchemy.orm import sessionmaker, declarative_base

# Membuat base untuk ORM
Base = declarative_base()

# Definisi model Siswa
class Siswa(Base):
    _tablename_ = 'siswa'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nama = Column(String, nullable=False)
    nis = Column(String, nullable=False, unique=True)
    kelas = Column(String, nullable=False)
    jurusan = Column(String, nullable=False)

    def _repr_(self):
        return f"<Siswa(id={self.id}, nama='{self.nama}', nis='{self.nis}', kelas='{self.kelas}', jurusan='{self.jurusan}')>"

# Setup database SQLite
engine = create_engine('sqlite:///data_siswa.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# Fungsi tambah data siswa
def tambah_data_siswa():
    nama = input("Masukkan Nama: ").strip()
    nis = input("Masukkan NIS: ").strip()
    kelas = input("Masukkan Kelas: ").strip()
    jurusan = input("Masukkan Jurusan: ").strip()

    if nis == "":
        print("❌ NIS tidak boleh kosong!")
        return

    # Periksa apakah NIS sudah ada
    if session.query(Siswa).filter_by(nis=nis).first():
        print("❌ NIS sudah terdaftar. Harus unik!")
        return

    siswa_baru = Siswa(nama=nama, nis=nis, kelas=kelas, jurusan=jurusan)
    session.add(siswa_baru)
    session.commit()
    print("✅ Data siswa berhasil ditambahkan.")

# Fungsi lihat semua data
def lihat_semua_data():
    data = session.query(Siswa).all()
    if not data:
        print("📂 Belum ada data siswa.")
        return
    print("\n=== DAFTAR DATA SISWA ===")
    for s in data:
        print(f"ID: {s.id}, Nama: {s.nama}, NIS: {s.nis}, Kelas: {s.kelas}, Jurusan: {s.jurusan}")

# Fungsi ubah data siswa
def ubah_data_siswa():
    try:
        id_siswa = int(input("Masukkan ID Siswa yang akan diubah: "))
    except ValueError:
        print("❌ ID harus berupa angka!")
        return

    siswa = session.query(Siswa).get(id_siswa)
    if not siswa:
        print("❌ Data siswa tidak ditemukan.")
        return

    print(f"Data saat ini: Nama={siswa.nama}, NIS={siswa.nis}, Kelas={siswa.kelas}, Jurusan={siswa.jurusan}")
    nama_baru = input("Nama baru (biarkan kosong jika tidak ingin diubah): ").strip()
    nis_baru = input("NIS baru (biarkan kosong jika tidak ingin diubah): ").strip()
    kelas_baru = input("Kelas baru (biarkan kosong jika tidak ingin diubah): ").strip()
    jurusan_baru = input("Jurusan baru (biarkan kosong jika tidak ingin diubah): ").strip()

    # Validasi NIS unik jika diubah
    if nis_baru and nis_baru != siswa.nis:
        if session.query(Siswa).filter_by(nis=nis_baru).first():
            print("❌ NIS sudah digunakan oleh siswa lain.")
            return
        siswa.nis = nis_baru

    if nama_baru:
        siswa.nama = nama_baru
    if kelas_baru:
        siswa.kelas = kelas_baru
    if jurusan_baru:
        siswa.jurusan = jurusan_baru

    session.commit()
    print("✅ Data siswa berhasil diperbarui.")

# Fungsi hapus data siswa
def hapus_data_siswa():
    try:
        id_siswa = int(input("Masukkan ID Siswa yang akan dihapus: "))
    except ValueError:
        print("❌ ID harus berupa angka!")
        return

    siswa = session.query(Siswa).get(id_siswa)
    if not siswa:
        print("❌ Data siswa tidak ditemukan.")
        return

    session.delete(siswa)
    session.commit()
    print("🗑 Data siswa berhasil dihapus.")

# Fungsi utama dengan menu CLI
def main():
    while True:
        print("\n=== MENU SISTEM DATA SISWA ===")
        print("1. Tambah Data Siswa")
        print("2. Lihat Semua Data")
        print("3. Ubah Data Siswa")
        print("4. Hapus Data Siswa")
        print("5. Keluar")
        pilihan = input("Pilih menu (1-5): ").strip()

        if pilihan == '1':
            tambah_data_siswa()
        elif pilihan == '2':
            lihat_semua_data()
        elif pilihan == '3':
            ubah_data_siswa()
        elif pilihan == '4':
            hapus_data_siswa()
        elif pilihan == '5':
            print("👋 Keluar dari program. Sampai jumpa!")
            break
        else:
            print("❌ Pilihan tidak valid. Silakan coba lagi.")

# Jalankan program
if __name__ == "_main_":
    main()