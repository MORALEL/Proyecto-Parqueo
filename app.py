
from flask import Flask, render_template, request, redirect
import pyodbc

app = Flask(__name__)

conn = pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=PCDEMABERICK\\SQLEXPRESS01;'
    'DATABASE=proyectoparqueo;'
    'Trusted_Connection=yes;'
)

cursor = conn.cursor()


# Página de inicio
@app.route('/')
def index():
     return render_template('index.html')

# Registro de usuario
@app.route('/registro_usuario', methods=['GET', 'POST'])
def registro_usuario():
    if request.method == 'POST':
        cedula = request.form['cedula']
        nombre = request.form['nombre']
        telefono = request.form['telefono']
        direccion = request.form['direccion']
        cursor.execute("INSERT INTO usuarios (cedula, nombre, telefono, direccion) VALUES (?, ?, ?, ?)",
                        (cedula, nombre, telefono, direccion))
        conn.commit()
        return redirect('/')
    return render_template('registro_usuario.html')

# Registro de vehículo
@app.route('/registro_vehiculo', methods=['GET', 'POST'])
def registro_vehiculo():
    if request.method == 'POST':
        placa = request.form['placa']
        marca = request.form['marca']
        modelo = request.form['modelo']
        id_usuario = request.form['id_usuario']

        
        if not placa or not marca or not modelo or not id_usuario:
            cursor.execute("SELECT id_usuario, nombre FROM usuarios")
            usuarios = cursor.fetchall()
            return render_template('registro_vehiculo.html', usuarios=usuarios, error="Todos los campos son obligatorios.")

        cursor.execute("INSERT INTO vehiculos (placa, marca, modelo, id_usuario) VALUES (?, ?, ?, ?)",
                        (placa, marca, modelo, id_usuario))
        conn.commit()
        return redirect('/')
    
    # Obtener lista de usuarios para el formulario
    cursor.execute("SELECT id_usuario, nombre FROM usuarios")
    usuarios = cursor.fetchall()
    return render_template('registro_vehiculo.html', usuarios=usuarios)

# Registro de reserva

max_espacios = 25
@app.route('/reserva', methods=['GET', 'POST'])
def reserva():
    if request.method == 'POST':
        id_vehiculo = request.form['id_vehiculo']
        fecha = request.form['fecha']
        hora_entrada = request.form['hora_entrada']
        hora_salida = request.form['hora_salida']
        espacio = request.form['espacio']

        if not id_vehiculo or not fecha or not hora_entrada or not hora_salida or not espacio:
            cursor.execute("SELECT id, placa FROM vehiculos")
            vehiculos = cursor.fetchall()
            return render_template('reserva.html', vehiculos=vehiculos, error="Todos los campos son obligatorios.")

        # Verificar si el espacio ya está reservado para esa fecha

        cursor.execute("""
            SELECT COUNT(*) FROM reservas
            WHERE fecha = ? AND espacio = ?
        """, (fecha, espacio))

        if cursor.fetchone()[0] > 0:
            
            cursor.execute("SELECT id, placa FROM vehiculos")
            vehiculos = cursor.fetchall()
            return render_template('reserva.html', vehiculos=vehiculos, error="Ese espacio ya está reservado para esa fecha.")


# Verificar si ya se alcanzó el límite de reservas para esa fecha
        cursor.execute("""
            SELECT COUNT(*) FROM reservas
            WHERE fecha = ?
        """, (fecha,))
        total_reservas = cursor.fetchone()[0]

        if total_reservas >= max_espacios:
            cursor.execute("SELECT id, placa FROM vehiculos")
            vehiculos = cursor.fetchall()
            return render_template('reserva.html', vehiculos=vehiculos, error="Se alcanzó el límite de reservas para esta fecha.")


# Insertar la nueva reserva
        cursor.execute("""
            INSERT INTO reservas (id_vehiculo, fecha, hora_entrada, hora_salida, espacio)
            VALUES (?, ?, ?, ?, ?)
        """, (id_vehiculo, fecha, hora_entrada, hora_salida, espacio))
        conn.commit()
        return redirect('/')

# Obtener lista de vehículos para mostrar en el formulario
    cursor.execute("SELECT id, placa FROM vehiculos")
    vehiculos = cursor.fetchall()
    return render_template('reserva.html', vehiculos=vehiculos)


# Ver reservas

@app.route('/ver_reservas')
def ver_reservas():
    cursor.execute("""
        SELECT r.id_reservas, v.placa, r.fecha, r.hora_entrada, r.hora_salida, r.espacio
        FROM reservas r
        JOIN vehiculos v ON r.id_vehiculo = v.id
        ORDER BY r.fecha DESC
    """)
    reservas = cursor.fetchall()
    return render_template('ver_reservas.html', reservas=reservas)

@app.route('/entrada', methods=['POST'])
def entrada():
    id_vehiculo = request.form['id_vehiculo']
    max_vehiculos = 15

    
    if not id_vehiculo:
        return "Debe seleccionar un vehículo."

if __name__ == '__main__':
    app.run(debug=True)

