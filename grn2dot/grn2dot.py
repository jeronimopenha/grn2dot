import networkx as nx


class Grn2dot:
    _instance = None

    # def __new__(cls):
    #    # if cls._instance is None:
    #    cls._instance = super().__new__(cls)
    #    return cls._instance

    def __init__(self, file_path):
        self.nodes, self.edges, self.equations = self.process_grn_file(self.read_file(file_path))
        self.digraph = nx.DiGraph()
        for node in self.nodes:
            if node in self.equations.keys():
                self.digraph.add_node(node, equation=self.equations[node])
            else:
                self.digraph.add_node(node)
        for key, edges_l in self.edges.items():
            for edge in edges_l:
                self.digraph.add_edge(edge, key)

    def get_nodes_vector(self):
        return self.nodes

    def get_edges_dict(self):
        return self.edges

    def get_equations_dict(self):
        return self.equations

    def get_nx_nodes(self):
        return self.digraph.nodes

    def get_nx_edges(self):
        return self.digraph.edges

    def get_nx_digraph(self):
        return self.digraph

    def get_dot_str(self):
        return nx.nx_agraph.to_agraph(self.digraph)

    def get_num_nodes(self):
        return len(self.nodes)

    def get_num_equations(self):
        return len(self.equations)

    def get_grn_mem_specifications(self):
        grn_mem_specifications = []
        for i in range(self.get_num_nodes()):
            grn_mem_specifications.append([self.get_nodes_vector()[i], i])

        counter = 0
        for key in self.get_equations_dict():
            equation = self.get_equations_dict()[key]
            eq_sp = []
            for i in range(self.get_num_nodes()):
                if self.get_nodes_vector()[i] in equation:
                    eq_sp.append(i)
            eq_sp.sort(reverse=True)
            grn_mem_specifications[counter].append(eq_sp)
            counter = counter + 1

        return grn_mem_specifications

    @staticmethod
    def read_file(file):
        file = open(file)
        content = file.read().split('\n')
        file.close()
        return content

    @staticmethod
    def process_grn_file(lines):
        nodes = []
        edges = {}
        equations = {}
        # treat the equations
        for line in lines:
            if line == '':
                continue
            line = line.strip()
            # looking for equations:
            node = ""
            if '=' in line:
                eq_parts = line.split("=")
                node = eq_parts[0]
                node = node.replace(' ', '')
                node = ' ' + node + ' '
                equations[node] = eq_parts[1]
            else:
                node = line
            if node not in nodes:
                nodes.append(node)

        # looking for edges:
        for key, equation in equations.items():
            # equation = equation.replace(' ', '')
            edges_l = equation
            edges_l = edges_l.replace('(', '')
            edges_l = edges_l.replace(')', '')
            edges_l = edges_l.replace('not', '')
            edges_l = edges_l.replace('and', '')
            edges_l = edges_l.replace('or', '')
            edges_l = edges_l.split(' ')
            e = []
            for edge in edges_l:
                if edge != '':
                    edge = ' ' + edge + ' '
                    e.append(edge)
                    if edge not in nodes:
                        nodes.append(edge)
            edges[key] = e
            # processing equations
            equation = equation.replace(' ','')
            equation = equation.replace('and', '&&')
            equation = equation.replace('or', '||')
            equation = equation.replace('not', '!')
            equation = equation.replace('||', ' || ')
            equation = equation.replace('&&', ' && ')
            equation = equation.replace('!', ' ! ')
            equation = equation.replace('(', ' ( ')
            equation = equation.replace(')', ' ) ')
            equation = " " + equation + " "
            equation = equation.replace("  ", " ")
            equation = equation.replace("   ", " ")
            equations[key] = equation
        return nodes, edges, equations

