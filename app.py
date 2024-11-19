from datetime import timedelta
from flask import Flask, render_template, request, redirect, url_for, flash, session, send_file
from flask_wtf import FlaskForm
from wtforms import StringField, FileField, SelectField, DecimalField, TextAreaField, DecimalField
from wtforms.validators import DataRequired, Length, EqualTo, NumberRange
import mysql.connector
import os
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from PIL import Image
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
#from app import app

db = SQLAlchemy()

app = Flask(__name__)

#######################################################################################
app.config['SESSION_PERMANENT'] = True  # True, La sesion dura lo indicado. False, hasta que cierro el navegador
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=10)  # Ajusta el tiempo de vida

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/ventas'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
#######################################################################################

app.config['SECRET_KEY'] = 'your_secret_key'
app.config['UPLOAD_FOLDER'] = 'static/images'
app.config['MAX_IMAGE_SIZE'] = (800, 800)

# Configuración de la base de datos
db_config = {
    #'user': 'root',         
    #'password': '',
    #'host': 'localhost',          
    #'database': 'ventas'

    'user': 'sql_angelo_user',         
    'password': '9FLKbE4MReFGKYRt9UCbsq2XIJuyk4BM',
    'host': 'dpg-csuadthu0jms738mhhd0-a',          
    'database': 'ventas'
}

class Producto(db.Model):
    __tablename__ = 'producto'
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.Integer, index=True)
    producto = db.Column(db.String(50))
    detalle = db.Column(db.String(250))
    imagen = db.Column(db.String(250))
    img1 = db.Column(db.String(250))
    img2 = db.Column(db.String(250))
    img3 = db.Column(db.String(250))
    #categoria = db.Column(db.Integer)
    categoria = db.Column(db.Integer, db.ForeignKey('categorias.cat'))  # Definir la clave foránea
    costo = db.Column(db.Numeric(10, 2))
    por1 = db.Column(db.Numeric(10, 2))
    precio1 = db.Column(db.Numeric(10, 2))
    por2 = db.Column(db.Numeric(10, 2))
    precio2 = db.Column(db.Numeric(10, 2))
    stock = db.Column(db.Numeric(10))

    # Relación con el modelo Cate
    categoria_relacion = relationship('Cate', back_populates='productos')  # Definir la relación
    
class Cate(db.Model):
    __tablename__ = 'categorias'
    cat = db.Column(db.Integer, primary_key=True)
    nomcat = db.Column(db.String(50))
    supercat = db.Column(db.String(250))
    superest = db.Column(db.Integer)
    subcat = db.Column(db.String(250))
    subest = db.Column(db.Integer)

    # Relación inversa con el modelo Producto
    productos = relationship('Producto', back_populates='categoria_relacion')
    
def get_db_connection():
    conn = mysql.connector.connect(**db_config)
    return conn

class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    @staticmethod
    def get(user_id):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM users WHERE id = %s', (user_id,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        if not user:
            return None
        return User(user['id'], user['username'], user['password'])

class LoginForm(FlaskForm):
    username = StringField('Usuario', validators=[DataRequired()])
    password = StringField('Contraseña', validators=[DataRequired()])

class RegisterForm(FlaskForm):
    username = StringField('Usuario', validators=[DataRequired()])
    password = StringField('Contraseña', validators=[DataRequired(), Length(min=6)])
    confirm_password = StringField('Confirmar Contraseña', validators=[DataRequired(), EqualTo('password')])

class ChangePasswordForm(FlaskForm):
    old_password = StringField('Contraseña Anterior', validators=[DataRequired()])
    new_password = StringField('Nueva Contraseña', validators=[DataRequired(), Length(min=6)])
    confirm_new_password = StringField('Confirmar Nueva Contraseña', validators=[DataRequired(), EqualTo('new_password')])

