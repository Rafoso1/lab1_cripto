# Algoritmo emisor (cifrado Cesar)

def cesar_cifrar(texto_plano, desplazamiento):
    texto_cifrado = ""
    for char in texto_plano:
        if char.isalpha():
            offset_ascii = ord('a') if char.islower() else ord('A')
            char_cifrado = chr((ord(char) - offset_ascii + desplazamiento) % 26 + offset_ascii)
            texto_cifrado += char_cifrado
        else:
            texto_cifrado += char
    return texto_cifrado

entrada = input()

ultimo_espacio = entrada.rfind(' ')

texto_plano = entrada[:ultimo_espacio]
desplazamiento = int(entrada[ultimo_espacio + 1:])

texto_cifrado = cesar_cifrar(texto_plano, desplazamiento)
print(texto_cifrado)

# 