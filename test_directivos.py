import unittest
from app import app, conexion  # IMPORTACIÓN CORRECTA

class TestDirectivos(unittest.TestCase):

    # ======= TEST CONEXIÓN ==========
    def test_conexion_db(self):
        """Verificar conexión a la BD"""
        try:
            cursor = conexion.cursor()
            cursor.execute("SELECT 1")
            cursor.close()
            ok = True
        except:
            ok = False

        self.assertTrue(ok, "No se pudo conectar a MySQL")
        print("✓ Conexión OK")


    # ======= CREATE ==========
    def test_crear(self):
        app_client = app.test_client()

        response = app_client.post("/agregar", data={
            "no_empleado": "9999",
            "nombre": "Test",
            "apellido_paterno": "Uno",
            "apellido_materno": "Dos",
            "puesto": "Director"
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        print("✓ CREATE OK")


    # ======= READ ==========
    def test_leer(self):
        app_client = app.test_client()

        # Insertar uno antes
        cursor = conexion.cursor()
        cursor.execute("""
            INSERT INTO directivos (no_empleado, nombre, apellido_paterno, apellido_materno, puesto)
            VALUES ('8888','Leer','P','M','Supervisor')
        """)
        conexion.commit()
        cursor.close()

        response = app_client.get("/?q=Leer")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Leer", response.data)
        print("✓ READ OK")


    # ======= UPDATE ==========
    def test_actualizar(self):
        app_client = app.test_client()

        cursor = conexion.cursor()
        cursor.execute("""
            INSERT INTO directivos (no_empleado, nombre, apellido_paterno, apellido_materno, puesto)
            VALUES ('7777','Original','OP','OM','CargoX')
        """)
        conexion.commit()
        id_insertado = cursor.lastrowid
        cursor.close()

        response = app_client.post(f"/actualizar/{id_insertado}", data={
            "no_empleado": "7777",
            "nombre": "Modificado",
            "apellido_paterno": "Nuevo",
            "apellido_materno": "NM",
            "puesto": "NuevoCargo"
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        print("✓ UPDATE OK")


    # ======= DELETE ==========
    def test_eliminar(self):
        app_client = app.test_client()

        cursor = conexion.cursor()
        cursor.execute("""
            INSERT INTO directivos (no_empleado, nombre, apellido_paterno, apellido_materno, puesto)
            VALUES ('6666','Eliminar','EP','EM','CargoDel')
        """)
        conexion.commit()
        id_insertado = cursor.lastrowid
        cursor.close()

        response = app_client.get(f"/eliminar/{id_insertado}", follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        print("✓ DELETE OK")


if __name__ == '__main__':
    unittest.main(verbosity=2)