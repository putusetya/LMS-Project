""" Module 'create_db' berfungsi untuk membuat koneksi ke server dan database.

Function create_tables() berfungsi untuk membuat tabel-tabel di dalam database.
Function insert_tables() berfungsi untuk menambahkan data pada tabel-tabel tersebut.
Data tersebut sebagai contoh data awal yang sudah tersimpan dalam database, 
Anda tidak harus menjalankan function insert_tables() pada module start.py.

"""


# Import library yang akan digunakan 
import mysql.connector 
from mysql.connector import Error
import init_variable

# Mendefinisikan variabel-variabel yang telah didefinisikan pada module init_variable
nama_host = init_variable.nama_host 
user = init_variable.user 
password = init_variable.password 
db = init_variable.db

# Membuat koneksi ke server
myconn = mysql.connector.connect(host = nama_host, user = user, 
                                     passwd = password)
# Membuat object cursor
mycursor = myconn.cursor()

try:
    # Membuat query pembuatan database
    query_membuat_db = "CREATE DATABASE {}".format(db)
    # Mengeksekusi query pembuatan database
    mycursor.execute(query_membuat_db)
except:
    print(f"\nDatabase dengan nama '{db}' sudah dibuat.")
    print("Anda dapat langsung menjalankan module main.py")
    print("-"*60)
    
# Membuat koneksi ke server dan database db
conn = mysql.connector.connect(host=nama_host, user=user,
                               passwd=password, database=db)
# Membuat object cursor yang terkoneksi dengan database db
cursor = conn.cursor()
    
    
def create_tables():
    """ Fungsi untuk membuat tabel-tabel dalam database.
    
    Tabel yang dibuat dari fungsi ini belum berisi data.
    
    """
    try:
        # Membuat daftar tabel bernama TABLES yang akan dibuat dalam database db
        TABLES = {}
        # Tabel 'book' berisi informasi buku dalam database.
        TABLES['book'] = (""" CREATE TABLE IF NOT EXISTS book(
                            kode VARCHAR(4) NOT NULL KEY,
                            judul VARCHAR(50) NOT NULL, 
                            penulis VARCHAR(50), 
                            kategori VARCHAR(50) NOT NULL, 
                            stok INT NOT NULL) """)
        # Tabel 'member' berisi informasi anggota perpustakaan dalam database.
        TABLES['member'] = (""" CREATE TABLE IF NOT EXISTS member (
                            id INT NOT NULL AUTO_INCREMENT KEY, 
                            nama VARCHAR(50),
                            tgl_lahir DATE, 
                            pekerjaan VARCHAR(50), 
                            alamat VARCHAR (70)) """)
        # Tabel 'issued_book' berisi informasi peminjaman buku.
        TABLES['issued_book'] = (""" CREATE TABLE IF NOT EXISTS issued_book(
                                kode VARCHAR(4),
                                judul VARCHAR(50), 
                                id INT,
                                nama VARCHAR(50),
                                tgl_pinjam DATE, 
                                tgl_kembali DATE) """)

        # Mengeksekusi query pembuatan tabel-tabel dalam database db
        for table in TABLES:
            table_list = TABLES[table]
            cursor.execute(table_list)
    except:
        print(f"Tabel-tabel dalam database '{db}' sudah dibuat.")
        

def insert_tables():
    """ Fungsi untuk mengisi tabel book dan tabel member dengan data. 
    
    Fungsi ini bersifat opsional, fungsi dapat dinonaktifkan atau dihilangkan.
    Untuk menambahkan data pada tabel book atau tabel member, 
    juga dapat menggunakan function add_book() atau add_member() pada module main.py.
    
    """
    try:
        insert_book = """ INSERT INTO book(kode, judul, penulis, kategori, stok)
                        VALUES('1011', 'Factfulness', 'Hans Rosling', 'Science', 7),
                        ('1012', 'Fit in 5', 'Whyte', 'Health', 5),
                        ('1013', 'Nadira', 'Leila S. Chudori', 'Fiction', 3),
                        ('1014', 'Citizen 4.0', 'Hermawan Kartajaya', 'Business', 6),
                        ('1015', 'Bringing Up Bebe', 'Pamela Druckerman', 'Parenting', 4) """
        insert_member = """ INSERT INTO member(nama, tgl_lahir, pekerjaan, alamat) 
                        VALUES('Abam', '1997-12-1', 'Mahasiswa', 'Jakarta'),
                        ('Alesha', '1992-10-12', 'Alumni', 'Bekasi'),
                        ('Joshua', '1996-6-11', 'Mahasiswa', 'Brebes'),
                        ('Jason', '1998-1-30', 'Mahasiswa', 'Surabaya'),
                        ('Rueben', '1990-8-5', 'Alumni', 'Palembang') """

        # Mengeksekusi penambahan data pada tabel book dan tabel member
        cursor.execute(insert_book)
        cursor.execute(insert_member)
        conn.commit()
    except:
        print(f"Tabel dan data contoh pada database '{db}' sudah dibuat.\n")
