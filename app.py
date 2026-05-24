from flask import Flask, render_template, request, redirect, url_for, flash, session
from db import iniciar_bd, execute_query


app = Flask(__name__)
app.secret_key = 'chave_secreta_123'

iniciar_bd() #inicia o BD e as tabelas


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
        #session['usuario'] = email
        #flash('Login realizado com sucesso!', 'success')
        #return redirect(url_for('listar_usuarios'))
    return render_template('base.html')


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
    sql = '''
        SELECT id_usuario,
        nome,
        cpf,
        data_nascimento,
        email,
        cidade,
        estado,
        status
        FROM usuarios
        ORDER BY id_usuario DESC;
    '''
    lista_dados = execute_query(sql, fetch=True)
    return render_template('usuarios/listar_usuarios.html', dados=lista_dados)


@app.route('/usuarios/inserir', methods=['GET', 'POST'])
def inserir_usuario():
    if request.method == 'POST':
        nome = request.form.get('nome', '').strip()
        cpf = request.form.get('cpf', '').strip()
        data_nascimento = request.form.get('data_nascimento', '').strip()
        email = request.form.get('email', '').strip()
        pais = request.form.get('pais', 'Brasil').strip()
        estado = request.form.get('estado', '').strip()
        cidade = request.form.get('cidade', '').strip()
        senha = request.form.get('senha', '').strip()
        status = request.form.get('status', 'Ativo').strip()


        if not nome:
            flash('O campo <b>NOME<b> é obrigatório', 'danger')
            return redirect(url_for('inserir_usuario'))

        if not cpf:
            flash('O campo <b>CPF<b> é obrigatório', 'danger')
            return redirect(url_for('inserir_usuario'))

        if not data_nascimento:
            flash('O campo <b>DATA<b> DE NASCIMENTO é obrigatório', 'danger')
            return redirect(url_for('inserir_usuario'))

        if not senha:
            flash('O campo <b>SENHA<b> é obrigatório', 'danger')
            return redirect(url_for('inserir_usuario'))
        

        sql = '''
            INSERT INTO usuarios
                (nome, cpf, data_nascimento, email, pais,
                 estado, cidade, senha, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        '''
        execute_query(sql, params=(
            nome, cpf, data_nascimento, email, pais,
            estado, cidade, senha, status
        ))

        flash('Usuário cadastrado com sucesso!', 'success')
        return redirect(url_for('listar_usuarios'))

    livros = execute_query('SELECT id_livro, titulo FROM livros ORDER BY titulo', fetch=True)
    return render_template('usuarios/inserir_usuario.html', livros=livros)
# ─── Rotas protegidas — Autores ───────────────────────────────────────────────

@app.route('/autores/listar')
def listar_autores():
    sql = '''
        SELECT id_autor, 
        nome, 
        nacionalidade, 
        nascimento,
        genero, 
        falecimento, 
        biografia, 
        situacao
        FROM autores
        ORDER BY id_autor DESC;
    '''
    lista_dados = execute_query(sql, fetch=True)
    return render_template('autores/listar_autores.html', dados=lista_dados)