class ProductForm(FlaskForm):
    codigo = StringField('Código', validators=[DataRequired()])
    producto = StringField('Producto', validators=[DataRequired()])
    detalle = TextAreaField('Detalle', validators=[DataRequired()], render_kw={"rows": 3, "cols": 80})
    imagen = FileField('Imagen')
    img1 = FileField('Imagen 1')
    img2 = FileField('Imagen 2')
    img3 = FileField('Imagen 3')
    categoria = SelectField('Categoría', choices=[], coerce=int, validators=[DataRequired()])
    costo = DecimalField('Costo', validators=[DataRequired()])
    por1 = DecimalField('Porcentaje 1', default=0)
    precio1 = DecimalField('Precio 1', default=0)
    por2 = DecimalField('Porcentaje 2', default=0)
    precio2 = DecimalField('Precio 2', default=0)
    stock = DecimalField('Stock', validators=[DataRequired()])
    
class CategForm(FlaskForm):
    #cat = DecimalField('Categoria', validators=[DataRequired()])
    cat = DecimalField('Categoría', validators=[NumberRange(min=0, max=99, message="La categoría debe ser > 0.")])
    nomcat = StringField('Nombre', validators=[DataRequired()])
    supercat = TextAreaField('Superior', render_kw={"rows": 2, "cols": 85})
    superest = DecimalField('EstiloSup')
    subcat = TextAreaField('Inferior', render_kw={"rows": 2, "cols": 85})
    subest = DecimalField('EstiloSub')

def resize_image(image_path, output_path, size):
    with Image.open(image_path) as img:
        img.thumbnail(size)
        img.save(output_path)

login_manager = LoginManager()   # Crea la instancia login_manager de la clase LoginManager
login_manager.init_app(app)     # El método init_app(app) conecta el LoginManager con la aplicación Flask (app).
login_manager.login_view = 'login'  # login_view indica cuál es la ruta o vista a la que se redirigirá
                                    # un usuario si intenta acceder a una parte de la aplicación que 
                                    # requiere autenticación pero no ha iniciado sesión.

