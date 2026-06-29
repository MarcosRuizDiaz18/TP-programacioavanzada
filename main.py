import datetime

# Patron seleccionado: singleton 
# Elegimos este para la clase de biblioteca por que el sistema tiene que tener solo 1 instancia que use todos los datos
# La metaclase que controla esto es la SingletonMeta, lo que está haciendo es controlar la creacion de instancias 
# y al ser de esta manera se concentra todo por el mismo canal y mantiene organizado sin confundir informacion


class SingletonMeta(type):
    _instancias = {}
    
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

# datos de usuarios
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

class Prestamo:
    def __init__(self, libro, usuario):
        self.libro = libro
        self.usuario = usuario
        self.fecha_Prestamo = datetime.date.today()
        self.fecha_Devolucion = None
    
    def registrar_devolucion(self):
        self.fecha_Devolucion = datetime.date.today()
    
    def mostrar_info(self):
        devuelto = f"Devuelto el: {self.fecha_Devolucion}" if self.fecha_Devolucion else "ACTIVO (Pendiente de devolución)"
        return f"Prestamo-> {self.libro.titulo} | Prestado a: {self.usuario.nombre} {self.usuario.apellido} | Fecha: {self.fecha_Prestamo} | Estado: {devuelto}"

# Los objetos Prestamo creados y modificados por la clase Biblioteca
# Relacion de clase Biblioteca, libro y biblioteca - usuario 
# Los Libros y Usuarios existen independiente de la bibliteca por que lo armamos en clases distintas pero si los registran

class Biblioteca(metaclass=SingletonMeta):
    def __init__(self):
        self.libros = []
        self.usuarios = []
        self.prestamos = []  # composicion: los prestamos son creados y destruidos por Biblioteca
    
    @log_operacion
    def alta_libro(self, libro):
        self.libros.append(libro)
        print(f"Libro '{libro.titulo}' agregado al sistema.")
    
    @log_operacion
    def modificacion_libro(self, isbn, nuevo_titulo=None, nuevo_autor=None, nuevo_año=None, nuevas_paginas=None):
        for libro in self.libros:
            if libro.isbn == isbn:
                if nuevo_titulo:
                    libro.titulo = nuevo_titulo
                if nuevo_autor:
                    libro.autor = nuevo_autor
                if nuevo_año:
                    libro.año = nuevo_año
                if nuevas_paginas:
                    libro.paginas = nuevas_paginas
                print(f"Libro con ISBN {isbn} actualizado.")
                return
        print(f"No se encontro ningun libro con el ISBN: {isbn}")

    @log_operacion
    def baja_libro(self, isbn):
        for libro in self.libros:
            if libro.isbn == isbn:
                self.libros.remove(libro)
                print(f"Libro '{libro.titulo}' eliminado del sistema")
                return
        print(f"No se encontro ningun libro con el ISBN: {isbn}")
    
    @log_operacion
    def listar_libros(self):
        print("\n--- LISTADO DE LIBROS EN SYSTEMA ---")
        if not self.libros:
            print("No hay libros registrados.")
        for libro in self.libros:
            print(libro.mostrar_info())
    
    @log_operacion
    def alta_usuario(self, usuario):
        self.usuarios.append(usuario)
        print(f"Usuario {usuario.nombre} {usuario.apellido} registrado.")
    
    @log_operacion
    def baja_usuario(self, dni):
        for usuario in self.usuarios:
            if usuario.dni == dni:
                self.usuarios.remove(usuario)
                print(f"Usuario con DNI {dni} eliminado.")
                return
        print(f"No se encontro ningun usuario con DNI: {dni}")

    @log_operacion
    def modificacion_usuario(self, dni, nuevo_correo):
        for usuario in self.usuarios:
            if usuario.dni == dni:
                usuario.correo = nuevo_correo
                print(f"Correo de {usuario.nombre} actualizado a: {nuevo_correo}")
                return
        print(f"No se encontro usuario con DNI: {dni}")
    
    @log_operacion
    def listar_usuarios(self):
        print("\n--- LISTADO DE USUARIOS EN SISTEMA ---")
        if not self.usuarios:
            print("No hay usuarios registrados.")
        for usuario in self.usuarios:
            print(usuario.mostrar_info())
    
    @log_operacion
    def registrar_prestamo(self, isbn, dni):
        libro_encontrado = None
        for l in self.libros:
            if l.isbn == isbn:
                libro_encontrado = l
                break
        
        usuario_encontrado = None
        for u in self.usuarios:
            if u.dni == dni:
                usuario_encontrado = u
                break
        
        if not libro_encontrado:
            print("[ERROR] El libro no existe en el sistema")
            return
        if not usuario_encontrado:
            print("[ERROR] El usuario no existe en el sistema")
            return
        if libro_encontrado.prestado:
            print(f"[ERROR] El libro '{libro_encontrado.titulo}' Ya posee un prestamo activo.")
            return
        
        nuevo_prestamo = Prestamo(libro_encontrado, usuario_encontrado)
        self.prestamos.append(nuevo_prestamo)
        libro_encontrado.prestado = True
        print(f"Prestamo registrado: '{libro_encontrado.titulo}' prestado a {usuario_encontrado.nombre}.")
    
    @log_operacion
    def registrar_devolucion(self, isbn):
        for prestamo in self.prestamos:
            if prestamo.libro.isbn == isbn and prestamo.fecha_Devolucion is None:
                prestamo.registrar_devolucion()
                prestamo.libro.prestado = False
                print(f"Devolución registrada para el libro: '{prestamo.libro.titulo}'.")
                return
        print("[ERROR] No se encontro un prestamos activo para ese ISBN")
    
    @log_operacion
    def consultar_prestamos_activos(self):
        print("\n--- PRESTAMOS ACTIVOS ---")
        activos = [p for p in self.prestamos if p.fecha_Devolucion is None]
        if not activos:
            print("No hay prestamos activos en este momento.")
        for p in activos:
            print(p.mostrar_info())        
                
