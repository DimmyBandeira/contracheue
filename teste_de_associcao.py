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

def associate_pdfs_to_users(db_config, pdf_directory):
    try:
        # Criar uma conexão com o banco de dados
        db = pymysql.connect(**db_config)
        cursor = db.cursor()

        # Listar os arquivos PDF no diretório
        pdf_files = [f for f in os.listdir(pdf_directory) if f.endswith('.pdf')]

        # Iterar pelos arquivos PDF e associá-los aos usuários
        for pdf_filename in pdf_files:
            # Extrair o ID do usuário do nome do arquivo PDF (supondo que o nome seja o ID)
            id_usuario = pdf_filename.replace('.pdf', '')

            # Verificar se o ID do usuário existe no banco de dados
            cursor.execute("SELECT id_usuario FROM usuarios WHERE id_usuario = %s", (id_usuario,))
            resultado = cursor.fetchone()

            if resultado:
                # Se o ID do usuário existir, atualize a coluna 'arquivo_pdf' com o nome do arquivo PDF
                cursor.execute("UPDATE usuarios SET arquivo_pdf = %s WHERE id_usuario = %s", (pdf_filename, id_usuario))
                db.commit()
            else:
                print(f"Usuário com ID {id_usuario} não encontrado no banco de dados.")

        # Feche a conexão com o banco de dados
        cursor.close()
        db.close()

        return True
    except Exception as e:
        print(f"Erro ao associar PDFs aos usuários: {str(e)}")
        return False

if __name__ == '__main__':
    success = associate_pdfs_to_users(db_config, pdf_directory)
    if success:
        print('Associação de PDFs aos usuários concluída com sucesso')
    else:
        print('Erro ao associar PDFs aos usuários')