@login_manager.user_loader      # define una función de "carga de usuarios". Esta función es utilizada por Flask-Login para obtener la información de un usuario basándose en su ID.
def load_user(user_id):     # Esta función define cómo Flask-Login debe buscar al usuario por su ID. El argumento user_id es el ID del usuario que ha iniciado sesión.
    return User.get(user_id)    # User.get(user_id) es una función que, en este caso, busca y devuelve el usuario con el ID especificado. Es posible que en tu aplicación la clase User esté vinculada a una base de datos y tenga un método get() para obtener un usuario.

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()  # Se crea una instancia del formulario LoginForm, definido mas arriba
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        if user and check_password_hash(user['password'], password):
            user_obj = User(user['id'], user['username'], user['password'])
            login_user(user_obj)
            return redirect(url_for('menu'))
        else:
            flash('Nombre de usuario o contraseña incorrectos.')

    return render_template('crud/login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        password = generate_password_hash(form.password.data)
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (username, password) VALUES (%s, %s)', (username, password))
        conn.commit()
        cursor.close()
        conn.close()
        flash('Usuario registrado exitosamente.')
        return redirect(url_for('login'))
    return render_template('crud/register.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    session.clear()  # Borra todas las variables de sesión
    return redirect(url_for('login'))

@app.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        old_password = form.old_password.data
        new_password = form.new_password.data
        if check_password_hash(current_user.password, old_password):
            new_password_hash = generate_password_hash(new_password)
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('UPDATE users SET password = %s WHERE id = %s', (new_password_hash, current_user.id))
            conn.commit()
            cursor.close()
            conn.close()
            flash('Contraseña cambiada exitosamente.')
            return redirect(url_for('index'))
        else:
            flash('Contraseña anterior incorrecta.')
    return render_template('crud/change_password.html', form=form)

@app.route('/')
@login_required
def menu():
    print("Este es un mensaje de prueba en la ruta raíz")

    return render_template('crud/menu.html')

@app.route('/crud/index', methods=['GET', 'POST'])
@login_required
def index():
    search_query = request.form.get('search')
    search_code = request.form.get('code')
    search_cat = request.form.get('cat')
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    query = 'SELECT * FROM producto WHERE 1=1'
    params = []
    
    if search_query:
        query += ' AND producto LIKE %s'
        params.append('%' + search_query + '%')
    if search_code:
        query += ' AND codigo LIKE %s'
        params.append(search_code + '%')
    if search_cat:
        query += ' AND categoria = %s'
        params.append(search_cat)

    cursor.execute(query, params)
    
    productos = cursor.fetchall()
    cursor.close()
    conn.close()
    
    # Obtener categorías
    categorias = obtener_categorias()
        
    return render_template('crud/index.html', productos=productos, categorias=categorias)


@app.route('/productos', methods=['GET'])
def productos():
    sort_by = request.args.get('sort_by', 'codigo')  # Valor por defecto es 'codigo'
    order = request.args.get('order', 'asc')  # Valor por defecto es ascendente
    
    if order == 'desc':
        sort_order = Producto.id.desc()
    else:
        sort_order = Producto.id.asc()

    # Cambia el orden según el valor de sort_by
    if sort_by == 'producto':
        sort_order = Producto.producto.desc() if order == 'desc' else Producto.producto.asc()
    elif sort_by == 'detalle':
        sort_order = Producto.detalle.desc() if order == 'desc' else Producto.detalle.asc()
    else:
        sort_order = Producto.codigo.desc() if order == 'desc' else Producto.codigo.asc()
    
    # Luego ordenas los productos usando la variable sort_order
    productos = Producto.query.order_by(sort_order).all()

    return render_template('crud/index.html', productos=productos)

########################    C R E A T E    #########################
@app.route('/crud/create', methods=['GET', 'POST'])
@login_required     # Decorador que verifica que este logueado. Si no, va a @login_manager
def create():
    form = ProductForm()
    
    # Obtener las categorías desde la base de datos
    categorias = obtener_categorias()  # Esta función debe retornar [(id, nombre), ...]
    form.categoria.choices = categorias
    #form.categoria.data = categorias
    
    if form.validate_on_submit():
        codigo = form.codigo.data
        producto = form.producto.data
        detalle = form.detalle.data
        categoria = form.categoria.data
        costo = form.costo.data
        por1 = form.por1.data
        precio1 = form.precio1.data
        por2 = form.por2.data
        precio2 = form.precio2.data
        stock = form.stock.data

        # Verificar si el código ya existe en la base de datos
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT id FROM producto WHERE codigo = %s', (codigo,))
        codigo_existente = cursor.fetchone()
        
        if codigo_existente:
            flash('⚠️ <strong>Advertencia:</strong> El código del producto ya existe. Elija un código diferente.', 'warning')
            cursor.close()
            conn.close()
            return render_template('crud/create.html', form=form)

        # Procesar imagen principal
        imagen = form.imagen.data
        if imagen:
            filename = secure_filename(imagen.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            imagen.save(file_path)
            resize_image(file_path, file_path, app.config['MAX_IMAGE_SIZE'])
            imagen_url = url_for('static', filename='images/' + filename)
        else:
            imagen_url = ''

        # Procesar imagen 1
        img1 = form.img1.data
        if img1:
            filename1 = secure_filename(img1.filename)
            file_path1 = os.path.join(app.config['UPLOAD_FOLDER'], filename1)
            img1.save(file_path1)
            resize_image(file_path1, file_path1, app.config['MAX_IMAGE_SIZE'])
            img1_url = url_for('static', filename='images/' + filename1)
        else:
            img1_url = ''

        # Procesar imagen 2
        img2 = form.img2.data
        if img2:
            filename2 = secure_filename(img2.filename)
            file_path2 = os.path.join(app.config['UPLOAD_FOLDER'], filename2)
            img2.save(file_path2)
            resize_image(file_path2, file_path2, app.config['MAX_IMAGE_SIZE'])
            img2_url = url_for('static', filename='images/' + filename2)
        else:
            img2_url = ''

        # Procesar imagen 3
        img3 = form.img3.data
        if img3:
            filename3 = secure_filename(img3.filename)
            file_path3 = os.path.join(app.config['UPLOAD_FOLDER'], filename3)
            img3.save(file_path3)
            resize_image(file_path3, file_path3, app.config['MAX_IMAGE_SIZE'])
            img3_url = url_for('static', filename='images/' + filename3)
        else:
            img3_url = ''

        # Insertar en la base de datos
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO producto (codigo, producto, detalle, imagen, img1, img2, img3, categoria, costo, por1, precio1, por2, precio2, stock) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                       (codigo, producto, detalle, imagen_url, img1_url, img2_url, img3_url, categoria, costo, por1, precio1, por2, precio2, stock))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('index'))

    return render_template('crud/create.html', form=form)


#*********************  EDITAR PRODUCTO ********************************************#
@app.route('/crud/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM producto WHERE id = %s', (id,))
    producto = cursor.fetchone()
    cursor.close()
    conn.close()
    
    if producto is None:
        flash('Producto no encontrado.', 'error')
        return redirect(url_for('index'))
    
    form = ProductForm(obj=producto)
    
    # Obtener las categorías desde la base de datos
    categorias = obtener_categorias()  # Esta función debe retornar [(id, nombre), ...]
    form.categoria.choices = categorias
    # Establece el valor actual de 'categoria' en el formulario
    
    # Asignar datos del producto al formulario solo en GET
    if request.method == 'GET':
        form.categoria.data = producto['categoria']
    
    temp_image_filename = None
    temp_img1_filename = None
    temp_img2_filename = None
    temp_img3_filename = None
    
    if form.validate_on_submit():
        if 'save' in request.form:
            codigo = form.codigo.data
            producto_name = form.producto.data
            detalle = form.detalle.data
            categoria = form.categoria.data
            #raise Exception(f"Valor de categoría seleccionado: {form.categoria.data}")
            costo = form.costo.data
            por1 = form.por1.data
            precio1 = form.precio1.data
            por2 = form.por2.data
            precio2 = form.precio2.data
            stock = form.stock.data
            
            # Validar que el código del producto no exista ya en la tabla
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT id FROM producto WHERE codigo = %s AND id != %s', (codigo, id))
            codigo_existente = cursor.fetchone()
            if codigo_existente:
                flash('El código del producto ya existe. Elija un código diferente.', 'warning')
                cursor.close()
                conn.close()
                return redirect(url_for('edit', id=id))

            
            imagen = form.imagen.data
            if imagen:
                temp_image_filename = secure_filename(imagen.filename)
                temp_file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'temp', temp_image_filename)
                final_file_path = os.path.join(app.config['UPLOAD_FOLDER'], temp_image_filename)
                imagen.save(temp_file_path)
                resize_image(temp_file_path, final_file_path, app.config['MAX_IMAGE_SIZE'])
                imagen_url = url_for('static', filename='images/' + temp_image_filename)
            else:
                imagen_url = producto['imagen']  # Utiliza la imagen ya guardada si no se sube una nueva

            img1 = form.img1.data
            if img1:
                temp_img1_filename = secure_filename(img1.filename)
                temp_file_path1 = os.path.join(app.config['UPLOAD_FOLDER'], 'temp', temp_img1_filename)
                final_file_path1 = os.path.join(app.config['UPLOAD_FOLDER'], temp_img1_filename)
                img1.save(temp_file_path1)
                resize_image(temp_file_path1, final_file_path1, app.config['MAX_IMAGE_SIZE'])
                img1_url = url_for('static', filename='images/' + temp_img1_filename)
            else:
                img1_url = producto['img1']

            img2 = form.img2.data
            if img2:
                temp_img2_filename = secure_filename(img2.filename)
                temp_file_path2 = os.path.join(app.config['UPLOAD_FOLDER'], 'temp', temp_img2_filename)
                final_file_path2 = os.path.join(app.config['UPLOAD_FOLDER'], temp_img2_filename)
                img2.save(temp_file_path2)
                resize_image(temp_file_path2, final_file_path2, app.config['MAX_IMAGE_SIZE'])
                img2_url = url_for('static', filename='images/' + temp_img2_filename)
            else:
                img2_url = producto['img2']

            img3 = form.img3.data
            if img3:
                temp_img3_filename = secure_filename(img3.filename)
                temp_file_path3 = os.path.join(app.config['UPLOAD_FOLDER'], 'temp', temp_img3_filename)
                final_file_path3 = os.path.join(app.config['UPLOAD_FOLDER'], temp_img3_filename)
                img3.save(temp_file_path3)
                resize_image(temp_file_path3, final_file_path3, app.config['MAX_IMAGE_SIZE'])
                img3_url = url_for('static', filename='images/' + temp_img3_filename)
            else:
                img3_url = producto['img3']

            final_imagen_url = imagen_url if imagen else producto['imagen']
            final_img1_url = img1_url if img1 else producto['img1']
            final_img2_url = img2_url if img2 else producto['img2']
            final_img3_url = img3_url if img3 else producto['img3']
            
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('UPDATE producto SET codigo = %s, producto = %s, detalle = %s, imagen = %s, img1 = %s, img2 = %s, img3 = %s, categoria = %s, costo = %s, por1 = %s, precio1 = %s, por2 = %s, precio2 = %s, stock = %s WHERE id = %s',
                           (codigo, producto_name, detalle, final_imagen_url, final_img1_url, final_img2_url, final_img3_url, categoria, costo, por1, precio1, por2, precio2, stock, id))
            conn.commit()
            cursor.close()
            conn.close()

            # Eliminar imágenes temporales
            if temp_image_filename:
                os.remove(os.path.join(app.config['UPLOAD_FOLDER'], 'temp', temp_image_filename))
            if temp_img1_filename:
                os.remove(os.path.join(app.config['UPLOAD_FOLDER'], 'temp', temp_img1_filename))
            if temp_img2_filename:
                os.remove(os.path.join(app.config['UPLOAD_FOLDER'], 'temp', temp_img2_filename))
            if temp_img3_filename:
                os.remove(os.path.join(app.config['UPLOAD_FOLDER'], 'temp', temp_img3_filename))

            return redirect(url_for('index'))

        elif 'cancel' in request.form:
            temp_image_path = os.path.join(app.config['UPLOAD_FOLDER'], 'temp', temp_image_filename) if temp_image_filename else None
            temp_img1_path = os.path.join(app.config['UPLOAD_FOLDER'], 'temp', temp_img1_filename) if temp_img1_filename else None
            temp_img2_path = os.path.join(app.config['UPLOAD_FOLDER'], 'temp', temp_img2_filename) if temp_img2_filename else None
            temp_img3_path = os.path.join(app.config['UPLOAD_FOLDER'], 'temp', temp_img3_filename) if temp_img3_filename else None

            if temp_image_path and os.path.isfile(temp_image_path):
                os.remove(temp_image_path)
            if temp_img1_path and os.path.isfile(temp_img1_path):
                os.remove(temp_img1_path)
            if temp_img2_path and os.path.isfile(temp_img2_path):
                os.remove(temp_img2_path)
            if temp_img3_path and os.path.isfile(temp_img3_path):
                os.remove(temp_img3_path)

            return redirect(url_for('index'))
    
    # Prellenar el formulario con el detalle actual   <--  DEBE IR AQUI
    form.detalle.data = producto['detalle']
    
    return render_template('crud/edit.html', form=form, producto=producto)


