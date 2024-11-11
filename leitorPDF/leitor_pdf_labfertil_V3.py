# é necessário instalar o PyMuPDF antes, execute no CMD:
# pip install PyMuPDF

# A correta configuração do leitor exigiria um domínio dos pontos (pt, a unidade de m,edida padrão dos PDFs),]
# mas seria conveniente um serviço como adobe acrobat, que é pago.
# Outra solução é com um campo amostral de PDFs maior, sabendo-se que de o método que extrai os dados se mostra bastante maleável,
# aceitando valores extras para ajustar o padding de cada variável individualmente.
#
#
#   A V3 corresponde a um script executavel dentro da linha de comando. abra o atual diretório no CMD e digite:
#   python leitor_pdf_labfertil_V3.py "Exemplo de Laudo - Análise de Solo.pdf"
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


import fitz  # PyMuPDF
import json  # Biblioteca para manipulação de JSON
import argparse  # Para manipulação de argumentos de linha de comando


def extrair_valor_ind_smp(pdf_path):
    pdf_document = fitz.open(pdf_path)
    page = pdf_document[0]  # Primeira página
    valor = extrair_valor_abaixo(page, "SMP", -10, 0, 10, 15)
    pdf_document.close()
    return valor

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

# Função auxiliar para encontrar o valor abaixo de uma palavra-chave
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

def main(pdf_path):
    # Extração dos dados
    SMP = extrair_valor_ind_smp(pdf_path)
    K = extrair_valor_k(pdf_path)
    base = extrair_valor_bases_v(pdf_path)
    argila = extrair_valor_argila(pdf_path)
    P = extrair_valor_p(pdf_path)

    #Substituição de vírgulas por pontos
    SMP = SMP.replace(',', '.')
    K = K.replace(',', '.')
    base = base.replace(',', '.')
    argila = argila.replace(',', '.')
    P = P.replace(',', '.')

    # Armazenando os dados em um dicionário
    dados_analise = {
        "Ind.SMP": SMP,
        "K": K,
        "Bases(%V)": base,
        "Argila": argila,
        "P": P
    }

    # Convertendo o dicionário para JSON
    dados_json = json.dumps(dados_analise, indent=4, ensure_ascii=False)

    # Exibindo o JSON
    print("=============Resultado da Análise (JSON):============")
    print(dados_json)

if __name__ == "__main__":
    # Configuração do parser de argumentos
    parser = argparse.ArgumentParser(description="Extrair dados de análise de solo a partir de um arquivo PDF.")
    parser.add_argument("pdf_path", help="Caminho para o arquivo PDF")

    # Parse do argumento
    args = parser.parse_args()

    # Chama a função principal passando o caminho do PDF
    main(args.pdf_path)
