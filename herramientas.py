import argparse
import socket
import nmap
import smtplib
import ssl
import subprocess
import sys
import os
from openpyxl import Workbook
from openpyxl import load_workbook
from requests import get
import re
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
import logging

logging.basicConfig(filename='errorres.txt', encoding='utf-8', level=logging.DEBUG)

def obtener_ip():
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

def services():#1 es bien y 0 es mal
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
      return info
  
  revisar_servicios()

  res = []
  lista = []
  servicios = open("archivo.txt", "r")
  lser = open("servicios.txt", "r")
  for line in servicios:
    lista.append(line)
    for o in lser:
        match = re.search(o,line)
        if match != None:
          res.append(1)
        else:
          res.append(0)
  return res

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

def enviar_correo():
  #Envio de correo
  em = MIMEMultipart("PLAIN")
  correo = 'confianet.client@gmail.com'
  contraseña = 'rivsvhjattmrcwpk'
  receptor = 'confianet.client@gmail.com'
  asunto = 'prueba'
  with open('archivo.txt','rb') as attachment:
    cuerpo = MIMEBase("application","octect-stream")
    cuerpo.set_payload(attachment.read())
    encoders.encode_base64(cuerpo)
    cuerpo.add_header('Content-Disposition', f"attachment; filename= {'Servicios-Activos.txt'}")
    em = MIMEMultipart()
    em['from'] = correo
    em['to'] = receptor
    em['Subject'] = asunto
    em.attach(cuerpo)
    #Aqui encriptamos utilizando el metodo SSL
    contexto = ssl.create_default_context()
    try:
      with smtplib.SMTP_SSL('smtp.gmail.com', 587, context= contexto) as smtp:smtp.login(correo, contraseña )
    except:
      with smtplib.SMTP_SSL('smtp.gmail.com', 465, context= contexto) as smtp:smtp.login(correo, contraseña )
    
    smtp.sendmail(correo,receptor, em.as_string())
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
parser.add_argument("-pi", "--puertoi", type=int, default=0, help="puerto donde iniciará el escaneo (default=0)")
parser.add_argument("-pf", "--puertof", type=int, default=100, help="puerto donde terminará el escaneo (default=100)")
parser.add_argument("-se", "--servicios", action="store_true", help="Si se indica, confirmará que los servicios escenciales estén inciados (guarda en servicios.txt)")
parser.add_argument("-er", "--errores", action="store_true",  help="Si se indica, creará un registro de errores (errores.txt)")
parser.add_argument("-vh", "--valorhash", action="store_true", help="Comprobará la integridad de archivos importantes")
parser.add_argument("-inf", "--informe", requires=True, help="Nombre del archivo que contendrá el informe")
param=parser.parse_args()

x=param.pi
y=param.pf
inf=param.inf

try:
  lista_servicios=services()
except:
  logging.error('Error al intentar escanear servicios')

try:
  lista_puertos=escan_puertos(x,y)
except:
  logging.error('Error al intentar ecanear puertos')

try:
  diccionario=obtener_info()
except:
  logging.warning('No hay conexion con la api ipgeolocation')

try:
  lista_hash=validar_hash()
  if lista_hash[0]='invalido':
    logging.error('Valores hash no coinciden')
except:
  logging.error('No se tiene acceso al directorio donde se encuentran los drivers')



if enviar_correo()!=1:
  logging.error('No se envío el correo correctamente')
