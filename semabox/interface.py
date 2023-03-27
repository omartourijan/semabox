#Importation des modules
import tkinter as tk
import tkinter.font as font
from tkinter import simpledialog
from main import *
import uuid
import os.path
import sqlite3
import os
import time
import socket



#--------------------------------------------------------------

# Définition du chemin du fichier contenant l'UID
fichier_uid = "uid.txt"

# Vérification si le fichier existe déjà
if os.path.exists(fichier_uid):
    # Lecture de l'UID depuis le fichier
    with open(fichier_uid, "r") as f:
        uid = f.read()
else:
    # Génération d'un nouvel UID
    uid = str(uuid.uuid4())

    # Enregistrement de l'UID dans le fichier
    with open(fichier_uid, "w") as f:
        f.write(uid)
Uid= uid
# Affichage de l'UID
uid =("UID : ", uid)

#conexion a la base de donnes

try:
    #Conexion a la base de donnes
    conn = sqlite3.connect('semabox.db')
    cur = conn.cursor()
    print("Connexion réussie à SQLite")
    
    #Cette commande verifie si la table existe deja ou pas
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='semabox'")
    result = cur.fetchone()

    if not result:
        # Si la table n'existe pas, créez-la   
        with open('schema.sql') as f:
             conn.executescript(f.read())
     
    # Vérifiez si la ligne existe déjà
    cur.execute("SELECT * FROM semabox WHERE uid=?",(Uid,))
    result = cur.fetchone()
    if not result:
        # Si la ligne n'existe pas, insérez-la
        sql = "INSERT INTO semabox  (uid ,hote , domaine, ip , public_ip , ) VALUES (?,?,?,?,?)"
        value = (Uid, Hostname,Domaine_name,Ip,Adresse_ip)
        count = cur.execute(sql,value)
        conn.commit()
        print("Enregistrement inséré avec succès dans la table semabox")
    #fermeture de la base de donnes 
    cur.close()
    conn.close()
    print("Connexion SQLite est fermée")

except sqlite3.Error as error:
    print("Erreur lors de l'insertion dans la table semabox", error)

# Fonction qui affiche les resultat

# Fonction pour ouvrir une seconde fenêtre Tkinter

class ScanReseau(tk.Frame):

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.config(bg="skyblue") # couleur de fond
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.port_label = tk.Label(self, text="Port à scanner : ")
        self.port_label.pack()
        self.port_entry = tk.Entry(self)
        self.port_entry.pack()

        self.subnet_label = tk.Label(self, text="Sous-réseau à scanner ex : 192.168.0.0/24 : ")
        self.subnet_label.pack()
        self.subnet_entry = tk.Entry(self)
        self.subnet_entry.pack()

        self.scan_button = tk.Button(self, text="Scan réseau", command=self.scan_network)
        self.scan_button.pack()

        self.result_label = tk.Label(self, text="", background="skyblue")
        self.result_label.pack()

        self.clear_button = tk.Button(self, text="Effacer le résultat", command=self.clear_result)
        self.clear_button.pack()

    def scan_network(self):
        port = int(self.port_entry.get())
        subnet = self.subnet_entry.get()

        active_ips = []
        threads = []

        def scan_ip(ip, port):
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.5)
            try:
                # Tentative de connexion au port spécifié
                result = sock.connect_ex((str(ip), port))
                if result == 0:
                    # Ajout de l'adresse IP active à la liste
                    active_ips.append(str(ip))
            except:
                pass
            sock.close()

        # Boucle de scan des adresses IP
        for ip in ipaddress.ip_network(subnet).hosts():
            t = threading.Thread(target=scan_ip, args=(ip, port))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        # Affichage des adresses IP actives avec le nom de l'hôte
        if active_ips:
            result_string = "Adresses IP actives avec le port " + str(port) + " ouvert :\n"
            for ip in active_ips:
                try:
                    hostname = socket.gethostbyaddr(ip)[0]
                except:
                    hostname = "Nom d'hôte introuvable"
                result_string += ip + " - " + hostname + "\n"
        else:
            result_string = "Aucune adresse IP active avec le port " + str(port) + " ouvert."
        self.result_label.config(text=result_string, background="skyblue")

    def clear_result(self):
        self.result_label.config(text="",background="skyblue")

def scan_de_port():
    scan = tk.Toplevel(semabox)
    scan.resizable(False,False)
    scan.title("scan de port")
    scan.geometry("300x200")
    label = tk.Label(scan, text="Bienvenue dans ma seconde fenêtre!")
    scan.config(bg="skyblue") # couleur de fond
    app = ScanReseau(master=scan)
    app.mainloop()
    label.pack()

def afficher_info():
    resultats = [uid,hostname,domain_name,ip,adresse_ip]
    for i, resultat in enumerate(resultats):
        label_infos[i].config(text=resultat)


def afficher_etat():
       resultats = ["Etat de la conexion",etat]
       for i, resultat in enumerate(resultats):
           label_etats[i].config(text=resultat)


# Fonction pour effacer les résultats
def effacer_resultats():
     
    for i in range(5):
           label_infos[i].config(text="")



    for i in range(2):
           label_etats[i].config(text="")



# Fonction pour demarrer la semabox

def restart_program():
    semabox.destroy() # Fermer la fenêtre actuelle
    semabox.__init__() # Recréer l'instance de Tk

# Ce code permet de faire un speedtest en download et en upload et retourne les valeurs de ceci en Mbps

def download_speed(file_size, url):
    start = time.time()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((url, 80))
    s.sendall(b'GET /large-file HTTP/1.1\r\nHost: example.com\r\n\r\n')
    s.recv(file_size)
    end = time.time()
    s.close()
    return file_size / (end - start)

