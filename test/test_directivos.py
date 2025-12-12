import unittest
import time
from proyecto import app, conexion  # Se importa igual que tu ejemplo

class TestCrud1(unittest.TestCase):
    """Pruebas unitarias para el CRUD de Directivos"""
    
    # ========== PRUEBA DE CONEXIÓN A LA BASE DE DATOS ==========
    def test_conexion_db(self):
        """Verificar que la conexión a la base de datos funciona"""
        try:
            cursor = conexion.cursor()
            cursor.execute("SELECT 1")
            cursor.close()
            conn_ok = True
        except:
            conn_ok = False

        self.assertTrue(conn_ok, "No se pudo conectar a la base de datos")
        print("✓ Conexión a base de datos exitosa")
    
    # ========== PRUEBAS CRUD ==========
    
    # Prueba 1: CREATE - Insertar un nuevo directivo
    def test_crear(self):
        """Verificar operación CREATE (agregar)"""
        app_client = app.test_client()
        response = app_client.post('/directivos/agregar', data={
            'nombre': 'TestNombre',
            'apellido_paterno': 'TestP',
            'apellido_materno': 'TestM',
            'cargo': 'Director',
            'correo': 'test@correo.com'
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        print("✓ CREATE: Directivo guardado")
    
    # Prueba 2: READ - Consultar un directivo existente
    def test_leer(self):
        """Verificar operación READ (consultar)"""
        app_client = app.test_client()

        # Insertar uno primero
        app_client.post('/directivos/agregar', data={
            'nombre': 'LeerNombre',
            'apellido_paterno': 'LeerP',
            'apellido_materno': 'LeerM',
            'cargo': 'Supervisor',
            'correo': 'leer@correo.com'
        })

        response = app_client.get('/directivos?q=LeerNombre')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'LeerNombre', response.data)
        print("✓ READ: Directivo consultado")
    
    # Prueba 3: UPDATE - Actualizar un directivo existente
    def test_actualizar(self):
        """Verificar operación UPDATE (editar)"""
        app_client = app.test_client()

        # Insertar un directivo primero
        cursor = conexion.cursor()
        cursor.execute("""
            INSERT INTO directivos (nombre, apellido_paterno, apellido_materno, cargo, correo)
            VALUES ('Original', 'OP', 'OM', 'CargoX', 'original@correo.com')
        """)
        conexion.commit()
        directivo_id = cursor.lastrowid
        cursor.close()

        # Actualizar
        response = app_client.post(f'/directivos/editar/{directivo_id}', data={
            'nombre': 'Modificado',
            'apellido_paterno': 'NP',
            'apellido_materno': 'NM',
            'cargo': 'NuevoCargo',
            'correo': 'nuevo@correo.com'
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        print("✓ UPDATE: Directivo actualizado")
    
    # Prueba 4: DELETE - Eliminar un directivo existente
    def test_eliminar(self):
        """Verificar operación DELETE (eliminar)"""
        app_client = app.test_client()

        # Insertar uno primero
        cursor = conexion.cursor()
        cursor.execute("""
            INSERT INTO directivos (nombre, apellido_paterno, apellido_materno, cargo, correo)
            VALUES ('Borrar', 'BP', 'BM', 'CargoDel', 'borrar@correo.com')
        """)
        conexion.commit()
        directivo_id = cursor.lastrowid
        cursor.close()

        # Eliminarlo
        response = app_client.get(f'/directivos/eliminar/{directivo_id}', follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        print("✓ DELETE: Directivo eliminado")
    
if __name__ == '__main__':  
    print("\n" + "="*50)
    print("PRUEBAS UNITARIAS - CRUD DIRECTIVOS")
    print("="*50 + "\n")
    unittest.main(verbosity=2)