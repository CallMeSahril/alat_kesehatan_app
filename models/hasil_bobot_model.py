# models/hasil_bobot_model.py
from config import get_db_connection


class HasilBobotModel:
    @staticmethod
    def get_all():
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM hasil_bobot_kriteria")
        result = cursor.fetchall()
        conn.close()
        return result

    @staticmethod
    def get_by_kriteria(id_kriteria):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT * FROM hasil_bobot_kriteria WHERE id_kriteria = %s", (id_kriteria,))
        result = cursor.fetchone()
        conn.close()
        return result
