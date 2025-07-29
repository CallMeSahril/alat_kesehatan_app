from config import get_db_connection
import numpy as np

class PerhitunganBobotModel:
    @staticmethod
    def get_matriks_kriteria():
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM kriteria ORDER BY id_kriteria")
        kriteria = cursor.fetchall()

        n = len(kriteria)
        matriks = np.ones((n, n))

        # Ambil semua data matriks_kriteria
        cursor.execute("SELECT * FROM matriks_kriteria")
        data = cursor.fetchall()

        # Buat dict untuk lookup
        nilai_dict = {(row['kriteria_1_id'], row['kriteria_2_id']): row['nilai_perbandingan'] for row in data}

        for i in range(n):
            for j in range(n):
                id1 = kriteria[i]['id_kriteria']
                id2 = kriteria[j]['id_kriteria']
                matriks[i][j] = nilai_dict.get((id1, id2), 1)

        conn.close()
        return kriteria, matriks

    @staticmethod
    def simpan_bobot(kriteria, bobot_list):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM hasil_bobot_kriteria")

        for i in range(len(kriteria)):
           cursor.execute(
                "INSERT INTO hasil_bobot_kriteria (id_kriteria, bobot) VALUES (%s, %s)",
                (kriteria[i]['id_kriteria'], float(round(bobot_list[i], 4)))
            )


        conn.commit()
        conn.close()
