class Node:
    def __init__(self, id, cost, predecessor=None):
        self.id = id
        self.cost = int(cost)
        self.predecessor = []
        self.successor = []
        self.inDegree = 0
        self.rank = 0

    def display(self):
        print(f"Nœud {self.id:<10}  Coût : {self.cost:<10}  Prédécesseurs : {' '.join(self.predecessor):<10}  Successeurs : {' '.join(self.successor):<10} Degrée entrant : {self.inDegree:<10} Rang : {self.rank:<10}")

class Graph:
    def __init__(self, name, file):
        self.name = name
        self.nodeList = []  # Liste des nœuds

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

    '''
    def calc_node_rank(self):
        tmpNodeList = self.nodeList.copy()
        rank = 0

        while tmpNodeList != []:
            for imaginaryNode in tmpNodeList:
                if imaginaryNode.inDegree == 0:
                    for realNode in self.nodeList:
                        if imaginaryNode.id == realNode.id:
                            realNode.rank = rank
                    for successor_id in imaginaryNode.successor:
                        for imaginaryNode in tmpNodeList:
                            if imaginaryNode.id == successor_id:
                                imaginaryNode.predecessor.remove(imaginaryNode.id) if imaginaryNode.id in imaginaryNode.predecessor else None
                                imaginaryNode.inDegree -= 1
                    tmpNodeList.remove(imaginaryNode)
                    rank += 1


    '''
    def calc_node_rank(self):
        tmpNodeList = self.nodeList.copy()
        root = "Alpha"
        rank = 0



        '''
        while tmpNodeList:
            for node in tmpNodeList:
                if node.inDegree == 0:
                    for i in self.nodeList:
                        if(node.id == i.id):
                            i.rank = rank
                    for successor_id in node.successor:
                        successor = next(n for n in self.nodeList if n.id == successor_id)
                        successor.predecessor.remove(node.id)
                        successor.inDegree -= 1
                    tmpNodeList.remove(node)
            rank += 1
            '''


    def sort_node_by_rank(self):
        self.nodeList.sort(key=lambda node: node.rank)



