import sqlite3
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

# SQLite veritabanına bağlan
conn = sqlite3.connect('deneme.db')
cursor = conn.cursor()
# Veriyi çek
cursor.execute("SELECT tag, COUNT(*) AS tekrar_sayisi FROM tagler GROUP BY tag LIMIT 50")
data = cursor.fetchall()

# Bağlantıyı kapat
conn.close()

# Verileri özellikler (X) ve hedef değişken (y) olarak ayır
tags = [row[0] for row in data]
repetition_counts = [row[1] for row in data]

# Aynı kelimenin tekrar sayılarını hesapla
word_repetitions = {}
for tag, count in zip(tags, repetition_counts):
    if tag in word_repetitions:
        word_repetitions[tag] += count
    else:
        word_repetitions[tag] = count

# Tekrar sayılarını elde et
repetitions = [word_repetitions[tag] for tag in tags]

# Verileri eğitim ve test kümelerine ayır
X = np.array(repetitions).reshape(-1, 1)
y = np.arange(len(X))

model = LinearRegression()
model.fit(X, y)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Regresyon doğrusunun eğim ve kesme noktası
slope = model.coef_[0]
intercept = model.intercept_
y_pred = model.predict(X_test)

# Grafiği oluştur
plt.figure(figsize=(10, 6))

# Noktaları çizdir
scatter = plt.scatter(X_train, y_train, color='blue')

# Regresyon doğrusunu çizdir
modelin_tahmin_ettigi_y = model.predict(X_train)
plt.plot(X_train, modelin_tahmin_ettigi_y, color='red')

# Noktaların üstüne gelindiğinde etiketlerin görünmesi için
for i, tag in enumerate(tags):
    plt.annotate(tag, (X[i], y[i]), textcoords="offset points", xytext=(0,10), ha='center', fontsize=7)

# Grafik ayarları
plt.title('Linear Regresyon Analizi')
plt.xlabel('Tekrar Sayisi')
plt.ylabel('Tag Sirasi')

# Renk eşleştirmesi için açıklamayı ekle
plt.legend([scatter], ['Etiket'], loc='upper left')

# Grafiği göster
plt.show()

print(f"Eğim (slope): {slope}")
print(f"Kesme Noktasi (intercept): {intercept}")
