import networkx as nx


class Grn2dot:
    _instance = None

    #def __new__(cls):
    #    # if cls._instance is None:
    #    cls._instance = super().__new__(cls)
    #    return cls._instance

    def __init__(self, file_path):
        self.nodes, self.edges, self.equations = self.process_grn_file(self.read_files(file_path))
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

    def get_dot_str(self):
        return nx.nx_agraph.to_agraph(self.digraph)

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
                equations[node.replace(' ', '')] = eq_parts[1]
            else:
                node = line
            if node not in nodes:
                nodes.append(node.replace(' ', ''))

        # looking for edges:
        for key, equation in equations.items():
            # equation = equation.replace('(', ' ( ')
            # equation = equation.replace(')', ' ) ')
            equation = equation.replace(' ', '')
            edges_l = equation
            edges_l = edges_l.replace('(', '')
            edges_l = edges_l.replace(')', '')
            edges_l = edges_l.replace('not', ' ')
            edges_l = edges_l.replace('and', ' ')
            edges_l = edges_l.replace('or', ' ')
            edges_l = edges_l.split(' ')
            e = []
            for edge in edges_l:
                if edge != '':
                    e.append(edge)
                    if edge not in nodes:
                        nodes.append(edge)
            edges[key] = e
            # processing equations
            equation = equation.replace('and', '&&')
            equation = equation.replace('or', '||')
            equation = equation.replace('not', '!')
            equations[key] = equation
        return nodes, edges, equations