@app.route('/autores/inserir', methods=['GET', 'POST'])
def inserir_autor():
    if request.method == 'POST':
        nome = request.form.get('nome', '').strip()
        nacionalidade = request.form.get('nacionalidade', '').strip()
        nascimento = request.form.get('nascimento', '').strip()
        falecimento = request.form.get('falecimento', '').strip()
        falecimento = falecimento if falecimento else None
        biografia = request.form.get('biografia', '').strip()
        situacao = request.form.get('situacao', '').strip()
        genero = request.form.get('genero', '').strip()


        if not nome:
            flash('O campo <b>NOME<b> é obrigatório', 'danger')
            return redirect(url_for('cadastrar_funcao'))

        if not nacionalidade:
            flash('O campo <b>NACIONALIDADE<b> é obrigatório', 'danger')
            return redirect(url_for('cadastrar_funcao'))

        if not genero:
            flash('O campo <b>GENERO<b> é obrigatório', 'danger')
            return redirect(url_for('cadastrar_funcao'))

        if not nascimento:
            flash('O campo <b>NASCIMENTO<b> é obrigatório', 'danger')
            return redirect(url_for('cadastrar_funcao'))

        if not biografia:
            flash('O campo <b>BIOGRAFIA<b> é obrigatório', 'danger')
            return redirect(url_for('cadastrar_funcao'))
        
        if not situacao:
            flash('O campo <b>SITUACAO<b> é obrigatório', 'danger')
            return redirect(url_for('cadastrar_funcao'))

        sql = '''
            INSERT INTO autores 
                (nome, nacionalidade, nascimento, genero, falecimento, biografia, situacao)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        '''
        execute_query(sql, params=(
            nome, nacionalidade, nascimento, genero, falecimento, biografia, situacao
        ))

        flash('Autor cadastrado com sucesso!', 'success')
        return redirect(url_for('listar_autores'))
    return render_template('autores/inserir_autor.html')


# -- #
@app.route('/funcoes/cadastrar', methods=['GET', 'POST'])
def cadastrar_funcao():
    if request.method == 'POST':
        titulo = request.form.get('titulo', '').strip()
        genero = request.form.get('genero', '').strip()
        ano = request.form.get('ano', '').strip()
        autor = request.form.get('autor', '').strip()
        paginas = request.form.get('paginas', '').strip()
        sinopse = request.form.get('sinopse', '').strip()
        perm_cadastrar = 1 if request.form.get('perm_cadastrar') else 0
        perm_editar = 1 if request.form.get('perm_editar') else 0
        perm_excluir = 1 if request.form.get('perm_excluir') else 0
        perm_listar = 1 if request.form.get('perm_listar') else 0


        if not titulo:
            flash('O campo <b>TITULO<b> é obrigatório', 'danger')
            return redirect(url_for('cadastrar_funcao'))

        if not sinopse:
            flash('O campo <b>SINOPSE<b> é obrigatório', 'danger')
            return redirect(url_for('cadastrar_funcao'))

        if not genero:
            flash('O campo <b>GENERO<b> é obrigatório', 'danger')
            return redirect(url_for('cadastrar_funcao'))

        if not ano:
            flash('O campo <b>ANO<b> é obrigatório', 'danger')
            return redirect(url_for('cadastrar_funcao'))

        if not autor:
            flash('O campo <b>AUTOR<b> é obrigatório', 'danger')
            return redirect(url_for('cadastrar_funcao'))

        if not paginas:
            flash('O campo <b>PAGINAS<b> é obrigatório', 'danger')
            return redirect(url_for('cadastrar_funcao'))

        sql = '''
            INSERT INTO livros 
                (titulo, autor, genero, ano, paginas, sinopse,
                perm_cadastrar, perm_editar, perm_excluir, perm_listar)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        '''
        execute_query(sql, params=(
            titulo, autor, genero, ano, paginas, sinopse,
            perm_cadastrar, perm_editar, perm_excluir, perm_listar
        ))

        flash('Livro cadastrado com sucesso!', 'success')
        return redirect(url_for('listar_funcao'))

    return render_template('funcoes/cadastrar_funcao.html')
    

# -- #
@app.route('/funcoes/listar', methods=['GET', 'POST'])
def listar_funcao():
    sql = '''
        SELECT id_livro, 
        titulo, 
        autor, 
        genero, 
        sinopse,
        ano, 
        paginas
        FROM livros
        ORDER BY id_livro DESC;
    '''
    lista_dados = execute_query(sql, fetch=True)
    return render_template('funcoes/listar_funcao.html', dados=lista_dados)

# ─── Equipe ───────────────────────────────────────────────────────────────────

@app.route('/equipe')
def equipe():
    return render_template('sobre_equipe.html')


if __name__ == '__main__':
    app.run(debug=True)
