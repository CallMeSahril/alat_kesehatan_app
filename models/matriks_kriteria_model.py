from config import get_db_connection

class MatriksKriteriaModel:
    @staticmethod
    def get_all():
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT mk.*, k1.nama_kriteria AS nama_kriteria_1, k2.nama_kriteria AS nama_kriteria_2
            FROM matriks_kriteria mk
            JOIN kriteria k1 ON mk.kriteria_1_id = k1.id_kriteria
            JOIN kriteria k2 ON mk.kriteria_2_id = k2.id_kriteria
        """)
        data = cursor.fetchall()
        conn.close()
        return data

    @staticmethod
    def insert(k1, k2, nilai):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO matriks_kriteria (kriteria_1_id, kriteria_2_id, nilai_perbandingan)
            VALUES (%s, %s, %s)
        """, (k1, k2, nilai))
        conn.commit()
        conn.close()

    @staticmethod
    def delete_all():
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM matriks_kriteria")
        conn.commit()
        conn.close()
