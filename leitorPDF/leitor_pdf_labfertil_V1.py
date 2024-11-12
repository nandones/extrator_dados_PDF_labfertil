# é necessário instalar o PyMuPDF antes, execute no CMD:
# pip install PyMuPDF
#
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
#                             +
# não aprecio esta vesão pela key ser o nome da variável enviada, como "P", que como key é " P ".


import fitz  # PyMuPDF
import json  # Biblioteca para manipulação de JSON

# Carrega o PDF
pdf_document = fitz.open(".\Exemplo de Laudo - Análise de Solo.pdf")
page = pdf_document[0]  # Primeira página

# Define as palavras-chave para busca
keywords = ["SMP", "K ", "Bases", "Argila", " P ", "CTC (pH 7,0)"]
extracted_values = {}

# Itera sobre as palavras-chave e extrai os valores
for keyword in keywords:
    # Localiza o texto da palavra-chave na página
    text_instances = page.search_for(keyword)
    if text_instances:
        # Pega o primeiro resultado encontrado
        rect = text_instances[0]
        
        # Define uma área logo abaixo da palavra-chave para capturar o valor
        below_rect = fitz.Rect(rect.x0-5, rect.y1, rect.x1+5, rect.y1 + 11)
        
        # Extrai o texto da área abaixo
        value = page.get_text("text", clip=below_rect).strip()
        extracted_values[keyword] = value

# Exibe os valores extraídos
for key, value in extracted_values.items():
    print(f"{key}: {value}")

# Fecha o documento
pdf_document.close()

# Converte o dicionário para JSON
dados_json = json.dumps(extracted_values, indent=4, ensure_ascii=False)

# Exibe o JSON
print("============= Resultado da Análise (JSON): =============")
print(dados_json)
