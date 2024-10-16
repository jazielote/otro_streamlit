import streamlit as st
import mysql.connector as mysql
import uuid
import json
import os

# Inicializar el estado de la sesión para el formulario de postulación
if "vacante_form" not in st.session_state:
    st.session_state["vacante_form"] = False

# Conectar a la base de datos
try:
    conexion = mysql.connect(
        host="localhost",
        user="root",
        password="",
        database="rrhh"
    )
    cursor = conexion.cursor()
except mysql.Error as err:
    st.error(f"Error al conectar a la base de datos: {err}")
    st.stop()

# Obtener el id de la vacante mediante el método GET
vacante_id = st.query_params.get("vacante_id", [None])

cursor.execute("SELECT * FROM pruebas WHERE vacante_id = %s", (vacante_id,))
prueba = cursor.fetchall()
prueba = json.loads(prueba[0][1])

# Función para mostrar la prueba y guardar las respuestas
def mostrar_prueba(prueba):
    if isinstance(prueba, dict) and "preguntas" in prueba and isinstance(prueba["preguntas"], list):
        respuestas = {}
        for i, item in enumerate(prueba["preguntas"]):
            respuesta = st.radio(item["pregunta"], item["opciones"], key=f"pregunta_{i}")
            respuestas[item["pregunta"]] = respuesta
        enviar = st.selectbox("Enviar", ["No", "Si"])
        if enviar == "Si":
            respuestas = json.dumps(respuestas)
            return respuestas
    else:
        st.error("El formato de la prueba no es correcto. Asegúrate de que 'prueba' sea un diccionario con una lista de preguntas.")


# Si no se ha proporcionado un id de vacante, mostrar un error y salir
if not vacante_id:
    st.error("No se ha proporcionado un ID de vacante")
    st.stop()

# Si se ha proporcionado un id de vacante, mostrar la solicitud de postulación
else:
    # Consulta para obtener la vacante
    query = f"SELECT * FROM vacantes WHERE id = '{vacante_id}'"
    cursor.execute(f"{query}")
    vacante = cursor.fetchone()

    if vacante:
        st.title(f"{vacante[2]}")
        st.markdown(f"""
        ### Descripción del puesto
        {vacante[3]}
        
        **Ubicación:** {vacante[4]}  
        **Salario:** {vacante[5]}  
        **Fecha de publicación:** {vacante[6]}  
        **Fecha de cierre:** {vacante[7]}  
        **Tipo de contrato:** {vacante[8]}  
        **Experiencia requerida:** {vacante[9]}  
        **Educación requerida:** {vacante[10]}  
        **Habilidades requeridas:** {vacante[11]}  
        """)

        if st.button("Postularme"):
            st.session_state["vacante_form"] = True

        if st.session_state["vacante_form"]:
            with st.form(key="postulacion_form"):
                nombre = st.text_input("Nombre")
                email = st.text_input("Email")
                telefono = st.text_input("Teléfono")
                cv = st.file_uploader("Subir CV", type=["pdf", "docx"])
                if prueba == None:
                    pass
                else:
                    resultado = mostrar_prueba(prueba)
                submit_button = st.form_submit_button(label="Postularme")


                if submit_button:
                    # Verificar que todos los campos están llenos
                    if not nombre or not email or not telefono or not cv:
                        st.error("Por favor, completa todos los campos del formulario.")
                    else:
                        # Crear la carpeta 'cv' si no existe
                        if not os.path.exists("cv"):
                            os.makedirs("cv")

                        # Guardar el archivo en la carpeta 'cv'
                        file_extension = cv.name.split('.')[-1]
                        file_name = f"{uuid.uuid4()}.{file_extension}"
                        file_path = os.path.join("cv", file_name)
                        with open(file_path, "wb") as f:
                            f.write(cv.read())

                        # Insertar la dirección del archivo en la base de datos
                        query = """
                        INSERT INTO postulaciones (id, vacante_id, nombre, email, telefono, cv, respuestas)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                        """
                        Uuid = str(uuid.uuid4())
                        values = (Uuid, vacante_id, nombre, email, telefono, file_path, resultado)
                        cursor.execute(query, values)
                        conexion.commit()

                        if cursor.rowcount == 1:
                            st.success("Postulación enviada correctamente")
                        else:
                            st.error("No se pudo enviar la postulación")

        # Consulta para obtener las solicitudes de postulación de la vacante
        query = "SELECT * FROM postulaciones WHERE vacante_id = %s"
        cursor.execute(query, (vacante_id,))
        solicitudes = cursor.fetchall()

        if solicitudes:
            st.header("Solicitudes de postulación")
            for i, solicitud in enumerate(solicitudes, start=1):
                st.markdown(f"{i}. {solicitud[2]} - {solicitud[3]} - {solicitud[4]}")
        else:
            st.info("No se encontraron solicitudes para esta vacante.")
    else:
        st.error("No se encontró la vacante.")