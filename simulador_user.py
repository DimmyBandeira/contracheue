import os
import pymysql

# Configurações de conexão com o banco de dados
db_config = {
    "host": "149.56.85.16",
    "user": "systemp1_contracheque",
    "password": "Sweda80@",
    "database": "systemp1_contracheque"
}

# Diretório onde os arquivos PDF estão localizados
pdf_directory = 'pages'

# Função para cadastrar usuários fictícios com base nos nomes dos arquivos PDF
def cadastrar_usuarios_ficticios(db_config, pdf_directory):
    try:
        # Criar uma conexão com o banco de dados
        db = pymysql.connect(**db_config)
        cursor = db.cursor()

        # Liste todos os arquivos PDF no diretório
        pdf_files = [f for f in os.listdir(pdf_directory) if f.endswith('.pdf')]

        # Para cada arquivo PDF, insira um usuário fictício com base no nome do arquivo
        for pdf_filename in pdf_files:
            # Use o nome do arquivo PDF (sem a extensão) como o ID do usuário fictício
            user_id = pdf_filename.replace('.pdf', '')

            # Nome fictício do usuário
            nome = f"Usuário {user_id}"

            # CPF fictício (você pode ajustar isso conforme necessário)
            cpf = "1234567890"

            # Insira o usuário fictício no banco de dados
            cursor.execute("INSERT INTO usuarios (nome, id_usuario, cpf) VALUES (%s, %s, %s)",
                           (nome, user_id, cpf))
            db.commit()

        # Feche a conexão com o banco de dados
        cursor.close()
        db.close()

        return True
    except Exception as e:
        print(f"Erro ao cadastrar usuários fictícios com base nos nomes dos arquivos PDF: {str(e)}")
        return False

if __name__ == '__main__':
    success = cadastrar_usuarios_ficticios(db_config, pdf_directory)
    if success:
        print('Usuários fictícios cadastrados com sucesso')
    else:
        print('Erro ao cadastrar usuários fictícios')
 
