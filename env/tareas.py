from database import session, Tarea
import json

class TareasManager:
    def __init__(self):
        pass

    def agregar_tarea(self, titulo, descripcion):
        try:
            nueva_tarea = Tarea(titulo=titulo, descripcion=descripcion)
            session.add(nueva_tarea)
            session.commit()
            print("Tarea agregada con éxito.")
        except Exception as e:
            print(f"Error al agregar tarea: {e}")

    def listar_tareas(self):
        tareas = session.query(Tarea).all()
        return tareas

    def marcar_completada(self, tarea_id):
        try:
            tarea = session.query(Tarea).get(tarea_id)
            if tarea:
                tarea.completada = True
                session.commit()
                print("Tarea marcada como completada.")
            else:
                print("Tarea no encontrada.")
        except Exception as e:
            print(f"Error al marcar tarea: {e}")

    def eliminar_completadas(self):
        try:
            session.query(Tarea).filter(Tarea.completada == True).delete()
            session.commit()
            print("Tareas completadas eliminadas.")
        except Exception as e:
            print(f"Error al eliminar tareas: {e}")

    def guardar_tareas(self, archivo_json):
        try:
            tareas = self.listar_tareas()
            data = [
                {"id": t.id, "titulo": t.titulo, "descripcion": t.descripcion, "completada": t.completada}
                for t in tareas
            ]
            with open(archivo_json, "w") as archivo:
                json.dump(data, archivo, indent=4)
            print(f"Tareas guardadas en {archivo_json}.")
        except Exception as e:
            print(f"Error al guardar tareas: {e}")

    def cargar_tareas(self, archivo_json):
        try:
            with open(archivo_json, "r") as archivo:
                data = json.load(archivo)
            for tarea in data:
                nueva_tarea = Tarea(
                    titulo=tarea["titulo"],
                    descripcion=tarea["descripcion"],
                    completada=tarea["completada"],
                )
                session.add(nueva_tarea)
            session.commit()
            print("Tareas cargadas con éxito.")
        except Exception as e:
            print(f"Error al cargar tareas: {e}")
