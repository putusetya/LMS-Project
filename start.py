""" Anda harus menjalankan module 'start' sebelum memulai program dengan module 'main'.

Module ini hanya dijalankan satu kali.
Module ini berfungsi untuk menjalankan program pada module 'create_db',
yaitu membuat koneksi ke server dan database.
Anda juga harus memanggil function create_tables() dari module 'create_db'.
Setelah menjalankan module start.py, Anda dapat menjalankan program LMS sederhana
dengan menjalankan module main.py

"""

# Import library yang akan digunakan
import mysql.connector 
from mysql.connector import Error
import init_variable
import create_db

# Memanggil function create_tables() dari module 'create_db'
# Function ini harus dijalankan
create_db.create_tables()

# Memanggil function insert_tables() dari module 'create_db'
# create_db.insert_tables()
