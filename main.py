from graph import *
test_list = ["exemple_cours.txt", "table 1.txt", "table 2.txt", "table 3.txt", "table 4.txt", "table 5.txt", "table 6.txt", "table 7.txt", "table 8.txt", "table 9.txt", "table 10.txt", "table 11.txt", "table 12.txt", "table 13.txt", "table 14.txt"]

def test_prog(test_list):
    for test in test_list:
        print("TEST DU FICHIER : ", test)
        test = Graphe(test, test)
        print("1 - Chargement du graphe \n")
        test.display_node()
        print("\n\n2 - Recherche de coûts négatifs dans le graphe")
        if test.has_negative_cost():
            print("\n On ne peut donc pas ordonnancer ce graphe\n")
            continue
        print("\n\n3 - Détection de cycle en utilisant l'algorithmme de Roy-Warshall\n")
        if test.is_cycling_explained():
            print("\n On ne peut donc pas ordonnancer ce graphe\n")
            continue
        print("\n\n4 - Calcul du rang de chaque noeud\n")
        test.calc_node_rank()
        test.sort_node_by_rank()
        test.display_node()
        print("\n\n5 - Affichage du calendrier final\n")
        test.display_calendar()

test_prog(test_list)