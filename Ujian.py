import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import locale

locale.setlocale(locale.LC_ALL, 'id_ID.UTF-8')

# Inisialisasi database
def init_db():
    conn = sqlite3.connect("makanan.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS menu (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama TEXT NOT NULL,
            harga INTEGER NOT NULL,
            kategori TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# Fungsi Tambah Data
def tambah_data():
    nama = entry_nama.get().strip()
    harga = entry_harga.get().strip()
    kategori = entry_kategori.get().strip()

    if not nama or not harga.isdigit() or not kategori:
        messagebox.showerror("Error", "Input tidak valid!")
        return

    conn = sqlite3.connect("makanan.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO menu (nama, harga, kategori) VALUES (?, ?, ?)", (nama, int(harga), kategori))
    conn.commit()
    conn.close()

    refresh_data()
    clear_entries()
    messagebox.showinfo("Success", "Data berhasil ditambahkan!")

# Fungsi Hapus Data
def hapus_data():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror("Error", "Pilih data untuk dihapus!")
        return

    item_id = tree.item(selected_item[0])['values'][0]

    conn = sqlite3.connect("makanan.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM menu WHERE id = ?", (item_id,))
    conn.commit()
    conn.close()

    refresh_data()
    messagebox.showinfo("Success", "Data berhasil dihapus!")

# Fungsi Ubah Data
def ubah_data():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror("Error", "Pilih data untuk diubah!")
        return

    item_id = tree.item(selected_item[0])['values'][0]
    nama = entry_nama.get().strip()
    harga = entry_harga.get().strip()
    kategori = entry_kategori.get().strip()

    if not nama or not harga.isdigit() or not kategori:
        messagebox.showerror("Error", "Input tidak valid!")
        return

    conn = sqlite3.connect("makanan.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE menu SET nama = ?, harga = ?, kategori = ? WHERE id = ?", (nama, int(harga), kategori, item_id))
    conn.commit()
    conn.close()

    refresh_data()
    clear_entries()
    messagebox.showinfo("Success", "Data berhasil diubah!")

# Fungsi Cari Data
def cari_data():
    query = entry_cari.get().strip().lower()

    for row in tree.get_children():
        tree.delete(row)

    conn = sqlite3.connect("makanan.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM menu WHERE LOWER(nama) LIKE ?", ('%' + query + '%',))
    results = cursor.fetchall()
    conn.close()

    for result in results:
        tree.insert("", "end", values=(result[0], result[1], locale.currency(result[2], grouping=True), result[3]))

# Fungsi Refresh Data
def refresh_data():
    for row in tree.get_children():
        tree.delete(row)

    conn = sqlite3.connect("makanan.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM menu")
    menus = cursor.fetchall()
    conn.close()

    for menu in menus:
        tree.insert("", "end", values=(menu[0], menu[1], locale.currency(menu[2], grouping=True), menu[3]))

# Fungsi Clear Input
def clear_entries():
    entry_nama.delete(0, tk.END)
    entry_harga.delete(0, tk.END)
    entry_kategori.delete(0, tk.END)

# Inisialisasi GUI
app = tk.Tk()
app.title("Aplikasi FoodShop")
app.geometry("800x600")
app.configure(bg="#f3f4ed")

init_db()

# Frame Input
frame_input = tk.Frame(app, bg="#f3f4ed", pady=10)
frame_input.pack()

tk.Label(frame_input, text="Nama Makanan:", font=("Arial", 12), bg="#f3f4ed", fg="#333333").grid(row=0, column=0, padx=10, pady=5, sticky="e")
entry_nama = tk.Entry(frame_input, font=("Arial", 12), width=30, bg="#e7ecef", fg="#333333")
entry_nama.grid(row=0, column=1, padx=10, pady=5)

tk.Label(frame_input, text="Harga:", font=("Arial", 12), bg="#f3f4ed", fg="#333333").grid(row=1, column=0, padx=10, pady=5, sticky="e")
entry_harga = tk.Entry(frame_input, font=("Arial", 12), width=30, bg="#e7ecef", fg="#333333")
entry_harga.grid(row=1, column=1, padx=10, pady=5)

tk.Label(frame_input, text="Kategori:", font=("Arial", 12), bg="#f3f4ed", fg="#333333").grid(row=2, column=0, padx=10, pady=5, sticky="e")
entry_kategori = tk.Entry(frame_input, font=("Arial", 12), width=30, bg="#e7ecef", fg="#333333")
entry_kategori.grid(row=2, column=1, padx=10, pady=5)

tk.Button(frame_input, text="Tambah", font=("Arial", 12), bg="#80ed99", command=tambah_data).grid(row=3, column=0, padx=10, pady=10)
tk.Button(frame_input, text="Ubah", font=("Arial", 12), bg="#57cc99", command=ubah_data).grid(row=3, column=1, padx=10, pady=10)
tk.Button(frame_input, text="Hapus", font=("Arial", 12), bg="#ff6b6b", fg="white", command=hapus_data).grid(row=3, column=2, padx=10, pady=10)

# Frame Cari
frame_search = tk.Frame(app, bg="#f3f4ed", pady=10)
frame_search.pack()

tk.Label(frame_search, text="Cari Nama:", font=("Arial", 12), bg="#f3f4ed", fg="#333333").pack(side="left", padx=10)
entry_cari = tk.Entry(frame_search, font=("Arial", 12), width=30, bg="#e7ecef", fg="#333333")
entry_cari.pack(side="left", padx=10)
tk.Button(frame_search, text="Cari", font=("Arial", 12), bg="#ffca3a", command=cari_data).pack(side="left", padx=10)

# Tabel
columns = ("ID", "Nama", "Harga", "Kategori")
tree = ttk.Treeview(app, columns=columns, show="headings", height=15)
tree.heading("ID", text="ID")
tree.heading("Nama", text="Nama")
tree.heading("Harga", text="Harga")
tree.heading("Kategori", text="Kategori")
tree.column("ID", anchor="center", width=50)
tree.column("Nama", anchor="w", width=250)
tree.column("Harga", anchor="e", width=100)
tree.column("Kategori", anchor="w", width=150)
tree.pack(fill="both", expand=True, padx=20, pady=10)

refresh_data()

app.mainloop()
