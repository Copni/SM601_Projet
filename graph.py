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
            f"Nœud {self.id:<10}  Coût : {self.cost:<10}  Prédécesseurs : {' '.join([pred.id for pred in self.predecessor]):<10}  Successeurs : {' '.join([suc.id for suc in self.successor]):<10} Rang : {self.rank if self.rank is not None else 'N/A':<10} Degré entrant : {self.inDegree:<10}")

class Graphe:
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

            # Ajout d'Alpha en tête
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

            # Conversion des id des prédécesseurs et successeurs par leurs adresses
            for node in self.nodeList:
                for i in range(len(node.predecessor)):
                    node.predecessor[i] = self.find_node(node.predecessor[i])
                for i in range(len(node.successor)):
                    node.successor[i] = self.find_node(node.successor[i])
        else :
            if isinstance(file, list) and all(isinstance(node, Node) for node in file):
                self.name = name
                self.nodeList = file
            else:
                print("Erreur de type")

    def find_node(self, id):
        for i in range(len(self.nodeList)):
            if id == self.nodeList[i].id:
                return self.nodeList[i]
        return False

    def duplicate(self, name = None):
        d = deepcopy(self)
        if name is not None:
            d.name = str(name)
        return d

    def duplicate_node_list(self):
        return deepcopy(self.nodeList)

    def display_node(self):
        if self.nodeList == []:
            print("Ce graphe est vide")
        else:
            for node in self.nodeList:
                node.display()  # Utilisation de la méthode de `Node`

    def has_negative_cost(self):
        for node in self.nodeList:
            if node.cost < 0:
                print("\n🔴 Ce graphe contient des coûts négatifs")
                return True
        print("\n✅ Ce graphe n'a que des coûts positifs")
        return False

    def display_adj_matrix(self):
        n = len(self.nodeList)
        adj = [[0] * n for _ in range(n)]

        # Création de la matrice d'adjacence
        for i in range(n):
            for j in range(n):
                if self.nodeList[j] in self.nodeList[i].successor:
                    adj[i][j] = 1

        # Définir les caractères de dessin de boîte
        horizontal = '─'
        vertical = '│'
        top_left = '┌'
        top_right = '┐'
        bottom_left = '└'
        bottom_right = '┘'
        cross = '┼'
        left_t = '├'
        right_t = '┤'
        top_t = '┬'
        bottom_t = '┴'

        # Construire la première ligne (en-tête)
        header = f"{top_left}{horizontal * 8}{top_t}" + f"{horizontal * 8}{top_t}" * (
                    n - 1) + f"{horizontal * 8}{top_right}"
        print(header)
        header = f"{vertical}{'':^8}{vertical}" + "".join(f"{node.id:^8}{vertical}" for node in self.nodeList)
        print(header)
        separator = f"{left_t}{horizontal * 8}{cross}" + f"{horizontal * 8}{cross}" * (
                    n - 1) + f"{horizontal * 8}{right_t}"
        print(separator)

        # Affichage de chaque ligne de la matrice
        for i in range(n):
            row = f"{vertical}{self.nodeList[i].id:^8}{vertical}" + "".join(
                f"{adj[i][j] if adj[i][j] != 0 else '':^8}{vertical}" for j in range(n))
            print(row)
            if i < n - 1:
                print(separator)
            else:
                footer = f"{bottom_left}{horizontal * 8}{bottom_t}" + f"{horizontal * 8}{bottom_t}" * (
                            n - 1) + f"{horizontal * 8}{bottom_right}"
                print(footer)


    def is_cycling(self):
        n = len(self.nodeList)
        adj = [[0] * n for _ in range(n)]

        # Création de la matrice d'adjacence
        for i in range(n):
            for j in range(n):
                if self.nodeList[j] in self.nodeList[i].successor:
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

    def is_cycling_explained(self):
        n = len(self.nodeList)
        adj = [[0] * n for _ in range(n)]

        # Création de la matrice d'adjacence
        for i in range(n):
            for j in range(n):
                if self.nodeList[j] in self.nodeList[i].successor:
                    adj[i][j] = 1

        # Définition des symboles pour l'affichage des matrices
        horizontal = '─'
        vertical = '│'
        top_left = '┌'
        top_right = '┐'
        bottom_left = '└'
        bottom_right = '┘'
        cross = '┼'
        left_t = '├'
        right_t = '┤'
        top_t = '┬'
        bottom_t = '┴'
        space = " " * 10  # Espacement entre les matrices

        # Fonction pour construire une matrice sous forme de texte
        def build_matrix(matrix, title):
            lines = []
            lines.append(f"{title}:")
            header = f"{top_left}" + f"{horizontal * 3}{top_t}" * (n - 1) + f"{horizontal * 3}{top_right}"
            lines.append(header)

            for i, row in enumerate(matrix):
                row_str = f"{vertical}" + "".join(f"{val:^3}{vertical}" for val in row)
                lines.append(row_str)

                if i < n - 1:  # Lignes intermédiaires
                    separator = f"{left_t}" + f"{horizontal * 3}{cross}" * (n - 1) + f"{horizontal * 3}{right_t}"
                    lines.append(separator)

            footer = f"{bottom_left}" + f"{horizontal * 3}{bottom_t}" * (n - 1) + f"{horizontal * 3}{bottom_right}"
            lines.append(footer)
            return lines

        # Génération de la matrice d'adjacence
        adj_matrix_text = build_matrix(adj, "Matrice d'adjacence")

        # Application de l'algorithme de Roy-Warshall
        for k in range(n):
            for i in range(n):
                for j in range(n):
                    adj[i][j] = adj[i][j] or (adj[i][k] and adj[k][j])

        # Génération de la matrice de transitivité
        adj_matrix_text = build_matrix(adj, "Matrice d'adjacence")
        trans_matrix_text = [" " * 10 + line for line in build_matrix(adj, "Matrice de transitivité")]

        # Affichage côte à côte des matrices
        print("\n".join(
            f"{adj_line}{space}{trans_line}" for adj_line, trans_line in zip(adj_matrix_text, trans_matrix_text)))

        # Vérification de la présence d'un cycle
        for i in range(n):
            if adj[i][i] == 1:
                print("🔴 Détection d'un 1 dans la grande diagonale -> Ce graphe à un cycle !")
                return True

        print("✅ Grande diagonale composée uniquement de 0 -> Ce graphe n'a pas de cycle")
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
                for suc in root.successor:
                    suc.inDegree -= 1
                    suc.predecessor.remove(root)

                # On attribue le rang au noeud racine de la liste originale
                for i in self.nodeList:
                    if root.id == i.id:
                        i.rank = rank

                # On supprime le noeud racine de la liste temporaire
                tmp_graph.nodeList.remove(root)

            rank += 1


    def sort_node_by_rank(self):
        self.nodeList.sort(key=lambda node: node.rank)

    def calc_earliest(self, node):
        if node not in self.nodeList:
            print("Le noeud n'est pas dans le graphe")
            return False

        if not node.predecessor:  # Si le nœud n'a pas de prédécesseurs, date au plus tôt = 0
            return [0, None]

        max_cost = 0  # Stocke le coût maximal parmi tous les chemins
        best_pred = None  # Stocke le meilleur prédécesseur

        for pred in node.predecessor:
            path_cost, _ = self.calc_earliest(pred)  # On récupère uniquement le coût
            path_cost += pred.cost

            if path_cost > max_cost:
                max_cost = path_cost
                best_pred = pred  # Met à jour le meilleur prédécesseur

        return [max_cost, best_pred]

    def calc_latest(self, node, project_duration):
        if node not in self.nodeList:
            print("Le noeud n'est pas dans le graphe")
            return False

        if not node.successor:  # Si le nœud n'a pas de successeurs, sa date au plus tard est égale à la durée du projet
            return [project_duration, None]

        min_cost = float('inf')  # Stocke le coût minimal parmi tous les chemins
        best_succ = None  # Stocke le meilleur successeur

        for succ in node.successor:
            path_cost, _ = self.calc_latest(succ, project_duration)  # Récupère latest du successeur
            path_cost -= node.cost  # On soustrait la durée de la tâche actuelle

            if path_cost < min_cost:
                min_cost = path_cost
                best_succ = succ  # Met à jour le meilleur successeur

        return [min_cost, best_succ]

    def calc_margins(self, node, project_duration):
        earliest, _ = self.calc_earliest(node)  # Récupération de la date au plus tôt
        latest, _ = self.calc_latest(node, project_duration)  # Récupération de la date au plus tard

        margin = latest - earliest  # Calcul de la marge totale

        return margin


    def display_calendar(self):
            # Trier les nœuds par rang
            self.sort_node_by_rank()

            # Définir les caractères de dessin de boîte
            horizontal = '─'
            vertical = '│'
            top_left = '┌'
            top_right = '┐'
            bottom_left = '└'
            bottom_right = '┘'
            cross = '┼'
            left_t = '├'
            right_t = '┤'
            top_t = '┬'
            bottom_t = '┴'

            # Construire les lignes du tableau
            ranks = [str(node.rank) for node in self.nodeList if node.rank is not None]
            nodes = [f"{node.id} ({node.cost})" for node in self.nodeList]
            predecessors = [', '.join(pred.id for pred in node.predecessor) for node in self.nodeList]
            earliest_dates = [
                f"{self.calc_earliest(node)[0]} ({self.calc_earliest(node)[1].id if self.calc_earliest(node)[1] else ''})"
                for node in self.nodeList]
            latest_dates = [
                f"{self.calc_latest(node, self.calc_earliest(self.find_node('Omega'))[0])[0]} ({self.calc_latest(node, self.calc_earliest(self.find_node('Omega'))[0])[1].id if self.calc_latest(node, self.calc_earliest(self.find_node('Omega'))[0])[1] else ''})"
                for node in self.nodeList]
            margins = [str(self.calc_margins(node, self.calc_earliest(self.find_node('Omega'))[0])) for node in self.nodeList]

            # Déterminer la largeur des colonnes
            max_rank_width = max(len("rang"), max(len(rank) for rank in ranks))
            max_node_width = max(len("Noeud et coût"), max(len(node) for node in nodes))
            max_pred_width = max(len("Prédécesseurs"), max(len(pred) for pred in predecessors))
            max_earliest_width = max(len("Date au plus tôt"), max(len(date) for date in earliest_dates))
            max_latest_width = max(len("Date au plus tard"), max(len(date) for date in latest_dates))
            max_margin_width = max(len("Marge totale"), max(len(margin) for margin in margins))

            # Construire la première ligne (rangs)
            first_line = f"{top_left}{horizontal * (max_rank_width + 2)}{top_t}{horizontal * (max_node_width + 2)}{top_t}{horizontal * (max_pred_width + 2)}{top_t}{horizontal * (max_earliest_width + 2)}{top_t}{horizontal * (max_latest_width + 2)}{top_t}{horizontal * (max_margin_width + 2)}{top_right}"
            second_line = f"{vertical} {'rang'.ljust(max_rank_width)} {vertical} {'Noeud et coût'.ljust(max_node_width)} {vertical} {'Prédécesseurs'.ljust(max_pred_width)} {vertical} {'Date au plus tôt'.ljust(max_earliest_width)} {vertical} {'Date au plus tard'.ljust(max_latest_width)} {vertical} {'Marge totale'.ljust(max_margin_width)} {vertical}"
            third_line = f"{left_t}{horizontal * (max_rank_width + 2)}{cross}{horizontal * (max_node_width + 2)}{cross}{horizontal * (max_pred_width + 2)}{cross}{horizontal * (max_earliest_width + 2)}{cross}{horizontal * (max_latest_width + 2)}{cross}{horizontal * (max_margin_width + 2)}{right_t}"

            # Construire les lignes de données
            data_lines = []
            for rank, node, pred, earliest, latest, margin in zip(ranks, nodes, predecessors, earliest_dates, latest_dates, margins):
                data_lines.append(f"{vertical} {rank.ljust(max_rank_width)} {vertical} {node.ljust(max_node_width)} {vertical} {pred.ljust(max_pred_width)} {vertical} {earliest.ljust(max_earliest_width)} {vertical} {latest.ljust(max_latest_width)} {vertical} {margin.ljust(max_margin_width)} {vertical}")

            # Construire la dernière ligne
            last_line = f"{bottom_left}{horizontal * (max_rank_width + 2)}{bottom_t}{horizontal * (max_node_width + 2)}{bottom_t}{horizontal * (max_pred_width + 2)}{bottom_t}{horizontal * (max_earliest_width + 2)}{bottom_t}{horizontal * (max_latest_width + 2)}{bottom_t}{horizontal * (max_margin_width + 2)}{bottom_right}"

            # Afficher le tableau
            print(first_line)
            print(second_line)
            print(third_line)
            for line in data_lines:
                print(line)
            print(last_line)


