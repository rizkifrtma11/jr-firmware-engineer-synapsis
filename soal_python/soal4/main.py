from function.mqtt_helper import MqttHelper
import time 


def main():
    # Meminta user memasukkan nama kandidat (harus satu kata)
    nama_kandidat = input("Masukkan nama kandidat (satu kata): ").strip()

    # Validasi input: tidak boleh kosong atau mengandung spasi
    if ' ' in nama_kandidat or not nama_kandidat:
        print("Nama kandidat harus satu kata tanpa spasi!")
        return

    # Membuat objek mqtt_client dari class MqttHelper dengan nama kandidat
    mqtt_client = MqttHelper(nama_kandidat)

    # Menghubungkan ke broker MQTT
    mqtt_client.connect()

    try:
        while True:
            # Publish data ke broker MQTT
            success, data = mqtt_client.publishData()

            # Jika ada data yang berhasil diproses
            if data is not None:
                # Simpan data ke file log CSV
                mqtt_client.logData(data, success)
                # Tampilkan informasi publish ke terminal
                mqtt_client.printPublishInfo(data, success)

            time.sleep(5)

    except KeyboardInterrupt:
        print("Program dihentikan oleh user")

    finally:
        mqtt_client.client.loop_stop()
        mqtt_client.client.disconnect()


if __name__ == "__main__":
    main()
