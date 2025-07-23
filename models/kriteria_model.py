from config import get_db_connection

class KriteriaModel:
    @staticmethod
    def get_all():
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM kriteria")
        result = cursor.fetchall()
        conn.close()
        return result

    @staticmethod
    def get_by_id(id_kriteria):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM kriteria WHERE id_kriteria = %s", (id_kriteria,))
        result = cursor.fetchone()
        conn.close()
        return result

    @staticmethod
    def insert(nama_kriteria):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO kriteria (nama_kriteria) VALUES (%s)", (nama_kriteria,))
        conn.commit()
        conn.close()

    @staticmethod
    def update(id_kriteria, nama_kriteria):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE kriteria SET nama_kriteria = %s WHERE id_kriteria = %s", (nama_kriteria, id_kriteria))
        conn.commit()
        conn.close()

    @staticmethod
    def delete(id_kriteria):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM kriteria WHERE id_kriteria = %s", (id_kriteria,))
        conn.commit()
        conn.close()
