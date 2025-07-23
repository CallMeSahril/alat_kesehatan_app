from config import get_db_connection


class KondisiModel:
    @staticmethod
    def get_all():
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM kondisi_alat")
        data = cursor.fetchall()
        conn.close()
        return data

    @staticmethod
    def get_by_id(id_kondisi):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT * FROM kondisi_alat WHERE id_kondisi = %s", (id_kondisi,))
        data = cursor.fetchone()
        conn.close()
        return data

    @staticmethod
    def insert(nama_kondisi):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO kondisi_alat (nama_kondisi) VALUES (%s)", (nama_kondisi,))
        conn.commit()
        conn.close()

    @staticmethod
    def update(id_kondisi, nama_kondisi):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE kondisi_alat SET nama_kondisi = %s WHERE id_kondisi = %s", (nama_kondisi, id_kondisi))
        conn.commit()
        conn.close()

    @staticmethod
    def delete(id_kondisi):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM kondisi_alat WHERE id_kondisi = %s", (id_kondisi,))
        conn.commit()
        conn.close()
