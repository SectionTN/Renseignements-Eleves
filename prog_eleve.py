from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QApplication, QMessageBox, QTableWidgetItem
from numpy import array
from pickle import load, dump


def compterChar(ch, c):
    nombre = 0
    for i in range(len(ch)):
        if ch[i] == c:
            nombre += 1
    return nombre


def verifDateNaissance(ch):
    if ch.find("/") == -1:
        return False
    if compterChar(ch, "/") != 2:
        return False

    premier_slash = ch.find("/")
    deuxieme_slash = ch.find("/", premier_slash + 1)

    jour = ch[:premier_slash]
    mois = ch[premier_slash + 1: deuxieme_slash]
    annee = ch[deuxieme_slash + 1:]

    if not (jour.isdigit() and mois.isdigit() and annee.isdigit()):
        return False

    jour = int(jour)
    mois = int(mois)
    annee = int(annee)

    annee_courante = 2024

    if not (1900 <= annee <= annee_courante):
        return False
    if not (1 <= mois <= 12):
        return False
    if not (1 <= jour <= 31):
        return False
    return True


def verifEmail(ch):
    if "@" not in ch or ch[0] == "@" or ch[-1] == "@" or compterChar(ch, "@") != 1:
        return False
    position_at = ch.find("@")
    partie_locale = ch[:position_at]
    partie_domaine = ch[position_at + 1:]
    if partie_locale != "" and partie_domaine != "":
        if "." in partie_domaine and compterChar(partie_domaine, ".") == 1:
            return True
    return False


def ajouter():
    matricule = window.matricule.text()
    prenom = window.prenom.text()
    nom = window.nom.text()
    datenaissance = window.daten.text()
    email = window.email.text()
    masculin = window.r_masculin.isChecked()
    feminin = window.r_feminin.isChecked()
    section = window.section.currentText()
    moyenne = window.moyenne.text()
    option_musique = window.c_musique.isChecked()
    option_dessin = window.c_dessin.isChecked()
    option_italien = window.c_italien.isChecked()
    if matricule == "" or prenom == "" or nom == "" or (masculin is False and feminin is False) or moyenne == "":
        QMessageBox.critical(window, "Erreur de saisie", "Saisir toutes les informations", QMessageBox.Ok)
    elif datenaissance == "" or not verifDateNaissance(datenaissance):
        QMessageBox.critical(window, "Erreur de saisie", "Date de Naissance malformé ou incorrecte", QMessageBox.Ok)
    elif email == "" or not verifEmail(email):
        QMessageBox.critical(window, "Erreur de saisie", "Email Malformé ou incorrecte", QMessageBox.Ok)
    elif section == "Selectionner Votre Section":
        QMessageBox.critical(window, "Erreur de saisie", "Choix de Section obligatoire", QMessageBox.Ok)
    elif not option_italien and not option_dessin and not option_musique:
        QMessageBox.critical(window, "Erreur de saisie", "Choix de Option(s) obligatoire", QMessageBox.Ok)
    else:
        file_eleve = open("eleves.dat", "ab")
        e = dict(matricule=str, prenom=str, nom=str, datenaissance=str, email=str, genre=str, section=str, moyenne=str,
                 options=str)
        genre = "M"
        if feminin:
            genre = "F"
        option = ""
        if option_musique:
            option += "Musique" + " "
        if option_italien:
            option += "Italien" + " "
        if option_dessin:
            option += "Dessin" + " "

        e["matricule"] = matricule
        e["nom"] = nom
        e["prenom"] = prenom
        e["datenaissance"] = datenaissance
        e["email"] = email
        e["genre"] = genre
        e["section"] = section
        e["moyenne"] = moyenne
        e["options"] = option
        dump(e, file_eleve)
        file_eleve.close()
        QMessageBox.information(window, "Ajout Complet", "Votre inscription est effectuée", QMessageBox.Ok)


def taille_fichier_dat():
    file_eleve = open("eleves.dat", "rb")
    i = 0
    eof = False
    try:
        while not eof:
            e = load(file_eleve)
            i += 1
    except:
        eof = True
        file_eleve.close()
    return i


