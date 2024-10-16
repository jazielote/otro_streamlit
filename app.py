import streamlit as st
import mysql.connector as mysql
import uuid
from streamlit_calendar import calendar
import smtplib
from email.message import EmailMessage
import ssl # Importar SSL para el envío de correos
import json

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
            st.session_state["userid"] = user[0] # Asumiendo que el id está en la primera columna
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
            st.session_state["userid"] = Uuid
            st.rerun()
            dashboard()
        else:
            st.error("No se pudo registrar el usuario")


# Función para enviar un correo
def enviar_email(remitente, destinatario, asunto, cuerpo, contraseña):
    # Crear el objeto del mensaje
    mensaje = EmailMessage()
    mensaje['Subject'] = asunto
    mensaje['From'] = remitente
    mensaje['To'] = destinatario
    mensaje.set_content(cuerpo)

    # Conectar al servidor SMTP de Gmail
    contexto = ssl.create_default_context()
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=contexto) as servidor:
            servidor.login(remitente, contraseña)
            servidor.send_message(mensaje)
        st.info("Correo enviado exitosamente")
    except Exception as e:
        st.error(f"Error al enviar el correo: {e}")
def solicitudes(id):
    st.title("Solicitudes")
    cursor.execute("SELECT * FROM postulaciones WHERE vacante_id = %s", (id,))
    postulaciones = cursor.fetchall()

    for postulacion in postulaciones:
        st.write(f"Nombre: {postulacion[2]}")
        st.write(f"Email: {postulacion[3]}")
        st.write(f"Teléfono: {postulacion[4]}")
        
        direccion_delodf = postulacion[5]
        with open(direccion_delodf, 'rb') as file:
            documento = file.read()
            
        st.download_button(label="Descargar CV", data=documento, file_name=direccion_delodf.split('/')[-1])

