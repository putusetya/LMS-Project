""" Module 'init_variable' memuat variabel-variabel 
    yang dibutuhkan untuk membuat koneksi ke server dan database di MySQL.

Anda harus mendefinisikan variabel-variabel dalam module ini sebelum memulai program.
Module ini akan di-import oleh semua module dalam program, yaitu:
create_db.py, start.py, dan main.py
    
"""

# Anda dapat mendefinisikan variabel berikut.
nama_host = "localhost" # Disesuaikan dengan nama komputer yang digunakan
user = "root" # Disesuaikan dengan nama user yang digunakan
password = "" # Disesuaikan dengan password yang digunakan
db = "library"  # Disesuaikan dengan nama database yang akan dibuat dan digunakan