def afficher():
    file_eleve = open("eleves.dat", "rb")
    N = taille_fichier_dat()
    window.t_toute_eleves.setRowCount(N)
    for i in range(N):
        e = load(file_eleve)
        window.t_toute_eleves.setItem(i, 0, QTableWidgetItem(e["matricule"]))
        window.t_toute_eleves.setItem(i, 1, QTableWidgetItem(e["nom"] + " " + e["prenom"]))
        window.t_toute_eleves.setItem(i, 2, QTableWidgetItem(e["genre"]))
        window.t_toute_eleves.setItem(i, 3, QTableWidgetItem(e["section"]))
        window.t_toute_eleves.setItem(i, 4, QTableWidgetItem(e["moyenne"]))
        window.t_toute_eleves.setItem(i, 5, QTableWidgetItem(e["options"]))
    file_eleve.close()


def percentage():
    file_eleve = open("eleves.dat", "rb")
    N = taille_fichier_dat()
    admis = 0
    fournee = 0
    refuse = 0
    for i in range(N):
        e = load(file_eleve)
        moyenne = float(e["moyenne"])
        if moyenne > 10:
            admis += 1
        elif 7 < moyenne < 10:
            fournee += 1
        else:
            refuse += 1
    admis = (admis / N) * 100
    fournee = (fournee / N) * 100
    refuse = (refuse / N) * 100
    window.i_admis.setText(str(admis))
    window.i_ajourne.setText(str(fournee))
    window.i_refuse.setText(str(refuse))
    file_eleve.close()


def annuler():
    window.matricule.setText("")
    window.prenom.setText("")
    window.nom.setText("")
    window.daten.setText("")
    window.email.setText("")
    window.r_masculin.setChecked(False)
    window.r_feminin.setChecked(False)
    window.section.setCurrentIndex(0)
    window.moyenne.setText("")
    window.c_musique.setChecked(False)
    window.c_dessin.setChecked(False)
    window.c_italien.setChecked(False)


def bulle(T, N):
    for i in range(N):
        for j in range(N - i - 1):
            if float(T[j]["moyenne"]) < float(T[j + 1]["moyenne"]):
                aux = T[j]
                T[j] = T[j + 1]
                T[j + 1] = aux

def classement():
    file_eleve = open("eleves.dat", "rb")
    N = taille_fichier_dat()
    T = array([dict] * N)
    window.t_toute_eleves.setRowCount(N)
    for i in range(N):
        e = load(file_eleve)
        T[i] = e
    file_eleve.close()
    bulle(T, N)
    window.t_toute_eleves.clear()
    window.t_toute_eleves.setRowCount(N)
    window.t_toute_eleves.setHorizontalHeaderLabels(
        ["Matricule", "Nom et Prénom", "Genre", "Section", "Moyenne", "Option(s)"])
    for k in range(N):
        window.t_toute_eleves.setItem(k, 0, QTableWidgetItem(T[k]["matricule"]))
        window.t_toute_eleves.setItem(k, 1, QTableWidgetItem(T[k]["prenom"] + " " + T[k]["nom"]))
        window.t_toute_eleves.setItem(k, 2, QTableWidgetItem(T[k]["genre"]))
        window.t_toute_eleves.setItem(k, 3, QTableWidgetItem(T[k]["section"]))
        window.t_toute_eleves.setItem(k, 4, QTableWidgetItem(T[k]["moyenne"]))
        window.t_toute_eleves.setItem(k, 5, QTableWidgetItem(T[k]["options"]))


def afficher_admis():
    window.l_eleve_admis.clear()
    file_eleve = open("eleves.dat", "rb")
    N = taille_fichier_dat()
    window.l_eleve_admis.addItem("Les élèves admis sont:")
    for i in range(N):
        e = load(file_eleve)
        nom_complete = e["prenom"] + " " + e["nom"]
        moyenne = float(e["moyenne"])
        if moyenne > 10:
            window.l_eleve_admis.addItem(nom_complete)
    file_eleve.close()


def fermer():
    return window.close()


application = QApplication([])
window = loadUi("interface_eleve.ui")
window.b_quitter.clicked.connect(fermer)
window.b_ajouter.clicked.connect(ajouter)
window.b_annuler.clicked.connect(annuler)
window.b_aff_tous_elev.clicked.connect(afficher)
window.b_percentage.clicked.connect(percentage)
window.b_classement.clicked.connect(classement)
window.b_nompre_admis.clicked.connect(afficher_admis)
window.show()
application.exec_()
