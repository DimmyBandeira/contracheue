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
                pdf = PdfFileReader(open(pdf_path, 'rb'))
                
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
                line_8 = csv_file.readlines()[7]  # Lê a linha 8 (índice 7)

            # Obtenha os três primeiros caracteres da linha 8
            new_name = line_8.strip()[:3]

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

