import pyodbc
from datetime import datetime
from tabulate import tabulate

def verificar_secuencia_corretrajes(fecha_inicio, fecha_fin):
    try:
        # Conectar a la base de datos usando la autenticación de Windows
        conn_str = (
            "DRIVER={SQL Server};"
            "SERVER=SERVERSQL;"
            "DATABASE=DATOS;"
            "Trusted_Connection=yes;"
        )
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        # Consulta SQL para obtener corretajes en el rango de fechas
        query = """
            SELECT ASIENTO, SECCIONB, FECHA
            FROM CORRETAJES
            WHERE FECHA BETWEEN ? AND ?
            ORDER BY ASIENTO, SECCIONB
        """
        cursor.execute(query, (fecha_inicio, fecha_fin))
        
        registros = cursor.fetchall()
        cursor.close()
        conn.close()

        if not registros:
            print("No se encontraron registros en el rango de fechas.")
            return

        # Procesamiento de los resultados
        asientos_A = sorted([(int(row.ASIENTO), row.FECHA) for row in registros if row.SECCIONB == 0])
        asientos_B = sorted([(int(row.ASIENTO), row.FECHA) for row in registros if row.SECCIONB == 1])

        def verificar_secuencia(asientos, seccion):
            numeros = [a[0] for a in asientos]
            fechas = [a[1] for a in asientos]
            
            numero_min, numero_max = min(numeros), max(numeros)
            numeros_faltantes = sorted(set(range(numero_min, numero_max + 1)) - set(numeros))
            
            def agrupar_secuencias(numeros):
                if not numeros:
                    return []
                secuencias = []
                inicio = numeros[0]
                for i in range(1, len(numeros)):
                    if numeros[i] != numeros[i-1] + 1:
                        secuencias.append((inicio, numeros[i-1]))
                        inicio = numeros[i]
                secuencias.append((inicio, numeros[-1]))
                return secuencias

            secuencias_faltantes = agrupar_secuencias(numeros_faltantes)
            faltantes_tabla = [(f"{inicio}-{fin}" if inicio != fin else f"{inicio}") for inicio, fin in secuencias_faltantes]
            print(f"Sección {seccion}:")
            print(tabulate([[item] for item in faltantes_tabla], headers=["Asientos Faltantes"], tablefmt="grid"))

            # Verificar secuencia de fechas
            desordenados = []
            for i in range(1, len(numeros)):
                if fechas[i] < fechas[i - 1]:
                    desordenados.append((numeros[i - 1], fechas[i - 1], numeros[i], fechas[i]))
            
            if desordenados:
                print(tabulate(desordenados, headers=["Asiento Anterior", "Fecha Anterior", "Asiento", "Fecha"], tablefmt="grid"))
            else:
                print(f"No hay problemas de secuencia de fechas en la sección {seccion}.")

        verificar_secuencia(asientos_A, 'A')
        verificar_secuencia(asientos_B, 'B')

        print("Verificación completada.")

    except pyodbc.Error as e:
        print(f"Error de base de datos: {e}")

# Ejemplo de uso
fecha_inicio = datetime(2024, 12, 1)
fecha_fin = datetime(2024, 12, 31)
verificar_secuencia_corretrajes(fecha_inicio, fecha_fin)
