# HerramientasDeCiberseguridad
Producto Integrador de Aprendizaje

Información general
Este script, considerado como una herramienta para ciberseguridad hace un escaneo de puertos de una dirección ip,
además de obtener su información geográfica, también se encarga de revisar valores hash del equipo, comparar dichos
valores y obtener servicios para enviar los resultados por vía correo electrónico por mencionar algunos usos

Requerimientos
  -Tener descargado el script “HashLib.ps1” 
	
  -El archivo “llave.txt”
	
  -Tener instaladas las librerías que se utilizarán
---> Nota: Todo lo anterior debe estar en la misma carpeta en la cual se encuentran los archivos de código fuente 

La sintaxis básica de nuestra herramienta es la siguiente:
usage: herra.py [-h] -pi PUERTOI -pf PUERTOF [-se] [-er] [-vh] -inf INFORME

Las opciones de argumentos que puede mostrar son:
  -h, --help            show this help message and exit
  
  -pi PUERTOI, --puertoi PUERTOI
                        puerto donde iniciará el escaneo
                        
  -pf PUERTOF, --puertof PUERTOF
                        puerto donde terminará el escaneo
                        
  -se, --servicios      Si se indica, confirmará que los servicios escenciales estén inciados (guarda en
                        servicios.txt)
                        
  -er, --errores        Si se indica, creará un registro de errores (errores.txt)
  
  -vh, --valorhash      Comprobará la integridad de archivos importantes
  
  -inf INFORME, --informe INFORME
                        Nombre del archivo que contendrá el informe

---> NOTA: POR MOTIVOS DE SEGURIDAD, SE DEBEN SEGUIR LAS SIGUIENTES RECOMENDACIONES:
            < > NO SE DEBE DEJAR LA API_KEY EN EL SCRIPT 
            < > NO SE DEBE DEJAR EL CORREO INTRODUCIDO
            < > NO SE DEBEN DEJAR CONTRASEÑAS EN EL CÓDIGO
                                                                                          
                                                                                          
                                                                                          ^~<#Noviembre/2022/>~^
