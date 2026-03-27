from flask import Flask, render_template, request, redirect, url_for, flash, session

app = Flask(__name__)
app.secret_key = 'biblioteca-digital-secret-key-2024'

# ─── Dados simulados ────────────────────────────────────────────────────────

USUARIOS = [
    {'id': 1, 'nome': 'Ana Souza',       'email': 'ana@email.com',    'perfil': 'Admin'},
    {'id': 2, 'nome': 'Bruno Lima',      'email': 'bruno@email.com',  'perfil': 'Leitor'},
    {'id': 3, 'nome': 'Carla Mendes',    'email': 'carla@email.com',  'perfil': 'Leitor'},
    {'id': 4, 'nome': 'Diego Ferreira',  'email': 'diego@email.com',  'perfil': 'Editor'},
    {'id': 5, 'nome': 'Elisa Ramos',     'email': 'elisa@email.com',  'perfil': 'Leitor'},
]

AUTORES = [
    {'id': 1, 'nome': 'Machado de Assis',   'nacionalidade': 'Brasileira', 'nascimento': '21/06/1839', 'obras': 9},
    {'id': 2, 'nome': 'Clarice Lispector',  'nacionalidade': 'Brasileira', 'nascimento': '10/12/1920', 'obras': 17},
    {'id': 3, 'nome': 'Jorge Amado',        'nacionalidade': 'Brasileira', 'nascimento': '10/08/1912', 'obras': 32},
    {'id': 4, 'nome': 'Gabriel García Márquez', 'nacionalidade': 'Colombiana', 'nascimento': '06/03/1927', 'obras': 11},
    {'id': 5, 'nome': 'Franz Kafka',        'nacionalidade': 'Tcheca',    'nascimento': '03/07/1883', 'obras': 7},
]

LIVROS = [
    {'id': 1, 'titulo': 'Dom Casmurro',          'autor': 'Machado de Assis',       'ano': 1899, 'genero': 'Romance',   'paginas': 256},
    {'id': 2, 'titulo': 'A Hora da Estrela',      'autor': 'Clarice Lispector',      'ano': 1977, 'genero': 'Novela',    'paginas': 88},
    {'id': 3, 'titulo': 'Gabriela, Cravo e Canela','autor': 'Jorge Amado',           'ano': 1958, 'genero': 'Romance',   'paginas': 368},
    {'id': 4, 'titulo': 'Cem Anos de Solidão',    'autor': 'Gabriel García Márquez', 'ano': 1967, 'genero': 'Romance',   'paginas': 448},
    {'id': 5, 'titulo': 'A Metamorfose',          'autor': 'Franz Kafka',            'ano': 1915, 'genero': 'Ficção',    'paginas': 96},
    {'id': 6, 'titulo': 'Memórias Póstumas',      'autor': 'Machado de Assis',       'ano': 1881, 'genero': 'Romance',   'paginas': 208},
]

# ─── Rotas públicas ──────────────────────────────────────────────────────────

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        senha = request.form.get('senha', '').strip()
        if not email or not senha:
            flash('Preencha e-mail e senha.', 'danger')
            return render_template('login.html')
        # Simulação: qualquer combinação não-vazia é aceita
        session['usuario'] = email
        flash('Login realizado com sucesso!', 'success')
        return redirect(url_for('listar_usuarios'))
    return render_template('login.html')


@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome  = request.form.get('nome', '').strip()
        email = request.form.get('email', '').strip()
        senha = request.form.get('senha', '').strip()
        conf  = request.form.get('confirmacao', '').strip()
        erros = []
        if not nome:   erros.append('Nome é obrigatório.')
        if not email:  erros.append('E-mail é obrigatório.')
        if not senha:  erros.append('Senha é obrigatória.')
        if senha != conf: erros.append('As senhas não coincidem.')
        if erros:
            for e in erros:
                flash(e, 'danger')
            return render_template('cadastro.html')
        flash('Cadastro realizado! Faça o login.', 'success')
        return redirect(url_for('login'))
    return render_template('cadastro.html')


@app.route('/logout')
def logout():
    session.clear()
    flash('Você saiu da sessão.', 'info')
    return redirect(url_for('login'))

# ─── Rotas protegidas — Usuários ─────────────────────────────────────────────

@app.route('/usuarios/listar')
def listar_usuarios():
    return render_template('usuarios/listar_usuarios.html', usuarios=USUARIOS)


@app.route('/usuarios/inserir', methods=['GET', 'POST'])
def inserir_usuario():
    if request.method == 'POST':
        nome   = request.form.get('nome', '').strip()
        email  = request.form.get('email', '').strip()
        perfil = request.form.get('perfil', '').strip()
        senha  = request.form.get('senha', '').strip()
        erros  = []
        if not nome:   erros.append('Nome é obrigatório.')
        if not email:  erros.append('E-mail é obrigatório.')
        if not perfil: erros.append('Perfil é obrigatório.')
        if not senha:  erros.append('Senha é obrigatória.')
        if erros:
            for e in erros:
                flash(e, 'danger')
            return render_template('usuarios/inserir_usuario.html')
        flash('Usuário cadastrado com sucesso!', 'success')
        return redirect(url_for('listar_usuarios'))
    return render_template('usuarios/inserir_usuario.html')

# ─── Rotas protegidas — Autores ───────────────────────────────────────────────

@app.route('/autores/listar')
def listar_autores():
    return render_template('autores/listar_autores.html', autores=AUTORES)


@app.route('/autores/inserir', methods=['GET', 'POST'])
def inserir_autor():
    if request.method == 'POST':
        nome          = request.form.get('nome', '').strip()
        nacionalidade = request.form.get('nacionalidade', '').strip()
        nascimento    = request.form.get('nascimento', '').strip()
        erros = []
        if not nome:          erros.append('Nome é obrigatório.')
        if not nacionalidade: erros.append('Nacionalidade é obrigatória.')
        if not nascimento:    erros.append('Data de nascimento é obrigatória.')
        if erros:
            for e in erros:
                flash(e, 'danger')
            return render_template('autores/inserir_autor.html')
        flash('Autor cadastrado com sucesso!', 'success')
        return redirect(url_for('listar_autores'))
    return render_template('autores/inserir_autor.html')

# ─── Rotas protegidas — Livros ────────────────────────────────────────────────

@app.route('/livros/listar')
def listar_livros():
    return render_template('livros/listar_livros.html', livros=LIVROS)


@app.route('/livros/inserir', methods=['GET', 'POST'])
def inserir_livro():
    if request.method == 'POST':
        titulo  = request.form.get('titulo', '').strip()
        autor   = request.form.get('autor', '').strip()
        ano     = request.form.get('ano', '').strip()
        genero  = request.form.get('genero', '').strip()
        paginas = request.form.get('paginas', '').strip()
        erros   = []
        if not titulo:  erros.append('Título é obrigatório.')
        if not autor:   erros.append('Autor é obrigatório.')
        if not ano:     erros.append('Ano de publicação é obrigatório.')
        if not genero:  erros.append('Gênero é obrigatório.')
        if not paginas: erros.append('Número de páginas é obrigatório.')
        if erros:
            for e in erros:
                flash(e, 'danger')
            return render_template('livros/inserir_livro.html', autores=AUTORES)
        flash('Livro cadastrado com sucesso!', 'success')
        return redirect(url_for('listar_livros'))
    return render_template('livros/inserir_livro.html', autores=AUTORES)

# ─── Equipe ───────────────────────────────────────────────────────────────────

@app.route('/equipe')
def equipe():
    return render_template('sobre_equipe.html')


if __name__ == '__main__':
    app.run(debug=True)
