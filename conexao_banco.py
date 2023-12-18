import pymysql

# Configurações de conexão com o banco de dados
db_config = {
    "host": "149.56.85.16",
    "user": "systemp1_contracheque",
    "password": "Sweda80@",
    "database": "systemp1_contracheque"
}

# Função para obter uma conexão com o banco de dados
def get_db_connection():
    try:
        connection = pymysql.connect(**db_config)
        print("Conexão com o banco de dados bem-sucedida.")
        return connection
    except pymysql.Error as error:
        print(f"Erro ao conectar ao banco de dados: {error}")
        return None



