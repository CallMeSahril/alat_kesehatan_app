from config import get_db_connection


class CustomerModel:
    @staticmethod
    def get_all():
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM customer")
        data = cursor.fetchall()
        conn.close()
        return data

    @staticmethod
    def get_by_id(id_customer):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT * FROM customer WHERE id_customer = %s", (id_customer,))
        data = cursor.fetchone()
        conn.close()
        return data

    @staticmethod
    def insert(nama, alamat):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO customer (nama_customer, alamat) VALUES (%s, %s)", (nama, alamat))
        conn.commit()
        conn.close()

    @staticmethod
    def update(id_customer, nama, alamat):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE customer SET nama_customer = %s, alamat = %s WHERE id_customer = %s",
                       (nama, alamat, id_customer))
        conn.commit()
        conn.close()

    @staticmethod
    def delete(id_customer):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM customer WHERE id_customer = %s", (id_customer,))
        conn.commit()
        conn.close()
