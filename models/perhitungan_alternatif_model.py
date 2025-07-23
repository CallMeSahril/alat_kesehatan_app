from config import get_db_connection


class PerhitunganAlternatifModel:
    @staticmethod
    def get_bobot_kriteria():
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM hasil_bobot_kriteria")
        bobot = {row['id_kriteria']: row['bobot'] for row in cursor.fetchall()}
        conn.close()
        return bobot

    @staticmethod
    def get_nilai_alternatif():
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT ba.id_data_alat, ba.id_kriteria, ba.nilai,
                   c.nama_customer, a.nama_alat
            FROM bobot_alternatif ba
            JOIN data_alat_kesehatan d ON ba.id_data_alat = d.id_data
            JOIN customer c ON d.id_customer = c.id_customer
            JOIN alat a ON d.id_alat = a.id_alat
        """)
        data = cursor.fetchall()
        conn.close()
        return data

    @staticmethod
    def simpan_hasil(ranking):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM hasil_akhir_alternatif")
        for item in ranking:
            cursor.execute("""
                INSERT INTO hasil_akhir_alternatif (id_data_alat, skor_akhir)
                VALUES (%s, %s)
            """, (item['id_data_alat'], item['skor_akhir']))
        conn.commit()
        conn.close()

    @staticmethod
    def get_skor_akhir_dict():
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT id_data_alat, skor_akhir FROM hasil_akhir_alternatif")
        data = cursor.fetchall()
        conn.close()
        return {row['id_data_alat']: row['skor_akhir'] for row in data}
