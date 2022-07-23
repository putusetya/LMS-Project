""" Module ini berisi daftar menu dari
    sistem manajemen perpustakaan sederhana.
    
Anda dapat menjalankan module ini setelah 
mendefinisikan variabel di init_variable.py
dan setelah menjalankan start.py di terminal.

"""

# Import library yang akan digunakan dalam main.py
import mysql.connector 
from mysql.connector import Error
import pandas as pd
from datetime import date, datetime, timedelta
import warnings
warnings.filterwarnings('ignore')
import init_variable

# Mendefinisikan variabel-variabel untuk koneksi ke server
# Nilai variabel berdasarkan input pada module 'init_variable'
nama_host = init_variable.nama_host 
user = init_variable.user 
password = init_variable.password 
db = init_variable.db  

# Membuat koneksi ke server dan database
conn = mysql.connector.connect(host=nama_host, user=user,
                               passwd=password, database=db)

# Membuat object cursor yang terkoneksi dengan database db
cursor = conn.cursor()


def add_member():
    """Fungsi untuk menambahkan anggota baru dalam database perpustakaan.
    """
    print("-"*60)
    print("PENDAFTARAN ANGGOTA BARU")
    print("-"*60)
    
    nama = input("Input Nama : ")
    tgl_lahir = input("Input Tanggal Lahir (YYYY-MM-DD) : ")
    pekerjaan = input("Input Pekerjaan : ")
    alamat = input("Input Alamat : ")
    
    try:
        variabel_member = {'nama': nama,'tgl_lahir': tgl_lahir,
                           'pekerjaan': pekerjaan,'alamat': alamat}
        insert_member = """ INSERT INTO member(nama, tgl_lahir, pekerjaan, alamat) 
                        VALUES(%(nama)s,%(tgl_lahir)s,%(pekerjaan)s,%(alamat)s) """
        cursor.execute(insert_member,variabel_member)
        conn.commit()
        print("\nPendaftaran anggota baru berhasil.\n")
    except:
        print("\nPendaftaran gagal. Periksa kembali input Anda.\n")
        
    menu()

    
def list_member():
    """Fungsi untuk menampilkan semua anggota perpustakaan beserta informasinya.
    """
    member_list = pd.read_sql_query(""" SELECT * FROM member """,conn)
    df_member = pd.DataFrame(member_list)
    
    print("-"*60)
    print("DAFTAR ANGGOTA PERPUSTAKAAN PACMANN")
    print("-"*60)
    print(df_member)

    menu()

    
def add_book():   
    """Fungsi untuk menambahkan buku baru dalam database perpustakaan.
    """
    print("-"*60)
    print("PENAMBAHAN DATA BUKU BARU")
    print("-"*60)
    
    kode = input("Input Kode : ")
    judul = input("Input Judul : ")
    penulis = input("Input Penulis : ")
    kategori = input("Input Kategori : ")
    stok = int(input("Input Jumlah/Stok : "))
    
    try:
        variabel_buku = {'kode': kode,'judul': judul,'penulis': penulis,
                         'kategori': kategori,'stok': stok}
        insert_buku = """ INSERT INTO book(kode,judul,penulis,kategori,stok) 
                        VALUES(%(kode)s,%(judul)s,%(penulis)s,%(kategori)s,
                        %(stok)s) """
        cursor.execute(insert_buku,variabel_buku)
        conn.commit()
        print("\nData buku berhasil ditambahkan.\n")
    except:
        print("\nPenambahan data buku gagal. Periksa kembali input Anda.\n")
        
    menu()

    
def list_book():
    """Fungsi untuk menampilkan semua anggota perpustakaan beserta informasinya.
    """
    book_list = pd.read_sql_query(""" SELECT * FROM book """,conn)
    df_book = pd.DataFrame(book_list)
    
    print("-"*60)
    print("DAFTAR BUKU PERPUSTAKAAN PACMANN")
    print("-"*60)
    print(df_book)
    
    menu()

    
def search_book():
    """Fungsi untuk melakukan pencarian buku berdasarkan judulnya.
    """
    print("\nPENCARIAN JUDUL BUKU")
    
    title = input('Input Judul: ')
    
    try:
        search = pd.read_sql_query('SELECT * FROM book WHERE judul LIKE "'+title+'";',conn)
        df_search = pd.DataFrame(search)
        print("-"*60)
        print(f"Hasil pencarian untuk judul: {title}\n")
        assert df_search.empty is False, "Judul buku tidak ditemukan. Periksa kembali input Anda.\n"
        print(df_search)
    except AssertionError as message:
        print(message)
        
    menu()

    
