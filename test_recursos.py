import unittest
from proyecto import app, conexion    # Ajusta "app" si tu archivo se llama diferente


class TestRecursos(unittest.TestCase):
    """Pruebas unitarias para el CRUD de recursos"""

    # ========== PRUEBA DE CONEXIÓN ==========
    def test_conexion_db(self):
        """Probar que la conexión a la BD funciona"""
        conn = conexion
        self.assertIsNotNone(conn, "No se pudo conectar a la base de datos")
        print("✓ Conexión a base de datos exitosa")

    # ========== CREATE ==========
    def test_crear(self):
        """Probar CREATE (agregar recurso)"""
        app_client = app.test_client()
        response = app_client.post(
            '/agregar',
            data={
                'no_control': '2025001',
                'fecha': '2025-01-10',
                'nombre': 'Recurso Test',
                'estadisticas': '10 lecturas',
                'materia': 'Matemáticas',
                'tipo': 'PDF'
            },
            follow_redirects=True
        )

        self.assertEqual(response.status_code, 200)
        print("✓ CREATE: Recurso agregado")

    # ========== READ ==========
    def test_leer(self):
        """Probar READ (listar recursos)"""
        app_client = app.test_client()

        response = app_client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Recursos', response.data)
        print("✓ READ: Recursos listados")

    # ========== UPDATE ==========
    def test_actualizar(self):
        """Probar UPDATE (editar recurso)"""

        app_client = app.test_client()

        # 1. Crear un recurso previo para editar
        app_client.post(
            '/agregar',
            data={
                'no_control': '2025002',
                'fecha': '2025-02-11',
                'nombre': 'Original',
                'estadisticas': '5 usos',
                'materia': 'Historia',
                'tipo': 'Video'
            }
        )

        # 2. Actualizar (usamos id=1 como ejemplo)
        response = app_client.post(
            '/editar/1',
            data={
                'no_control': '2025002',
                'fecha': '2025-02-11',
                'nombre': 'Modificado',
                'estadisticas': '20 usos',
                'materia': 'Historia',
                'tipo': 'Documento'
            },
            follow_redirects=True
        )

        self.assertEqual(response.status_code, 200)
        print("✓ UPDATE: Recurso actualizado")

    # ========== DELETE ==========
    def test_eliminar(self):
        """Probar DELETE (eliminar recurso)"""

        app_client = app.test_client()

        # Crear un recurso para poder eliminarlo
        app_client.post(
            '/agregar',
            data={
                'no_control': '2025003',
                'fecha': '2025-03-15',
                'nombre': 'Eliminar Test',
                'estadisticas': '3 vistas',
                'materia': 'Biología',
                'tipo': 'Imagen'
            }
        )

        # Eliminar recurso con id=1 (o el id que exista)
        response = app_client.get('/eliminar/1', follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        print("✓ DELETE: Recurso eliminado")


if __name__ == '__main__':
    print("\n" + "=" * 50)
    print("PRUEBAS UNITARIAS - RECURSOS")
    print("=" * 50 + "\n")
    unittest.main(verbosity=2)