from config import get_db_connection


class BobotAlternatifModel:
    @staticmethod
    def get_all():
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT ba.*, 
                c.nama_customer, 
                d.id_data, 
                k.nama_kriteria
            FROM bobot_alternatif ba
            JOIN data_alat_kesehatan d ON ba.id_data_alat = d.id_data
            JOIN customer c ON d.id_customer = c.id_customer
            JOIN kriteria k ON ba.id_kriteria = k.id_kriteria
            ORDER BY ba.id_data_alat, ba.id_kriteria
        """)
        data = cursor.fetchall()
        conn.close()
        return data

    @staticmethod
    def insert(id_data_alat, id_kriteria, nilai):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO bobot_alternatif (id_data_alat, id_kriteria, nilai)
            VALUES (%s, %s, %s)
        """, (id_data_alat, id_kriteria, nilai))
        conn.commit()
        conn.close()

    @staticmethod
    def delete_by_data_alat(id_data_alat):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM bobot_alternatif WHERE id_data_alat = %s", (id_data_alat,))
        conn.commit()
        conn.close()