def issue_book():
    """Fungsi untuk melakukan peminjaman buku.
    
    Jika buku dipinjam, stok buku pada tabel book akan berkurang 1 pcs.
    Buku harus dikembalikan paling lambat 7 hari setelah tanggal peminjaman.
    
    """
    print("-"*60)
    print("PEMINJAMAN BUKU")
    print("-"*60)
    print("Masukkan ID Peminjam dan Kode Buku")
    
    try:
        id_member = input("ID Member: ")
        cursor.execute('SELECT nama FROM member WHERE id="'+id_member+'";')
        nama = (cursor.fetchall())[0][0]
        print("Nama Member:",nama)
        
        kode = input("Kode Buku: ")
        cursor.execute('SELECT judul FROM book WHERE kode="'+kode+'";')
        judul = (cursor.fetchall())[0][0]
        print("Judul Buku:",judul)
        
        query_stok ='SELECT stok FROM book WHERE kode="'+kode+'" AND judul="'+judul+'";'    
        cursor.execute(query_stok)
        stok = cursor.fetchall()
        int_stok = stok[0][0]
        
        tgl_pinjam = date.today()
        tgl_kembali = tgl_pinjam + timedelta(days=7)
        stok_update = int_stok-1
        
        if int_stok > 0:
            variabel_pinjam = {'kode': kode, 'judul': judul, 'id': id_member, 
                               'nama': nama, 'tgl_pinjam': tgl_pinjam, 'tgl_kembali': tgl_kembali}
            insert_pinjam = 'INSERT INTO issued_book(kode, judul, id, nama, tgl_pinjam, tgl_kembali)\
                            VALUES(%(kode)s,%(judul)s,%(id)s,%(nama)s,%(tgl_pinjam)s,%(tgl_kembali)s);'
            cursor.execute(insert_pinjam, variabel_pinjam)
            cursor.execute('UPDATE book SET stok=%s WHERE kode=%s;', (stok_update,kode))
            conn.commit()
            print(f"\nBuku berhasil dipinjamkan kepada {nama}.")
            print(f"Mohon mengembalikan buku paling lambat pada {tgl_kembali}.\n")
        else:
            print("\nMaaf, stok buku sedang kosong.\n")
    except:
        print("\nTerjadi kesalahan. Periksa kembali input Anda.")
        
    menu()

        
def list_issued_book():
    """Fungsi untuk menampilkan daftar peminjaman buku beserta informasinya.
    """
    issued_book = pd.read_sql_query('SELECT * FROM issued_book;',conn)
    df_issued = pd.DataFrame(issued_book)
    
    print("-"*60)
    print("DAFTAR PEMINJAMAN BUKU")
    print("-"*60)
    print(df_issued)
    
    menu()
    

def return_book():
    """Fungsi untuk melakukan pengembalian buku yang dipinjam.
    
    Jika buku telah dikembalikan, stok buku pada tabel book bertambah 1 pcs,
    dan data buku di daftar peminjaman dihapus.
    
    """
    print("-"*60)
    print("PENGEMBALIAN BUKU")
    print("-"*60)
    print("Masukkan ID Peminjam dan Kode Buku")
    
    try:
        id_member = input("ID Member: ")
        cursor.execute('SELECT nama FROM member WHERE id="'+id_member+'";')
        nama = (cursor.fetchall())[0][0]
        print("Nama Member:",nama)
        kode = input('Kode Buku: ')
        cursor.execute('SELECT judul FROM book WHERE kode="'+kode+'";')
        judul = (cursor.fetchall())[0][0]
        print('Judul Buku:',judul)
        
        query_stok ='SELECT stok FROM book WHERE kode="'+kode+'" AND judul="'+judul+'";'    
        cursor.execute(query_stok)
        stok = cursor.fetchall()
        int_stok = stok[0][0]
        stok_update = int_stok+1
        
        cursor.execute('DELETE FROM issued_book WHERE kode=%s AND id=%s;', (kode, id_member))
        cursor.execute('UPDATE book SET stok=%s WHERE kode=%s;', (stok_update, kode))
        conn.commit()
        print("\nTerima kasih. Pengembalian buku berhasil.\n")
        
    except:
        print("\nTerjadi kesalahan. Periksa kembali input Anda.")
        
    menu()

    
def menu():
    """Fungsi untuk menampilkan daftar tugas.
    """
    print("-"*60)
    print("SELAMAT DATANG DI PERPUSTAKAAN SEDERHANA PACMANN")
    print("-"*60)
    print("1. Pendaftaran Anggota Baru")
    print("2. Pendaftaran Buku Baru")
    print("3. Peminjaman Buku")
    print("4. Tampilkan Daftar Anggota")
    print("5. Tampilkan Daftar Buku")
    print("6. Tampilkan Daftar Peminjaman")
    print("7. Pengembalian Buku")
    print("8. Pencarian Judul Buku")
    print("9. Exit\n")
    
    choice = int(input('Masukkan Nomor Tugas : '))
    
    try:
        if choice == 1:
            add_member()
        elif choice == 2:
            add_book()
        elif choice == 3:
            issue_book()
        elif choice == 4:
            list_member()
        elif choice == 5:
            list_book()
        elif choice == 6:
            list_issued_book()
        elif choice == 7:
            return_book()
        elif choice == 8:
            search_book()
        elif choice == 9:
            print("-"*60)
            print("Terima kasih telah mengunjungi Perpustakaan Pacmann.")
            print("-"*60)
            pass
        else:
            print("Input Anda Salah.\n")
            menu()
    except:
        print("Input Anda salah.\n")
        menu()
        
menu()