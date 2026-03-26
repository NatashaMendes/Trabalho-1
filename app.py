# Importa Flask e também a função render_template
from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def pagina_inicial():
    # render_template busca o arquivo na pasta templates/
    # e retorna seu conteúdo como resposta HTTP
    return render_template('index.html')


@app.route('/autor')
def autor():
    return render_template('autor.html')


@app.route('/livro')
def livro():
    return render_template('livro.html')

@app.route('/sobre_equipe')
def sobre_equipe():
    return render_template('sobre_equipe')


@app.route('/usuario/<nome>')
def perfil_usuario(nome):
    # <nome> na rota captura qualquer texto nessa posição da URL
    # Esse valor é passado automaticamente como parâmetro para a função
    # Exemplo: acessar /usuario/joao passa nome='joao' para esta função
    return f'<h1>Perfil do usuário: {nome}</h1><p>Olá, {nome}! Sua conta está ativa.</p>'
    # O 'f' antes das aspas cria uma f-string: permite inserir variáveis
    # Python diretamente no texto usando chaves {}




# Bloco de execução: só roda quando o arquivo é executado diretamente
if __name__ == '__main__':
    # debug=True ativa o recarregamento automático ao salvar o arquivo
    # NUNCA use debug=True em produção (servidor público)
    app.run(debug=True) 

