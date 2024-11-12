# é necessário instalar o PyMuPDF e o Flaskantes, execute no CMD:
# pip install PyMuPDF
# pip install Flask

# A correta configuração do leitor exigiria um domínio dos pontos (pt, a unidade de m,edida padrão dos PDFs),]
# mas seria conveniente um serviço como adobe acrobat, que é pago.
# Outra solução é com um campo amostral de PDFs maior, sabendo-se que de o método que extrai os dados se mostra bastante maleável,
# aceitando valores extras para ajustar o padding de cada variável individualmente.
#
#
# API Flask: O Flask é usado para criar um servidor web simples.
# Rota /upload_pdf: O endpoint /upload_pdf recebe um arquivo PDF via método POST. O arquivo é salvo temporariamente no servidor e processado.
# Envio de Arquivo via HTTP: O arquivo PDF é enviado por um cliente (como um navegador ou outro script).
#
# O algoritmo identifica o sucesso em coletar dados de todos os campos. Caso o faça, envia junto ao json a String 
# status : "success", enquanto a falha envia junto ao json status : "failed", junto com uma chave cujo valor 
# não identificado volta como null.

# Para executar a aplicação:
# 1) Instalar dependencias:
#
#    pip install Flask
#    pip install PyMuPDF
#
# 2) configure o servidor Flask:
#
#   2.1] Alterar o Host: substitua app.run(debug=True) por app.run(host='0.0.0.0', port=5000, debug=True). 
#   Isso faz com que o Flask escute em todas as interfaces de rede da máquina, permitindo que outros dispositivos
#   na mesma rede acessem a aplicação.
#
#   2.2] Permissões de Firewall: Verifique se o firewall do sistema permite conexões na porta 5000.
#   Se necessário, adicione uma regra para liberar essa porta.
#
#   2.3] Acesso pela Rede: Depois de configurar, outro dispositivo poderá acessar a aplicação substituindo 127.0.0.1 
#   pelo endereço IP da máquina onde o Flask está rodando. Por exemplo, se o IP for 192.168.1.10,
#   a URL de acesso seria http://192.168.1.10:5000/upload_pdf.
#
# 3) Inicie o servidor Flask:
#  Após abrir o atual diretóro no CMD, digite:
#
#    python leitor_pdf_labfertil_V4.py
#
#  ou rode a aplicação por uma IDE.
#
# 4)Enviar o PDF via POST Request:
#  Usando cURL: No CMD, execute:
#
#    curl -X POST -F "file=@C:/caminho/para/seu/arquivo/Exemplo de Laudo - Análise de Solo.pdf" http://127.0.0.1:5000/upload_pdf
#
# 5)Receber a resposta:
#  A resposta será um JSON contendo os dados extraídos do PDF.
#
#                             -
#                             ^
#                          y1-| - -X===============X
#                             |    |###############|
#                          y0-| - -X===============X
#                             |    '               '
#                             |    '               '
#    - <______________________|____'_______________'___> +
#                             |    '               '
#                             |    xo              x1 
#                             |
#                             V
#      
from flask import Flask, request, jsonify
import fitz  # PyMuPDF
import json

app = Flask(__name__)


def extrair_valor_k(pdf_path):
    pdf_document = fitz.open(pdf_path)
    page = pdf_document[0]
    valor = extrair_valor_abaixo(page, "K ", -10, 0, 10, 11)
    pdf_document.close()
    return valor

def extrair_valor_bases_v(pdf_path):
    pdf_document = fitz.open(pdf_path)
    page = pdf_document[0]
    valor = extrair_valor_abaixo(page, "Bases", -10, 0, 10, 11)
    pdf_document.close()
    return valor

def extrair_valor_argila(pdf_path):
    pdf_document = fitz.open(pdf_path)
    page = pdf_document[0]
    valor = extrair_valor_abaixo(page, "Argila", -10, 0, 10, 11)
    pdf_document.close()
    return valor

def extrair_valor_p(pdf_path):
    pdf_document = fitz.open(pdf_path)
    page = pdf_document[0]
    valor = extrair_valor_abaixo(page, " P ", -10, 0, 10, 11)
    pdf_document.close()
    return valor

def extrair_valor_ind_smp(pdf_path):
    pdf_document = fitz.open(pdf_path)
    page = pdf_document[0]  # Primeira página
    valor = extrair_valor_abaixo(page, "SMP", -10, 0, 10, 15)
    pdf_document.close()
    return valor

def extrair_valor_ctc(pdf_path):
    pdf_document = fitz.open(pdf_path)
    page = pdf_document[0]
    valor = extrair_valor_abaixo(page, "CTC (pH 7,0)", -10, 0, 10, 11)
    pdf_document.close()
    return valor

def extrair_valor_abaixo(page, keyword, left=-5, top=0, right=5, below=11):
    # Localiza o texto da palavra-chave na página
    text_instances = page.search_for(keyword)
    if text_instances:
        # Pega o primeiro resultado encontrado
        rect = text_instances[0]
        
        # Define uma área logo abaixo da palavra-chave para capturar o valor
        below_rect = fitz.Rect(rect.x0 + left, rect.y1 + top, rect.x1 + right, rect.y1 + below)
        
        # Extrai o texto da área abaixo
        value = page.get_text("text", clip=below_rect).strip()
        return value
    return None

@app.route('/upload_pdf', methods=['POST'])
def upload_pdf():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    # Salva o arquivo PDF temporariamente
    pdf_path = './temp_pdf.pdf'
    file.save(pdf_path)



    

    # Extração dos dados
    SMP = extrair_valor_ind_smp(pdf_path)
    K = extrair_valor_k(pdf_path)
    base = extrair_valor_bases_v(pdf_path)
    argila = extrair_valor_argila(pdf_path)
    P = extrair_valor_p(pdf_path)
    CTC = extrair_valor_ctc(pdf_path)

    if(SMP == None or K == None or base == None or argila == None or P == None or CTC == None):
        status = "failed"
    else:
        status = "success"

    if(SMP != None):
        SMP = SMP.replace(',', '.')#Substituição de vírgulas por pontos
        SMP = float(SMP)#transforma os dados em float
    if(K != None):
        K = K.replace(',', '.')
        K = float(K)
    if(base != None):
        base = base.replace(',', '.')
        base = float(base)
    if(argila != None):
        argila = argila.replace(',', '.')
        argila = float(argila)
    if(P != None):
        P = P.replace(',', '.')
        P = float(P)
    if(CTC != None):
        CTC = CTC.replace(',', '.')
        CTC = float(CTC)

    # Armazenando os dados em um dicionário
    dados_analise = {
        "status": status,
        "bases": base,
        "SMP": SMP,
        "CTC_ph7": CTC,
        "argila": argila,
        "P": P,
        "K": K,
    }

    # Convertendo o dicionário para JSON
    dados_json = json.dumps(dados_analise, indent=4, ensure_ascii=False)
    print(dados_json)
    return jsonify(dados_json)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
