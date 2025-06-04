# Dokumentasi Proyek – Synapsis Challenge

## 1. Soal 1  
**File:** `soal1/app.py`  
**Fungsi:** Menghitung maksimum, minimum, rata-rata, dan modus dari sebuah list angka.  
**Cara menjalankan kode:**  
```bash
python .\soal1\app.py
```

---

## 2. Soal 2  
**File:** `soal2/app.py`  
**Fungsi:** API yang menerima nama dan nilai siswa, lalu mengembalikan respons nama, huruf nilai dan status kelulusan.  
**Dependensi:** `Flask`  
**Cara install dependensi:**  
```bash
pip install Flask
```  
**Cara menjalankan kode:**  
```bash
python .\soal2\app.py
```

---

## 3. Soal 3  
**File:** `soal3/main.py`, `function/weather_helper.py`  
**Fungsi:** Meminta interval waktu dan nama kota, kemudian mengambil data cuaca (temperatur & kelembapan) secara periodik dari OpenWeather API.  
**Dependensi:** `requests` `function`
**Cara install dependensi:**  
```bash
pip install requests function
```  
**Cara menjalankan kode:**  
```bash
python -m soal3.main
```

---

## 4. Soal 4  
**File:** `soal4/main.py`, `function/mqtt_helper.py`  
**Fungsi:** Mengirim data sensor acak ditambah data cuaca (dari file JSON) ke broker MQTT, menyimpan log dalam format CSV.  
**Dependensi:** `paho-mqtt`, file `function/mqtt_helper.py`  
**Cara install dependensi:**  
```bash
pip install paho-mqtt
```  
**Cara menjalankan kode:**  
```bash
python -m soal4.main
```
