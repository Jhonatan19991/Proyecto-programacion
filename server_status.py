import psutil
import csv
import time
from datetime import datetime

# Definir la ruta del archivo CSV donde se guardará la información
ruta = "C:/Users/TuUsuario/Downloads/datos.csv"

# Definir la cantidad de horas que se desea monitorear
horas_a_monitorear = 24*60*60*60 # equivalente a 2 meses

# Definir la frecuencia de monitoreo en segundos
frecuencia_de_monitoreo = 120 # cada 2 minutos

# Escribir los encabezados del archivo CSV
with open(ruta, mode='w', newline='') as csv_file:
    fieldnames = ['mes', 'dia_de_la_semana', 'dia', 'hora', 'minuto', 'cpu_percent', 'ram_percent', 'top_1', 'top_2', 'top_3']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()

# Comenzar el monitoreo
hora_de_inicio = time.time()
while time.time() < hora_de_inicio + horas_a_monitorear:
    # Obtener la información de CPU y RAM
    cpu_percent = psutil.cpu_percent()
    ram_percent = psutil.virtual_memory().percent

    # Obtener el tiempo actual y separarlo en mes, día de la semana, día, hora y minuto
    tiempo_actual = datetime.now()
    mes = tiempo_actual.month
    dia_de_la_semana = tiempo_actual.strftime('%A')
    dia = tiempo_actual.day
    hora = tiempo_actual.hour
    minuto = tiempo_actual.minute

    # Obtener el top 3 de procesos que más recursos están utilizando
    procesos = []
    for proceso in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
        try:
            proceso_info = proceso.as_dict(attrs=['pid', 'name', 'cpu_percent', 'memory_percent'])
            proceso_info['nombre'] = proceso_info.pop('name')
            procesos.append(proceso_info)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    top_3_procesos = sorted(procesos, key=lambda x: x['cpu_percent'] + x['memory_percent'], reverse=True)[:3]
    top_1 = top_3_procesos[0]['nombre'] if len(top_3_procesos) > 0 else ''
    top_2 = top_3_procesos[1]['nombre'] if len(top_3_procesos) > 1 else ''
    top_3 = top_3_procesos[2]['nombre'] if len(top_3_procesos) > 2 else ''

    # Escribir los datos en el archivo CSV
    with open(ruta, mode='a', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow([mes, dia_de_la_semana, dia, hora, minuto, cpu_percent, ram_percent, top_1, top_2, top_3])

    # Esper
