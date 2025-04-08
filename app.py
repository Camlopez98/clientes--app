import streamlit as st

# Base de datos de clientes
clientes = {}

# Menú de opciones
menu = ["Registrar cliente", "Eliminar cliente", "Buscar cliente", "Listar todos", "Listar preferenciales"]
opcion = st.sidebar.selectbox("Menú", menu)

# Funciones
def mostrar_cliente(cedula, info):
    st.write(f"**Cédula:** {cedula}")
    st.write(f"Nombre: {info['NOMBRE']} {info['APELLIDO']}")
    st.write(f"Correo: {info['CORREO']}")
    st.write(f"Teléfono: {info['TELEFONO']}")
    st.write(f"Dirección: {info['DIRECCION']}")
    st.write(f"Preferencial: {'Sí' if info['PREFERENCIAL'] else 'No'}")
    st.markdown("---")

# Registro
if opcion == "Registrar cliente":
    st.title("Registrar nuevo cliente")
    cedula = st.text_input("Cédula")
    nombre = st.text_input("Nombre")
    apellido = st.text_input("Apellido")
    correo = st.text_input("Correo")
    telefono = st.text_input("Teléfono")
    direccion = st.text_input("Dirección")
    preferencial = st.checkbox("¿Cliente preferencial?")
    
    if st.button("Registrar"):
        if cedula in clientes:
            st.warning("Ya existe un cliente con esa cédula.")
        else:
            clientes[cedula] = {
                "NOMBRE": nombre,
                "APELLIDO": apellido,
                "CORREO": correo,
                "TELEFONO": telefono,
                "DIRECCION": direccion,
                "PREFERENCIAL": preferencial
            }
            st.success("Cliente registrado con éxito.")

# Eliminar
elif opcion == "Eliminar cliente":
    st.title("Eliminar cliente")
    cedula = st.text_input("Cédula a eliminar")
    if st.button("Eliminar"):
        if cedula in clientes:
            del clientes[cedula]
            st.success("Cliente eliminado.")
        else:
            st.warning("Cliente no encontrado.")

# Buscar
elif opcion == "Buscar cliente":
    st.title("Buscar cliente")
    cedula = st.text_input("Cédula a buscar")
    if st.button("Buscar"):
        if cedula in clientes:
            mostrar_cliente(cedula, clientes[cedula])
        else:
            st.warning("Cliente no encontrado.")

# Listar todos
elif opcion == "Listar todos":
    st.title("Lista de todos los clientes")
    if not clientes:
        st.info("No hay clientes registrados.")
    for cedula, info in clientes.items():
        mostrar_cliente(cedula, info)

# Listar preferenciales
elif opcion == "Listar preferenciales":
    st.title("Clientes preferenciales")
    encontrados = False
    for cedula, info in clientes.items():
        if info["PREFERENCIAL"]:
            mostrar_cliente(cedula, info)
            encontrados = True
    if not encontrados:
        st.info("No hay clientes preferenciales.")
