import csv
import folium
import webbrowser


def read_doc(doc, typedoc, date):
    """
    Fonction créant des listes contenant la lattitude et la longitude d'un lieu, et le nombre
    de données (cas de coronavirus, morts ou personnes soignées )correspondant à ce lieu.
    Une fois stockées ces informations sont utilisées pour créer une carte avec la fonction
    create_map.

    Parameters
    ----------
    doc: document csv
    typedoc: string
    date: string

    Return
    ------
    tabnumbercase: list

    See also
    --------
    fonction create_map
    """
    #Création des listes
    tablattitude = []
    tablongitude = []
    tabnumbercase = []
    #Ajout des données dans les listes
    for i in doc:
        tablattitude.append(i['Lat'])
        tablongitude.append(i['Long'])
        tabnumbercase.append(i[date])
    #Conversion des nombres str en int de la liste tabnumbercase
    for i in range(0, len(tabnumbercase)):
        tabnumbercase[i] = int(tabnumbercase[i])
    for i in range(0,len(tablattitude)):
        tablattitude[i] = str(tablattitude[i])
    for i in range(0,len(tablattitude)):
        tablongitude[i] = str(tablongitude[i])
    #Appel de la fonction create_map
    create_map(tablattitude, tablongitude, tabnumbercase, typedoc)
    return tabnumbercase

#Cas vrai
#file_csv1 = open('coronavirus_conf.csv', 'r')
#read_csv1 = csv.DictReader(file_csv1)
#assert read_doc(read_csv1, "confirmed", "2/28/20") == list

#Cas faux
#file_csv1 = open('coronavirus_conf.csv', 'r')
#read_csv1 = csv.DictReader(file_csv1)
#assert read_doc(read_csv1, "confirmed", "2/28/20") == dict

#Cas limite
#file_csv1 = open('coronavirus_conf.csv', 'r')
#read_csv1 = csv.DictReader(file_csv1)
#assert read_doc(read_csv1, "confirmed", "2/28/20") == []

#Cas hors-limite
#file_csv1 = open('coronavirus_conf.csv', 'r')
#read_csv1 = csv.DictReader(file_csv1)
#assert read_doc(read_csv1, 1, "test") == list


def create_map(lattitude, longitude, numbercase, typedoc):
    """
    Fonction créant une carte avec les données récupérées par la fonction read_doc,
    la fonction fait ensuite un test afin de savoir si le document en question est
    celui des cas confirmés, des morts, ou des guéris du coronavirus elle place ensuite
    les points sur une carte stockée dans un fichier html.

    Parameters
    ----------
    lattitude: list
    longitude: list
    numbercase: list
    typedoc: str

    Return
    ------
    None
    """
    #variable m stockant la carte
    m = folium.Map(
        location=[30.59674644470215, 114.2780990600586], #centrage de la carte sur la Chine
        zoom_start=5, #Zoom sur la Chine
        tiles='Stamen Terrain' #Design de la carte
    )
    if typedoc == "confirmed":
        confirmed = 0
        #Calcul du nombre de personne ayant le coronavirus
        for i in numbercase:
            confirmed = confirmed + i
        print("Cas de coronavirus :", confirmed, "personnes")
        print("")
        #réinitialisation de i
        i = 0
        #placement des points sur la carte
        while i < len(lattitude):
            #suppression des points affichant le nombre 0
            if numbercase[i] != 0:
                folium.Marker([lattitude[i], longitude[i]], popup=numbercase[i],
                              icon=folium.Icon(color="red", icon='ok')).add_to(m)
            i += 1
            m.save('map_confirmed.html')
    if typedoc == "dead":
        dead = 0
        # Calcul du nombre de personne décédées du coronavirus
        for i in numbercase:
            dead = dead + i
        print("Morts :", dead, "personnes")
        print("")
        i = 0
        # placement des points sur la carte
        while i < len(lattitude):
            # suppression des points affichant le nombre 0
            if numbercase[i] != 0:
                folium.Marker([lattitude[i], longitude[i]], popup=numbercase[i],
                              icon=folium.Icon(color="black", icon='screenshot')).add_to(m)
            i += 1
            m.save('map_dead.html')
    if typedoc == "recovered":
        recovered = 0
        # Calcul du nombre de personne guéries du coronavirus
        for i in numbercase:
            recovered = recovered + i
        print("Guéris :", recovered,"personnes")
        print("")
        i = 0
        # placement des points sur la carte
        while i < len(lattitude):
            # suppression des points affichant le nombre 0
            if numbercase[i] != 0:
                folium.Marker([lattitude[i], longitude[i]], popup=numbercase[i],
                              icon=folium.Icon(color="green", icon='heart')).add_to(m)
            i += 1
            m.save('map_recovered.html')

