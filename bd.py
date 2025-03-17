import sqlite3
from tkinter import *
from tkinter import messagebox

# Conectar a la base de datos (si no existe, se creará)
def conectar_db():
    return sqlite3.connect('mi_base_de_datos.db')

# Crear la tabla si no existe
def crear_tabla():
    conexion = conectar_db()
    cursor = conexion.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            edad INTEGER NOT NULL,
            email TEXT NOT NULL UNIQUE
        )
    ''')
    conexion.commit()
    conexion.close()

# Función para incluir un registro
def incluir_registro():
    nombre = entry_nombre.get()
    edad = entry_edad.get()
    email = entry_email.get()

    if nombre and edad and email:
        try:
            conexion = conectar_db()
            cursor = conexion.cursor()
            cursor.execute('''
                INSERT INTO usuarios (nombre, edad, email)
                VALUES (?, ?, ?)
            ''', (nombre, int(edad), email))
            conexion.commit()
            conexion.close()
            messagebox.showinfo("Éxito", "Registro incluido con éxito.")
            limpiar_campos()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "El email ya existe en la base de datos.")
    else:
        messagebox.showwarning("Advertencia", "Todos los campos son obligatorios.")

# Función para consultar un registro por ID
def consultar_registro():
    id_usuario = entry_id.get()

    if id_usuario:
        conexion = conectar_db()
        cursor = conexion.cursor()
        cursor.execute('SELECT * FROM usuarios WHERE id = ?', (int(id_usuario),))
        registro = cursor.fetchone()
        conexion.close()

        if registro:
            messagebox.showinfo("Registro Encontrado", 
                               f"ID: {registro[0]}\nNombre: {registro[1]}\nEdad: {registro[2]}\nEmail: {registro[3]}")
        else:
            messagebox.showinfo("No Encontrado", "Registro no encontrado.")
    else:
        messagebox.showwarning("Advertencia", "Ingrese un ID para consultar.")

# Función para modificar un registro
def modificar_registro():
    id_usuario = entry_id.get()
    nombre = entry_nombre.get()
    edad = entry_edad.get()
    email = entry_email.get()

    if id_usuario and nombre and edad and email:
        conexion = conectar_db()
        cursor = conexion.cursor()
        cursor.execute('''
            UPDATE usuarios
            SET nombre = ?, edad = ?, email = ?
            WHERE id = ?
        ''', (nombre, int(edad), email, int(id_usuario)))
        conexion.commit()
        conexion.close()

        if cursor.rowcount > 0:
            messagebox.showinfo("Éxito", "Registro modificado con éxito.")
            limpiar_campos()
        else:
            messagebox.showinfo("No Encontrado", "Registro no encontrado.")
    else:
        messagebox.showwarning("Advertencia", "Todos los campos son obligatorios.")

# Función para eliminar un registro
def eliminar_registro():
    id_usuario = entry_id.get()

    if id_usuario:
        conexion = conectar_db()
        cursor = conexion.cursor()
        cursor.execute('DELETE FROM usuarios WHERE id = ?', (int(id_usuario),))
        conexion.commit()
        conexion.close()

        if cursor.rowcount > 0:
            messagebox.showinfo("Éxito", "Registro eliminado con éxito.")
            limpiar_campos()
        else:
            messagebox.showinfo("No Encontrado", "Registro no encontrado.")
    else:
        messagebox.showwarning("Advertencia", "Ingrese un ID para eliminar.")

# Función para limpiar los campos de entrada
def limpiar_campos():
    entry_id.delete(0, END)
    entry_nombre.delete(0, END)
    entry_edad.delete(0, END)
    entry_email.delete(0, END)

# Crear la ventana principal
root = Tk()
root.title("Gestión de Usuarios")
root.geometry("400x300")

# Crear etiquetas y campos de entrada
label_id = Label(root, text="ID:")
label_id.grid(row=0, column=0, padx=10, pady=10)
entry_id = Entry(root)
entry_id.grid(row=0, column=1, padx=10, pady=10)

label_nombre = Label(root, text="Nombre:")
label_nombre.grid(row=1, column=0, padx=10, pady=10)
entry_nombre = Entry(root)
entry_nombre.grid(row=1, column=1, padx=10, pady=10)

label_edad = Label(root, text="Edad:")
label_edad.grid(row=2, column=0, padx=10, pady=10)
entry_edad = Entry(root)
entry_edad.grid(row=2, column=1, padx=10, pady=10)

label_email = Label(root, text="Email:")
label_email.grid(row=3, column=0, padx=10, pady=10)
entry_email = Entry(root)
entry_email.grid(row=3, column=1, padx=10, pady=10)

# Crear botones
button_incluir = Button(root, text="Incluir Registro", command=incluir_registro)
button_incluir.grid(row=4, column=0, padx=10, pady=10)

button_consultar = Button(root, text="Consultar Registro", command=consultar_registro)
button_consultar.grid(row=4, column=1, padx=10, pady=10)

button_modificar = Button(root, text="Modificar Registro", command=modificar_registro)
button_modificar.grid(row=5, column=0, padx=10, pady=10)

button_eliminar = Button(root, text="Eliminar Registro", command=eliminar_registro)
button_eliminar.grid(row=5, column=1, padx=10, pady=10)

# Iniciar la aplicación
crear_tabla()
root.mainloop()
