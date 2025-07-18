import json
from datetime import datetime

# Clase base: Tarea
class Tarea:
    def __init__(self, titulo, descripcion, fecha_limite, prioridad):
        self.__titulo = titulo
        self.__descripcion = descripcion
        self.__fecha_limite = self.validar_fecha(fecha_limite)
        self.__prioridad = prioridad
        self.__completada = False

    # Encapsulamiento: getters y setters
    def get_titulo(self): return self.__titulo
    def get_descripcion(self): return self.__descripcion
    def get_fecha_limite(self): return self.__fecha_limite
    def get_prioridad(self): return self.__prioridad
    def esta_completada(self): return self.__completada
    def set_completada(self, estado): self.__completada = estado

    def to_dict(self):
        return {
            'tipo': self.__class__.__name__,
            'titulo': self.__titulo,
            'descripcion': self.__descripcion,
            'fecha_limite': self.__fecha_limite.strftime('%Y-%m-%d'),
            'prioridad': self.__prioridad,
            'completada': self.__completada
        }

    @staticmethod
    def validar_fecha(fecha_str):
        try:
            return datetime.strptime(fecha_str, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Formato de fecha inválido. Use AAAA-MM-DD.")

    def notificar(self):
        return f"Tarea general: {self.__titulo} - Vence el {self.__fecha_limite.date()}"

# Subclases específicas con polimorfismo
class Examen(Tarea):
    def notificar(self):
        return f"Examen: {self.get_titulo()} - Estudia antes del {self.get_fecha_limite().date()}"

class Proyecto(Tarea):
    def notificar(self):
        return f"Proyecto: {self.get_titulo()} - Entrega hasta el {self.get_fecha_limite().date()}"

class TareaRapida(Tarea):
    def notificar(self):
        return f"Tarea Rápida: {self.get_titulo()} - Realiza antes del {self.get_fecha_limite().date()}"

# Colección de tareas
tareas = []

# Función para agregar una nueva tarea
def agregar_tarea():
    tipos_disponibles = ('Examen', 'Proyecto', 'TareaRapida')
    print("Tipos de tarea:")
    for i, tipo in enumerate(tipos_disponibles, 1):
        print(f"{i}. {tipo}")

    seleccion = input("Seleccione el tipo de tarea (1-3): ")
    if seleccion not in ['1', '2', '3']:
        print("Tipo inválido.")
        return

    titulo = input("Título: ")
    descripcion = input("Descripción: ")
    fecha = input("Fecha límite (AAAA-MM-DD): ")
    prioridad = input("Prioridad (Alta/Media/Baja): ")

    try:
        clase = (Examen, Proyecto, TareaRapida)[int(seleccion) - 1]
        nueva_tarea = clase(titulo, descripcion, fecha, prioridad)
        tareas.append(nueva_tarea)
        print("Tarea agregada correctamente.")
    except Exception as e:
        print("Error al agregar tarea:", e)

# Función para listar tareas pendientes
def listar_tareas():
    pendientes = [t for t in tareas if not t.esta_completada()]
    pendientes.sort(key=lambda t: t.get_fecha_limite())

    if not pendientes:
        print("No hay tareas pendientes.")
        return

    for i, tarea in enumerate(pendientes):
        print(f"[{i}] {tarea.notificar()} - Prioridad: {tarea.get_prioridad()}")

# Función para marcar tarea como completada
def marcar_completada():
    listar_tareas()
    try:
        indice = int(input("Ingrese el número de la tarea completada: "))
        tareas[indice].set_completada(True)
        print("Tarea marcada como completada.")
    except (IndexError, ValueError):
        print("Índice no válido.")

# Función para alertar tareas próximas a vencer
def alertar_tareas():
    hoy = datetime.now()
    hay_alertas = False

    for tarea in tareas:
        if not tarea.esta_completada():
            dias_restantes = (tarea.get_fecha_limite() - hoy).days
            if 0 <= dias_restantes <= 2:
                print(f"Alerta: {tarea.notificar()} (faltan {dias_restantes} días)")
                hay_alertas = True

    if not hay_alertas:
        print("No hay tareas próximas a vencer.")

# Guardar tareas en archivo JSON
def guardar_json():
    try:
        with open("tareas.json", "w") as archivo:
            json.dump([t.to_dict() for t in tareas], archivo, indent=4)
        print("Tareas guardadas en tareas.json.")
    except Exception as e:
        print("Error al guardar:", e)

# Cargar tareas desde archivo JSON
def cargar_json():
    global tareas
    try:
        with open("tareas.json", "r") as archivo:
            datos = json.load(archivo)

        tareas = []
        for d in datos:
            tipo = d['tipo']
            clase = {'Examen': Examen, 'Proyecto': Proyecto, 'TareaRapida': TareaRapida}.get(tipo, Tarea)
            tarea = clase(d['titulo'], d['descripcion'], d['fecha_limite'], d['prioridad'])
            tarea.set_completada(d['completada'])
            tareas.append(tarea)

        print("Tareas cargadas desde tareas.json.")
    except FileNotFoundError:
        print("El archivo tareas.json no existe.")
    except json.JSONDecodeError:
        print("El archivo JSON está corrupto.")
    except Exception as e:
        print("Error al cargar tareas:", e)

# Menú principal
def menu():
    while True:
        print("\nGestor de Tareas Académicas")
        print("1. Agregar nueva tarea")
        print("2. Listar tareas pendientes")
        print("3. Marcar tarea como completada")
        print("4. Ver tareas próximas a vencer")
        print("5. Guardar tareas en archivo")
        print("6. Cargar tareas desde archivo")
        print("0. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            agregar_tarea()
        elif opcion == '2':
            listar_tareas()
        elif opcion == '3':
            marcar_completada()
        elif opcion == '4':
            alertar_tareas()
        elif opcion == '5':
            guardar_json()
        elif opcion == '6':
            cargar_json()
        elif opcion == '0':
            print("Programa finalizado.")
            break
        else:
            print("Opción no válida.")

# Ejecución
if __name__ == "__main__":
    menu()