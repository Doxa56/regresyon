import sqlite3
import openpyxl
import os
import datetime

# Yeni dosya adı oluşturma
timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
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
sheet.cell(row=1, column=1, value="Başliklar")
sheet.cell(row=1, column=2, value="Tekrar Sayilari")

# Verileri yaz
for row_index, (tagler, tekrar_sayisi) in enumerate(rows, start=2):
    sheet.cell(row=row_index, column=1, value=tagler)
    sheet.cell(row=row_index, column=2, value=tekrar_sayisi)

# Dosyayı kaydet
workbook.save(xlsx_filename)

# Bağlantıyı kapat
conn.close()

print(f"Veriler Excel dosyasina {xlsx_filename} olarak kaydedildi.")
