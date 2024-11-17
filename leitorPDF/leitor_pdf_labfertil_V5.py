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
#    pip install flask-cors
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
#    python leitor_pdf_labfertil_V5.py
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
from flask_cors import CORS # type: ignore

app = Flask(__name__)
CORS(app)

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

def extrair_valor_k(pdf_path):
    pdf_document = fitz.open(pdf_path)
    page = pdf_document[0]
    valor = extrair_valor_abaixo(page, "K ", -10, 0, 10, 90)
    pdf_document.close()
    return valor

# valor das bases(%V)removido do projeto final
def extrair_valor_bases_v(pdf_path):
    pdf_document = fitz.open(pdf_path)
    page = pdf_document[0]
    valor = extrair_valor_abaixo(page, "Bases", -5, 0, 25, 90)
    pdf_document.close()
    return valor

def extrair_valor_argila(pdf_path):
    pdf_document = fitz.open(pdf_path)
    page = pdf_document[0]
    valor = extrair_valor_abaixo(page, "Argila", -5, 0, 5, 90)
    pdf_document.close()
    return valor

def extrair_valor_p(pdf_path):
    pdf_document = fitz.open(pdf_path)
    page = pdf_document[0]
    valor = extrair_valor_abaixo(page, " P ", -10, 0, 10, 90)
    pdf_document.close()
    return valor

def extrair_valor_ind_smp(pdf_path):
    pdf_document = fitz.open(pdf_path)
    page = pdf_document[0]  # Primeira página
    valor = extrair_valor_abaixo(page, "SMP", -5, 0, 10, 90)
    pdf_document.close()
    return valor

def extrair_valor_ctc(pdf_path):
    pdf_document = fitz.open(pdf_path)
    page = pdf_document[0]
    valor = extrair_valor_abaixo(page, "CTC (pH 7,0)", -10, 0, 10, 90)
    pdf_document.close()
    return valor

def extrair_valor_ref(pdf_path):
    pdf_document = fitz.open(pdf_path)
    page = pdf_document[0]  # Primeira página
    valor = extrair_valor_abaixo(page, " Ref. ", -30, 0, 35, 110)
    pdf_document.close()
    return valor
def trata_dados(data):
    # Divide a string por espaços e substitui vírgulas por pontos
    data = data.split()
    data = [elemento.replace(',', '.') for elemento in data]

    # Verifica se todos os valores podem ser convertidos para float
    for valor in data:
        try:
            float(valor)
        except ValueError:
            valor = "erro"
            return valor

    # Converte todos os valores para float
    data = [float(valor) for valor in data]
    print(data, "len(", len(data), ")")
    return data

def criar_json( CTC, SMP, K, P, argila, ref):

    # Verifica se todos os arrays possuem o mesmo tamanho
    n = len(CTC)
    if not all(len(arr) == n for arr in [SMP, K, P, argila, ref]):
        return json.dumps({"status": "failed", "error": "Os arrays têm tamanhos diferentes"})
    if n == 0:
        return json.dumps({"status": "failed", "error": "Nenhum valor capturado"})
    
    
    # Cria a lista de dicionários para o JSON
    data = []
    for i in range(n):
        item = {
            "id": i + 1,  # Define o ID iniciando em 1
            "ref":ref[i],
            "SMP": SMP[i],
            "CTC_ph7": CTC[i],
            "argila": argila[i],
            "P": P[i],
            "K": K[i]
        }
        data.append(item)
    
    # Estrutura o JSON final
    resultado = {
        "status": "success",
        "data": data
    }
    
    # Converte para JSON formatado
    return json.dumps(resultado, indent=4, ensure_ascii=False)

print('''

    __       _  __                               __ ____     __        __     ____             __   _  __            ______                
   / /___   (_)/ /_ ____   _____     ____   ____/ // __/    / /____ _ / /_   / __/___   _____ / /_ (_)/ /    _   __ / ____/   ____   __  __
  / // _ \ / // __// __ \ / ___/    / __ \ / __  // /_     / // __ `// __ \ / /_ / _ \ / ___// __// // /    | | / //___ \    / __ \ / / / /
 / //  __// // /_ / /_/ // /       / /_/ // /_/ // __/    / // /_/ // /_/ // __//  __// /   / /_ / // /     | |/ /____/ /_  / /_/ // /_/ / 
/_/ \___//_/ \__/ \____//_/______ / .___/ \__,_//_/______/_/ \__,_//_.___//_/   \___//_/    \__//_//_/______|___//_____/(_)/ .___/ \__, /  
                          /_____//_/              /_____/                                            /_____/              /_/     /____/   

      ''')

@app.route('/')
def home():
    
    return "servidor online🔥🔥🔥"

@app.route('/upload_pdf', methods=['POST'])
def upload_pdf():
    if 'file' not in request.files:
        log = {
            "status" : "failed",
            "error" : "não há arquivo"            
        }
        return jsonify(log), 400
    file = request.files['file']
    
    if file.filename == '':
        log = {
            "status" : "failed",
            "error" : "Não há arquivo selecionado"            
        }
        return jsonify(log), 400
    
    # Salva o arquivo PDF temporariamente
    pdf_path = './temp_pdf.pdf'
    file.save(pdf_path)

    # Extração dos dados
    SMP = extrair_valor_ind_smp(pdf_path)
    K = extrair_valor_k(pdf_path)
    #base = extrair_valor_bases_v(pdf_path)
    argila = extrair_valor_argila(pdf_path)
    P = extrair_valor_p(pdf_path)
    CTC = extrair_valor_ctc(pdf_path)
    ref = extrair_valor_ref(pdf_path)

    CTC = trata_dados(CTC)
    #base = trata_dados(base)
    K = trata_dados(K)
    argila = trata_dados(argila)
    P = trata_dados(P)
    SMP = trata_dados(SMP)
    ref = ref.split('\n')
    print(ref,"len(" ,len(ref),")")

    if (CTC == "erro" or K == "erro" or argila == "erro" or P == "erro" or SMP == "erro"):
        log = {
            "status" : "failed",
            "error" : "presença de valor não numérico"            
        }
        print(log)
        return jsonify(log), 400
    
    else:

        json_resultado = criar_json(CTC, SMP, K, P, argila, ref)
        print(json_resultado)
        
        print('''

                                      __                   __                                                                            
.---.-..-----..--.--..---.-..----..--|  |.---.-..-----..--|  |.-----.    .-----..-----..--.--..---.-.    .----..-----..-----.            
|  _  ||  _  ||  |  ||  _  ||   _||  _  ||  _  ||     ||  _  ||  _  |    |     ||  _  ||  |  ||  _  |    |   _||  -__||  _  | __  __  __ 
|___._||___  ||_____||___._||__|  |_____||___._||__|__||_____||_____|    |__|__||_____| \___/ |___._|    |__|  |_____||__   ||__||__||__|
       |_____|                                                                                                           |__|            

          ''')
        return jsonify(json_resultado)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
    #app.run(debug=True)
