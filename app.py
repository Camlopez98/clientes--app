import streamlit as st
import sqlite3

# Conexión a la base de datos (se crea si no existe)
conn = sqlite3.connect('clientes.db', check_same_thread=False)
c = conn.cursor()

# Crear tabla si no existe
c.execute('''
    CREATE TABLE IF NOT EXISTS clientes (
        cedula TEXT PRIMARY KEY,
        nombre TEXT,
        apellido TEXT,
        correo TEXT,
        telefono TEXT,
        direccion TEXT,
        preferencial BOOLEAN
    )
''')
conn.commit()

# Funciones
def registrar_cliente_sqlite(cedula, nombre, apellido, correo, telefono, direccion, preferencial):
    try:
        c.execute('INSERT INTO clientes VALUES (?, ?, ?, ?, ?, ?, ?)', 
                  (cedula, nombre, apellido, correo, telefono, direccion, preferencial))
        conn.commit()
        st.success("✅ Cliente registrado con éxito.")
    except sqlite3.IntegrityError:
        st.error("⚠️ Ya existe un cliente con esa cédula.")

def eliminar_cliente_sqlite(cedula):
    c.execute('DELETE FROM clientes WHERE cedula = ?', (cedula,))
    conn.commit()
    st.success("🗑️ Cliente eliminado (si existía).")

def buscar_cliente_sqlite(cedula):
    c.execute('SELECT * FROM clientes WHERE cedula = ?', (cedula,))
    cliente = c.fetchone()
    if cliente:
        st.write(f"**Cédula:** {cliente[0]}")
        st.write(f"**Nombre:** {cliente[1]} {cliente[2]}")
        st.write(f"**Correo:** {cliente[3]}")
        st.write(f"**Teléfono:** {cliente[4]}")
        st.write(f"**Dirección:** {cliente[5]}")
        st.write(f"**Preferencial:** {'✅ Sí' if cliente[6] else '❌ No'}")
    else:
        st.warning("Cliente no encontrado.")

def mostrar_clientes(preferenciales=False):
    if preferenciales:
        c.execute('SELECT * FROM clientes WHERE preferencial = 1')
    else:
        c.execute('SELECT * FROM clientes')
    datos = c.fetchall()
    for cliente in datos:
        st.write(f"**Cédula:** {cliente[0]} | **Nombre:** {cliente[1]} {cliente[2]} | **Preferencial:** {'✅' if cliente[6] else '❌'}")

# Interfaz Streamlit
st.title("📋 Sistema de Registro de Clientes")

menu = ["Registrar Cliente", "Eliminar Cliente", "Buscar Cliente", "Listar Todos", "Listar Preferenciales"]
opcion = st.sidebar.selectbox("Menú", menu)

if opcion == "Registrar Cliente":
    st.subheader("🧾 Registrar un nuevo cliente")
    cedula = st.text_input("Cédula")
    nombre = st.text_input("Nombre")
    apellido = st.text_input("Apellido")
    correo = st.text_input("Correo")
    telefono = st.text_input("Teléfono")
    direccion = st.text_area("Dirección")
    preferencial = st.checkbox("¿Es cliente preferencial?")

    if st.button("Registrar Cliente"):
        if cedula and nombre and apellido:
            registrar_cliente_sqlite(cedula, nombre, apellido, correo, telefono, direccion, preferencial)
        else:
            st.warning("Por favor completa los campos obligatorios.")

elif opcion == "Eliminar Cliente":
    st.subheader("🗑️ Eliminar cliente")
    cedula = st.text_input("Cédula del cliente a eliminar")
    if st.button("Eliminar"):
        eliminar_cliente_sqlite(cedula)

elif opcion == "Buscar Cliente":
    st.subheader("🔍 Buscar cliente")
    cedula = st.text_input("Cédula del cliente a buscar")
    if st.button("Buscar"):
        buscar_cliente_sqlite(cedula)

elif opcion == "Listar Todos":
    st.subheader("📄 Lista de todos los clientes")
    mostrar_clientes(preferenciales=False)

elif opcion == "Listar Preferenciales":
    st.subheader("🌟 Lista de clientes preferenciales")
    mostrar_clientes(preferenciales=True)
