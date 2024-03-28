from colorsys import rgb_to_hsv, hsv_to_rgb
from scapy.all import *
import string
from collections import Counter
import sys
from scapy.layers.inet import IP

def obtener_primer_caracter(pcap_file):
    cifrado = ""

    # Construye la ruta completa al archivo pcapng
    archivo_pcapng = "./" + pcap_file
    
    # Lee el archivo pcapng
    paquetes = rdpcap(archivo_pcapng)

    # Recorre todos los paquetes y obtiene el primer carácter de cada uno
    for paquete in paquetes:
        if Raw in paquete and IP in paquete:
            if paquete[IP].src == "127.0.0.1":
                cifrado += chr(paquete[Raw].load[0])

    return cifrado

pcap_file = sys.argv[1]
cifrado = obtener_primer_caracter(pcap_file)
print("Mensaje:", cifrado)

# Frecuencia aproximada de letras en español
frecuencia_letras = {
    'a': 0.125,'b': 0.014,'c': 0.046,'d': 0.055,
    'e': 0.136,'f': 0.010,'g': 0.018,'h': 0.007,
    'i': 0.062,'j': 0.004,'k': 0.001,'l': 0.040,
    'm': 0.028,'n': 0.070,'o': 0.086,'p': 0.024,
    'q': 0.010,'r': 0.067,'s': 0.079,'t': 0.047,
    'u': 0.037,'v': 0.011,'w': 0.001,'x': 0.002,
    'y': 0.010,'z': 0.004
}
def rgb_to_ansi(r, g, b):
    r = int(r * 5)
    g = int(g * 5)
    b = int(b * 5)
    return 16 + 36 * r + 6 * g + b

def green_color():
    return rgb_to_ansi(*hsv_to_rgb(1/3, 1, 1))

# Algoritmo receptor (descifrado Cesar)
def cesar_descifrar(cifrado, desplazamiento):
    texto_plano = ""
    for char in cifrado:
        if char.isalpha():
            offset_ascii = ord('a') if char.islower() else ord('A')
            char_descifrado = chr((ord(char) - offset_ascii - desplazamiento) % 26 + offset_ascii)
            texto_plano += char_descifrado
        else:
            texto_plano += char
    return texto_plano

def asignar_probabilidades(texto):
    probabilidades = {}
    for letra in texto:
        if letra.isalpha():
            letra = letra.lower()
            probabilidades[letra] = frecuencia_letras.get(letra, 0)
    return probabilidades

def fuerza_bruta(cifrado):
    for desplazamiento in range(26):
        texto_descifrado = cesar_descifrar(cifrado, desplazamiento)
        probabilidades = asignar_probabilidades(texto_descifrado)
        probabilidad_total = sum(probabilidades.values())
        # Umbral de probabilidad para considerar el texto en español
        umbral = 0.8
        if probabilidad_total > umbral:
            green_code = green_color()
            print(f"Desplazamiento {desplazamiento}: \033[38;5;{green_code}m{texto_descifrado}\033[0m")
        else:
            print(f"Desplazamiento {desplazamiento}: {texto_descifrado}")

fuerza_bruta(cifrado)
