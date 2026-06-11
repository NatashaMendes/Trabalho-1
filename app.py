# session permite armazenar dados entre requisições do mesmo usuário,
# como as informações de quem está logado.
# wraps é necessário para criar o decorator login_required corretamente.
from functools import wraps
from flask import Flask, render_template, redirect, url_for, request, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from db import iniciar_bd, execute_query, execute_one

app = Flask(__name__)
app.secret_key = '123'

iniciar_bd()

@app.context_processor
def injetar_usuario():
    """
    Disponibiliza o usuário logado em todos os templates automaticamente.
    Agora retorna os dados reais da sessão em vez de None fixo.
    O template acessa com: usuario_logado.nome, usuario_logado.iniciais, etc.
    """
    return dict(usuario_logado=session.get('usuario'))

# ─── Rotas públicas ──────────────────────────────────────────────────────────

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/sobre')
def sobre():
    return render_template('sobre.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        senha = request.form.get('senha', '').strip()

        if not email or not senha:
            flash('Preencha e-mail e senha.', 'danger')
            return redirect(url_for('login'))

        usuario = execute_query(
            'SELECT * FROM usuarios WHERE email = %s',
            params=(email,), fetch=True
        )

        if not usuario:
            flash('E-mail ou senha inválidos.', 'danger')
            return redirect(url_for('login'))

        usuario = usuario[0]

        if usuario['senha'] != senha:
            flash('E-mail ou senha inválidos.', 'danger')
            return redirect(url_for('login'))

        if usuario['status'] != 'Ativo':
            flash('Usuário inativo. Contate o administrador.', 'warning')
            return redirect(url_for('login'))

        session['usuario'] = {
            'id':       usuario['id_usuario'],
            'nome':     usuario['nome'],
            'email':    usuario['email'],
        }

        flash(f'Bem-vindo, {usuario["nome"]}!', 'success')
        return redirect(url_for('listar_funcao'))

    return render_template('login.html')


@app.route('/logout')
def logout():
    # session.clear() remove todos os dados da sessão,
    # efetivamente deslogando o usuário.
    session.clear()
    flash('Sessão encerrada com sucesso.', 'info')
    return redirect(url_for('login'))


@app.route('/recuperar-senha')
def recuperar_senha():
    return render_template('forgot_password.html')


@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome  = request.form.get('nome', '').strip()
        email = request.form.get('email', '').strip()
        senha = request.form.get('senha', '').strip()
        conf  = request.form.get('confirmacao', '').strip()
        erros = []
        if not nome:      erros.append('Nome é obrigatório.')
        if not email:     erros.append('E-mail é obrigatório.')
        if not senha:     erros.append('Senha é obrigatória.')
        if senha != conf: erros.append('As senhas não coincidem.')
        if erros:
            for e in erros:
                flash(e, 'danger')
            return render_template('cadastro.html')

        sql = '''
            INSERT INTO usuarios (nome, email, senha)
            VALUES (%s, %s, %s)
        '''
        execute_query(sql, params=(nome, email, senha))

        flash('Cadastro realizado! Faça o login.', 'success')
        return redirect(url_for('login'))
    return render_template('cadastro.html')



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
        situacao = request.form.get('situacao', '').strip()
        livro_id = request.form.get('livro_id', '').strip()


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
        
        if not pais:
            flash('O campo <b>PAIS<b> é obrigatório', 'danger')
            return redirect(url_for('inserir_usuario'))
        
        if not estado:
            flash('O campo <b>ESTADO<b> é obrigatório', 'danger')
            return redirect(url_for('inserir_usuario'))
        
        if not cidade:
            flash('O campo <b>CIDADE<b> é obrigatório', 'danger')
            return redirect(url_for('inserir_usuario'))
        
        if not status:
            flash('O campo <b>STATUS<b> é obrigatório', 'danger')
            return redirect(url_for('inserir_usuario'))
        
        if not situacao:
            flash('O campo <b>SITUACAO<b> é obrigatório', 'danger')
            return redirect(url_for('inserir_usuario'))
        
        if not livro_id:
            flash('O campo <b>LIVRO_ID<b> é obrigatório', 'danger')
            return redirect(url_for('inserir_usuario'))

        sql = '''
            INSERT INTO usuarios
                (nome, cpf, data_nascimento, email, pais,
                 estado, cidade, senha, status, situacao, livro_id )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        '''
        execute_query(sql, params=(
            nome, cpf, data_nascimento, email, pais,
            estado, cidade, senha, status, situacao, livro_id
        ))

        flash('Usuário cadastrado com sucesso!', 'success')
        return redirect(url_for('listar_usuarios'))

    livros = execute_query('SELECT id_livro, titulo FROM livros ORDER BY titulo', fetch=True)
    return render_template('usuarios/inserir_usuario.html', livros=livros)


@app.route('/usuarios/alterar/<int:id>', methods=['GET', 'POST'])
def usuarios_alterar(id):
    if request.method == 'POST':
        nome = request.form.get('nome', '').strip()
        cpf = request.form.get('cpf', '').strip()
        data_nascimento = request.form.get('data_nascimento', '').strip() or None
        email = request.form.get('email', '').strip()
        pais = request.form.get('pais', 'Brasil').strip()
        estado = request.form.get('estado', '').strip()
        cidade = request.form.get('cidade', '').strip()
        senha = request.form.get('senha', '').strip()
        status = request.form.get('status', '').strip()
        situacao = request.form.get('situacao', '').strip()
        livro_id = request.form.get('livro_id', '').strip()

        if not all([nome, cpf, estado, cidade, status, situacao]):
            flash('Preencha todos os campos obrigatórios.', 'danger')
            return redirect(url_for('usuarios_alterar', id=id))

        try:
            if senha:
                sql = '''
                    UPDATE usuarios SET
                        nome = %s, cpf = %s, data_nascimento = %s,
                        email = %s, pais = %s, estado = %s, cidade = %s,
                        senha = %s, status = %s, situacao = %s, livro_id = %s
                    WHERE id_usuario = %s
                '''
                dados = (nome, cpf, data_nascimento, email, pais,
                         estado, cidade, senha, status, situacao, livro_id, id)
            else:
                sql = '''
                    UPDATE usuarios SET
                        nome = %s, cpf = %s, data_nascimento = %s,
                        email = %s, pais = %s, estado = %s, cidade = %s,
                        status = %s, situacao = %s, livro_id = %s
                    WHERE id_usuario = %s
                '''
                dados = (nome, cpf, data_nascimento, email, pais,
                         estado, cidade, status, situacao, livro_id, id)

            execute_query(sql, dados)
            flash(f'Usuário {nome} alterado com sucesso!', 'success')
            return redirect(url_for('listar_usuarios'))

        except Exception as e:
            flash(f'Erro ao alterar usuário: {e}', 'danger')
            return redirect(url_for('usuarios_alterar', id=id))

    item = execute_query(
        'SELECT * FROM usuarios WHERE id_usuario = %s', params=(id,), fetch=True
    )
    if not item:
        flash('Usuário não encontrado.', 'danger')
        return redirect(url_for('listar_usuarios'))

    livros = execute_query('SELECT id_livro, titulo FROM livros ORDER BY titulo', fetch=True)
    return render_template('usuarios/inserir_usuario.html', 
                           item=item[0], livros=livros)


@app.route('/usuarios/excluir/<int:id>', methods=['POST'])
def excluir_usuario(id):
    try:
        execute_query('DELETE FROM usuarios WHERE id_usuario = %s', params=(id,))
        flash('Usuario excluído com sucesso.', 'success')
    except Exception as e:
        flash(f'Erro ao excluir usuario: {e}', 'danger')
    return redirect(url_for('listar_usuario'))

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


@app.route('/autores/alterar/<int:id>', methods=['GET', 'POST'])
def autores_alterar(id):
    if request.method == 'POST':
        nome           = request.form.get('nome', '').strip()
        nacionalidade  = request.form.get('nacionalidade', '').strip()
        nascimento     = request.form.get('nascimento', '').strip()
        falecimento    = request.form.get('falecimento', '').strip() or None
        biografia      = request.form.get('biografia', '').strip()
        situacao       = request.form.get('situacao', '').strip()
        genero         = request.form.get('genero', '').strip()

        sql = '''
            UPDATE autores SET
                nome = %s, nacionalidade = %s, nascimento = %s,
                falecimento = %s, biografia = %s, situacao = %s, genero = %s
            WHERE id_autor = %s
        '''
        execute_query(sql, params=(
            nome, nacionalidade, nascimento, falecimento,
            biografia, situacao, genero, id
        ))
        flash('Autor alterado com sucesso!', 'success')
        return redirect(url_for('listar_autores'))

    item = execute_query(
        'SELECT * FROM autores WHERE id_autor = %s', params=(id,), fetch=True
    )
    if not item:
        flash('Autor não encontrado.', 'danger')
        return redirect(url_for('listar_autores'))

    return render_template('autores/inserir_autor.html', item=item[0])


@app.route('/autores/excluir/<int:id>', methods=['POST'])
def excluir_autor(id):
    try:
        execute_query('DELETE FROM autores WHERE id_autor = %s', params=(id,))
        flash('Autor excluído com sucesso.', 'success')
    except Exception as e:
        flash(f'Erro ao excluir autor: {e}', 'danger')
    return redirect(url_for('listar_autores'))

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


@app.route('/funcoes/alterar/<int:id>', methods=['GET', 'POST'])
def funcoes_alterar(id):
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
            flash('O campo <b>Titulo</b> é obrigatório.', 'danger')
            return redirect(url_for('funcoes_alterar', id=id))

        try:
            sql = '''
                UPDATE funcoes SET
                    titulo               = %s,
                    genero             = %s,
                    ano  = %s,
                    autor = %s,
                    paginas = %s,
                    sinopse          = %s,
                    perm_cadastrar  = %s,
                    perm_editar = %s,
                    perm_excluir  = %s,
                    perm_listar = %s
                WHERE id_funcao = %s
            '''
            dados = (titulo, genero, ano,
                     autor, paginas, sinopse, perm_cadastrar, perm_editar, perm_excluir, perm_listar, id)
            execute_query(sql, dados)
            flash(f'Função <b>{titulo}</b> alterada com sucesso!', 'success')
            return redirect(url_for('funcoes_listar'))
        except Exception as e:
            flash(f'Erro ao alterar função: {e}', 'danger')
            return redirect(url_for('funcoes_alterar', id=id))

    item = execute_one('SELECT * FROM funcoes WHERE id_funcao = %s', (id,))
    if not item:
        flash('Função não encontrada.', 'danger')
        return redirect(url_for('funcoes_listar'))

    return render_template('dashboard/funcoes/form.html',
                           titulo='Alterar Função', modo='alterar', item=item)


@app.route('/funcoes/excluir/<int:id>', methods=['POST'])
def excluir_livro(id):
    try:
        execute_query('DELETE FROM livros WHERE id_livro = %s', params=(id,))
        flash('Livro excluído com sucesso.', 'success')
    except Exception as e:
        flash(f'Erro ao excluir livro: {e}', 'danger')
    return redirect(url_for('listar_funcao'))
# ─── Equipe ───────────────────────────────────────────────────────────────────

@app.route('/equipe')
def equipe():
    return render_template('sobre_equipe.html')


if __name__ == '__main__':
    app.run(debug=True)
