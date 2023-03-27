#Importation des modules

import requests
import socket
import threading
import time
import ipaddress
import os
from tkinter import simpledialog

#Definition des fonction

# Ce code permet de voir si la connection à google est établie ou non

#ok
def get_connection_status():
    try:
        response = requests.get("http://google.com", timeout=5)
        if response.status_code == 200:
            conexion = "vous êtes bien connecté"
            return conexion
        else:
            conexion = "déconnecté"
            return conexion
    except requests.exceptions.RequestException:
        conexion = "déconnecté"
        return conexion
    
# Ce code récupère le nom d'hôte ainsi que le domaine et son adresse ip et l'adresse publique

def get_ip_and_domain_name():
    hostname = socket.gethostname()
    domain_name = socket.getfqdn(hostname)
    ip = socket.gethostbyname(hostname)
    publique_ip = requests.get('https://api.ipify.org')
    adresse_ip = publique_ip.text
    return hostname, domain_name, ip,adresse_ip


#Appele de la fonction

#---------------------------------------------------------------------1

# Etat de la conexion

etat = get_connection_status()

if etat == "vous êtes bien connecté":

    # Semabox info
    
    hostname, domain_name, ip,adresse_ip = get_ip_and_domain_name()

    # Variable pour la base de donnes

    Hostname = hostname
    Domaine_name = domain_name
    Ip = ip
    Adresse_ip = adresse_ip

    hostname = "Nom d'hôte", hostname
    domain_name = "Nom de domaine : ", domain_name
    ip = "Adresse IP : ", ip
    adresse_ip = "ip publique : " , adresse_ip

else :

    hostname = etat
    domain_name = etat
    ip = etat
    adresse_ip = etat


#---------------------------------------------------------------------2
