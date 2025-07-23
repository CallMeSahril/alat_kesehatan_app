from config import get_db_connection

class TahunModel:
    @staticmethod
    def get_all():
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM tahun_produksi")
        data = cursor.fetchall()
        conn.close()
        return data

    @staticmethod
    def get_by_id(id_tahun):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM tahun_produksi WHERE id_tahun = %s", (id_tahun,))
        data = cursor.fetchone()
        conn.close()
        return data

    @staticmethod
    def insert(tahun):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO tahun_produksi (tahun) VALUES (%s)", (tahun,))
        conn.commit()
        conn.close()

    @staticmethod
    def update(id_tahun, tahun):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE tahun_produksi SET tahun = %s WHERE id_tahun = %s", (tahun, id_tahun))
        conn.commit()
        conn.close()

    @staticmethod
    def delete(id_tahun):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tahun_produksi WHERE id_tahun = %s", (id_tahun,))
        conn.commit()
        conn.close()
