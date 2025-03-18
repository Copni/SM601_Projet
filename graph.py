from copy import deepcopy

class Node:
    def __init__(self, id, cost, predecessor=None, successor=None, inDegree=None, rank=None):
        self.id = str(id)
        self.cost = int(cost)
        self.predecessor = predecessor if predecessor is not None else []
        self.successor = successor if successor is not None else []
        self.inDegree = inDegree
        self.rank = rank


    def duplicate(self, name = None):
        d = deepcopy(self)
        if name is not None:
            d.id = str(name)
        return d


    def display(self):
        print(
            f"Nœud {self.id:<10}  Coût : {self.cost:<10}  Prédécesseurs : {' '.join(self.predecessor):<10}  Successeurs : {' '.join(self.successor):<10} Degrée entrant : {self.inDegree if self.inDegree is not None else 'N/A':<10} Rang : {self.rank if self.rank is not None else 'N/A':<10}")


class Graph:
    def __init__(self, name, file=None):
        self.name = str(name)
        self.nodeList = []  # Liste des nœuds

        if isinstance(file, str) :
            with open(file, 'r') as f:
                lines = f.readlines()

                for i in range(len(lines)):

                    node_data = lines[i].strip('\n') # On retire le saut à la ligne
                    node_data = node_data.split() # On sépare la chaine de caractère à chaque espace
                    node = Node(node_data[0], node_data[1])
                    if(len(node_data) > 2):
                        node.predecessor = node_data[2:]

                    self.nodeList.append(node)  # Ajout du nœud à la liste

            # On met à jour les successeurs
            for node in self.nodeList:
                for i in self.nodeList:
                    if node.id in i.predecessor:
                        node.successor.append(i.id)
                node.successor = list(set(node.successor))

            # On ajoute Alpha et Omega

            alpha_node = Node("Alpha", 0)
            omega_node = Node("Omega", 0)

            # Ajouter d'Alpha en tête
            self.nodeList.insert(0, alpha_node)
            for node in self.nodeList[1:]:
                if not node.predecessor:
                    node.predecessor.append("Alpha")
                    alpha_node.successor.append(node.id)

            # Ajout d'Omega en dernière position
            self.nodeList.append(omega_node)
            for node in self.nodeList[:-1]:
                if not node.successor:
                    node.successor.append("Omega")
                    omega_node.predecessor.append(node.id)

            # Calcul du degré entrant de chaque nœud
            for node in self.nodeList:
                node.inDegree = len(node.predecessor)
        else :
            if isinstance(file, list) and all(isinstance(node, Node) for node in file):
                self.name = name
                self.nodeList = file
            else:
                print("Erreur de type")


    def duplicate(self, name = None):
        d = deepcopy(self)
        if name is not None:
            d.name = str(name)
        return d

    def duplicateNodeList(self):
        return deepcopy(self.nodeList)


    def display_node(self):
        if self.nodeList == []:
            print("Ce graph est vide")
        else:
            print(f"Graph : {self.name}\n")
            for node in self.nodeList:
                node.display()  # Utilisation de la méthode de `Node`


    def has_negative_cost(self):
        for node in self.nodeList:
            if node.cost < 0:
                return True
        return False

    def is_cycling(self):
        n = len(self.nodeList)
        adj = [[0] * n for _ in range(n)]

        # Création de la matrice d'adjacence
        for i in range(n):
            for j in range(n):
                if self.nodeList[j].id in self.nodeList[i].successor:
                    adj[i][j] = 1

        # Application de l'algorithme de Roy-Warshall (cf lien Wikipedia du cours)
        for k in range(n):
            for i in range(n):
                for j in range(n):
                    adj[i][j] = adj[i][j] or (adj[i][k] and adj[k][j])

        # Vérification de la présence de cycle
        for i in range(n):
            if adj[i][i] == 1:
                return True
        return False


    def find_node(self, id):
        for i in range(len(self.nodeList)):
            if id == self.nodeList[i].id:
                return self.nodeList[i]
        return False

    def calc_node_rank(self):
        tmp_graph = self.duplicate("duplicate_graph")

        # On initialise rank
        rank = 0

        # On applique l'algorithme de calcul de rang
        while tmp_graph.nodeList:
            # Trouver tous les nœuds sans prédécesseurs
            zero_in_degree_nodes = [node for node in tmp_graph.nodeList if not node.predecessor]

            # Si aucun nœud sans prédécesseur n'est trouvé, il y a un cycle
            if not zero_in_degree_nodes:
                print("Cycle détecté, impossible de calculer les rangs")
                return

            for root in zero_in_degree_nodes:

                # On supprime le noeud racine des prédécésseurs des successeurs
                for suc_id in root.successor:
                    suc = tmp_graph.find_node(suc_id)
                    suc.inDegree -= 1
                    suc.predecessor.remove(root.id)

                # On attribut le rang au noeud racine de la list originale
                for i in self.nodeList:
                    if root.id == i.id:
                        i.rank = rank

                # On supprime le noeud racine de la liste temporaire
                tmp_graph.nodeList.remove(root)

            rank += 1

    def sort_node_by_rank(self):
        self.nodeList.sort(key=lambda node: node.rank)


