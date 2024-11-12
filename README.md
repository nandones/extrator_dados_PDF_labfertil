# Projeto de Extração de Dados de Laudos Labfertil com Flask e PyMuPDF

  - Este projeto foi desenvolvido como microsserviço de um trabalho da disciplina de **Inteligência Artificial** para extrair dados específicos (``Ind. SMP``,``CTC (pH 7,0)``,``K``,``Bases(V%)``,``Argila``,``P``) de laudos de análise de solo emitidos pelo **Labfertil**. Utiliza **Flask** para criar uma API e **PyMuPDF** para manipular PDFs, permitindo que os dados sejam extraídos e retornados ao fazer a requisição por meio de um ``json`` a partir de PDFs enviados via requisição HTTP ``POST``.<br>
  - Há uma cópia de Laudo de Análise de solo presente no repositório apenas para evidenciar com qual arquivo PDF a aplicação trabalha.<br>
  - Caso haja mais de um valor para um campo, como no exemplo deste repositório, o programa irá trabalhar com os valores da primeira linha, ignorando os demais.
  - O programa irá gerar um PDF temporário a partir do PDF recebido pela requisição, que será sobreescrito após nova requisição.
  

## Estrutura do Projeto

1. **Script principal:** `leitor_pdf_labfertil_V4.py` - Script que implementa o servidor Flask e a lógica de extração de dados.
2. **Dependências:** `requirements.txt` - Lista de pacotes Python necessários, incluindo:
   - Flask
   - PyMuPDF (fitz)

3. **Servidor Hospedado:** Uma versão do servidor foi hospedada em `http://nandones.pythonanywhere.com/upload_pdf`, que:
   - Aceita apenas requisições **POST**.
   - Processa PDFs enviados para o sufixo `/upload_pdf` dessa URL.
   - confira se o servidor ainda está online, clique [aqui](http://nandones.pythonanywhere.com/upload_pdf) e esteja atento ao status do erro:
   - ````405 Method Not Allowed````: Tentativa de usar método ``GET`` onde aceita-se apenas método ``POST``, porém, significa que a URL foi encontrada e o servidor está no ar.
   - ````404 Not Found````: Significa que a URL não foi encontrada e o servidor está fora do ar.
   - Caso online, você poderá testá-la via cURL no **CMD**:
```shell
curl -X POST -F "file=@C:/caminho/para/seu/arquivo/Exemplo de Laudo - Análise de Solo.pdf" http://nandones.pythonanywhere.com/upload_pdf
```

## Configuração e Execução

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

Exemplo de JSON de resposta numa operação de sucesso:
```json
{
    "status": "success",
    "bases": 1.23,
    "SMP": 5.67,
    "CTC_ph7": 7.89,
    "argila": 3.21,
    "P": 4.56,
    "K": 6.78
}
```

Exemplo de JSON de resposta numa operação onde há falha:
```json
{
    "status": "failed",
    "bases": 1.23,
    "SMP": 5.67,
    "CTC_ph7": null,
    "argila": 3.21,
    "P": 4.56,
    "K": 6.78
}
```
---
Obrigado por se interessar pelo projeto!
