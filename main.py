from graph import *
import os

test_list = ['exemple_cours.txt', "table 1.txt", "table 2.txt", "table 3.txt", "table 4.txt", "table 5.txt", "table 6.txt", "table 7.txt", "table 8.txt", "table 9.txt", "table 10.txt", "table 11.txt", "table 12.txt", "table 13.txt", "table 14.txt"]


def test_prog(test_list):
    for test in test_list:
        print("TEST DU FICHIER : ", test)
        test = Graphe(test, test)
        print("1 - Chargement du graphe et matrice des valeurs\n")
        test.display_node()
        print()
        test.display_value_matrix()
        print("\n\n2 - Recherche de coûts négatifs dans le graphe")
        if test.has_negative_cost():
            print("\n On ne peut donc pas ordonnancer ce graphe\n")
            continue
        print("\n\n3 - Détection de cycle en utilisant l'algorithmme de Roy-Warshall\n")
        if test.is_cycling_explained():
            print("\n On ne peut donc pas ordonnancer ce graphe\n")
            continue
        print("\n\n4 - Calcul du rang de chaque noeud\n")
        test.calc_node_rank_explained()
        test.sort_node_by_rank()
        test.display_node()
        print("\n\n5 - Affichage du calendrier final\n")
        test.display_calendar()
        print("\n\n6 - Affichage des chemins\n")
        test.display_extrem_path()
        print("\nChemin critique : ")
        test.display_critical_path()
        print("\n")

def menu():
    txt_files = [f for f in os.listdir('.') if f.endswith('.txt')]
    if not txt_files:
        print("Aucun fichier .txt trouvé dans le répertoire courant.")
        return

    print("Sélectionnez un fichier à tester :")
    for i, file in enumerate(txt_files, 1):
        print(f"{i}. {file}")

    choice = int(input("Entrez le numéro du fichier (0 pour quitter) : "))
    if choice == 0:
        print("Quitter le programme.")
        return
    elif 1 <= choice <= len(txt_files):
        selected_file = txt_files[choice - 1]
        test_prog([selected_file])
        menu()
    else:
        print("Choix invalide.")
        menu()

menu()