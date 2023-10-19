import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from PIL import Image
import cv2



# fonction qui converte le message a un tableau des bits
def convert_to_bit(msg):
    return [bit for char in msg for bit in bin(ord(char))[2:]]

def code_hamming(bits):
    n = len(bits)
    m = next(i for i in range(n + 1) if 2 ** i >= n + i + 1)
    code = [0] * (n + m)
    j = 0

    for i in range(1, len(code) + 1):
        if not (i & (i - 1)):  # if i is a power of 2
            continue
        code[i - 1] = int(bits[j])
        j += 1

    for i in range(1, len(code) + 1):
        if (i & (i - 1)):  # if i is not a power of 2
            continue
        code[i - 1] = sum(int(code[j]) for j in range(i - 1, len(code), 2 * i)) % 2

    return code


def codage_with_image(tab, image_path):
    p = 2
    X = 0
    Y = 0

    # Calculer la taille de la figure en fonction de la longueur du message
    figure_size = 6 + len(tab) * 0.1  # Ajustez ce facteur pour contrôler la taille de l'image

    figure, ax = plt.subplots(figsize=(figure_size, figure_size))

    for i in tab:
        if i == 0:
            color = 'red'
        else:
            color = 'black'

        rectangle = patches.Rectangle((X - p/2, Y - p/2), p, p, fill=False, color=color)
        ax.add_patch(rectangle)
        p += 0.1  # Ajustez la taille des rectangles si nécessaire

    plt.xlim(-figure_size/2, figure_size/2)
    plt.ylim(-figure_size/2, figure_size/2)
    ax.set_aspect(1)

    # Supprimer les marges blanches autour de la figure et les axes x et y
    plt.axis('off')
    plt.subplots_adjust(left=0, right=1, top=1, bottom=0)

    # Enregistrer l'image avec uniquement les rectangles
    plt.savefig('output_with_image.png', bbox_inches='tight', pad_inches=0, transparent=True)
    plt.show()

def codage_without_image(tab):
    p = 2
    X = 0
    Y = 0

    # Calculer la taille de la figure en fonction de la longueur du message
    figure_size = 6 + len(tab) * 0.1  # Ajustez ce facteur pour contrôler la taille de l'image

    figure, ax = plt.subplots(figsize=(figure_size, figure_size))

    # Ajouter un rectangle blanc au début de l'image
    rectangle_blanc = patches.Rectangle((X - p/2, Y - p/2), p, p, fill=False, color='white')
    ax.add_patch(rectangle_blanc)

    for i in tab:
        if i == 0:
            color = 'red'
        else:
            color = 'black'

        rectangle = patches.Rectangle((X - p/2, Y - p/2), p, p, fill=False, color=color)
        ax.add_patch(rectangle)
        p += 0.1  # Ajustez la taille des rectangles si nécessaire

    plt.xlim(-figure_size/2, figure_size/2)
    plt.ylim(-figure_size/2, figure_size/2)
    ax.set_aspect(1)

    # Supprimer les marges blanches autour de la figure et les axes x et y
    plt.axis('off')
    plt.subplots_adjust(left=0, right=1, top=1, bottom=0)

    # Enregistrer l'image avec uniquement les rectangles
    plt.savefig('output_without_image.png', bbox_inches='tight', pad_inches=0, transparent=True)
    plt.show()


from PIL import Image

def decode_image_with_known_distance(image_path, distance):
    # Ouvrir l'image
    img = Image.open(image_path)

    # Charger les pixels de l'image
    pixels = img.load()

    # Initialiser une liste pour stocker les bits extraits
    bits = []

    # Commencer au premier pixel en haut à gauche
    x, y = 0, 0

    while y < img.height:  # Parcourir les lignes de haut en bas
        pixel = pixels[x, y]

        # Si le pixel est rouge (ou une couleur claire), ajouter '1', sinon ajouter '0'
        if sum(pixel) > 128:  # Vous pouvez ajuster ce seuil en fonction de votre image
            bits.append('1')
        else:
            bits.append('0')

        # Avancer en diagonale en fonction de la distance spécifiée
        num_pixels = int(round(distance / (2**0.5)))  # Utilisez la formule de Pythagore
        for _ in range(num_pixels):
            x += 1
            y += 1

            # Si nous avons dépassé la largeur de l'image, passez à la ligne suivante
            if x >= img.width:
                x = 0
                y += 1

    # Convertir la liste de bits en une chaîne de caractères
    bit_string = ''.join(bits)

    return bit_string

def distance_entre_rectangles_diagonale(tab):
    p = 2
    X = 0
    Y = 0
    distance_entre_diagonales = []

    for i in range(len(tab) - 1):
        rectangle1 = np.array([(X - p/2, Y - p/2), (X + p/2, Y + p/2)])
        rectangle2 = np.array([(X + p/2, Y - p/2), (X - p/2, Y + p/2)])
        distance = np.linalg.norm(rectangle2 - rectangle1)  # Calcul de la distance euclidienne
        distance_entre_diagonales.append(distance)

        X += 0.1  # Ajustez la taille des rectangles si nécessaire

    return distance_entre_diagonales


def main():

    while True:
        print("================== Menu ===================")
        print("0. Quitter le programme")
        print("1. Coder une information SANS image")
        print("2. Coder une information AVEC image")
        print("3. decodage")
        print("4")

        choice = input("Votre choix: ")

        if choice == '0':
            break

        elif choice == '1':
            msg = input("Entrez le message: ")
            tab = convert_to_bit(msg)
            print("le message converti en bit:", tab)

            h = code_hamming(tab)
            print("Code Hamming : ", h)

            codage_without_image(h)

        elif choice == '2':
            msg = input("Entrez le message: ")
            tab = convert_to_bit(msg)
            print("le message converti en bit:", tab)

            h = code_hamming(tab)
            print("Code Hamming : ", h)

            image_path = input("Entrez le chemin de l'image (logo.png par défaut): ") or 'logo.png'
            codage_with_image(h, image_path)
        elif choice == '3':
            image_path = input("Entrez le chemin de l'image (output_without_image.png par défaut): ") or 'output_without_image.png'
            distance = 2.8284271247461903  # Distance entre chaque paire de rectangles en pixels
            result = decode_image_with_known_distance(image_path, distance)
            print("Bits extraits de l'image:", result)
        elif choice == '4':
            msg = input("Entrez le message: ")
            tab = convert_to_bit(msg)
            print("le message converti en bit:", tab)

            h = code_hamming(tab)
            print("Code Hamming : ", h)

            distances = distance_entre_rectangles_diagonale(h)
            print("Distances entre chaque paire de rectangles en diagonale (en pixels):", distances)




        else:
            print("Choix non valide. Essayez encore.")

if __name__ == "__main__":
    main()