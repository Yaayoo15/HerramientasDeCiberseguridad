#Se importan las librerías necesarias para el funcionamiento del script
import argparse
import socket
import nmap
import smtplib
import ssl
import subprocess
import sys
import os
from requests import get
import re
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
import logging

#Se usa el constructor de logging para poder llevar control del registro de errores
  #El archivo será llamado "errores.txt", utilizando UTF-8 como codificación y registrando errores de tipo DEBUG
logging.basicConfig(filename='errorres.txt', encoding='utf-8', level=logging.DEBUG)

#Función para obtener una IP pública por medio de la API de "ipify"
def obtener_ip():
  #Guardamos la dirección obtenida convertida en .text en la variable ip
  ip = get('https://api.ipify.org').text
  return ip


def obtener_info():
  ip_p=obtener_ip()
  f = open("llave.txt", "r")
  API_KEY=f
  params = dict(apiKey=API_KEY, ip=ip_p)
  respuesta = get('https://api.ipgeolocation.io/ipgeo', params=params)
  r = respuesta.json()
  f.close()
  return r


def run(cmd):
  completed_tmp = subprocess.run(["powershell", "-Command", cmd], capture_output=True, text = True)
  completed =  completed_tmp.stdout.splitlines()
  return completed
  
def revisar_servicios():
  comando = "Get-Service | Where-Object {$_.Status -eq 'Running'}"
  info = run(comando)
  with open("archivo.txt", "w") as file:
    for i in info:
      file.write(f"{i}\n")
  return 1

def localhost():
  hostname = socket.gethostname()
  ip_address = socket.gethostbyname(hostname)
  return ip_address

def escan_puertos(begin,end):
  lpuertos=[]
  Target = localhost()
  Scanner = nmap.PortScanner()
  for i in range (begin,end+1):
    Result=Scanner.scan(Target,str(i))
    Result=Result['scan'][Target]['tcp'][i]['state']
    lpuertos.append(Result)
  return lpuertos

def enviar_correo(ruta, ruta1):
  #Envio de correo
  em = MIMEMultipart("PLAIN")
  correo = ''
  contraseña = ''
  reseptor = ''
  asunto = 'Resultados del Script'
  with open(ruta,'rb') as attachment:
      cuerpo = MIMEBase("application","octect-stream")
      cuerpo.set_payload(attachment.read())
  encoders.encode_base64(cuerpo)
  cuerpo.add_header('Content-Disposition', f"attachment; filename= {'Informe.txt'}")
  with open(ruta1,'rb') as attachment:
      cuerpo2 = MIMEBase("application","octect-stream")
      cuerpo2.set_payload(attachment.read())
  encoders.encode_base64(cuerpo2)
  cuerpo2.add_header('Content-Disposition', f"attachment; filename= {'serviciosactivos.txt'}")

  em = MIMEMultipart()
  em['from'] = correo
  em['to'] = reseptor
  em['Subject'] = asunto
  em.attach(cuerpo)
  em.attach(cuerpo2)

  #Aqui encriptamos utilizando el metodo SSL

  contexto = ssl.create_default_context()

  with smtplib.SMTP_SSL('smtp.gmail.com', 465, context= contexto) as smtp:
      smtp.login(correo, contraseña )
      smtp.sendmail(correo,reseptor, em.as_string())
  return 1

def validar_hash():
  salida=[]
  script='HashLab.ps1'
  path=os.path.abspath(script)
  subprocess.Popen(["powershell.exe",path], stdout=sys.stdout)

  Drivers = "Drivers.txt"
  Drivers2 = "Drivers2.txt"
  pDrivers=os.path.abspath(Drivers)
  pDrivers2=os.path.abspath(Drivers2)

  if os.path.exists(pDrivers) and os.path.exists(pDrivers2):

      ADrivers = open(pDrivers,mode='r')
      ADrivers2 = open(pDrivers2,mode='r')

      Lista = ADrivers.read().split('\n')
      Lista2 = ADrivers2.read().split('\n')

      Lista.sort()
      Lista2.sort()

      if Lista == Lista2 :
          salida.append('valido')
      else:
          with open('Drivers.txt','r') as D1:
              with open('Drivers2.txt','r') as D2:
                  Modificados = set(D1).difference(D2)
          with open('Modificados.txt','w') as Modi:
              for line in Modificados:
                  Modi.write(line)
          salida.append('invalido')
  return salida

parser = argparse.ArgumentParser()
parser.add_argument("-pi", "--puertoi", type=int, required=True, help="puerto donde iniciará el escaneo")
parser.add_argument("-pf", "--puertof", type=int, required=True, help="puerto donde terminará el escaneo")
parser.add_argument("-se", "--servicios", action="store_true", help="Si se indica, confirmará que los servicios escenciales estén inciados (guarda en servicios.txt)")
parser.add_argument("-er", "--errores", action="store_true",  help="Si se indica, creará un registro de errores (errores.txt)")
parser.add_argument("-vh", "--valorhash", action="store_true", help="Comprobará la integridad de archivos importantes")
parser.add_argument("-inf", "--informe", required=True, help="Nombre del archivo que contendrá el informe")
args = parser.parse_args()

x=args.puertoi
y=args.puertof
inf=args.informe

ruta_comp=os.path.abspath(inf) #C:/user/...

informe = open(ruta_comp,'w')
informe.write('INFORME DE RESULTADOS\n\n')
informe.close()

if args.servicios:
  try:
    revisar_servicios()
    algo=os.path.abspath('archivo.txt')
  except:
    logging.error('Error al intentar escanear servicios')

try:
  lista_puertos=escan_puertos(x,y)
  
  informe = open(ruta_comp,'a')
  informe.write('\n======================================================\nServicios:\n')
  cant = len(lista_puertos)
  informe.write('\n\nCantidad de puertos escaneados: '+ str(cant))
  informe.close()
  
except:
  logging.error('Error al intentar ecanear puertos')

try:
  with open(ruta_comp, "a") as diccionario:
    diccionario.write("======================================================\nResultados de ip: \n\n")
    for llave, valor  in obtener_info().items():
        diccionario.write("%s %s\n" %(llave, valor))
except:
  logging.warning('No hay conexion con la api ipgeolocation')

if args.valorhash:
  try:
    lista_hash=validar_hash()
    with open(ruta_comp, "a") as pepe:
      if lista_hash[0]=='invalido':
        logging.warning('Valores hash no coinciden')
        pepe.write('\n\nA L E R T A... Valores hash no coinciden.')
      else:
        pepe.write('\n\n======================================================\nVALORES HASH VALIDADOS')
  except:
    logging.error('No se tiene acceso al directorio donde se encuentran los drivers')

if enviar_correo(ruta_comp,algo)!=1:
  logging.error('Correo no enviado')
