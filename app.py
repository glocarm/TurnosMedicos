from flask import Flask, flash, render_template, request, redirect, url_for, jsonify
from datetime import datetime, timedelta
import psycopg2

app = Flask(__name__ , static_url_path='/static')

app.secret_key = '1234'

# Configuración de conexión a PostgreSQL
def get_db_connection():
    conn = psycopg2.connect(
        host="52.41.36.82",       
#54.191.253.12
#44.226.122.3
        database="Turnos",
        user="postgres",       
        password="1234"  
    )
    return conn

# Página principal 
@app.route('/')
def login():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.close()
    conn.close()
    return render_template('login.html')  

@app.route('/ingresar', methods=['POST'])
def ingresar():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        _email= request.form['email']
        _contrasena = request.form['contrasena']
        sql="SELECT * FROM usuarios WHERE email = %s AND contrasena = %s;"
        params=(_email, _contrasena)
        cur.execute(sql, params)
        tipousu = cur.fetchone() 
        if tipousu and tipousu[5]=='admin':
            return redirect('/home')
        elif tipousu and tipousu[5]=='Medico':
            return redirect('/Turnos')
        else:
            return redirect('/')
    finally:
        cur.close()

# Página principal 
@app.route('/home')
def home():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.close()
    conn.close()
    return render_template('home.html' )

#Filtrar con Barra de Búsqueda
def filtrar_tabla(tabla, sql1, sql2, template, parametros):
    conn = get_db_connection()
    cur = conn.cursor()
    resultados = []
    context = {}
    try:
        if parametros is not None:
            # Asegurar que parametros sea una tupla
            if not isinstance(parametros, tuple):
                parametros = (parametros,)
            cur.execute(sql1, parametros)
        else:
            cur.execute(sql2)
        resultados = cur.fetchall()
    except Exception as e:
        print(f"Error en la consulta: {e}")
    finally:
        # Mapear el template  
        if template == 'usuarios.html':
            context['usuarios'] = resultados
        elif template == 'especialidades.html':
            context['especialidades'] = resultados
        elif template == 'medicos.html':
            context['medicos'] = resultados
        elif template == 'medicosturnos.html':
            context['medicos'] = resultados
        elif template == 'reportesPDF.html':
            context['listadoturnos'] = resultados
        cur.close()
        conn.close()
        return render_template(template, **context)

# Gestor de búsqueda de usuarios
@app.route('/filtrarusuarios')
def filtrarusuarios():
    busqueda = request.args.get('buscar','')  
    parametros = ('%' + busqueda + '%', '%'+busqueda+'%', '%'+busqueda+'%')
    sql1 = "SELECT * FROM usuarios WHERE nombre LIKE %s OR apellido LIKE %s OR email LIKE %s;"
    sql2 = "SELECT * FROM usuarios;"
    return filtrar_tabla('usuarios', sql1, sql2, 'usuarios.html', parametros)

# Gestor de búsqueda de especialidades
@app.route('/filtraresp')
def filtraresp():
    busqueda = request.args.get('buscar', '')  
    parametros = ('%' + busqueda + '%',) 
    print('Parametros:', parametros)
    sql1 = "SELECT * FROM especialidades WHERE nombrespec LIKE %s;"
    sql2 = "SELECT * FROM especialidades;"
    return filtrar_tabla('especialidades', sql1, sql2, 'especialidades.html', parametros)

# Gestor de búsqueda de médicos
@app.route('/filtrarmedico')
def filtrarmedico():
    busqueda = request.args.get('buscar', '')  
    parametros = ('%' + busqueda + '%', '%'+busqueda+'%', '%'+busqueda+'%', '%'+busqueda+'%')
    sql1 ="SELECT m.id , m.nombremed ,m.apellidomed ,  m.telefono,m.direccionmed,m.cedulamed, e.id , e.nombrespec FROM medicos m JOIN especialidades e ON m.especialidad_id = e.id AND (nombremed LIKE %s OR apellidomed LIKE %s   OR cedulamed LIKE %s OR direccionmed LIKE %s);"
    sql2 ="SELECT m.id , m.nombremed ,m.apellidomed ,  m.telefono,m.direccionmed,	m.cedulamed, e.id , e.nombrespec FROM medicos m JOIN especialidades e ON m.especialidad_id = e.id ORDER BY m.id;"
    return filtrar_tabla('medicos', sql1, sql2, 'medicos.html', parametros)

