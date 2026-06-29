import datetime

class SingletonMeta(type):
    _instancias_ = {}
    
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instancias:
            #si la clase no fue creada antes, la crea y lo guarda
            cls._instancias[cls] = super().__call__(*args, **kwargs)
        return cls._instancias[cls]

#decorador propio, lo usamos para avisa en la terminal cada vez que se realice una accion importante
def log_operacion(funcion):
    def wrapper(*args, **kwargs):
        print(f"\n[LOG] Ejecutando: {funcion.__name__.upper()}...")
        resultado = funcion(*args, **kwargs)
        print("[LOG] accion finalizada con exito.")
        return resultado
    return wrapper

#Modelo de datos
class persona:
    def __init__(self, nombre, apellido, dni):
        self.nombre = nombre
        self.apellido = apellido
        self.dni = dni
    
    def mostrar_info(self):
        return f"{self.nombre} {self.apellido} (DNI: {self.dni})"

class Usuario(persona):
    def __init__(self, nombre, apellido, dni, correo):
        super().__init__(nombre, apellido, dni)
        self.correo = correo
    
    def mostrar_info(self):
        return f"Usuario: {self.nombre} {self.apellido} | DNI: {self.dni} | Email: {self.correo}"

class Libro:
    def __init__(self, titulo, autor, isbn, año, paginas):
        self.titulo = titulo
        self.autor = autor
        self.isbn = isbn
        self.año = año
        self.paginas = paginas
        self.prestado = False 
    
    def mostrar_info(self):
        estado = "PRESTADO" if self.prestado else "DISPONIBLE"
        return f"Libro: '{self.titulo}' - Autor: {self.autor} (ISBN: {self.isbn}) [{estado}]"