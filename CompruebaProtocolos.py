import pyodbc
from datetime import datetime
from tabulate import tabulate

def verificar_secuencia_escrituras(fecha_inicio, fecha_fin):
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

        # Consulta SQL para obtener escrituras en el rango de fechas
        query = """
            SELECT NUMERO, FECHA
            FROM ESCRITURAS
            WHERE FECHA BETWEEN ? AND ?
            ORDER BY NUMERO
        """
        cursor.execute(query, (fecha_inicio, fecha_fin))
        
        registros = cursor.fetchall()
        cursor.close()
        conn.close()

        if not registros:
            print("No se encontraron registros en el rango de fechas.")
            return

        # Procesamiento de los resultados
        numeros = [row.NUMERO for row in registros]
        fechas = [row.FECHA for row in registros]

        # Verificar números faltantes
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
        
        print(tabulate([[item] for item in faltantes_tabla], headers=["Números Faltantes"], tablefmt="grid"))

        # Verificar secuencia de fechas
        desordenados = []
        for i in range(1, len(numeros)):
            if fechas[i] < fechas[i - 1]:
                desordenados.append((numeros[i - 1], fechas[i - 1], numeros[i], fechas[i]))
        
        if desordenados:
            print(tabulate(desordenados, headers=["Número Anterior", "Fecha Anterior", "Número", "Fecha"], tablefmt="grid"))
        else:
            print("No hay problemas de secuencia de fechas.")

        print("Verificación completada.")

    except pyodbc.Error as e:
        print(f"Error de base de datos: {e}")

# Ejemplo de uso
fecha_inicio = datetime(2024, 12, 1)
fecha_fin = datetime(2024, 12, 31)
verificar_secuencia_escrituras(fecha_inicio, fecha_fin)