def upload_speed(file_size, url):
    start = time.time()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((url, 80))
    s.sendall(b'POST /large-file HTTP/1.1\r\nHost: example.com\r\nContent-Length: file_size\r\n\r\n')
    s.sendall(b'0'*file_size)
    end = time.time()
    s.close()
    return file_size / (end - start)

def display_speeds():
    file_size = 1 # 100MB
    url = "example.com"
    download_speed_result = download_speed(file_size, url)
    upload_speed_result = upload_speed(file_size, url)
    download_label.config(text="Download speed: {:.2f} Mbps".format(download_speed_result))
    upload_label.config(text="Upload speed: {:.2f} Mbps".format(upload_speed_result))


# Interface graphique tkinter

#Declaration de la fenetre 
semabox = tk.Tk()

#Empecher le resize de la fenetre
semabox.resizable(False,False)

semabox.title("SEMABOX")
semabox.geometry("900x550")  # taille de la fentre 
semabox.maxsize(880, 520)  # largeur x hauteur
semabox.config(bg="skyblue") # couleur de fond

# Creation des cadre gauche et droit

left_frame = tk.Frame(semabox, width=250, height=500, bg='skyblue3')
left_frame.place(x=10, y=10)

right_frame = tk.Frame(semabox, width=600, height=500, bg='skyblue3')
right_frame.place(x=270, y=10)

right_frame2 = tk.Frame(semabox, width=600, height=500, bg='skyblue3')
right_frame2.place(x=270, y=10)



#Creation de l'encadrement du titre

info = tk.Frame(right_frame2, width=1000, height=70, bg='skyblue4')
info.place(x=0.5, y=0)

info2 = tk.Frame(info, width=1000, height=70, bg='skyblue4')
info2.place(x=230, y=15)

# Creation du titre

titre = tk.Label(info2, text="SEMABOX", font=("Arial", 24),bg='skyblue4')
titre.pack()

# Creation des cadres droit et gauche dans l'encadremment gauche

tk.Label(left_frame, text="Semabox info",bg="skyblue4").place(relx=0.32, rely=0.05)


# cadre d'affichage des info de la semabox

info = tk.Frame(left_frame, width=400, height=170, bg='white')
info.place(x=0.5, rely=0.15)

info4 = tk.Frame(left_frame ,width=250, height=150, bg='white')
info4.place(x=5, y=75)

info3 = tk.Frame(left_frame, width=100, height=30, bg='skyblue3')
info3.place(x=0.4, rely=0.10)

# Encadrement des button de la semabox

left_frame_left = tk.Frame(left_frame, width=100, height=245, bg='skyblue4')
left_frame_left.place(x=3, rely=0.5)

left_frame_left2 = tk.Frame(left_frame, width=115, height=245, bg='skyblue4')
left_frame_left2.place(x=3, rely=0.5)

left_frame_right = tk.Frame(left_frame, width=115, height=245, bg='skyblue4')
left_frame_right.place(x=130, rely=0.5)

left_frame_right2 = tk.Frame(left_frame, width=115, height=245, bg='skyblue4')
left_frame_right2.place(x=130, rely=0.5)

# Créer le bouton actualiser et qui affiche les info de notre resseau
bouton = tk.Button(info3, text="Actualisation" ,command=afficher_info)
bouton.pack()

#--------------------------------------------------------------------------------

# Créer les étiquettes pour afficher les résultats des ip de la semabox
label_infos = []
for i in range(5):
    label_info = tk.Label(info4,bg='white',font=("arial black", 7))
    label_info.pack(padx=0, pady=5)
    label_infos.append(label_info)


# bouton = tk.Button(left_frame_left2, text="Speed test",command=afficher_speedtest)
# bouton.pack(padx=30, pady=30)

# Creation d'une étiquette pour afficher le résultat du speedtest

info5 = tk.Frame(right_frame2 ,width=250, height=150, bg='skyblue3')
info5.place(x=50, y=100)

# speed test

# Buton pour lance le speed test
button = tk.Button(left_frame_left2, text="SpeedTest")
button.pack(padx=30, pady=30)

    

# button qui afiche l'etat de la conexion

bouton1 = tk.Button(left_frame_left2, text="Etat Actuel", command=afficher_etat)
bouton1.pack(padx=30, pady=30)    

#Creation etiquete pour aficher letat de la conexion 

info6 = tk.Frame(right_frame2 ,width=250, height=150, bg='skyblue3')
info6.place(x=35, y=200)

label_etats = []
for i in range(2):

    label_etat = tk.Label(info6,bg='skyblue3')
    label_etat.pack(padx=30, pady=10)
    label_etats.append(label_etat)

#Creation des Butons

bouton = tk.Button(left_frame_left2, text="Lancer un Scan", command=scan_de_port)
bouton.pack(padx=0, pady=30)


bouton = tk.Button(left_frame_right2, text="Redemarer",command=restart_program )
bouton.pack(padx=30, pady=30)

bouton = tk.Button(left_frame_right2, text="in dev")
bouton.pack(padx=30, pady=30)

effacer_button = tk.Button(left_frame_right2, text="Nettoyer", command=effacer_resultats)
effacer_button.pack(padx=30, pady=30)


#interface du speedtest

    # Créer le titre
titre = tk.Label(info5, text="speedtest", font=("Arial", 13),bg='skyblue3')
titre.pack()

    # Ajouter les widgets
download_label = tk.Label(info5, text="",bg='skyblue3')
upload_label = tk.Label(info5, text="",bg='skyblue3')
test_button = tk.Button(info5, text="Lancer", command=display_speeds)

download_label.pack()
upload_label.pack()
test_button.pack()




# Lancer 
# Démarrer la boucle principale
semabox.mainloop()
