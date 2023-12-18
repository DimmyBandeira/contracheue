from flask import Flask, render_template, request, send_file
import pymysql

app = Flask(__name__)

# Configurações de conexão com o banco de dados
db_config = {
    "host": "149.56.85.16",
    "user": "systemp1_contracheque",
    "password": "Sweda80@",
    "database": "systemp1_contracheque"
}

# Rota para exibir os usuários e links para os PDFs
@app.route('/usuarios')
def listar_usuarios():
    try:
        # Criar uma conexão com o banco de dados
        db = pymysql.connect(**db_config)
        cursor = db.cursor()

        # Consulta para recuperar os dados dos usuários e nomes dos arquivos PDF
        cursor.execute("SELECT id_usuario, nome, cpf, arquivo_pdf FROM usuarios")

        # Recupere todos os registros do banco de dados
        usuarios = cursor.fetchall()

        # Feche a conexão com o banco de dados
        cursor.close()
        db.close()

        # Renderize a página HTML e passe os dados para ela
        return render_template('lista_usuarios.html', usuarios=usuarios)

    except Exception as e:
        return f"Erro ao listar usuários: {str(e)}"

# Rota para baixar PDFs
@app.route('/download_pdf/<arquivo>')
def download_pdf(arquivo):
    try:
        # Substitua 'caminho_para_o_arquivo_pdf' pelo caminho real do arquivo PDF em seu sistema
        arquivo_path = f'./caminho/para/seu/pdf/{arquivo}.pdf'  

        # Configurar a resposta HTTP para baixar o arquivo como anexo
        return send_file(arquivo_path, as_attachment=True)

    except Exception as e:
        return f"Erro ao baixar PDF: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True, port=8081)  # Inicie na porta 8081 ou outra de sua escolha


