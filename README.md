# Análise de Imagem

Esse projeto utiliza Python e bibliotecas de visão computacional para a detecção de idade em uma imagem e para colorir imagens em escala de cinza. O aplicativo é baseado em uma interface gráfica (GUI) para facilitar o uso.

## Instalação de Dependências

Certifique-se de ter o Python instalado. Você pode instalar as dependências necessárias executando os seguintes comandos no terminal:

```bash
pip install numpy
pip install opencv-python
pip install dlib
```

## Download do Modelo (Apenas para a funcionalidade de colorir imagem):

Você precisará baixar os dados pré-treinados deste local e colocá-los na pasta do modelo:
https://www.dropbox.com/s/dx0qvhhp5hbcx7z/colorization_release_v2.caffemodel?dl=1

## Escolha da Versão a ser Utilizada

Você pode utilizar uma versão GUI que permite buscar por imagens em seu dispositivo e possui uma experiencia mais visual ou também pode utilizar a versão CLI (necessário atribuir o caminho e nome correto as imagens: images1/pessoa.jpg (modelo de reconhecimento de idade) e images2/img1.jpg (modelo de colorir imagens)


# Funcionalidades

## Detecção de Idade

Esta funcionalidade permite identificar a idade das pessoas em uma imagem. Para utilizar:

1. Execute o programa.
2. Selecione a opção 'Detecção de Idade' na interface.
3. Escolha uma imagem na janela de diálogo exibida (apenas GUI).
4. Aguarde a detecção de rostos e visualize os resultados.

## Colorir Imagem

Essa funcionalidade permite adicionar cores a uma imagem em escala de cinza. Para usar:

1. Execute o programa.
2. Selecione a opção 'Colorir Imagem' na interface.
3. Escolha uma imagem em escala de cinza na janela de diálogo exibida (apenas GUI).
4. Aguarde o processo de colorização e visualize a imagem resultante.

## Como Executar

1. Baixe o código ou clone o repositório.
2. Instale as dependências necessárias.
3. Instale o modelo (Apenas para a funcionalidade de colorir imagem).
4. Execute o arquivo Python `main.py`.
5. Use a interface para selecionar a ação desejada e escolher a imagem.

## Observações

Lembre-se: se estiver utilizando a versão da linha de comando (CLI), é necessário ter as imagens a serem processadas nas pastas `images1` e `images2` antes de executar o programa.


