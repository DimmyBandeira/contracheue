import os
from PyPDF2 import PdfFileReader
from tabula import read_pdf
from tqdm import tqdm

# Diretório onde os PDFs estão localizados
pdf_directory = 'pages'

# Função para converter uma página do PDF em CSV
def convert_page_to_csv(pdf_path, page_number, csv_path):
    try:
        # Use a biblioteca tabula para extrair a página do PDF como um DataFrame
        df = read_pdf(pdf_path, pages=page_number)[0]
        
        # Salve o DataFrame em um arquivo CSV separado
        df.to_csv(csv_path, index=False)
        
        return True
    except Exception as e:
        print(f"Erro ao converter a página {page_number} para CSV: {str(e)}")
        return False

# Função para converter todos os PDFs no diretório
def convert_all_pdfs():
    try:
        # Liste todos os arquivos PDF no diretório
        pdf_files = [f for f in os.listdir(pdf_directory) if f.endswith('.pdf')]

        # Crie um diretório temporário para salvar os arquivos CSV
        temp_dir = 'temp_csv'
        os.makedirs(temp_dir, exist_ok=True)

        # Progresso usando tqdm
        with tqdm(total=len(pdf_files), desc="Convertendo PDFs para CSVs") as pbar:
            # Para cada arquivo PDF, inicie uma thread de conversão
            for pdf_filename in pdf_files:
                pdf_path = os.path.join(pdf_directory, pdf_filename)
                with open(pdf_path, 'rb') as file:
                    pdf = PdfFileReader(file)
                    for page_number in range(pdf.getNumPages()):
                        csv_filename = os.path.join(temp_dir, f'{pdf_filename}_page_{page_number + 1}.csv')
                        convert_page_to_csv(pdf_path, page_number + 1, csv_filename)
                        pbar.update(1)

            pbar.close()

        # Renomeie os arquivos PDF com base na linha 8 de cada CSV
        for pdf_filename in pdf_files:
            pdf_path = os.path.join(pdf_directory, pdf_filename)
            csv_filename = os.path.join(temp_dir, f'{pdf_filename}_page_1.csv')
            
            # Abra o CSV e leia a linha 8
            with open(csv_filename, 'r', encoding='utf-8') as csv_file:
                lines = csv_file.readlines()
                csv_file.close()

            line_8 = lines[7].replace('\n', '')  # Lê a linha 8 (índice 7)
            line_2 = lines[1].replace('\n', '')
            if(pdf_path.__contains__('_9')):
                print('chegou')
            # Obtenha os três primeiros caracteres da linha 8
            ano = line_2.split(',')[1].split(' ')[2]
            mes = buscarNumeroMes(line_2.split(',')[1].split(' ')[0])
            id_usuario = line_8.split(' ')[0]
            new_name = ano + mes + id_usuario

            # Renomeie o arquivo PDF
            new_pdf_filename = f'{new_name}.pdf'
            new_pdf_path = os.path.join(pdf_directory, new_pdf_filename)
            os.rename(pdf_path, new_pdf_path)

        return True
    except Exception as e:
        print(f"Erro ao processar os PDFs: {str(e)}")
        return False

if __name__ == '__main__':
    success = convert_all_pdfs()
    if success:
        print('Conversão e renomeação concluídas')
    else:
        print('Erro ao processar os PDFs')


def buscarNumeroMes(nomeMes):
    if nomeMes == 'Janeiro':
        return '01'
    elif nomeMes == 'Fevereiro':
        return '02'
    elif nomeMes == 'Março':
        return '03'
    elif nomeMes == 'Abril':
        return '04'
    elif nomeMes == 'Maio':
        return '05'
    elif nomeMes == 'Junho':
        return '06'
    elif nomeMes == 'Julho':
        return '07'
    elif nomeMes == 'Agosto':
        return '08'
    elif nomeMes == 'Setembro':
        return '09'
    elif nomeMes == 'Outubro':
        return '10'
    elif nomeMes == 'Novembro':
        return '11'
    elif nomeMes == 'Dezembro':
        return '12'
    else:
        return '00'