#Cas vrai
#assert create_map([30], [114], [5], "confirmed") == Point créé en Chine avec le nombre 5 affiché (stocké dans map_confirmed.html)

#Cas faux
#assert create_map([30], [114], [5], "confirmed") == Point créé en France avec le nombre 83 affiché (stocké dans map_death.html)

#Cas limite
#assert create_map([], [], [], "") == False

#Cas hors-limite
#assert create_map([30], [114], [5], "confirmed") == 25

def choice():
    """
    Fonction demandant à l'utilisateur s'il souhaite ouvrir le fichier html index.html
    s'il répond 1, le fichier s'ouvre sur un navigateur, s'il répond 2, le fichier ne s'ouvre pas.
    La fonction prend en compte les erreurs d'entrées de l'utilisateur.

    Parameters
    ----------
    None

    Return
    ------
    None
    """
    while True:
        try:
            #choix de l'utilisateur
            choice = int(input("Ouvrir le site répertoriant les cartes du coronavirus (1), ne pas ouvrir le site "
                           "répertoriant les cartes (2)."))
            #Vérification que l'utilisateur a bien rentré le nombre 1 ou 2
            if choice == 1 or choice == 2:
                #si l'utilisateur souhaite ouvrir le fichier html
                if choice == 1:
                    #ouverture du navigateur
                    webbrowser.open_new_tab('file:///F:/NSI/projet/coronavirus/index.html#') #changer la direction du fichier
                    break
                #si l'utilisateur ne souhaite pas ouvrir le fichier html
                else:
                    print(
                        "Vous avez choisi de ne pas lancer le site répertoriant les cartes de l'avancée du coronavirus, vous pouvez quand même "
                        "le trouver dans le dossier coronavirus sous le nom index.html.")
                    break
            #nombre différent de 1 ou 2
            else:
                print("Saisie incorrecte :")
        #Rentrée incorrecte
        except ValueError:
            print("Saisie incorrecte :")

#cas vrai
#assert choice() == fin du programme

#cas faux
#assert choice() == programme infini



###########################################
#     	Programme Principal
###########################################

# Création d'un flux de lecture vers le fichier passé en paramètre

file_csv1 = open('time_series_19-covid-Confirmed.csv', 'r')
file_csv2 = open('time_series_19-covid-Deaths.csv', 'r')
file_csv3 = open('time_series_19-covid-Recovered.csv', 'r')

# Lecture du fichier CSV dans un flux CSV en fonction des entêtes de la première ligne du CSV
read_csv1 = csv.DictReader(file_csv1)
read_csv2 = csv.DictReader(file_csv2)
read_csv3 = csv.DictReader(file_csv3)

#Pour actualiser récupérer les fichiers sur https://github.com/CSSEGISandData/COVID-19
date = str(input("Rentrez une date que vous souhaitez consulter sous la forme mm/jj/aa (exemple 2/21/20) : "))


print("Statistiques du coronavirus : ")

read_doc(read_csv1, "confirmed", date)
#read_doc(read_csv2, "dead", date)
#read_doc(read_csv3, "recovered", date)




# Fermeture du flux de lecture sur le fichier
file_csv1.close()
file_csv2.close()
file_csv3.close()

choice()