# Gestor de búsqueda para PDF
@app.route('/filtrarpdf')
def filtrarpdf():
    busqueda = request.args.get('buscar', '')  
    parametros = ('%' + busqueda + '%', '%'+busqueda+'%', '%'+busqueda+'%' , '%'+busqueda+'%', '%'+busqueda+'%')
    sql1 ="select t.id,h.medico_id, m.nombremed, m.apellidomed, h.dia_semana,h.hora_inicio, t.usuario_id, u.nombre, u.apellido, t.turno_id, h.hora_inicio, t.fecha from horarios_medico h JOIN turnos t ON h.id=t.turno_id JOIN medicos m ON m.id=h.medico_id JOIN usuarios u ON u.id=t.usuario_id AND ( nombremed LIKE %s OR apellidomed LIKE %s OR dia_semana LIKE %s OR nombre LIKE %s OR apellido LIKE %s) order by t.fecha ASC;"
    sql2 ="select t.id,h.medico_id, m.nombremed, m.apellidomed, h.dia_semana,h.hora_inicio, t.usuario_id, u.nombre, u.apellido, t.turno_id, h.hora_inicio, t.fecha from horarios_medico h JOIN turnos t ON h.id=t.turno_id JOIN medicos m ON m.id=h.medico_id JOIN usuarios u ON u.id=t.usuario_id ORDER BY fecha ASC;"
    return filtrar_tabla('medicos', sql1, sql2, 'reportesPDF.html', parametros)
 
# Gestión de Usuarios
@app.route('/usuarios')
def usuarios():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM usuarios ORDER BY id;')
    usuarios = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('usuarios.html', usuarios=usuarios, )

@app.route('/agregarusu', methods=['POST'])
def agregarusu():
    nombre = request.form['nombre']
    apellido = request.form['apellido']
    email = request.form['email']
    contrasena = request.form['contrasena']
    tipo_usuario = request.form['tipo_usuario']
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute('INSERT INTO usuarios (nombre, apellido, email, contrasena, tipo_usuario) VALUES (%s,%s,%s,%s,%s);', (nombre, apellido, email, contrasena, tipo_usuario,))
        conn.commit()
    except psycopg2.Error as e:
        conn.rollback()
        return f"Error al agregar: {e}"
    finally:
        cur.close()
        conn.close()
    return redirect(url_for('usuarios'))

