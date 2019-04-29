# Erich Johnson
# Com Sci 471
# This project is to implement BFS, DFS, and Uniform Cost Search
# FUNCTION AND CLASSES
# This is to implement Breadth First Search

import sys


class GraphNode:
    weights = []
    next_nodes = []
    known = False

    def __init__(self, node):
        self.nodes_name = node
        self.node_path_to_start = -1  # This is done to show it does not have a path yet
        self.weights = []  # Is the list of weights to the adjacent nodes
        self.next_nodes = []  # Is a list of the adjacent nodes by their nodes_name
        self.path_cost = -1  # This is done as a way to show infinity

    def add_child(self, next_node, weight):  # Adds the weight and the next_node to the list on
        self.weights.append(weight)   # the same time so the same index is for the same node
        self.next_nodes.append(next_node)


class WeightedGraph:

    nodes_list = {}  # nodes_list is in a graph format where (reference, object)

    def __init__(self):
        self.nodes_list = {}

    def add_node_simplified(self, finish):  # add nodes to nodes_list but only contains the name
        new_node = GraphNode(finish)
        # self.nodes_list[finish] = new_node
        self.nodes_list[finish] = new_node

    def add_node(self, start, finish, weight):  # adds a nodes and the relevant information
        start_exist = False
        for ref, node in self.nodes_list.items():  # is the way to go through the nodes_list
            if node.nodes_name == start:  # checks to see the node being added is already there
                start_exist = True
        if start_exist is False:  # if not create a new node
            new_node = GraphNode(start)
            # self.nodes_list[start] = new_node
            self.nodes_list[start] = new_node
        self.nodes_list[start].next_nodes.append(finish)
        self.nodes_list[start].weights.append(weight)

        finish_exist = False
        if len(self.nodes_list) > 1:  # checks to see if the finish node needs to be added
            for ref, node in self.nodes_list.items():
                if node.nodes_name is finish:
                    finish_exist = True
    #                node.previous_node.append(start)
        if finish_exist is False:
            self.add_node_simplified(finish)


def bfs(graph, start, finish):  # Breadth First Graph
    node = start
    graph.nodes_list[start].path_cost = 0
    graph.nodes_list[start].known = True
    if start is finish:  # Make sure start is not also the goal
        return()
    frontier = []  # Frontier is a queue
    finish_found = False
    frontier.append(node)
    while len(frontier) is not 0 and finish_found is False:  # keep going till goal is found or no more nodes in queue
        node = frontier.pop(0)
        graph.nodes_list[node].path_cost = 0  # TBH idk if I need this but the program works so...

        for child in graph.nodes_list[node].next_nodes:  # goes through each adjacent node
            if graph.nodes_list[child].known is False and child not in frontier:  # if the child has not been seen added
                graph.nodes_list[child].known = True  # then the node is added to the search queue and marked as seed
                graph.nodes_list[child].node_path_to_start = graph.nodes_list[node].nodes_name
                if child is finish:
                    return()
                frontier.append(child)  # adds child once we know it is not also the goal
    return()


# This is to implement Depth First Search
def dfs(graph, start, finish):
    stack = []
    stack.append(start)  # creates a stack first end last out
    finish_found = False
    while len(stack) is not 0 or finish_found is False:  # will go till stack is empty or path is found
        start = stack.pop()
        if start is finish:
            finish_found = True
        else:  # will go through node to see if it known yet and then create a stack from the adj nodes not known
            if graph.nodes_list[start].known is False:  # then adds the list to the back of the list
                graph.nodes_list[start].known = True
                temp_stack = []
                for next_node in graph.nodes_list[start].next_nodes:

                     if graph.nodes_list[next_node].known is False:
                         temp_stack.append(next_node)
                        #   stack.append(next_node)
                         graph.nodes_list[next_node].node_path_to_start = start
                temp_stack.sort()
                temp_stack.reverse()
                stack.extend(temp_stack)
    return()


def results(graph, finish):  # prints the results in the desired outcome
    node = finish
    queue = [node]
    while graph.nodes_list[node].node_path_to_start is not -1:
        node = graph.nodes_list[node].node_path_to_start
        queue.append(node)

    queue.reverse()
    print(queue)
    return queue


# this is to implement Uniform Cost Search
def ucs(graph, start, finish):
    node = start
    graph.nodes_list[node].path_cost = 0
    frontier = []  # queue ordered by Path-Cost, with node as the only element
    frontier.append(graph.nodes_list[node])
    finish_found = False
    while len(frontier) is not 0:  # goes till frontier is empty
        node = frontier.pop(0)
        if node.nodes_name is finish:  # checks to see if found goal
            return()
        node.known = True
        iterator = 0
        for child in node.next_nodes:
            temp_path_cost = node.path_cost + node.weights[iterator]
            # if the node has not been seen at all it adds it to the weight list and adding to the queue
            if graph.nodes_list[child].known is False and graph.nodes_list[child] not in frontier:
                graph.nodes_list[child].known = True
                frontier.append(graph.nodes_list[child])
                graph.nodes_list[child].node_path_to_start = node.nodes_name
                graph.nodes_list[child].path_cost = temp_path_cost
            # updates the path and the weight of the path if the path is better than the last one
            elif graph.nodes_list[child] in frontier and graph.nodes_list[child].path_cost > temp_path_cost:
                graph.nodes_list[child].node_path_to_start = node.nodes_name
                graph.nodes_list[child].path_cost = temp_path_cost
            iterator += 1
        # makes sure that the queue is ordered by path_cost from min to max
        sorted(frontier, key=lambda GraphNodeTEMP: GraphNodeTEMP.path_cost)
    return()


# main code

# used to parse command line


FileInput = str(sys.argv[1])
Start_Node = int(sys.argv[2])
End_Node = int(sys.argv[3])
Search_type = str(sys.argv[4])


Graph = WeightedGraph()


# for  line in FileTemp:
with open(FileInput) as FileTemp:
    for line in FileTemp:
        Node, NextNode, Weight = map(int, line.split())  # parses the line and splitting each parses into a int

        original = True
        for ref, node_in_graph in Graph.nodes_list.items():  # checks to see if node was made yet
            if node_in_graph.nodes_name is Node:
                original = False

        if original is True:  # if it wasn't then the node is created like normal
            Graph.add_node(Node, NextNode, Weight)
        elif original is False:  # it adds the child to the node
            Graph.nodes_list[Node].add_child(NextNode, Weight)
            originalFinal = True
            for ref, node_in_graph in Graph.nodes_list.items():
                if node_in_graph.nodes_name is NextNode:
                    originalFinal = False
            if originalFinal is True:
                new_node = GraphNode(NextNode)
                Graph.nodes_list[NextNode] = new_node


if Search_type == "BFS":  # runs if bread first search was found
    bfs(Graph, Start_Node, End_Node)
elif Search_type == "DFS":  # runs if depth first search was found
    dfs(Graph, Start_Node, End_Node)
elif Search_type == "UCS":  # runs if uniform cost search was found
    ucs(Graph, Start_Node, End_Node)
results(Graph, End_Node)