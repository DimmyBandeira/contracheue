import pymysql
from flask import Flask, request, render_template

app = Flask(__name__)

# Configurações de conexão com o banco de dados
db_config = {
    "host": "149.56.85.16",
    "user": "systemp1_contracheque",
    "password": "Sweda80@",
    "database": "systemp1_contracheque"
}

# Rota para a página de cadastro de usuários
@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form['nome']
        id = request.form['id']
        cpf = request.form['cpf']

        # Criar uma conexão com o banco de dados
        db = pymysql.connect(**db_config)
        cursor = db.cursor()

        # Inserir dados no banco de dados
        cursor.execute("INSERT INTO usuarios (nome, id_usuario, cpf) VALUES (%s, %s, %s)", (nome, id, cpf))
        db.commit()

        cursor.close()
        db.close()

        return "Cadastro realizado com sucesso!"
    
    return render_template('cadastro.html')

if __name__ == '__main__':
    app.run(debug=True)


