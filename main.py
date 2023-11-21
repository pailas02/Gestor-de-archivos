import os
import tkinter as tk
import shutil
from Tree import NaryTree
from Tree import Gestor
from tkinter import ttk, filedialog, messagebox, simpledialog


class DirectoryExplorer:

    def __init__(self, master):
    
        # Configuración inicial de la interfaz
        self.master = master
        self.master.title("Explorador de Archivos")
        
        # Configurar botones (por ahora estarán ocultos)
        self.buttons = [
            ("Destino", self.go_up),
            ("Crear carpeta", self.agregar),
            ("Crear Archivo", self.agregar_archivo),
            ("Renombrar", self.rename),
            ("Copiar", self.copiar),
            ("Cortar", self.cortar),
            ("Pegar", self.pegar),
            ("Eliminar", self.delete),
            ("Salir", self.quit)
        ]
        
        # Configurar menú contextual
        self.setup_context_menu()

        # Estructuras de datos para el árbol y la ruta actual
        self.tree = NaryTree()
        self.current_path = os.getcwd()

        # Variable de control para mostrar la ruta actual en la interfaz
        self.path_var = tk.StringVar()
        self.path_var.set(self.current_path)

        # Variables para copiar y cortar
        self.path_copy = None
        self.is_copiar = False
        self.ruta_origen = None

        # Configuración del Treeview (árbol visual)
        self.treeview = ttk.Treeview(self.master)
        self.treeview.pack(fill=tk.BOTH, expand=True)

        # Llenar el árbol visual y binario
        self.populate_treeview()

        # Asociar eventos a funciones
        self.treeview.bind('<<TreeviewOpen>>', self.on_open)
        self.treeview.bind('<Double-Button-1>', self.on_select)

        # Configuración de la entrada de búsqueda
        self.entry = tk.Entry(self.master)
        self.entry.place(relx=1, y=0, anchor="ne")
        self.entry.bind("<KeyRelease>", lambda event: self.find_archive())
        
            
    def setup_context_menu(self):
        # Crear el menú contextual
        self.context_menu = tk.Menu(self.master, tearoff=0)
        for text, command in self.buttons:
            self.context_menu.add_command(label=text, command=command)

        # Asociar menú contextual a clic derecho
        self.master.bind("<Button-3>", self.show_context_menu)

    def show_context_menu(self, event):
        # Mostrar el menú contextual en las coordenadas del clic derecho
        self.context_menu.post(event.x_root, event.y_root)

    def populate_treeview(self):
        # Llenar el árbol visual y binario con los elementos del directorio actual
        self.treeview.delete(*self.treeview.get_children())
        self.add_directory("", self.current_path)

    def add_directory(self, parent, path, obj=None):
        # Agregar un directorio y sus elementos al árbol visual y binario
        name = os.path.basename(path)
        item = self.treeview.insert(parent, "end", text=name, open=False)
        archivo = Gestor(name, path, os.path.isdir(path), item, obj)
        self.tree.add_node(archivo, obj)

        if os.path.isdir(path):
            for item_name in os.listdir(path):
                item_path = os.path.join(path, item_name)
                self.add_directory(item, item_path, archivo)

    def on_open(self, event):
        # Al abrir un directorio desde el árbol visual, no se está utilizando actualmente
        pass

    def on_select(self, event):
        # Al hacer doble clic en un elemento del árbol, abrirlo si es un archivo
        item = self.treeview.focus()
        path = self.get_item_path(item)

        if os.path.isdir(path):
            # Puedes expandir o colapsar el directorio al hacer doble clic si lo deseas
            pass
        else:
            os.startfile(path)

    def get_item_path(self, item) -> str:
        # Obtener la ruta completa de un elemento en el árbol visual
        text = self.treeview.item(item, "text")
        return self.tree.find_node(text, item).data.path

    def agregar(self):
        # Crear una nueva carpeta en el directorio actual
        item = self.treeview.focus()
        path = self.get_item_path(item)
        new_name = simpledialog.askstring("Crear Carpeta", f"Ingrese el nombre")
        if new_name:
            ruta_completa = os.path.join(path, new_name)
            try:
                os.makedirs(ruta_completa)
                self.populate_treeview()
            except OSError as error:
                messagebox.showerror("Error", f"No se pudo crear la carpeta")

    def agregar_archivo(self):
        # Crear un nuevo archivo en el directorio actual
        item = self.treeview.focus()
        path = self.get_item_path(item)
        new_name = simpledialog.askstring("Crear Archivo", "Ingrese el nombre")
        if new_name:
            ruta_completa = os.path.join(path, new_name)
            try:
                with open(ruta_completa, "w"):
                    pass
                self.populate_treeview()
            except OSError as error:
                messagebox.showerror("Error", f"No se pudo crear el Archivo")

    def go_up(self):
        # Cambiar al directorio padre y actualizar el árbol
        carpeta = filedialog.askdirectory()
        self.tree.vaciar_arbol()
        self.treeview.delete(*self.treeview.get_children())
        self.current_path = carpeta
        self.add_directory("", carpeta)

    def rename(self):
        # Renombrar un archivo o carpeta
        item = self.treeview.focus()
        path = self.get_item_path(item)
        if path:
            new_name = simpledialog.askstring("Renombrar", f"Ingrese el nuevo nombre para '{os.path.basename(path)}'")
            if new_name:
                new_path = os.path.join(os.path.dirname(path), new_name)
                try:
                    os.rename(path, new_path)
                    self.populate_treeview()
                except OSError as error:
                    messagebox.showerror("Error", f"No se pudo renombrar '{os.path.basename(path)}'")

    def delete(self):
        # Eliminar un archivo o carpeta
        item = self.treeview.focus()
        path = self.get_item_path(item)
        if path:
            confirm = messagebox.askyesno("Eliminar", f"¿Estás seguro de que deseas eliminar '{os.path.basename(path)}'?")
            if confirm:
                try:
                    if os.path.isdir(path):
                        shutil.rmtree(path)
                    else:
                        os.remove(path)
                    self.populate_treeview()
                except OSError:
                    messagebox.showerror("Error", f"No se pudo eliminar '{os.path.basename(path)}'")

    def quit(self):
        # Salir de la aplicación
        self.master.quit()

    def copiar(self):
        # Copiar un archivo o carpeta
        item = self.treeview.focus()
        path = self.get_item_path(item)
        self.path_copy = path
        self.is_copiar = True

    def cortar(self):
        # Cortar un archivo o carpeta
        item = self.treeview.focus()
        path = self.get_item_path(item)
        self.is_copiar = False
        self.ruta_origen = path

    def pegar(self):
        # Pegar un archivo o carpeta copiado o cortado
        item = self.treeview.focus()
        path = self.get_item_path(item)
        if self.is_copiar:
            if os.path.isdir(path):
                try:
                    archivo_destino = os.path.join(path, os.path.basename(self.path_copy))
                    if not os.path.exists(archivo_destino):
                        shutil.copy(self.path_copy, path)
                    else:
                        base_ruta = os.path.basename(self.path_copy)
                        base_ruta = self.get_copy_name(base_ruta)
                        new_path = os.path.join(path, base_ruta)
                        shutil.copy(self.path_copy, new_path)
                    self.populate_treeview()
                except Exception as e:
                    messagebox.showerror("Error", f"No se pudo copiar '{os.path.basename(self.path_copy)}'")
        else:
            try:
                if os.path.dirname(self.ruta_origen) != path:
                    shutil.move(self.ruta_origen, path)
                    self.populate_treeview()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo cortar '{os.path.basename(self.path_copy)}'")

    def find_archive(self):
        # Buscar archivos y actualizar el árbol visual con los resultados
        valor = self.entry.get()
        if valor != "":
            node_list = self.tree.search_node(valor)
            if node_list is not None:
                self.treeview.delete(*self.treeview.get_children())
                for obj in node_list:
                    self.add_directory("", obj.data.path)
            else:
                self.treeview.delete(*self.treeview.get_children())
                self.add_directory("", self.current_path)

    def get_copy_name(self, base_name):
        # Obtener un nombre único para una copia del archivo
        if "." in base_name:
            partes = base_name.split(".")
            base_name = partes[0] + "_copy." + partes[1]
        else:
            base_name = base_name + "_copy"
        return base_name


if __name__ == "__main__":
    root = tk.Tk()
    DirectoryExplorer(root)
    root.mainloop()
