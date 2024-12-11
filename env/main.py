import tkinter as tk
from tkinter import messagebox
from tareas import TareasManager  

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestión de Tareas")

        self.gestor = TareasManager()

        # Marco para entrada de tareas
        self.frame_entrada = tk.Frame(self.root)
        self.frame_entrada.pack(pady=10)

        tk.Label(self.frame_entrada, text="Título:").grid(row=0, column=0)
        self.titulo_var = tk.StringVar()
        tk.Entry(self.frame_entrada, textvariable=self.titulo_var, width=30).grid(row=0, column=1)

        tk.Label(self.frame_entrada, text="Descripción:").grid(row=1, column=0)
        self.descripcion_var = tk.StringVar()
        tk.Entry(self.frame_entrada, textvariable=self.descripcion_var, width=30).grid(row=1, column=1)

        tk.Button(self.frame_entrada, text="Agregar Tarea", command=self.agregar_tarea).grid(row=2, column=0, columnspan=2, pady=5)

        # Marco para lista de tareas
        self.frame_lista = tk.Frame(self.root)
        self.frame_lista.pack(pady=10)

        self.lista_tareas = tk.Listbox(self.frame_lista, width=50, height=15)
        self.lista_tareas.pack()

        # Label para mostrar la descripción de la tarea seleccionada
        self.descripcion_label = tk.Label(self.root, text="Descripción: ", anchor="w")
        self.descripcion_label.pack(fill="x", padx=10, pady=5)

        # Marco para botones
        self.frame_botones = tk.Frame(self.root)
        self.frame_botones.pack(pady=10)

        tk.Button(self.frame_botones, text="Marcar Completada", command=self.marcar_completada).pack(side=tk.LEFT, padx=5)
        tk.Button(self.frame_botones, text="Eliminar Completadas", command=self.eliminar_completadas).pack(side=tk.LEFT, padx=5)

        # Actualizar la lista al iniciar
        self.actualizar_lista()

    def agregar_tarea(self):
        """Agrega una nueva tarea."""
        titulo = self.titulo_var.get().strip()
        descripcion = self.descripcion_var.get().strip()
        if titulo:
            self.gestor.agregar_tarea(titulo, descripcion)
            self.actualizar_lista()
            self.titulo_var.set("")
            self.descripcion_var.set("")
        else:
            messagebox.showwarning("Advertencia", "El título no puede estar vacío.")

    def actualizar_lista(self):
        """Actualiza la lista de tareas en el Listbox."""
        self.lista_tareas.delete(0, tk.END)
        tareas = self.gestor.listar_tareas()
        self.tareas_map = {tarea.id: tarea for tarea in tareas}  # Mapea ID a tarea
        for tarea in tareas:
            estado = "✔" if tarea.completada else "✘"
            self.lista_tareas.insert(tk.END, f"[{tarea.id}] {tarea.titulo} - {estado}")
        # Vincula el evento de selección
        self.lista_tareas.bind("<<ListboxSelect>>", self.mostrar_descripcion)

    def mostrar_descripcion(self, event):
        """Muestra la descripción de la tarea seleccionada."""
        seleccion = self.lista_tareas.curselection()
        if seleccion:
            tarea_id = int(self.lista_tareas.get(seleccion).split("]")[0][1:])
            tarea = self.tareas_map[tarea_id]
            self.descripcion_label.config(text=f"Descripción: {tarea.descripcion}")
        else:
            self.descripcion_label.config(text="Descripción: ")

    def marcar_completada(self):
        """Marca la tarea seleccionada como completada."""
        seleccion = self.lista_tareas.curselection()
        if seleccion:
            tarea_id = int(self.lista_tareas.get(seleccion).split("]")[0][1:])
            self.gestor.marcar_completada(tarea_id)
            self.actualizar_lista()
        else:
            messagebox.showwarning("Advertencia", "Selecciona una tarea para marcarla como completada.")

    def eliminar_completadas(self):
        """Elimina todas las tareas completadas."""
        self.gestor.eliminar_completadas()
        self.actualizar_lista()

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
