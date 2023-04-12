import argparse
import psutil
import csv
import time
from datetime import datetime

# Utilizar argparse para permitir la especificación de la ruta del archivo CSV al ejecutar el script
parser = argparse.ArgumentParser()
parser.add_argument("ruta", help="Ruta donde se guardará el archivo CSV")
args = parser.parse_args()
ruta = args.ruta
# Escribir los encabezados del archivo CSV si el archivo no existe
try:
    with open(ruta, mode='r') as csv_file:
        pass
except FileNotFoundError:
    with open(ruta, mode='w', newline='') as csv_file:
        fieldnames = ['mes', 'dia_de_la_semana', 'dia', 'hora', 'minuto', 'cpu_percent', 'ram_percent', 'top_1', 'top_2', 'top_3']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

# Comenzar el monitoreo
hora_de_inicio = time.time()

    # Obtener la información de CPU y RAM
cpu_percent = psutil.cpu_percent(interval=1)
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
procesos_dict = {}
for proceso in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
    try:
        proceso_info = proceso.as_dict(attrs=['pid', 'name', 'cpu_percent', 'memory_percent'])
        proceso_info['nombre'] = proceso_info.pop('name')
        if proceso_info['nombre'] not in procesos_dict:
            procesos_dict[proceso_info['nombre']] = True
            procesos.append(proceso_info)
    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
        pass

# Obtener el top 3 de procesos que más recursos están utilizando
top_3_procesos = sorted(procesos, key=lambda x: x['cpu_percent'] + x['memory_percent'], reverse=True)[:3]
top_1 = top_3_procesos[0]['nombre'] if len(top_3_procesos) > 0 else ''
top_2 = top_3_procesos[1]['nombre'] if len(top_3_procesos) > 1 and top_3_procesos[1]['nombre'] != top_1 else ''
top_3 = top_3_procesos[2]['nombre'] if len(top_3_procesos) > 2 and top_3_procesos[2]['nombre'] != top_2 else ''

# Escribir los datos en el archivo CSV en modo "append"
with open(ruta, mode='a', newline='') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow([mes, dia_de_la_semana, dia, hora, minuto, cpu_percent, ram_percent, top_1, top_2, top_3])