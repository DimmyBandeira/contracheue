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

# Função para salvar os arquivos PDF no banco de dados
def save_pdfs_to_database(db_config):
    try:
        # Criar uma conexão com o banco de dados
        db = pymysql.connect(**db_config)
        cursor = db.cursor()

        # Consulta SQL para adicionar uma coluna de chave estrangeira à tabela de PDFs
        alter_table_sql = """
        ALTER TABLE tabela_de_pdfs
        ADD COLUMN id_usuario INT,
        ADD FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario);
        """

        # Execute o comando SQL para adicionar a chave estrangeira
        cursor.execute(alter_table_sql)

        # Commit para salvar as alterações
        db.commit()

        # Para cada arquivo PDF, faça o seguinte:
        for pdf_filename in os.listdir(pdf_directory):
            pdf_path = os.path.join(pdf_directory, pdf_filename)

            # O nome do arquivo PDF (pdf_filename) já é o ID do usuário
            user_id = pdf_filename.replace('.pdf', '')

            # Leia o conteúdo do arquivo PDF
            with open(pdf_path, 'rb') as pdf_file:
                pdf_content = pdf_file.read()

            # Insira o conteúdo do PDF no banco de dados associado ao usuário
            cursor.execute("INSERT INTO tabela_de_pdfs (id_usuario, conteudo_pdf) VALUES (%s, %s)",
                           (user_id, pdf_content))
            db.commit()

        # Feche a conexão com o banco de dados
        cursor.close()
        db.close()

        return True
    except Exception as e:
        print(f"Erro ao salvar arquivos PDF no banco de dados: {str(e)}")
        return False

if __name__ == '__main__':
    success = save_pdfs_to_database(db_config)
    if success:
        print('Arquivos PDF associados aos usuários e salvos no banco de dados com sucesso')
    else:
        print('Erro ao associar arquivos PDF aos usuários e salvar no banco de dados')
