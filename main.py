from PIL import Image
import numpy as np
import os
import platform
from colorama import Fore, Style


def verify_skin(skin: Image) -> bool:
    if skin.size != (64, 64):
        return False

    m = simplify_matrix(matrix(skin))

    pixels = np.array(m)

    sects = [
        pixels[0:8, 8:24],
        pixels[9:16, 0:32],
        pixels[16:20, 20:28],
        pixels[16:20, 44:50],
        pixels[20:32, 0:54],
        pixels[48:52, 36:42],
        pixels[52:64, 16:46],
    ]

    for sect in sects:
        if np.all(sect != 1):
            return False

    return True


def simplify_matrix(matrix: list) -> list:
    new_matrix = []

    for y in range(len(matrix)):
        new_row = []
        for x in range(len(matrix[0])):
            color = matrix[y][x]

            if color == (0, 0, 0, 0):
                new_row.append(0)
            else:
                new_row.append(1)
        new_matrix.append(new_row)

    return new_matrix


def matrix(img: Image) -> list:
    width, height = img.size

    pixels = []

    for y in range(height):
        row = []
        for x in range(width):
            r, g, b, a = img.getpixel((x, y))
            row.append((r, g, b, a))
        pixels.append(row)

    return pixels


def clear():
    if platform.system() == "Windows":
        os.system("cls")
    elif platform.system() == "Linux" or platform.system() == "Darwin":
        os.system("clear")


if __name__ == "__main__":
    clear()
    try:
        skin = Image.open(f"{input('Enter the skin path: ')}").convert("RGBA")
    except:
        print(f"{Fore.RED}This image could not be found.{Style.RESET_ALL}")
        exit()

    if verify_skin(skin):
        print(
            f"{Fore.GREEN}This skin is valid or meets the minimum requirements.{Style.RESET_ALL}"
        )
    else:
        print(
            f"{Fore.RED}This skin is invalid or does not meet the minimum requirements.{Style.RESET_ALL}"
        )
