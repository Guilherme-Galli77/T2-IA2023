#Instalar modulos 
#pip install numpy
#pip install opencv-python
#pip install dlib

import cv2
import dlib
import numpy as np
from cv2 import dnn
from tkinter import *
from tkinter import filedialog

# Função para detectar a idade em uma imagem
def detectar_idade(imagem):
    # Modelo para detecção de idade
    pesos_idade = "Models/age_deploy.prototxt"
    configuracao_idade = "Models/age_net.caffemodel"
    age_Net = cv2.dnn.readNet(configuracao_idade, pesos_idade)

    # Requisitos do modelo para a imagem
    ageList = ['(0-2)', '(4-6)', '(8-12)', '(15-20)', '(25-32)', '(38-43)', '(48-53)', '(60-100)']
    modelo_media = (78.4263377603, 87.7689143744, 114.895847746)

    # Pré-processamento para detecção de rosto
    detector_faces = dlib.get_frontal_face_detector()
    img_cinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
    faces = detector_faces(img_cinza)

    if not faces:
        print('Nenhum rosto detectado.')
        return None

    frame = imagem.copy()
    for face in faces:
        x = face.left()
        y = face.top()
        x2 = face.right()
        y2 = face.bottom()

        # Redimensionar coordenadas para a imagem
        box = [x, y, x2, y2]
        cv2.rectangle(frame, (x, y), (x2, y2), (0, 200, 200), 2)

        # Extrair o rosto e preparar para a previsão de idade
        face_img = frame[box[1]:box[3], box[0]:box[2]]
        blob = cv2.dnn.blobFromImage(face_img, 1.0, (227, 227), modelo_media, swapRB=False)

        # Previsão de idade
        age_Net.setInput(blob)
        age_preds = age_Net.forward()
        idade = ageList[age_preds[0].argmax()]

        cv2.putText(frame, f'Idade: {idade}', (box[0], box[1] - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2, cv2.LINE_AA)

    return frame

# Função para colorir uma imagem em escala de cinza
def colorir_imagem(caminho_imagem):
    # Caminhos dos modelos
    proto_file = 'Models/colorization_deploy_v2.prototxt'
    model_file = 'Models/colorization_release_v2.caffemodel'
    hull_pts = 'Models/pts_in_hull.npy'

    # Leitura do modelo e pré-processamento da imagem
    net = dnn.readNetFromCaffe(proto_file, model_file)
    kernel = np.load(hull_pts)
    img = cv2.imread(caminho_imagem)
    scaled = img.astype("float32") / 255.0
    lab_img = cv2.cvtColor(scaled, cv2.COLOR_BGR2LAB)

    # Adicionar centros de cluster como convoluções ao modelo
    class8 = net.getLayerId("class8_ab")
    conv8 = net.getLayerId("conv8_313_rh")
    pts = kernel.transpose().reshape(2, 313, 1, 1)
    net.getLayer(class8).blobs = [pts.astype("float32")]
    net.getLayer(conv8).blobs = [np.full([1, 313], 2.606, dtype="float32")]

    # Restante do processo de colorização
    resized = cv2.resize(lab_img, (224, 224))
    L = cv2.split(resized)[0]
    L -= 50

    net.setInput(cv2.dnn.blobFromImage(L))
    ab_channel = net.forward()[0, :, :, :].transpose((1, 2, 0))
    ab_channel = cv2.resize(ab_channel, (img.shape[1], img.shape[0]))

    L = cv2.split(lab_img)[0]
    colorized = np.concatenate((L[:, :, np.newaxis], ab_channel), axis=2)
    colorized = cv2.cvtColor(colorized, cv2.COLOR_LAB2BGR)
    colorized = np.clip(colorized, 0, 1)
    colorized = (255 * colorized).astype("uint8")

    return colorized

# Função principal para selecionar a operação desejada
def main():
    def escolher_opcao(op):
        if op == 1:
            file_path = filedialog.askopenfilename()  # Permite escolher a imagem
            img = cv2.imread(file_path)
            img = cv2.resize(img, (720, 640))
            resultado = detectar_idade(img)

            if resultado is not None:
                cv2.imshow("Detectando Idade", resultado)
                cv2.waitKey(0)

        elif op == 2:
            file_path = filedialog.askopenfilename()  # Permite escolher a imagem
            imagem_colorida = colorir_imagem(file_path)

            # Exibir a imagem colorida
            cv2.imshow("Escala de Cinza -> Colorida", imagem_colorida)
            cv2.waitKey(0)

        else:
            print("Escolha inválida.")

    def design_gui():
        root = Tk()
        root.title("Análise de Imagem")

        label = Label(root, text="Escolha uma opção:", font=("Arial", 14))
        label.pack()

        button1 = Button(root, text="Detecção de Idade", command=lambda: escolher_opcao(1),
                         font=("Arial", 12), bg="#4CAF50", fg="white")
        button1.pack(pady=10)

        button2 = Button(root, text="Colorir Imagem", command=lambda: escolher_opcao(2),
                         font=("Arial", 12), bg="#008CBA", fg="white")
        button2.pack(pady=10)

        root.geometry("300x200")
        root.configure(bg="#f0f0f0")  # Cor de fundo da janela

        root.mainloop()

    design_gui()

if __name__ == "__main__":
    main()