"""
SingletonMeta.__call__                  	    — Controla que Biblioteca solo se instancie una vez, cada vez que se llama Biblioteca, devuelve la misma instancia existente en lugar de crear una nueva
log_operacion(funcion) 				            — Decorador que imprime en consola un mensaje de inicio y fin cada vez que se ejecuta la funcion decorada. Se aplica con @log_operacion sobre los metodos de Biblioteca
persona.__init__(nombre, apellido, dni) 	    — Crea una persona con nombre, apellido y DNI
persona.mostrar_info() 				            — Retorna nombre completo y DNI como texto
Usuario.__init__(nombre, apellido, dni, correo) — Hereda de persona y agrega el campo correo
Usuario.mostrar_info() 				            — Retorna los datos del usuario (nombre, DNI, email) formateados
Libro.__init__(titulo, autor, isbn, a, paginas) — Crea un libro
Libro.mostrar_info() 				            — Retorna los datos del libro mas su estado (PRESTADO / DISPONIBLE)
Prestamo.__init__(libro, usuario) 		        — Registra un prestamo con fecha de hoy. fecha_Devolucion queda en None hasta que se devuelva
Prestamo.registrar_devolucion() 		        — Marca la fecha de devolución con la fecha actual
Prestamo.mostrar_info() 			            — Retorna info del préstamo: libro, usuario, fecha de préstamo y estado
Biblioteca.__init__() 				            — Inicializa las tres listas: libros, usuarios, prestamos
alta_libro(libro) 				                — Agrega un objeto Libro a la lista de libros
modificacion_libro(isbn, ...)			        — Busca un libro por ISBN y actualiza los campos que se pasen (titulo, autor, año, paginas)
baja_libro(isbn) 				                — Busca un libro por ISBN y lo elimina de la lista
listar_libros() 				                — Imprime todos los libros registrados
alta_usuario(usuario) 				            — Agrega un objeto Usuario a la lista de usuarios
baja_usuario(dni) 				                — Busca un usuario por DNI y lo elimina de la lista
modificacion_usuario(dni, nuevo_correo) 	    — Busca un usuario por DNI y actualiza su correo
listar_usuarios() 				                — Imprime todos los usuarios registrados
registrar_prestamo(isbn, dni) 			        — Busca el libro (por ISBN) y el usuario (por DNI), valida que existan y que el libro esté disponible, y crea un nuevo Prestamo
registrar_devolucion(isbn) 			            — Busca un préstamo activo por ISBN y lo marca como devuelto, liberando el libro
consultar_prestamos_activos() 			        — Filtra e imprime los préstamos donde fecha_Devolucion es None
"""