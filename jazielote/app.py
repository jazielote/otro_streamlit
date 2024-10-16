import streamlit as st
import mysql.connector as mysql
import uuid

# Conectar a la base de datos
conexion = mysql.connect(
    host="localhost",
    user="root",
    password="",
    database="rrhh"
)
cursor = conexion.cursor()

def login():
    st.title("Login")

    email = st.text_input("E-mail")
    password = st.text_input("Contraseña", type="password")

    if st.button("Login"):
        cursor.execute("SELECT * FROM users WHERE email = %s AND contrasena = %s", (email, password))
        user = cursor.fetchone()

        if user:
            st.session_state["username"] = user[1]  # Asumiendo que el nombre está en la segunda columna
            st.success("Login exitoso")
            st.rerun()  # Recargar la página para limpiar el contenido
        else:
            st.error("Credenciales incorrectas")

def register():
    st.title("Registro de usuarios")

    nombre = st.text_input("Nombre")
    email = st.text_input("E-mail")
    telefono = st.text_input("Teléfono")
    password = st.text_input("Contraseña", type="password")

    if st.button("Registrar"):
        # Generar un nuevo UUID para cada registro
        Uuid = str(uuid.uuid4())
        
        cursor.execute("INSERT INTO users (id, nombre, telefono, email, contrasena) VALUES (%s, %s, %s, %s, %s)", (Uuid, nombre, telefono, email, password))
        conexion.commit()  # Confirmar la transacción
        
        if cursor.rowcount == 1:
            st.success("Usuario registrado correctamente")
            st.session_state["username"] = nombre
            st.rerun()  # Recargar la página para limpiar el contenido
        else:
            st.error("No se pudo registrar el usuario")

def dashboard():
    if "username" in st.session_state:
        st.title("Dashboard")
        st.header(f"Hola {st.session_state['username']}!")
    else:
        st.error("No has iniciado sesión")

def main():
    st.sidebar.title("Menu")
    if "username" in st.session_state:
        if st.sidebar.button("Dashboard"):
            dashboard()
    else:
        if st.sidebar.button("Login"):
            login()
        if st.sidebar.button("Registro"):
            register()

if __name__ == "__main__":
    main()

# Cerrar el cursor y la conexión al final del script
cursor.close()
conexion.close()
