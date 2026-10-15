# Importaciones al inicio del archivo (Estándar PEP 8)
from database import agregar_transaccion as db_agregar_transaccion
from database import (
    eliminar_transaccion,
    obtener_gastos_por_categoria,
    obtener_resumen_financiero,
    obtener_transacciones,
)
from datetime import datetime

def mostrar_menu():
    print("\n========================================")
    print("   BIENVENIDO AL PORTAFOLIO DE FINANZAS   ")
    print("========================================")
    print("1. Agregar una transacción")
    print("2. Ver historial de transacciones")
    print("3. Ver reportes financieros")
    print("4. Eliminar una transacción")
    print("5. Salir")


def pedir_numero_flotante(mensaje):
    """Pide un número flotante asegurando que no se ingresen letras o valores negativos."""
    while True:
        try:
            monto = float(input(mensaje))
            if monto < 0:
                print("[ERROR] El valor no puede ser negativo.")
                continue
            return monto
        except ValueError:
            print("[ERROR] Entrada inválida. Ingresa un número (ej. 45.50).")


def pedir_numero_entero(mensaje):
    """Pide un número entero asegurando que no se ingresen letras o valores negativos."""
    while True:
        try:
            valor = int(input(mensaje))
            if valor < 0:
                print("[ERROR] El valor no puede ser negativo.")
                continue
            return valor
        except ValueError:
            print("[ERROR] Entrada inválida. Ingresa un número entero.")


def pedir_texto_valido(mensaje):
    """Pide un texto asegurando que no esté vacío y no sea solo un número."""
    while True:
        texto = input(mensaje).strip()
        if not texto:
            print("[ERROR] El campo no puede estar vacío. Inténtalo de nuevo.")
            continue
        if texto.replace(".", "", 1).isdigit():
            print(
                "[ERROR] Entrada inválida. No se permiten solo números en este campo."
            )
            continue
        return texto



def pedir_fecha_valida(mensaje):
    """Pide una fecha y valida que cumpla estrictamente con el formato YYYY-MM-DD y sea real."""
    while True:
        fecha_str = input(mensaje).strip()
        try:
            # datetime.strptime intenta convertir el texto al formato de fecha estándar
            # Si el usuario escribe algo mal o una fecha inexistente, Python lanzará un ValueError
            fecha_convertida = datetime.strptime(fecha_str, "%Y-%m-%d")

            # Opcional:  formatearla para asegurar que siempre se guarde limpia
            return fecha_convertida.strftime("%Y-%m-%d")

        except ValueError:
            print(
                "[ERROR] Formato de fecha inválido. Por favor, usa el formato año-mes-día (ej. 2026-10-13)."
            )

def agregar_transaccion():
    print("\n--- AGREGAR NUEVA TRANSACCIÓN ---")
    tipo = input("Tipo de transacción (Ingreso / Gasto): ").strip().lower()

    while tipo not in ["ingreso", "gasto"]:
        print("[ERROR] Opción no válida. Escribe 'ingreso' o 'gasto'.")
        tipo = input("Tipo de transacción (Ingreso / Gasto): ").strip().lower()

    monto = pedir_numero_flotante("Monto ($): ")
    categoria = pedir_texto_valido("Categoría (ej. Comida, Transporte, Ventas): ")

    # Función defensiva de fecha
    fecha = pedir_fecha_valida("Fecha (Formato AAAA-MM-DD, ej. 2026-10-13): ")

    db_agregar_transaccion(tipo, monto, categoria, fecha)
    print("✅ ¡Transacción agregada correctamente a la base de datos!")


def mostrar_historial():
    print("\n--- HISTORIAL DE TRANSACCIONES ---")
    transacciones = obtener_transacciones()

    if not transacciones:
        print("ℹ️ No hay transacciones registradas todavía.")
        return

    print(f"{'ID':<4} | {'TIPO':<8} | {'MONTO':<10} | {'CATEGORÍA':<22} | {'FECHA'}")
    print("-" * 70)
    for t in transacciones:
        print(f"{t[0]:<4} | {t[1]:<8} | ${t[2]:<9.2f} | {t[3]:<22} | {t[4]}")


def eliminar_registro():
    print("\n--- ELIMINAR TRANSACCIÓN ---")
    mostrar_historial()

    transaccion_id = pedir_numero_entero(
        "\nIngresa el ID de la transacción que deseas eliminar: "
    )

    confirmacion = (
        input(
            f"¿Estás seguro de eliminar el registro con ID {transaccion_id}? (s/n): "
        )
        .strip()
        .lower()
    )

    if confirmacion == "s":
        eliminado = eliminar_transaccion(transaccion_id)
        if eliminado:
            print(
                f"🗑️ Transacción con ID {transaccion_id} eliminada correctamente."
            )
        else:
            print(
                f"[ERROR] No se encontró ninguna transacción con el ID {transaccion_id}."
            )
    else:
        print("ℹ️ Operación cancelada.")


def mostrar_reportes():
    print("\n========================================")
    print("          📊 REPORTES FINANCIEROS        ")
    print("========================================")

    total_ingresos, total_gastos, balance_neto = obtener_resumen_financiero()

    print(f"💰 Total Ingresos:  ${total_ingresos:,.2f}")
    print(f"💸 Total Gastos:    ${total_gastos:,.2f}")
    print("-" * 40)

    if balance_neto > 0:
        print(f"🟢 Balance Neto:    ${balance_neto:,.2f} (¡Vas con ganancias!)")
    elif balance_neto < 0:
        print(
            f"🔴 Balance Neto:   -${abs(balance_neto):,.2f} (Cuidado: Gastos superan ingresos)"
        )
    else:
        print(f"🟡 Balance Neto:    $0.00 (Punto de equilibrio exacto)")

    print("\n--- 📁 GASTOS POR CATEGORÍA ---")
    gastos_cat = obtener_gastos_por_categoria()

    if not gastos_cat:
        print("ℹ️ No hay gastos registrados para agrupar por categoría.")
    else:
        print(f"{'CATEGORÍA':<22} | {'TOTAL GASTADO'}")
        print("-" * 40)
        for categoria, suma_monto in gastos_cat:
            print(f"{categoria:<22} | ${suma_monto:,.2f}")
    print("========================================")


def ejecutar_sistema():
    print("📁 Conectando y cargando datos de la base de datos...")
    obtener_transacciones()
    print("✅ Sistema listo.")

    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción (1 - 5): ").strip()

        if opcion == "1":
            agregar_transaccion()
        elif opcion == "2":
            mostrar_historial()
        elif opcion == "3":
            mostrar_reportes()
        elif opcion == "4":
            eliminar_registro()  
        elif opcion == "5":
            print("\n¡Gracias por usar el Portafolio de Finanzas! Hasta luego.")
            break
        else:
            print("[ERROR] Opción no válida. Por favor, inténtelo de nuevo.")


if __name__ == "__main__":
    ejecutar_sistema()