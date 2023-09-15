import sqlite3
import pandas as pd

# Conectar a la base de datos SQLite
conn = sqlite3.connect('mi_base_de_datos.db')  # Reemplaza 'tu_base_de_datos.db' con la ruta a tu base de datos

def obtener_codigo_por_nombre(nombre_alumno):
    cursor = conn.cursor()
    cursor.execute("SELECT Codigo FROM Alumnos WHERE Nombre LIKE ?", ('%' + nombre_alumno + '%',))
    codigo_alumno = cursor.fetchone()
    return codigo_alumno[0] if codigo_alumno is not None else None

while True:
    # Opción para buscar por código o nombre del alumno
    opcion_busqueda = input("¿Deseas buscar por código (c) o nombre (n) del alumno? ").lower()

    if opcion_busqueda == 'c':
        # Búsqueda por código del alumno
        codigo_alumno = input("Ingresa el código del alumno: ")
        break
    elif opcion_busqueda == 'n':
        # Búsqueda por nombre del alumno
        nombre_alumno = input("Ingresa el nombre o parte del nombre del alumno: ")
        codigo_alumno = obtener_codigo_por_nombre(nombre_alumno)
        if codigo_alumno is not None:
            break
        else:
            print("Alumno no encontrado.")
    else:
        print("Opción de búsqueda no válida. Por favor, ingresa 'c' o 'n'.")

# Función para obtener el historial de pagos de un alumno
def obtener_historial_pagos(codigo_alumno):
    cursor = conn.cursor()

    # Obtener nombre del alumno
    cursor.execute("SELECT Nombre FROM Alumnos WHERE Codigo = ?", (codigo_alumno,))
    nombre_alumno = cursor.fetchone()
    if nombre_alumno is not None:
        nombre_alumno = nombre_alumno[0]

        # Obtener historial de pagos de SEMESTRE2022_1 excluyendo la primera columna
        cursor.execute("SELECT * FROM Semestre_2022_1 WHERE id_alumno = ?", (codigo_alumno,))
        historial_semestre1 = cursor.fetchall()
        historial_semestre1 = [row[1:] for row in historial_semestre1]  # Excluir la primera columna

        # Obtener historial de pagos de SEMESTRE2022_2 excluyendo la primera columna
        cursor.execute("SELECT * FROM Semestre_2022_2 WHERE id_alumno = ?", (codigo_alumno,))
        historial_semestre2 = cursor.fetchall()
        historial_semestre2 = [row[1:] for row in historial_semestre2]  # Excluir la primera columna

        cursor.execute("SELECT * FROM Semestre_2023_1 WHERE id_alumno = ?", (codigo_alumno,))
        historial_semestre3 = cursor.fetchall()
        historial_semestre3 = [row[1:] for row in historial_semestre3]  # Excluir la primera columna

        cursor.execute("SELECT * FROM Semestre_2023_2 WHERE id_alumno = ?", (codigo_alumno,))
        historial_semestre4 = cursor.fetchall()
        historial_semestre4 = [row[1:] for row in historial_semestre4]  # Excluir la primera columna

        # Calcular el monto total para cada tabla de historial de pagos
        monto_total_semestre1 = sum(row[1] for row in historial_semestre1)
        monto_total_semestre2 = sum(row[1] for row in historial_semestre2)
        monto_total_semestre3 = sum(row[1] for row in historial_semestre3)
        monto_total_semestre4 = sum(row[1] for row in historial_semestre4)

        # Calcular el monto general sumando todos los montos de todas las tablas
        monto_general = monto_total_semestre1 + monto_total_semestre2 + monto_total_semestre3 + monto_total_semestre4

        return nombre_alumno, historial_semestre1, historial_semestre2, historial_semestre3, historial_semestre4, \
               monto_total_semestre1, monto_total_semestre2, monto_total_semestre3, monto_total_semestre4, monto_general

    return None

# Obtener el historial de pagos del alumno
historial = obtener_historial_pagos(codigo_alumno)

if historial:
    nombre_alumno, historial_semestre1, historial_semestre2, historial_semestre3, historial_semestre4, \
    monto_total_semestre1, monto_total_semestre2, monto_total_semestre3, monto_total_semestre4, monto_general = historial

    # Crear DataFrames de pandas para SEMESTRE2022_1 y SEMESTRE2022_2
    df_semestre1 = pd.DataFrame(historial_semestre1, columns=["VOUCHER", "MONTO", "BANCO", "FECHA", "B.V.", "RI", "FECHA RI", "OBSERVACION"])
    df_semestre2 = pd.DataFrame(historial_semestre2, columns=["VOUCHER", "MONTO", "BANCO", "FECHA", "B.V.", "RI", "FECHA RI", "OBSERVACION"])
    df_semestre3 = pd.DataFrame(historial_semestre3, columns=["VOUCHER", "MONTO", "BANCO", "FECHA", "B.V.", "RI", "FECHA RI", "OBSERVACION"])
    df_semestre4 = pd.DataFrame(historial_semestre4, columns=["VOUCHER", "MONTO", "BANCO", "FECHA", "B.V.", "RI", "FECHA RI", "OBSERVACION"])

    # Agregar una columna de contador
    df_semestre1.insert(0, 'N°', range(1, 1 + len(df_semestre1)))
    df_semestre2.insert(0, 'N°', range(1, 1 + len(df_semestre2)))
    df_semestre3.insert(0, 'N°', range(1, 1 + len(df_semestre3)))
    df_semestre4.insert(0, 'N°', range(1, 1 + len(df_semestre4)))

    # Imprimir el nombre y código del alumno
    print(f"\nNombre del Alumno: {nombre_alumno}")
    print(f"Codigo del Alumno: {codigo_alumno}\n")

    # Imprimir historial de pagos de SEMESTRE2022_1 en formato de tabla
    print("Historial de Pagos SEMESTRE2022_1:")
    print(df_semestre1.to_string(index=False))

    # Imprimir el monto total de SEMESTRE2022_1
    print(f"\nMonto Total SEMESTRE2022_1: {monto_total_semestre1}")

    # Imprimir historial de pagos de SEMESTRE2022_2 en formato de tabla
    print("\nHistorial de Pagos SEMESTRE2022_2:")
    print(df_semestre2.to_string(index=False))

    # Imprimir el monto total de SEMESTRE2022_2
    print(f"\nMonto Total SEMESTRE2022_2: {monto_total_semestre2}")

    # Imprimir historial de pagos de SEMESTRE2023_1 en formato de tabla
    print("\nHistorial de Pagos SEMESTRE2023_1:")
    print(df_semestre3.to_string(index=False))

    # Imprimir el monto total de SEMESTRE2023_1
    print(f"\nMonto Total SEMESTRE2023_1: {monto_total_semestre3}")

    # Imprimir historial de pagos de SEMESTRE2023_2 en formato de tabla
    print("\nHistorial de Pagos SEMESTRE2023_2:")
    print(df_semestre4.to_string(index=False))

    # Imprimir el monto total de SEMESTRE2023_2
    print(f"\nMonto Total SEMESTRE2023_2: {monto_total_semestre4}")

    # Imprimir el monto general
    print(f"\nMonto General: {monto_general}")

else:
    print("Código o nombre de alumno no encontrado.")

# Cerrar la conexión a la base de datos
conn.close()