def vacantes():
    cursor = conexion.cursor()
    st.title("Mis Vacantes")
    cursor.execute("SELECT * FROM vacantes WHERE iduser = %s", (st.session_state["userid"],))
    vacantes = cursor.fetchall()
    userid = st.session_state["userid"]
    
    if "vacante_form" not in st.session_state:
        st.session_state["vacante_form"] = False

    if st.button("Nueva Vacante"):
        st.session_state["vacante_form"] = not st.session_state["vacante_form"]

    if st.session_state["vacante_form"]:
        st.title("Nueva Vacante")
        with st.form(key="formulario"):
            titulo = st.text_input("Título")
            descripcion = st.text_area("Descripción")
            ubicacion = st.text_input("Ubicación")
            salario = st.number_input("Salario", step=100, min_value=0, format="%d", value=0)
            fecha_publicacion = st.date_input("Fecha de publicación")
            fecha_cierre = st.date_input("Fecha de cierre")
            tipo_contrato = st.selectbox("Tipo de contrato", ["Tiempo completo", "Medio tiempo", "Temporal", "Permanente", "Practicante"])
            experiencia_requerida = st.text_input("Experiencia requerida")
            educacion_requerida = st.text_input("Educación requerida")
            habilidades_requeridas = st.text_input("Habilidades requeridas")
            submit_button = st.form_submit_button(label="Registrar")

            if submit_button:
                Uuid = str(uuid.uuid4())
                userid = st.session_state["userid"]
                query = """
                INSERT INTO `vacantes`(`id`, `iduser`, `titulo`, `descripcion`, `ubicacion`, `salario`, `fecha_publicacion`, `fecha_cierre`, `tipo_contrato`, `experiencia_requerida`, `educacion_requerida`, `habilidades_requeridas`)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                values = (
                    Uuid, 
                    userid, 
                    titulo, 
                    descripcion, 
                    ubicacion, 
                    salario, 
                    fecha_publicacion, 
                    fecha_cierre, 
                    tipo_contrato, 
                    experiencia_requerida, 
                    educacion_requerida, 
                    habilidades_requeridas
                )
                cursor.execute(query, values)
                conexion.commit()
                if cursor.rowcount == 1:
                    st.success("Vacante registrada correctamente")
                else:
                    st.error("No se pudo registrar la vacante")
    else:
        cursor.execute("SELECT * FROM vacantes WHERE iduser = %s", (userid,))
        vacantes = cursor.fetchall()
        for vacante in vacantes:
            st.write(f"{vacante[2]} - salario: {vacante[5]}")


def ver_entrevistas():
    st.title("Entrevistas")
    userid = st.session_state["userid"]
    
    # Ejecutando la consulta para obtener las vacantes del usuario
    query = "SELECT * FROM vacantes WHERE `iduser` = %s"
    cursor.execute(query, (userid,))
    vacantes = cursor.fetchall()

    # Creando un cuadro de selección con los datos obtenidos
    vacantes_select = st.selectbox("Vacante seleccionada", [vacante[2] for vacante in vacantes])

    # Obteniendo el id de la vacante seleccionada
    vacante_id = [vacante[0] for vacante in vacantes if vacante[2] == vacantes_select][0]
    
    # Ejecutando la consulta para obtener las postulaciones de la vacante seleccionada
    query_postulaciones = "SELECT * FROM entrevistas WHERE `vacante_id` = %s"
    cursor.execute(query_postulaciones, (vacante_id,))
    entrevistas = cursor.fetchall()

    # Preparando los eventos para el calendario
    eventos = []
    for entrevista in entrevistas:
        id_postulante = entrevista[1].decode('utf-8')
        query_postulante = "SELECT * FROM postulaciones WHERE vacante_id = %s"
        cursor.execute(query_postulante, (id_postulante,))
        postulante = cursor.fetchone()

        evento = {
            'title': postulante[2],
            "start": entrevista[3].strftime("%Y-%m-%dT%H:%M:%S"),  # Convertir datetime a string
            "end": entrevista[3].strftime("%Y-%m-%dT%H:%M:%S")  # Convertir datetime a string
        }
        eventos.append(evento)
    
    # Cerrando el cursor
    cursor.close()
    
    # Mostrando el calendario
    st.write(calendar(events=eventos))


def configurarEmail():
    #verfica la tabla users si estan las columnas email_correo" y "email_password, si no estan la crea"    
    cursor.execute("SHOW COLUMNS FROM users LIKE 'email_correo'")
    verificaColumnas = cursor.fetchone()
    if not verificaColumnas:
        cursor.execute("ALTER TABLE users ADD COLUMN email_correo VARCHAR(255)")  
    
    cursor.execute("SHOW COLUMNS FROM users LIKE 'password_correo'")
    verificaColumnas = cursor.fetchone()
    if not verificaColumnas:     
        cursor.execute("ALTER TABLE users ADD COLUMN password_correo VARCHAR(255)")
    
    st.title("Configurar E-mail") # <== el titulo
    st.info("Esta información se solicita para poder automatizar el envío de E-mails a postulares.") # <== la infomación
    
    # Consulta a la base de datos para verificar si los campos están vacíos
    userid = st.session_state["userid"]
    cursor.execute("SELECT email_correo, password_correo FROM users WHERE id=%s", (userid,))
    verificaColumnas = cursor.fetchone()
    
    if verificaColumnas and verificaColumnas[0] and verificaColumnas[1]:    
    # Si las columnas no están vacías, deshabilite los campos y botones de forma predeterminada
        email_disabled = True
        password_disabled = True
        enviar_disabled = True
    else:
        # la misma mamada, pero a la inversa.
        email_disabled = False
        password_disabled = False
        enviar_disabled = False
    
    # Initialize session state variables
    if "email_disabled" not in st.session_state:
        st.session_state["email_disabled"] = email_disabled
    if "password_disabled" not in st.session_state:
        st.session_state["password_disabled"] = password_disabled
    if "enviar_disabled" not in st.session_state:
        st.session_state["enviar_disabled"] = enviar_disabled
    
    with st.container(border=True):
        emailCorreo = st.text_input("E-mail", key="email", disabled=st.session_state["email_disabled"])
        emailPassword = st.text_input("Contraseña", key="password", disabled=st.session_state["password_disabled"])
        botonEnviar = st.button("Enviar", disabled=st.session_state["enviar_disabled"], type="primary")
        botonCambiar = st.button("Cambiar", key="cambiar", type="secondary")
    

    
    if botonEnviar:
        if emailCorreo and emailPassword:
            try:
                # Aqui se actualizar la información en la base de datos.
                userid = st.session_state["userid"]
                cursor.execute("UPDATE users SET email_correo=%s, password_correo=%s WHERE id=%s", (emailCorreo, emailPassword, userid))
                conexion.commit()
                st.success("Configuración guardada exitosamente.")
                # Bloquea los campos de correo electrónico, contraseña y el botón "Enviar"
                st.session_state["email_disabled"] = True
                st.session_state["password_disabled"] = True
                st.session_state["enviar_disabled"] = True
            except Exception as e:
                st.error(f"Error al enviar el correo: {e}")
        else:
            st.error("Por favor, completa todos los campos.")
    
    if botonCambiar:
        # Desbloquea los campos de correo electrónico, contraseña con el botón "Enviar"
        st.session_state["email_disabled"] = False
        st.session_state["password_disabled"] = False
        st.session_state["enviar_disabled"] = False

    # v== la informacion parte 2
    st.info("Recomendación: Deberias utilizar un correo profesional exclusivo para el envío de E-mails automatizado.\nDebes configurar una contraseña de aplicación en dicho correo.")


def formularioContacto():
    st.title("Formulario de contacto")  # El titulo

    # Obtener el correo electrónico y contraseña (El de envío de E-mails a postulares) del usuario actual
    try:
        cursor.execute("SELECT email_correo, password_correo FROM users WHERE id = %s", (st.session_state["userid"],))
        usuarioCorreo, usuarioContrasena = cursor.fetchone()
    except Exception as e:
        st.error(f"Error al obtener la información del usuario: {e}")
        return

    # Obtener el correo electrónico del postulante
    try:
        cursor.execute("SELECT email FROM postulaciones")
        postulanteEmails = cursor.fetchall()
    except Exception as e:
        st.error(f"Error al obtener la información de los postulantes: {e}")
        return

    # Select box para elegir el mail del postulante
    opcionesPostulantes = ["Ninguno"] + [email[0] for email in postulanteEmails]

    # Donde se llena el formulario (asunto, mensaje y correo del postulante) de contacto
    with st.form(key="formulario"):
        asunto = st.text_input("Asunto")
        mensaje = st.text_area("Mensaje")
        postulanteEmail = st.selectbox("Seleccione el correo electrónico del postulante",opcionesPostulantes)
        botonEnviar = st.form_submit_button("Enviar")

    # Enviar el correo electrónico
    if botonEnviar:
        if asunto and mensaje:
            if  postulanteEmail == "Ninguno":
                st.warning("Por favor, completa todos los campos.")
            else:
                try:
                    enviar_email(usuarioCorreo, postulanteEmail, asunto, mensaje, usuarioContrasena)
                    st.success("Formulario enviado exitosamente.")
                except Exception as e:
                    st.error(f"Error al enviar el correo: {e}")
        else:
            st.warning("Por favor, completa todos los campos.")


def entrevistas():
    st.title("Agendar Entrevistas")
    opciones = st.selectbox("Acciones", ["Ver Entrevistas", "Agendar Entrevista"])
    if opciones == "Ver Entrevistas":
        ver_entrevistas()
    elif opciones == "Agendar Entrevista":
        userid = st.session_state["userid"]
        # Ejecutando la consulta para obtener las vacantes del usuario
        query = "SELECT * FROM vacantes WHERE `iduser` = %s"
        cursor.execute(query, (userid,))
        vacantes = cursor.fetchall()

        # Creando un cuadro de selección con los datos obtenidos
        vacantes_select = st.selectbox("Vacante", [vacante[2] for vacante in vacantes])
        if vacantes_select:
        # Obteniendo el id de la vacante seleccionada
            vacante_id = [vacante[0] for vacante in vacantes if vacante[2] == vacantes_select][0]

        # Ejecutando la consulta para obtener las postulaciones de la vacante seleccionada
        query_postulaciones = "SELECT * FROM postulaciones WHERE `vacante_id` = %s"
        cursor.execute(query_postulaciones, (vacante_id,))
        postulaciones = cursor.fetchall()
            
        # Creando un select con las postulaciones obtenidas
        postulaciones_select = st.selectbox("Postulación", [postulacion[2] for postulacion in postulaciones])

        # Obteniendo el id de la postulación seleccionada
        if postulaciones_select:
            postulacion_id = [postulacion[0] for postulacion in postulaciones if postulacion[2] == postulaciones_select][0]
        
        fecha = st.date_input("Fecha de la entrevista")
        
        Uuid = str(uuid.uuid4())

        # Agendando la entrevista
        if st.button("Agendar"):
            cursor.execute("INSERT INTO entrevistas (id, vacante_id, postulacion_id, fecha) VALUES (%s, %s, %s, %s)", (Uuid, vacante_id, postulacion_id, fecha))
            conexion.commit()
            if cursor.rowcount == 1:
                st.success("Entrevista agendada correctamente")
                cursor.execute("SELECT * FROM users WHERE id = %s", (userid,))
                user = cursor.fetchone()
                cursor.execute("SELECt * FROM postulaciones WHERE id = %s", (postulacion_id,))
                postulacion = cursor.fetchone()
                destinatario = postulacion[3]
                remitente = user[5]
                password = user[6]
                asunto = f"Confirmación de Entrevista para el Puesto de {vacantes_select}"
                cuerpo = f"""
                Estimado/a {postulaciones_select},

                Espero que este mensaje le encuentre bien.

                Nos complace informarle que hemos revisado su solicitud para el puesto de {vacantes_select} y nos gustaría invitarle a una entrevista para discutir su candidatura con más detalle.

                Detalles de la entrevista:

                Fecha: {fecha}
                Por favor, confirme su disponibilidad respondiendo a este correo a la mayor brevedad posible. Si tiene alguna pregunta o necesita reprogramar la entrevista, no dude en comunicarse con nosotros.

                Agradecemos su interés en formar parte de nuestro equipo y esperamos conocerle pronto.

                Atentamente,

                {user[1]}
                En caso de querer contactarnos, puede hacerlo a:
                {user[3]}
                {user[5]}
                """
                enviar_email(remitente, destinatario, asunto, cuerpo, password)

            else:
                st.error("No se pudo agendar la entrevista")

def pruebas():
    st.title("Crear pruebas a los postulantes")
    
    if "prueba_form" not in st.session_state:
        st.session_state["prueba_form"] = False
    if "preguntas" not in st.session_state:
        st.session_state["preguntas"] = []

    cursor.execute("SELECT * FROM vacantes WHERE iduser = %s", (st.session_state["userid"],))
    vacantes = cursor.fetchall()
    vacantes_select = st.selectbox("Vacante", [vacante[2] for vacante in vacantes])
    vacante_id = [vacante[0] for vacante in vacantes if vacante[2] == vacantes_select][0]

    if st.button("Prueba"):
        st.session_state["prueba_form"] = True

    if st.session_state["prueba_form"]:
        st.title("Prueba")
        
        with st.form(key="formulario"):
            pregunta = st.text_input("Pregunta")
            opciones = st.text_area("Opciones (separadas por comas)")
            agregar_pregunta = st.form_submit_button(label="Agregar Pregunta")

            if agregar_pregunta:
                opciones_lista = opciones.split(',')
                st.session_state["preguntas"].append({
                    "pregunta": pregunta,
                    "opciones": opciones_lista
                })
                st.success("Pregunta agregada")

        if st.session_state["preguntas"]:
            st.subheader("Preguntas añadidas")
            for idx, pregunta in enumerate(st.session_state["preguntas"]):
                st.write(f"Pregunta {idx + 1}: {pregunta['pregunta']}")
                st.write("Opciones:")
                for opcion in pregunta["opciones"]:
                    st.write(f"- {opcion}")

        if st.button("Guardar Prueba"):
            prueba_id = str(uuid.uuid4())
            prueba_json = {
                "id": prueba_id,
                "vacante_id": vacante_id,
                "preguntas": st.session_state["preguntas"]
            }
            prueba_json_str = json.dumps(prueba_json, default=str)  # Convertir a cadena JSON
            cursor.execute("INSERT INTO pruebas (vacante_id, prueba) VALUES (%s, %s)", (vacante_id, prueba_json_str))
            conexion.commit()
            if cursor.rowcount == 1:
                st.success("Prueba guardada correctamente")
            else:
                st.error("No se pudo guardar la prueba")
            st.session_state["preguntas"] = []
            st.session_state["prueba_form"] = False

def dashboard():
    if "username" in st.session_state:
        userid = bytes(st.session_state["userid"])
        st.title("Dashboard")
        st.header(f"Hola {st.session_state['username']}!")
        st.subheader(f"Postulantes actuales")
        cursor.execute("SELECT * FROM vacantes WHERE iduser = %s", (userid,))
        vacantes = cursor.fetchall()
        postulantes = []
        for vacante in vacantes:
            cursor.execute("SELECT * FROM postulaciones WHERE vacante_id = %s", (vacante[0],))
            postulaciones = cursor.fetchall()
            for postulante in postulaciones:
                postulantes.append(postulante)
        for postulante in postulantes:
            try:
                if postulante[6]:
                    respuestas = json.loads(postulante[6].decode("utf-8"))
            except json.JSONDecodeError as e:
                st.write(f"Error al decodificar JSON: {e}")
            st.write(f"Nombre: {postulante[2]} - contacto: {postulante[3]} y {postulante[4]} \n Respuestas a la prueba:")
            if respuestas:
                for key, value in respuestas.items():
                    st.write(f"{key}: {value}")
                respuestas = []

        
    else:
        st.error("No has iniciado sesión")

def main():
    st.sidebar.title("Menu")
    if "username" in st.session_state:
        menu_option = st.sidebar.selectbox("Selecciona una opción", ["Dashboard", "Vacantes","Entrevistas","Configurar E-mail","Pruebas", "Contacto con el postulante (E-mail)"])
    else:
        menu_option = st.sidebar.selectbox("Selecciona una aplicación", ["Iniciar sesión", "Registro"])

    if menu_option == "Dashboard":
        dashboard()
    elif menu_option == "Vacantes":
        vacantes()
    elif menu_option == "Iniciar sesión":
        login()
    elif menu_option == "Registro":
        register()
    elif menu_option == "Entrevistas":
        entrevistas()
    elif menu_option == "Configurar E-mail":
        configurarEmail()
    elif menu_option == "Pruebas":
        pruebas()
    elif menu_option == "Contacto con el postulante (E-mail)":
        formularioContacto()


if __name__ == "__main__":
    main()