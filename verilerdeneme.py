import sqlite3
import openpyxl
import os
import datetime

# Yeni dosya adı oluşturma
timestamp = datetime.datetime.now().strftime("%Y_%m_%d_%H.%M.%S")
xlsx_filename = f"veriler_{timestamp}.xlsx"

# SQLite veritabanına bağlan
conn = sqlite3.connect('deneme.db')
cursor = conn.cursor()

# Verileri çek
cursor.execute("SELECT tag, COUNT(*) AS tekrar_sayisi FROM tagler GROUP BY tag ORDER BY tekrar_sayisi DESC LIMIT 50")
rows = cursor.fetchall()

# Workbook oluştur
workbook = openpyxl.Workbook()
sheet = workbook.active

# Başlıkları yaz
sheet.append(["Başliklar", "Tekrar Sayilari"])

# Verileri yaz
for tagler, tekrar_sayisi in rows:
    sheet.append([tagler, tekrar_sayisi])

# Dosyayı kaydet
workbook.save(xlsx_filename)

# Bağlantıyı kapat
conn.close()

print(f"Veriler Excel dosyasına {xlsx_filename} olarak kaydedildi.")
