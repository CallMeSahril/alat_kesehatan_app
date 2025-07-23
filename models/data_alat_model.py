from config import get_db_connection


class DataAlatModel:
    @staticmethod
    def get_all():
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT d.*, c.nama_customer, a.nama_alat, a.merk, a.tahun_produksi, k.nama_kondisi
            FROM data_alat_kesehatan d
            JOIN customer c ON d.id_customer = c.id_customer
            JOIN alat a ON d.id_alat = a.id_alat
            JOIN kondisi_alat k ON d.id_kondisi = k.id_kondisi
            ORDER BY d.id_data ASC
        """)
        result = cursor.fetchall()
        conn.close()
        return result

    @staticmethod
    def insert(data):
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = """
        INSERT INTO data_alat_kesehatan (
            id_customer, id_alat, garansi_tahun, tgl_instalasi,
            jumlah_maintenance, m1, m2, m3, m4, m5, m6, m7, m8, m9, m10, id_kondisi
        ) VALUES (%s, %s, %s, %s,
                  %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (
            data['id_customer'], data['id_alat'], data['garansi_tahun'], data['tgl_instalasi'],
            data['jumlah_maintenance'], data['m1'], data['m2'], data['m3'], data['m4'], data['m5'],
            data['m6'], data['m7'], data['m8'], data['m9'], data['m10'], data['id_kondisi']
        )
        cursor.execute(sql, values)
        conn.commit()
        conn.close()

    # @staticmethod
    # def get_by_id(id_data):
    #     conn = get_db_connection()
    #     cursor = conn.cursor(dictionary=True)
    #     cursor.execute(
    #         "SELECT * FROM data_alat_kesehatan WHERE id_data = %s", (id_data,))
    #     result = cursor.fetchone()
    #     conn.close()
    #     return result

    @staticmethod
    def get_by_id(id_data):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT d.*, a.tahun_produksi, k.nama_kondisi
            FROM data_alat_kesehatan d
            JOIN alat a ON d.id_alat = a.id_alat
            JOIN kondisi_alat k ON d.id_kondisi = k.id_kondisi
            WHERE d.id_data = %s
        """, (id_data,))
        result = cursor.fetchone()
        conn.close()
        return result

    @staticmethod
    def update(id_data, data):
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = """
            UPDATE data_alat_kesehatan SET
                id_customer=%s, id_alat=%s, garansi_tahun=%s, tgl_instalasi=%s,
                jumlah_maintenance=%s, m1=%s, m2=%s, m3=%s, m4=%s, m5=%s,
                m6=%s, m7=%s, m8=%s, m9=%s, m10=%s, id_kondisi=%s
            WHERE id_data = %s
        """
        values = (
            data['id_customer'], data['id_alat'], data['garansi_tahun'], data['tgl_instalasi'],
            data['jumlah_maintenance'], data['m1'], data['m2'], data['m3'], data['m4'], data['m5'],
            data['m6'], data['m7'], data['m8'], data['m9'], data['m10'], data['id_kondisi'], id_data
        )
        cursor.execute(sql, values)
        conn.commit()
        conn.close()

    @staticmethod
    def get_skor_akhir():
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT id_data_alat, skor_akhir FROM hasil_akhir_alternatif
        """)
        hasil = cursor.fetchall()
        conn.close()
        return {row['id_data_alat']: row['skor_akhir'] for row in hasil}

    @staticmethod
    def get_all_filtered_by_year(tahun):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        sql = """
        SELECT d.*, c.nama_customer, a.nama_alat, a.merk, a.tahun_produksi, k.nama_kondisi
        FROM data_alat_kesehatan d
        JOIN customer c ON d.id_customer = c.id_customer
        JOIN alat a ON d.id_alat = a.id_alat
        JOIN kondisi_alat k ON d.id_kondisi = k.id_kondisi
        WHERE YEAR(d.tgl_instalasi) = %s
        ORDER BY d.tgl_instalasi ASC
        """
        cursor.execute(sql, (tahun,))
        result = cursor.fetchall()
        conn.close()
        return result

    @staticmethod
    def get_years():
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT DISTINCT YEAR(tgl_instalasi) AS tahun FROM data_alat_kesehatan ORDER BY tahun DESC")
        years = [row[0] for row in cursor.fetchall()]
        conn.close()
        return years
    # @staticmethod
    # def get_all_filtered_by_install_date(bulan, tahun):
    #     conn = get_db_connection()
    #     cursor = conn.cursor(dictionary=True)
    #     sql = """
    #         SELECT d.*, c.nama_customer, a.nama_alat, a.merk, a.tahun_produksi, k.nama_kondisi
    #         FROM data_alat_kesehatan d
    #         JOIN customer c ON d.id_customer = c.id_customer
    #         JOIN alat a ON d.id_alat = a.id_alat
    #         JOIN kondisi_alat k ON d.id_kondisi = k.id_kondisi
    #         WHERE YEAR(d.tgl_instalasi) = %s AND MONTH(d.tgl_instalasi) <= %s
    #         ORDER BY d.id_data ASC
    #     """
    #     cursor.execute(sql, (tahun, bulan))
    #     result = cursor.fetchall()
    #     conn.close()
    #     return result

    @staticmethod
    def delete(id_data):
        conn = get_db_connection()
        cursor = conn.cursor()

        # Hapus data yang berkaitan di tabel anak
        cursor.execute(
            "DELETE FROM bobot_alternatif WHERE id_data_alat = %s", (id_data,))
        cursor.execute(
            "DELETE FROM hasil_akhir_alternatif WHERE id_data_alat = %s", (id_data,))
        # Tambahkan jika ada tabel lain yang punya FK ke data_alat_kesehatan...

        # Lalu hapus parent-nya
        cursor.execute(
            "DELETE FROM data_alat_kesehatan WHERE id_data = %s", (id_data,))
        conn.commit()
        conn.close()