@app.route('/editarusu/<int:id>')
def editarusu(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM usuarios WHERE id = %s;', (id,))
    usuario = cur.fetchone()
    cur.close()
    conn.close()
    return jsonify(usuario)

@app.route('/actualizarusu/<int:id>', methods=['POST'])
def actualizarusu(id):
    nombre = request.form['nombre']
    apellido = request.form['apellido']
    email= request.form['email']
    contrasena = request.form['contrasena']
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute('UPDATE usuarios SET nombre = %s, apellido= %s, email= %s, contrasena= %s WHERE id = %s;', (nombre,apellido, email, contrasena, id))
        conn.commit()
    except psycopg2.Error as e:
        conn.rollback()
        return f"Error al actualizar: {e}"
    finally:
        cur.close()
        conn.close()
    return redirect(url_for('usuarios'))

@app.route('/eliminarusu/<int:id>', methods=['GET','POST'])
def eliminarusu(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM turnos WHERE usuario_id = %s;",(id,))
    tieneturno=cur.fetchall()
    print(tieneturno)
    if tieneturno:
        flash("El usuario tiene turno(s) reservados","error")
    else:
        try:
            cur.execute('DELETE FROM usuarios WHERE id = %s;', (id,))
            conn.commit()
        except psycopg2.Error as e:
            conn.rollback()
            return f"Error al eliminar: {e}"
        finally:
            cur.close()
            conn.close()
    return redirect(url_for('usuarios'))

# Gestión de Especialidades
@app.route('/especialidades')
def especialidades():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM especialidades ORDER BY id;')
    especialidades = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('especialidades.html', especialidades=especialidades, )

@app.route('/agregar', methods=['POST'])
def agregar():
    nombrespec = request.form['nombrespec']
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute('INSERT INTO especialidades (nombrespec) VALUES (%s);', (nombrespec,))
        conn.commit()
    except psycopg2.Error as e:
        conn.rollback()
        return f"Error al agregar: {e}"
    finally:
        cur.close()
        conn.close()
    return redirect(url_for('especialidades'))

@app.route('/editar/<int:id>')
def editar(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM especialidades WHERE id = %s;', (id,))
    especialidad = cur.fetchone()
    cur.close()
    conn.close()
    return jsonify(especialidad)

@app.route('/actualizar/<int:id>', methods=['POST'])
def actualizar(id):
    nombrespec = request.form['nombrespec']
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute('UPDATE especialidades SET nombrespec = %s WHERE id = %s;', (nombrespec, id))
        conn.commit()
    except psycopg2.Error as e:
        conn.rollback()
        return f"Error al actualizar: {e}"
    finally:
        cur.close()
        conn.close()
    return redirect(url_for('especialidades'))

@app.route('/eliminar/<int:id>', methods=['GET','POST'])
def eliminar(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM medicos WHERE especialidad_id = %s;', (id,))
    tienemed=cur.fetchall()
    if tienemed:
        flash("Hay médicos registrados con la especialidad que intenta eliminar","error")
    else:
        try:
            cur.execute('DELETE FROM especialidades WHERE id = %s;', (id,))
            conn.commit()
        except psycopg2.Error as e:
            conn.rollback()
            return f"Error al eliminar: {e}"
        finally:
            cur.close()
            conn.close() 
    return redirect(url_for('especialidades'))

# Gestión de Médicos
@app.route('/medicos')
def medicos():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT m.id , m.nombremed ,m.apellidomed ,  m.telefono,m.direccionmed,	m.cedulamed, e.id , e.nombrespec FROM medicos m JOIN especialidades e ON m.especialidad_id = e.id ORDER BY m.id;')
    medicos = cur.fetchall()
    cur.execute('SELECT * FROM especialidades ORDER BY id;')
    especialidades = cur.fetchall()    
    cur.close()
    conn.close()
    return render_template('medicos.html', medicos=medicos , especialidades=especialidades, )

@app.route('/agregarmed', methods=['POST'])
def agregarmed():
    _nombremed = request.form['nombremed']
    _apellidomed = request.form['apellidomed']
    _especialidad = request.form['especialidadid']
    _telefonomed = request.form['telefonomed']
    _direccionmed = request.form['direccionmed']
    _cedulamed = request.form['cedulamed']
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute('INSERT INTO medicos (nombremed, apellidomed, especialidad_id, telefono, direccionmed, cedulamed) VALUES (%s, %s, %s, %s, %s, %s);', (_nombremed,_apellidomed,_especialidad,_telefonomed, _direccionmed,_cedulamed))
        conn.commit()
    except psycopg2.Error as e:
        conn.rollback()
        return f"Error al agregar: {e}"
    finally:
        cur.close()
        conn.close()
    return redirect(url_for('medicos'))

@app.route('/editarmed/<int:id>') 
def editarmed(id): 
    conn = get_db_connection() 
    cur = conn.cursor() 
    cur.execute('SELECT * FROM medicos WHERE id = %s;', (id,)) 
    medico= cur.fetchone() 
    cur.close() 
    conn.close() 
    return jsonify(medico)

@app.route('/actualizarmed/<int:id>', methods=['POST']) 
def actualizarmed(id): 
    _nombremed = request.form['nombremed'] 
    _apellidomed = request.form['apellidomed'] 
    conn = get_db_connection() 
    cur = conn.cursor() 
    try: 
        cur.execute('UPDATE medicos SET nombremed= %s, apellidomed=%s WHERE id = %s;', (_nombremed,_apellidomed, id)) 
        conn.commit() 
    except psycopg2.Error as e: 
        conn.rollback() 
        return f"Error al actualizar: {e}" 
    finally: 
        cur.close() 
        conn.close() 
    return redirect(url_for('medicos'))

@app.route('/eliminarmed/<int:id>', methods=['POST'])
def eliminarmed(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('select h.id from turnos t JOIN horarios_medico H ON h.medico_id=%s and h.id=t.turno_id;',(id,))
    tieneturno=cur.fetchall()
    if not(tieneturno):
        try:
            cur.execute('DELETE FROM medicos WHERE id = %s;', (id,))
            conn.commit()
        except psycopg2.Error as e:
            conn.rollback()
            return f"Error al eliminar: {e}"
        finally:
            cur.close()
            conn.close()
    else:
        flash('No se puede eliminar datos del médico. Tiene Turno(s) asignados','error')
    return redirect(url_for('medicos'))

# Activar agregar Horario a un Médico
@app.route('/agregarHorariomed/<int:id>', methods=['GET'])
def agregarHorariomed(id):
    print(id)
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM medicos where id=%s;",(id,))
    medico = cur.fetchone()
    cur.close()
    return render_template('/agregarhorarios.html', medico=medico,  )
    
# Agregar Horario Semanal a un Médico
@app.route('/agregarHoramed/<int:id>', methods=['POST'])
def agregarHoramed(id):
    conn = get_db_connection()
    cur = conn.cursor()
    medico_id=request.form.get('id')
    dia_semana=request.form['dia_semana'] 
    hora_inicio=request.form['hora_inicio'] 
    hora_fin=request.form['hora_fin'] 
    duracion=request.form['duracion'] 
    medico_id=id
    activo=True
    # Convertir horarios a objetos datetime para facilitar cálculos
    hora_inicio = datetime.strptime(hora_inicio, '%H:%M')
    hora_fin = datetime.strptime(hora_fin, '%H:%M')
    duracion = int(duracion)  # en minutos
    # Función para generar intervalos de tiempo
    def generar_horarios(hora_inicio, hora_fin, duracion):
        horarios = []
        current_time = hora_inicio
        while current_time < hora_fin:
            next_time = current_time + timedelta(hours=duracion)
            if next_time > hora_fin:
                next_time = hora_fin
            horarios.append((current_time.strftime('%H:%M'), next_time.strftime('%H:%M')))
            current_time = next_time
        return horarios
    horarios_por_dia = generar_horarios(hora_inicio, hora_fin, duracion)
    for inicio, fin in horarios_por_dia:
        activo = True
        cur.execute(
            "INSERT INTO horarios_medico (medico_id, dia_semana, hora_inicio, hora_fin, duracion, activo) "
            "VALUES (%s, %s, %s, %s, %s, %s);",
            (medico_id, dia_semana, inicio, fin, duracion, activo)
        )
    conn.commit()
    cur.close()
    return redirect(url_for('medicos'))

# Gestión de Turnos
@app.route('/Turnos')
def Turnos():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT m.id , m.nombremed ,m.apellidomed ,  m.telefono,m.direccionmed,	m.cedulamed, e.id , e.nombrespec FROM medicos m JOIN especialidades e ON m.especialidad_id = e.id ORDER BY m.id;')
    medicos = cur.fetchall()
    cur.execute('SELECT * FROM especialidades ORDER BY id;')
    especialidades = cur.fetchall()    
    cur.close()
    conn.close()
    return render_template('medicosturnos.html', medicos=medicos , especialidades=especialidades, )

# Ver Horario de Médico
@app.route('/VerHorariomed/<int:id>', methods=['GET'])
def VerHorariomed(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM horarios_medico WHERE medico_id=%s;',(id,))
    horarios = cur.fetchall()
    cur.execute('SELECT * FROM medicos WHERE id=%s;',(id,))
    medico = cur.fetchall()
    cur.close()
    return render_template('/horarios.html', horarios=horarios , medico=medico,  )
    
# Agendar Turno a Paciente
@app.route('/agendarturno/<int:id>', methods=['GET'])
def agendarturno(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM horarios_medico WHERE medico_id=%s;',(id,))
    horarios = cur.fetchall()
    cur.execute('SELECT * FROM medicos WHERE id=%s;',(id,))
    medico = cur.fetchone()
    cur.execute("SELECT * FROM usuarios where tipo_usuario='Paciente';")
    pacientes= cur.fetchall()
    print(pacientes)
    cur.close()
    return render_template('/agendarturno.html', medico=medico , horarios=horarios , pacientes=pacientes, )

#Reservar Turno Médico
@app.route('/reservaturno', methods=['GET', 'POST'])
def reservaturno():
    usuario_id = request.args.get('id')
    id = request.args.get('horario_id')
    fecha = request.args.get('fecha')
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * from turnos WHERE turno_id=%s AND fecha=%s;', (id, fecha,))
    turNodisponible=cur.fetchone()
    if not(turNodisponible):
        try:
            cur.execute('INSERT INTO turnos (usuario_id, turno_id, fecha) VALUES (%s,%s,%s);',(usuario_id, id, fecha))
            conn.commit()
        except psycopg2.Error as e:
            conn.rollback()
            return f"Error al insertar: {e}"
        finally:
            cur.close()
            conn.close()
    else:
       flash("Turno No Disponible","error")
    return redirect(url_for('Turnos'))

# Reporte en PDF de Turnos Médicos
@app.route('/reportes', methods=['GET', 'POST'])
def reportes(): 
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('select t.id,h.medico_id, m.nombremed, m.apellidomed, h.dia_semana,h.hora_inicio, t.usuario_id, u.nombre, u.apellido, t.turno_id, h.hora_inicio, t.fecha from horarios_medico h JOIN turnos t ON h.id=t.turno_id JOIN medicos m ON m.id=h.medico_id JOIN usuarios u ON u.id=t.usuario_id ORDER BY fecha ASC;')
    listadoturnos=cur.fetchall()     
    conn.commit()
    cur.close()
    return render_template('/reportesPDF.html', listadoturnos=listadoturnos,)

# Salir
@app.route('/salir')
def salir():   
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
