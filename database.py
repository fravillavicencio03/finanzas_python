import sqlite3

DB_NAME = "finanzas.db"


def obtener_conexion():
    """Crea y devuelve una conexión a la base de datos SQLite."""
    return sqlite3.connect(DB_NAME)


def inicializar_base_datos():
    """Crea la tabla de transacciones si no existe previamente."""
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    query = """
    CREATE TABLE IF NOT EXISTS transacciones (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tipo TEXT NOT NULL,
        monto REAL NOT NULL,
        categoria TEXT NOT NULL,
        fecha TEXT NOT NULL
    )
    """
    cursor.execute(query)
    conexion.commit()
    conexion.close()


def agregar_transaccion(tipo, monto, categoria, fecha):
    """Inserta una nueva transacción asegurando que el tipo se guarde normalizado en minúsculas."""
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    # Normalizamos el tipo a minúsculas antes de guardarlo para evitar errores
    tipo_normalizado = tipo.strip().lower()

    query = """
    INSERT INTO transacciones (tipo, monto, categoria, fecha)
    VALUES (?, ?, ?, ?)
    """
    cursor.execute(query, (tipo_normalizado, monto, categoria, fecha))
    conexion.commit()
    conexion.close()


def obtener_transacciones():
    """Recupera todas las transacciones almacenadas en la base de datos."""
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT id, tipo, monto, categoria, fecha FROM transacciones")
    resultados = cursor.fetchall()
    conexion.close()
    return resultados


# --- NUEVAS FUNCIONES DE REPORTES FINANCIEROS ---


def obtener_resumen_financiero():
    """Calcula totales usando LOWER() para evitar conflictos de mayúsculas."""
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    # Usamos LOWER(tipo) para atrapar tanto 'ingreso' como 'Ingreso' o variaciones
    cursor.execute(
        "SELECT SUM(monto) FROM transacciones WHERE LOWER(tipo) = 'ingreso'"
    )
    res_ingresos = cursor.fetchone()[0]
    total_ingresos = res_ingresos if res_ingresos else 0.0

    cursor.execute(
        "SELECT SUM(monto) FROM transacciones WHERE LOWER(tipo) = 'gasto'"
    )
    res_gastos = cursor.fetchone()[0]
    total_gastos = res_gastos if res_gastos else 0.0

    conexion.close()

    balance_neto = total_ingresos - total_gastos
    return total_ingresos, total_gastos, balance_neto


def obtener_gastos_por_categoria():
    """Agrupa los gastos normalizando el tipo con LOWER()."""
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    query = """
    SELECT categoria, SUM(monto) 
    FROM transacciones 
    WHERE LOWER(tipo) = 'gasto' 
    GROUP BY categoria
    """
    cursor.execute(query)
    resultados = cursor.fetchall()
    conexion.close()
    return resultados


def eliminar_transaccion(transaccion_id):
    """Elimina una transacción de la base de datos utilizando su ID único."""
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("DELETE FROM transacciones WHERE id = ?", (transaccion_id,))
    filas_afectadas = cursor.rowcount  # Verifica si el ID existía
    conexion.commit()
    conexion.close()

    return filas_afectadas > True or filas_afectadas == 1