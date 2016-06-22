__author__ = 'sam.royston'

from xml.etree.cElementTree import SubElement, ElementTree, Element
from datetime import datetime
import os

class Node(object):
    def __init__(self, id, label = None, attributes=None, x=None, y=None, z=None, r=None, g=None, b=None, size=1):
        self.id = id
        if label is None:
            self.label = self.id
        else:
            self.label = label
        self.attributes = attributes
        self.position = [x,y,z]
        self.color = [r,g,b]
        if not self.has_color():
            self.color = [200,200,200]
        self.size = size

    def has_position(self):
        return not None in self.position

    def has_color(self):
        return not None in self.color


class Edge(object):
    def __init__(self, source, target, attributes=None, weight=None):
        self.source = source
        self.target = target
        self.attributes = attributes


class Graph(object):
    def __init__(self, igraph_obj=None, layout=None):
        self.nodes = {}
        self.edges = []
        if igraph_obj is not None:
            self.load_igraph(igraph_obj, layout)


    def load_igraph(self,graph, layout = None):
        for n in graph.vs:
            node = Node(n.index, label=n["name"])
            if layout is not None:
                node.position =  layout.coords[n.index]
            self.add_node(node)
        for (source,target) in graph.get_edgelist():
            edge = Edge(source,target)
            self.add_edge(edge)

    def add_node(self, node):
        """
        nodes are unique, so we add to a dictionary
        """
        if node.__class__ == Node:
            self.nodes[node.id] = node
        else:
            raise TypeError("nodes must be of type gexdat.Node")

    def add_edge(self, edge):
        if edge.__class__ == Edge:
            self.edges.append(edge)
        else:
            raise TypeError("edges must be of type gexdat.Edge")

    def create_base_element(self, description="hungry", creator="hippo", edge_type='undirected', mode='static'):
        attributes = {"xmlns:viz":"http://www.gexf.net/1.2draft/viz"}
        root = Element("gexf", attrib=attributes)
        date = datetime.today().strftime("%m_%d_%y")
        meta = SubElement(root, "meta", lastmodifieddate=date)
        if description is not None:
            SubElement(meta,"description").text = description
        if creator is not None:
            SubElement(meta,"creator").text = creator
        graph = SubElement(root, "graph", defaultedgetype=edge_type, mode=mode)
        return root, graph

    def add_nodes_element(self, nodes):
        """
        make nodes xml element from nodes
        """
        nodes_el = Element("nodes")
        for node_id in nodes.keys():
            node = nodes[node_id]
            gexf_node = SubElement(nodes_el, 'node', id=str(node.id), label=str(node.label))
            SubElement(gexf_node, 'attvalues')
            SubElement(gexf_node, 'viz:size', value=str(node.size))
            if node.has_position():
                SubElement(gexf_node, 'viz:position', x=str(node.position[0]), y=str(node.position[1]), z=str(node.position[2]))
            if node.has_color():
                SubElement(gexf_node, 'viz:color', r=str(node.color[0]), y=str(node.color[1]), z=str(node.color[2]))
        return nodes_el

    def add_edges_element(self, edges):
        """
        create xml element from edge list
        """
        edges = Element("edges")
        for edge in self.edges:
            gexf_edge = SubElement(edges,'edge', source=str(edge.source), target=str(edge.target))
            SubElement(gexf_edge, "attvalues")
        return edges

    def write_gexf(self, filename, ):
        """
        writes the graph in gexf format to file with no modifications to the object
        """
        root, graph = self.create_base_element()

        self.add_nodes_element(self.nodes)
        self.add_edges_element(self.edges)

        tree = ElementTree(root)
        print "saved to: " + os.getcwd() + '/' + filename
        tree.write(os.getcwd() + '/' + filename)

class TimeShift(object):
    def __init__(self, graphs = None, xml = None):
        self.graphs = graphs
        self.xml = self.xml_from_graphs(graphs)
        self.edge_dict = {}
    def assimilate_graph(self, graph):
        pass

    def xml_from_graphs(self, graphs):
        root = Graph.create_base_element()
        pass

    def write_fused_gexf(self, filename):
        tree = ElementTree(self.xml)

        self.xml.write(os.getcwd() + '/' + filename)
