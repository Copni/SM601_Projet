from graph import *

test = Graph("MonGraph", "exemple_cours.txt")
test.display_node()
print("Ce graph contient de svaleurs négatives : " + str(test.has_negative_cost()))
print("Ce graphe contient un cycle : " + str(test.is_cycling()))
test.calc_node_rank()
print("ok")
test.sort_node_by_rank()
test.display_node()
test.display_calendar()