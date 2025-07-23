from config import get_db_connection

class AlatModel:
    @staticmethod
    def get_all():
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM alat")
        data = cursor.fetchall()
        conn.close()
        return data

    @staticmethod
    def get_by_id(id_alat):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM alat WHERE id_alat = %s", (id_alat,))
        data = cursor.fetchone()
        conn.close()
        return data

    @staticmethod
    def insert(nama, merk, tahun):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO alat (nama_alat, merk, tahun_produksi) VALUES (%s, %s, %s)", (nama, merk, tahun))
        conn.commit()
        conn.close()

    @staticmethod
    def update(id_alat, nama, merk, tahun):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE alat SET nama_alat=%s, merk=%s, tahun_produksi=%s WHERE id_alat=%s", (nama, merk, tahun, id_alat))
        conn.commit()
        conn.close()

    @staticmethod
    def delete(id_alat):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM alat WHERE id_alat=%s", (id_alat,))
        conn.commit()
        conn.close()
