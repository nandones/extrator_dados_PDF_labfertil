# Projeto de Extração de Dados de Laudos Labfertil com Flask e PyMuPDF

  - Este projeto foi desenvolvido como microsserviço de um trabalho da disciplina de **Inteligência Artificial** para extrair dados específicos (``Ind. SMP``,``CTC (pH 7,0)``,``K``,``Bases(V%)``,``Argila``,``P``) de laudos de análise de solo emitidos pelo **Labfertil**. Utiliza **Flask** para criar uma API e **PyMuPDF** para manipular PDFs, permitindo que os dados sejam extraídos e retornados ao fazer a requisição por meio de um ``json`` a partir de PDFs enviados via requisição HTTP ``POST``.<br>
  - Há uma cópia de Laudo de Análise de solo presente no repositório apenas para evidenciar com qual arquivo PDF a aplicação trabalha.<br>
  - O leitor de PDFs irá ler e devolver os valores múltiplas linhas, caso haja múltiplas linhas, as dividindo por id, do 1 (primeira linha) até n (enésima linha).
  - Faz um tratamento de dados bastante rigoroso com as exceções encontradas, devolvendo "status" : "failed" e "error" : "a descrição do erro em questão" no json retornado.
  - O programa irá gerar um PDF temporário a partir do PDF recebido pela requisição, que será sobreescrito após nova requisição.
  
## Estrutura do Projeto

1. **Script principal:** `leitor_pdf_labfertil_V5.py` - Script que implementa o servidor Flask e a lógica de extração de dados.
2. **Dependências:** `requirements.txt` - Lista de pacotes Python necessários, incluindo:
   - Flask
   - PyMuPDF (fitz)

3. **Servidor Hospedado:** Uma versão do servidor foi hospedada em `http://nandones.pythonanywhere.com/upload_pdf`, que:
   - Processa PDFs enviados para o sufixo `/upload_pdf` dessa URL.
   - confira se o servidor ainda está online, clique [aqui](http://nandones.pythonanywhere.com) e esteja atento ao status do erro:
   - Caso online, você poderá testá-la via cURL no **CMD**:
```shell
curl -X POST -F "file=@C:/caminho/para/seu/arquivo/Exemplo de Laudo - Análise de Solo.pdf" http://nandones.pythonanywhere.com/upload_pdf
```

## Configuração e Execução Local

### Requisitos

1. **Instale as dependências listadas em `requirements.txt`:**

   ```bash
   pip install -r requirements.txt
   ```
## Configuração do Servidor Flask
Para permitir que outros dispositivos acessem o servidor na rede:
1. No código, substitua:
    ```python
    app.run(debug=True)
    ```
   por:
    ```python
    app.run(host='0.0.0.0', port=5000, debug=True)
    ```
2. Verifique se o firewall permite conexões na porta 5000.

## Execução da Aplicação
1. Execute o script a partir do terminal no diretório do arquivo:
    ```shell
    python leitor_pdf_labfertil_V4.py
    ```
   ou rode a aplicação por uma IDE.
   
## Enviar um PDF para Processamento
Para enviar o PDF para a aplicação via cURL no **CMD**:
```shell
curl -X POST -F "file=@C:/caminho/para/seu/arquivo/Exemplo de Laudo - Análise de Solo.pdf" http://127.0.0.1:5000/upload_pdf
```
# Estrutura de Retorno
A resposta será um ``JSON`` com os valores extraídos. Em caso de falha, o campo ``"status"`` será ``"failed"`` e os campos não identificados terão valor ``null``.

Exemplo de JSON de resposta numa operação de sucesso onde há 1 conjuntos de valores:
```json
{
    "status": "success",
    "data": [
        {
            "id": 1,
            "bases": 82.42,
            "SMP": 6.21,
            "CTC_ph7": 19.52,
            "argila": 35.0,
            "P": 9.6,
            "K": 117.0
        }
    ]
}
```

Exemplo de JSON de resposta numa operação de sucesso onde há 3 conjuntos de valores:
```json
{
    "status": "success",
    "data": [
        {
            "id": 1,
            "bases": 82.42,
            "SMP": 6.21,
            "CTC_ph7": 19.52,
            "argila": 35.0,
            "P": 9.6,
            "K": 117.0
        },
        {
            "id": 2,
            "bases": 83.28,
            "SMP": 6.16,
            "CTC_ph7": 21.73,
            "argila": 37.0,
            "P": 15.6,
            "K": 151.0
        },
        {
            "id": 3,
            "bases": 86.77,
            "SMP": 6.34,
            "CTC_ph7": 22.28,
            "argila": 40.0,
            "P": 11.5,
            "K": 153.0
        }
    ]
}
```

Exemplo de JSON de resposta numa operação de sucesso onde há 8 conjuntos de valores:
```json
{
    "status": "success",
    "data": [
        {
            "id": 1,
            "bases": 12.42,
            "SMP": 16.31,
            "CTC_ph7": 19.52,
            "argila": 135.0,
            "P": 19.6,
            "K": 117.0
        },
        {
            "id": 2,
            "bases": 23.28,
            "SMP": 26.16,
            "CTC_ph7": 21.73,
            "argila": 237.0,
            "P": 215.6,
            "K": 251.0
        },
        {
            "id": 3,
            "bases": 36.77,
            "SMP": 36.34,
            "CTC_ph7": 322.28,
            "argila": 340.0,
            "P": 311.5,
            "K": 353.0
        },
        {
            "id": 4,
            "bases": 40.44,
            "SMP": 4.78,
            "CTC_ph7": 4.777,
            "argila": 450.0,
            "P": 4.44,
            "K": 400.3
        },
        {
            "id": 5,
            "bases": 50.55,
            "SMP": 5.78,
            "CTC_ph7": 5.0,
            "argila": 500.0,
            "P": 560.0,
            "K": 543.8
        },
        {
            "id": 6,
            "bases": 60.66,
            "SMP": 66.0,
            "CTC_ph7": 6.78,
            "argila": 677.0,
            "P": 691.3,
            "K": 670.0
        },
        {
            "id": 7,
            "bases": 7.77,
            "SMP": 77.0,
            "CTC_ph7": 777.0,
            "argila": 777.0,
            "P": 750.0,
            "K": 78.0
        },
        {
            "id": 8,
            "bases": 88.89,
            "SMP": 88.45,
            "CTC_ph7": 890.19,
            "argila": 8.88,
            "P": 8.19,
            "K": 890.0
        }
    ]
}
```
Exemplo de JSON de resposta com erro onde não há nenhum conjunto de valores:
```json
{"status": "failed", "error": "Nenhum valor capturado"}
```
Exemplo de JSON de resposta com erro onde há inconsistência com a quantidade de valores (ex: 7 dados em "K" e 6 em "P"):
```json
{"status": "failed", "error": "Os arrays t\u00eam tamanhos diferentes"}
```
Exemplo de JSON de resposta com erro onde há inconsistência com os caracteres (valores com letras ou mais de uma vírgula):
```json
{
  "error": "presen\u00e7a de valor n\u00e3o num\u00e9rico",
  "status": "failed"
}
```

---
Obrigado por se interessar pelo projeto!