@app.route('/view/<int:id>')
@login_required
def view(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM producto WHERE id = %s', (id,))
    producto = cursor.fetchone()
    cursor.close()
    conn.close()
    return render_template('crud/view.html', producto=producto)

@app.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM producto WHERE id = %s', (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('index'))

#######################################################################
#######################    CATEGORIAS    ##############################
#######################################################################

@app.route('/crud/categ/categorias', methods=['GET', 'POST'])
@login_required
def categorias():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
        
    query = 'SELECT * FROM categorias'

    cursor.execute(query)
    
    categorias = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return render_template('crud/categ/categorias.html', categorias=categorias)


######################## CATEGORIAS - Create #########################
@app.route('/crud/categ/create_c', methods=['GET', 'POST'])
@login_required
def create_c():
    form = CategForm()
    
    if form.validate_on_submit():
        cat = form.cat.data
        nomcat = form.nomcat.data
        supercat = form.supercat.data
        superest = form.superest.data
        subcat = form.subcat.data
        subest = form.subest.data

        # Conexión a la base de datos
        conn = get_db_connection()
        cursor = conn.cursor()

        # Verificar si ya existe una categoría con el mismo valor
        cursor.execute('SELECT * FROM categorias WHERE cat = %s', (cat,))
        categoria_existente = cursor.fetchone()

        # Importante: Si hay más resultados, asegúrate de que no queden sin leer
        cursor.fetchall()  # Esto vacía cualquier resultado pendiente
        
        if categoria_existente:
            # Si la categoría ya existe, mostrar una advertencia
            #flash('La categoría ya existe. Por favor, elige otra.', 'warning')
            flash('⚠️ <strong>Advertencia:</strong> La categoría ya existe. Por favor, elige otra.', 'warning')
        else:
            # Insertar la nueva categoría si no existe
            cursor.execute('INSERT INTO categorias (cat, nomcat, supercat, superest, subcat, subest) VALUES (%s, %s, %s, %s, %s, %s)',
                           (cat, nomcat, supercat, superest, subcat, subest))
            conn.commit()
            #flash('Categoría creada exitosamente.', 'success')

            # Redirigir después de crear la categoría
            cursor.close()
            conn.close()
            return redirect(url_for('categorias'))  # Asegúrate de tener la ruta correcta

        cursor.close()
        conn.close()

    # Si la categoría es duplicada, el formulario se recarga con el mensaje de advertencia
    return render_template('crud/categ/create_c.html', form=form)

#-------------------------------------------------------------------------------#
############################    EDICION  ##############################
#-------------------------------------------------------------------------------#
@app.route('/crud/categ/edit_c/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_c(id):
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM categorias WHERE cat = %s', (id,))
    categoria = cursor.fetchone()
    cursor.close()
    conn.close()
    form = CategForm(obj=categoria)
   
    if categoria is None:
        flash('Categoria no encontrada.', 'error')
        return redirect(url_for('categorias'))

    if form.validate_on_submit():
        
        if 'save' in request.form:
            cat = form.cat.data
            nomcat = form.nomcat.data
            supercat = form.supercat.data
            superest = form.superest.data
            subcat = form.subcat.data
            subest = form.subest.data

            # Verificar si el nuevo código de categoría ya existe
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute('SELECT * FROM categorias WHERE cat = %s AND cat != %s', (cat, id))
            categoria_existente = cursor.fetchone()

            if categoria_existente:
                flash('El código de categoría ingresado ya existe. Por favor, elija un código diferente.', 'warning')
                cursor.close()
                conn.close()
                return render_template('crud/categ/edit_c.html', form=form, categoria=categoria)


            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('UPDATE categorias SET nomcat = %s, supercat = %s, superest = %s, subcat = %s, subest = %s WHERE cat = %s',
                           (nomcat, supercat, superest, subcat, subest, id))
            conn.commit()
            cursor.close()
            conn.close()

            return redirect(url_for('categorias'))

        elif 'cancel' in request.form:

            return redirect(url_for('categorias'))
    
    # Prellenar el formulario con los TextAreaField actuales   <--  DEBE IR AQUI
    form.supercat.data = categoria['supercat']
    form.subcat.data = categoria['subcat']
    
    return render_template('crud/categ/edit_c.html', form=form, categoria=categoria)

@app.route('/delete_c/<int:id>', methods=['POST'])
@login_required
def delete_c(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM categorias WHERE cat = %s', (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('categorias'))

def obtener_categorias():
    categorias = db.session.query(Cate.cat, Cate.nomcat).all()
    return [(int(c.cat), c.nomcat) for c in categorias]

######  MASCARA PARA IMPORTES  ######
def formato_pesos(value):
    formatted_value = "{:,.2f}".format(value)
    return formatted_value.replace(",", "#").replace(".", ",").replace("#", ".")
    
app.jinja_env.filters['formato_pesos'] = formato_pesos


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
    