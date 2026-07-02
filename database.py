import sqlite3


DATABASE = "usuarios_apidb"


def conectar():
    return sqlite3.connect(DATABASE)


def crear_tabla():

    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS consultas(

            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ciudad TEXT,
            temperatura REAL,
            viento REAL

        )
    """)

    conexion.commit()
    conexion.close()


def guardar_consulta(ciudad, temperatura, viento):

    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""

        INSERT INTO consultas(ciudad,temperatura,viento)

        VALUES(?,?,?)

    """, (ciudad, temperatura, viento))

    conexion.commit()
    conexion.close()


def consultar_datos():

    conexion = conectar()

    cursor = conexion.cursor()

    cursor.execute("SELECT * FROM consultas")

    datos = cursor.fetchall()

    conexion.close()

    return datos


def eliminar_datos():

    conexion = conectar()

    cursor = conexion.cursor()

    cursor.execute("DELETE FROM consultas")

    conexion.commit()

    conexion.close()