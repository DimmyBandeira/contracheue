import os
from PyPDF2 import PdfFileReader, PdfFileWriter
from flask import Flask, render_template, request, jsonify, Response
import threading
import time

app = Flask(__name__)

# Variável global para rastrear o progresso
progresso_atual = 0
processo_concluido = False

def count_pdf_pages(input_pdf_path):
    with open(input_pdf_path, 'rb') as pdf_file:
        pdf_reader = PdfFileReader(pdf_file)
        return pdf_reader.getNumPages()

def split_pdf_pages(input_pdf_path, output_directory, progress_callback):
    global progresso_atual  # Referência à variável global
    global processo_concluido

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    total_pages = count_pdf_pages(input_pdf_path)  # Conta o número total de páginas

    with open(input_pdf_path, 'rb') as pdf_file:
        pdf_reader = PdfFileReader(pdf_file)

        for page_number in range(total_pages):
            pdf_writer = PdfFileWriter()
            pdf_writer.addPage(pdf_reader.getPage(page_number))

            output_pdf_path = os.path.join(output_directory, f"page_{page_number + 1}.pdf")
            with open(output_pdf_path, 'wb') as output_file:
                pdf_writer.write(output_file)

            # Atualizar o progresso com base no número de páginas processadas e no total de páginas
            progresso_atual = (page_number + 1) / total_pages * 100
            progress_callback(progresso_atual)

    print(f"{total_pages} páginas do PDF separadas e salvas em {output_directory}")

    # Quando o processo estiver concluído, defina a variável global como True
    processo_concluido = True

def send_progress(progress_callback):
    while progresso_atual < 100:
        progress_callback(progresso_atual)
        time.sleep(1)

@app.route("/", methods=["GET", "POST"])
def index():
    global processo_concluido

    if request.method == "POST":
        uploaded_file = request.files["file"]
        if uploaded_file.filename != "":
            temp_pdf = "temp.pdf"
            uploaded_file.save(temp_pdf)

            output_directory = "pages"

            def progress_callback(progress):
                return progress

            progress_thread = threading.Thread(target=split_pdf_pages, args=(temp_pdf, output_directory, progress_callback))
            progress_thread.start()

            progress_sender_thread = threading.Thread(target=send_progress, args=(progress_callback,))
            progress_sender_thread.start()

            return "Arquivo enviado com sucesso!"

    return render_template("index.html", processo_concluido=processo_concluido)

@app.route("/progress")
def progress():
    def generate():
        while progresso_atual < 100:
            yield f"data: {progresso_atual}\n\n"
            time.sleep(1)
        yield "data: 100\n\n"
    
    return Response(generate(), mimetype="text/event-stream")

if __name__ == "__main__":
    app.run(debug=True)



