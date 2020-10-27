import os
import sys
import argparse
class Node():
    def __init__(self,char,heuristic):
        self.name = char
        self.heuristic = heuristic
        self.visited = False
        self.children = []
        
    def add_child(self, node):
        self.children.append(node)
    def reset_visit(self):
        self.visited = True





def BFS(root):
    queue = []
    closed_nodes = []
    queue.append(root)
    while queue:
        node = queue.pop(0)
        closed_nodes.append(node)
        for child in node.children:
            if not child.visited:
                queue.append(child)
                child.visited = True
        print("OPEN")
        [print(node.name) for node in queue]
        print("---------------------------------")
        print("CLOSED")
        [print(node.name) for node in closed_nodes]
        print("---------------------------------")
            
def DFS(root):
    print(root.name)
    root.visited = True
    for child in root.children:
        if not child.visited:
            DFS(child)

def min_max_node_heuristic(node,minim):
    """
    Finds the max/min child of a given nodes children
    max = True
    min = False
    """
    if node.children == []: return node
    return_node = node.children[0]
    for child in node.children:
        if minim:
            if return_node.heuristic >= child.heuristic:
                return_node = child
        else:
            if return_node.heuristic <= child.heuristic:
                return_node = child

    return return_node


def a_star(root):
    #TODO: Add weights to graph
    return None

def hill_climbing(root,minim):
    print(root.name)
    if not root.children == []:
        node = min_max_node_heuristic(root,minim)
        return hill_climbing(node,minim)
        


def  best_first_search(root):
    queue = []
    queue.append(root)
    closed_nodes = []
    while queue:
        node = queue.pop(0)
        node.visited = True
        closed_nodes.append(node)

        for child in node.children:
            if not child.visited:
                queue.append(child)
        #make the queue a priority queue
        queue.sort(key = lambda x: x.heuristic, reverse = True)
        print("OPEN")
        [print(node.name) for node in queue]
        print("---------------------------------")
        print("CLOSED")
        [print(node.name) for node in closed_nodes]
        print("---------------------------------")




def minimax(node,maxmin):
    value_list = []
    if node.children == []:
        print(f"Node {node.name} is an terminal node returning {node.heuristic}")
        return node.heuristic
    #maximizing player
    if maxmin is True:
        for child in node.children:
            value_list.append(minimax(child,not maxmin))
            value = max(value_list)            
            print(f"Searching from node {node.name}")
        print(f"Max for this layer is {value}")

        return value
    else:
        for child in node.children:
            value_list.append(minimax(child,not maxmin))
            value = min(value_list)
            print(f"Searching from node {node.name}")
        print(f"Min for this layer is {value}")
        return value
     
def minimax_alpha_beta(node, alpha,beta,maxmin):
    value_list = []
    if node.children == []:
        print(f"Node {node.name} is an terminal node returning {node.heuristic}")

        return node.heuristic
    #maximizing player
    if maxmin is True:
        for child in node.children:
            value_list.append(minimax_alpha_beta(child,alpha,beta,not maxmin))
            value = max(value_list)
            
            if value > alpha:
                print(f"Searching from node {node.name}")
                print(f"Max is greater than the alpha changing alpha {alpha} to {value}")
            alpha = max(alpha, value)
            print(f"Alpha {alpha} Beta {beta}")
            if alpha >= beta:
                print(f"Pruning the children of {node.name} after {child.name}")
                break
        return value
    #minimizing player
    else:
        for child in node.children:
            value_list.append(minimax_alpha_beta(child,alpha,beta,not maxmin))
            value = min(value_list)
            if value < beta:
                print(f"Min is less than the beta changing beta {beta} to {value}")
            beta = min(beta, value)
            print(f"Alpha {alpha} Beta {beta}")
            if alpha >= beta:
                print(f"Searching from node {node.name}")
                print(f"Pruning the children of {node.name} after {child.name}")
                break
        return value



def parse_node(parsed_node):
    """
    Creates node from given node description ('node name'/'node value')
    """
    return Node(parsed_node.split('/')[0],int(parsed_node.split('/')[1]))


def exists(node_list,node_to_check):
    for node in node_list:
        if node.name == node_to_check.name:
            return True
    return False

def get_node(node_list,node_to_check):
    for node in node_list:
        if node.name == node_to_check.name:
            return node
    return None

def create_graph_from_input(filename):
    """
    Parses the file in form of 'node_name'/'node value' | 'node_name'/'node value', 'node_name'/'node value'
    where the '|' signifies the children of node of the left side of the '|' seperated by commas
    """
    f = open(filename,"r")
    existing_nodes = []
    for row in f:
        parsing_line = row.split('|')
        root_node = parse_node(parsing_line[0])
        
        if not exists(existing_nodes,root_node):
            existing_nodes.append(root_node)
        else:
            root_node = get_node(existing_nodes,root_node)
        list_of_children = parsing_line[1].split(',')
        for child in list_of_children:
            child_node = parse_node(child)
            if  child_node not in existing_nodes:
                root_node.add_child(child_node)
                existing_nodes.append(child_node)
            else:
                node = get_node(existing_nodes,child)
                root_node.add_child(node)
        
    
    return existing_nodes[0]

def use_algorithm(algorithm_name,root,min_max_node_heuristic=None):
    """
    Parse input with matching algorithm
    """
    switch = {
        'hillclimbing':hill_climbing,
        'alphabeta':minimax_alpha_beta,
        'minimax': minimax,
        'BFS': BFS,
        'DFS': DFS,
        'astar':a_star,
        'bestfirst':best_first_search
    }
    func = switch.get(algorithm_name)
    if algorithm_name == 'alphabeta' and min_max_node_heuristic is not None:
        func(root,-1000,1000,min_max_node_heuristic)
    elif min_max_node_heuristic is not None:
        func(root,min_max_node_heuristic)
    else:
        func(root)
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('Graph File',metavar='-file',type=str, help='File containing the graph')
    parser.add_argument('Algorithm',metavar='-alg',type=str, help='The selected algorithm, can choose from:\
         hill climbing (hillclimbing), Minimax (minimax) ,Breadth-first search (BFS),Depth-first-search (DFS), best first search (bestfirst), A* (astar), and minimax w/ alphabeta pruning (alphabeta)')
    parser.add_argument('Max/Min',metavar='-max',type=str, help='If using hill climbing, minimax, or alpha beta, sepcify if the first or main constraint should be maximum or minimum')
    root_node = create_graph_from_input(sys.argv[1])
    if  sys.argv[2] == 'hillclimbing' or sys.argv[2] == 'minimax' or sys.argv[2] == 'alphabeta':
        bool_string = sys.argv[3].lower()
        bool_eval = True if bool_string == 'true' or bool_string == 'max'  else False 
        use_algorithm(sys.argv[2],root_node,min_max_node_heuristic=bool_eval)
    else:
        use_algorithm(sys.argv[2],root_node)
    print(":) enjoy!")
    pass