import sqlite3
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

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
    word_repetitions[tag] = word_repetitions.get(tag, 0) + count

# Tekrar sayılarını elde et
repetitions = [word_repetitions[tag] for tag in tags]

# Verileri eğitim ve test kümelerine ayır
X = np.array(repetitions).reshape(-1, 1)
y = np.arange(len(X))

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LinearRegression()
model.fit(X_train, y_train)

# Regresyon doğrusunun eğim ve kesme noktası
slope = model.coef_[0]
intercept = model.intercept_
y_pred = model.predict(X_test)

# Grafiği çiz
plt.figure(figsize=(10, 6))
plt.scatter(X_train, y_train, color='blue', label='Gerçek Veriler')
plt.plot(X_train, model.predict(X_train), color='red', label='Regresyon Doğrusu')

plt.title('Linear Regresyon Analizi')
plt.xlabel('Tekrar Sayisi')
plt.ylabel('Tagler')
plt.legend()
plt.show()

print(f"Eğim (slope): {slope}")
print(f"Kesme Noktasi (intercept): {intercept}")
