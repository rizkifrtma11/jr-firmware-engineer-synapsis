import paho.mqtt.client as mqtt
import json
import random
import csv
import os
from datetime import datetime, timezone, timedelta


class MqttHelper:
    def __init__(self, candidate_name, log_dir='log', broker='test.mosquitto.org', port=1883):
        # Validasi nama kandidat tidak boleh ada spasi
        if ' ' in candidate_name.strip():
            raise ValueError("Nama kandidat harus satu kata tanpa spasi")
        
        # Inisialisasi atribut
        self.name = candidate_name.strip()
        self.broker = broker
        self.port = port
        self.topic = f"mqtt/{self.name}/data"  # Topik MQTT nama kandidat
        self.log_dir = os.path.join(os.getcwd(), log_dir)

        # Buat folder log if not exist
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)
        
        # Setup client MQTT
        self.client = mqtt.Client()
        self.client.on_connect = self.onConnect
        self.client.on_publish = self.onPublish
        self.connected = False
        
        self.last_publish_status = None


    # Fungsi untuk menghubungkan ke broker MQTT
    def connect(self):
        try:
            self.client.connect(self.broker, self.port, 60)
            self.client.loop_start()
        except Exception as e:
            print("Error connecting MQTT:", e)


    # Callback ketika berhasil/tidak terkoneksi ke broker
    def onConnect(self, client, userdata, flags, rc):
        if rc == 0:
            self.connected = True
            print("Connected to MQTT Broker!")
        else:
            print(f"Failed to connect with result code {rc}")


    # Callback saat data berhasil dikirim
    def onPublish(self, client, userdata, mid):
        self.last_publish_status = "Success"


    # Mendapatkan timestamp dalam format UTC
    def _getTimestampUtc(self):
        return datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')


    # Mendapatkan timestamp dalam timezone GMT+7 (WIB)
    def _getTimestampGmt7(self):
        gmt7 = timezone(timedelta(hours=7))
        return datetime.now(gmt7).strftime('%Y-%m-%d %H:%M:%S')


    # Membaca data cuaca dari file JSON yang disimpan sebelumnya
    def readWeatherData(self):
        path = os.path.join(os.getcwd(), 'log', 'data_weather.json')
        try:
            with open(path, 'r') as f:
                data = json.load(f)
            temp = float(data.get('temp', 0))
            humidity = float(data.get('humidity', 0))
            return temp, humidity
        except Exception as e:
            print(f"Failed to read weather data: {e}")
            return 0.0, 0.0


    # Menghasilkan data sensor acak dan ambil suhu & kelembaban dari file
    def generateSensorData(self):
        sensor1 = random.randint(0, 100)
        sensor2 = round(random.uniform(0, 1000), 2)
        sensor3 = random.choice([True, False])
        sensor4, sensor5 = self.readWeatherData()
        return {
            "sensor1": sensor1,
            "sensor2": sensor2,
            "sensor3": sensor3,
            "sensor4": sensor4,
            "sensor5": sensor5
        }


    # Fungsi untuk mengirim data sensor ke broker MQTT
    def publishData(self):
        if not self.connected:
            print("MQTT not connected")
            return False, None

        # Siapkan payload data
        data_payload = {
            "nama": self.name,
            "data": self.generateSensorData(),
            "timestamp": self._getTimestampUtc()
        }

        json_data = json.dumps(data_payload)  # Konversi ke JSON string
        self.last_publish_status = "Failed"  # Reset status sebelum publish

        try:
            self.client.publish(self.topic, json_data)  # Kirim data
            self.client.loop(timeout=1)  # Tunggu sejenak untuk on_publish dijalankan
            status = self.last_publish_status
            return status == "Success", data_payload
        except Exception as e:
            print("Error during publish:", e)
            return False, data_payload


    # Menyimpan data yang dikirim ke file log .csv
    def logData(self, data, status):
        # Nama file log berdasarkan tanggal saat ini
        filename = f"mqtt_log_{datetime.now().strftime('%y%m%d')}.csv"
        path = os.path.join(self.log_dir, filename)
        
        # Header kolom
        header = ['timestamp', 'sensor1', 'sensor2', 'sensor3', 'sensor4', 'sensor5', 'status']
        timestamp = self._getTimestampGmt7()  # Gunakan waktu lokal

        # Data yang akan ditulis sebagai 1 baris
        row = [
            timestamp,
            data['data']['sensor1'],
            data['data']['sensor2'],
            data['data']['sensor3'],
            data['data']['sensor4'],
            data['data']['sensor5'],
            "Success" if status else "Failed"
        ]

        file_exists = os.path.isfile(path)

        try:
            with open(path, 'a', newline='') as csvfile:
                writer = csv.writer(csvfile, delimiter=';')
                if not file_exists:
                    writer.writerow(header)  # Tulis header jika file baru
                writer.writerow(row)  # Tulis data baris
        except Exception as e:
            print("Failed to write log:", e)


    # Menampilkan informasi hasil publish di terminal
    def printPublishInfo(self, data, status):
        print(f"Timestamp : {self._getTimestampGmt7()}")
        print("Action : Publish")
        print(f"Topic : {self.topic}")
        print(f"Data : {json.dumps(data)}")
        print(f"State : {'Success' if status else 'Failed'}\n")
