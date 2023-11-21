class NaryTreeNode(object):
    def __init__(self, data):
        # Nodo en un árbol n-ario con datos y una lista de hijos
        self.data = data
        self.children = []

class NaryTree(object):
    def __init__(self):
        # Inicializar un árbol n-ario con la raíz y una copia de respaldo
        self.root = None
        self.respaldo = None 

    def add_node(self, data, parent=None):
        # Añadir un nuevo nodo al árbol
        new_node = NaryTreeNode(data)
        if parent is None:
            # Si no se especifica el padre, el nuevo nodo se convierte en la raíz
            self.root = new_node
        else:
            # Buscar el nodo padre y agregar el nuevo nodo como hijo
            parent_nodes = self._find_node(parent.name, parent.id, self.root)
            for node in parent_nodes:
                node.children.append(new_node)

    def _vaciar_arbol(self, nodo):
        # Eliminar recursivamente los hijos de un nodo
        for hijo in nodo.children:
            self._vaciar_arbol(hijo)

        # Limpiar la lista de hijos del nodo
        nodo.children.clear()

    def vaciar_arbol(self):
        # Vaciar todo el árbol
        self._vaciar_arbol(self.root)
        self.root = None

    def _find_node(self, data, id, current_node):
        # Buscar nodos que coincidan con el nombre y el id (si se proporciona)
        nodes = []
        id_node = current_node.data.id if id is not None else None
        if current_node.data.name == data and id_node == id:
            nodes.append(current_node)
        for child in current_node.children:
            nodes += self._find_node(data, id, child)
        return nodes

    def _search_node(self, data, current_node):
        # Buscar nodos que contengan el nombre dado
        nodes = []
        if data in current_node.data.name:
            nodes.append(current_node)
        for child in current_node.children:
            nodes += self._search_node(data, child)
        return nodes

    def find_node(self, data, id):
        # Encontrar un nodo específico por nombre e id
        nodes = self._find_node(data, id, self.root)
        return nodes[0] if nodes else None

    def search_node(self, data):
        # Buscar nodos que contengan el nombre dado
        return self._search_node(data, self.root)

    def _eliminar_nodo(self, arbol, nodo):
        # Eliminar un nodo específico del árbol
        if arbol == nodo:
            arbol = None
            return

        padre = None
        for hijo in arbol.children:
            if hijo == nodo:
                padre = arbol
                break

        if padre:
            padre.children.remove(hijo)
        else:
            for hijo in arbol.children:
                self._eliminar_nodo(hijo, nodo)

    def eliminar_nodo(self, nodo):
        # Eliminar un nodo del árbol
        self._eliminar_nodo(self.root, nodo)

    def _print_node(self, node, altura=0):
        # Imprimir el árbol recursivamente
        if node:
            print((altura * "--") + str(node.data.name) + str(node.data.id))
            for node_children in node.children:
                self._print_node(node_children, altura + 1)

    def print_node(self):
        # Imprimir el árbol
        self._print_node(self.root)


class Gestor(object):
    def __init__(self, name, path, isDir, id, father=None):
        # Clase para representar un archivo con nombre, ruta, tipo (directorio o archivo), id y padre
        self.name = name
        self.path = path
        self.father = father
        self.isDir = isDir
        self.id = id
  