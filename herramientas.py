import argparse
import socket
import nmap
import smtplib
import ssl
import subprocess
from openpyxl import Workbook
from requests import get
import re
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
import logging

logging.basicConfig(filename='errorres.txt', encoding='utf-8', level=logging.DEBUG)

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
  
#--------------------------------------------------------------------------
def obtener_ip():
  ip = get('https://api.ipify.org').text
  return ip

def sho():
  ans = get('https://api.shodan.io/shodan/host/{189.158.196.209}?key=').text
  with open("shodan.txt", "w") as s:
    s.write(ans)
  return ans

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
  #solo drivers vitales
  #si no existe crear, si existe comparar con los drivers del system32
  return

parser = argparse.ArgumentParser()
parser.add_argument("-pi", "--puertoi", type=int, default=0, help="puerto donde iniciará el escaneo (default=0)")
parser.add_argument("-pf", "--puertof", type=int, default=100, help="puerto donde terminará el escaneo (default=100)")
#falta revisar
parser.add_argument("-se", "--servicios", action="store_true", help="Si se indica, confirmará que los servicios escenciales estén inciados (guarda en servicios.txt)")
parser.add_argument("-er", "--errores", action="store_true",  help="Si se indica, creará un registro de errores (errores.txt)")
parser.add_argument("-vh", "--valorhash", action="store_true", help="Comprobará la integridad de archivos importantes")
parser.add_argument("-in", "--informe", requires=True, help="Nombre del archivo que contendrá el informe")
param=parser.parse_args()

x=param.pi
y=param.pf
inf=param.in

try:
  lista_servicios=services()
except:
  logging.error('Error al intentar escanear servicios')

try:
  lista_puertos=escan_puertos(x,y)
except:
  logging.error('Error al intentar ecanear puertos')


  

  
from openpyxl import Workbook 
from openpyxl import load_workbook

wb = Workbook()

filesheet = "./prueba.xlsx"

wb.save(filesheet)

wb = load_workbook(filesheet)

sheet = wb.active
sheet.title = "Resultados1"

wb.save(filesheet)
