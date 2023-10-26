import sys

# Rotar a la derecha la entrada x en n bits
def ROR(x, n, bits=32):
    mask = (1 << n) - 1
    return ((x >> n) | (x << (bits - n))) & ((1 << bits) - 1)

# Rotar a la izquierda la entrada x en n bits
def ROL(x, n, bits=32):
    return ((x << n) | (x >> (bits - n))) & ((1 << bits) - 1)

# Convertir la oración de entrada en bloques binarios
def blockConverter(sentence):
    encoded = []
    res = ""
    for i in range(len(sentence)):
        temp = bin(ord(sentence[i]))[2:]
        if len(temp) < 8:
            temp = "0" * (8 - len(temp)) + temp
        res = res + temp
        if len(res) == 32:
            encoded.append(int(res, 2))
            res = ""
    return encoded

# Convertir bloques de enteros largos en una cadena
def deBlocker(blocks):
    s = ""
    for ele in blocks:
        temp = bin(ele)[2:]
        if len(temp) < 32:
            temp = "0" * (32 - len(temp)) + temp
        for i in range(0, 4):
            s = s + chr(int(temp[i * 8:(i + 1) * 8], 2))
    return s

# Generar la clave s[0... 2r+3] a partir de la cadena de usuario
def generateKey(userkey):
    r = 12
    w = 32
    b = len(userkey)
    modulo = 2 ** 32
    s = (2 * r + 4) * [0]
    s[0] = 0xB7E15163
    for i in range(1, 2 * r + 4):
        s[i] = (s[i - 1] + 0x9E3779B9) % (2 ** w)
    encoded = blockConverter(userkey)
    enlength = len(encoded)
    l = enlength * [0]
    for i in range(1, enlength + 1):
        l[enlength - i] = encoded[i - 1]
    v = 3 * max(enlength, 2 * r + 4)
    A = B = i = j = 0
    for index in range(v):
        A = s[i] = ROL((s[i] + A + B) % modulo, 3, 32)
        B = l[j] = ROL((l[j] + A + B) % modulo, (A + B) % 32, 32)
        i = (i + 1) % (2 * r + 4)
        j = (j + 1) % enlength
    return s

# Cifrar una oración con la clave s
def encrypt(sentence, s):
    encoded = blockConverter(sentence)
    A, B, C, D = encoded
    r = 12
    w = 32
    modulo = 2 ** 32
    lgw = 5
    B = (B + s[0]) % modulo
    D = (D + s[1]) % modulo
    for i in range(1, r + 1):
        t_temp = (B * (2 * B + 1)) % modulo
        t = ROL(t_temp, lgw, 32)
        u_temp = (D * (2 * D + 1)) % modulo
        u = ROL(u_temp, lgw, 32)
        tmod = t % 32
        umod = u % 32
        A = (ROL(A ^ t, umod, 32) + s[2 * i]) % modulo
        C = (ROL(C ^ u, tmod, 32) + s[2 * i + 1]) % modulo
        A, B, C, D = B, C, D, A
    A = (A + s[2 * r + 2]) % modulo
    C = (C + s[2 * r + 3]) % modulo
    return [A, B, C, D]

# Descifrar una oración cifrada con la clave s
def decrypt(encoded_sentence, s):
    A, B, C, D = encoded_sentence
    r = 12
    w = 32
    modulo = 2 ** 32
    lgw = 5
    C = (C - s[2 * r + 3]) % modulo
    A = (A - s[2 * r + 2]) % modulo
    for j in range(1, r + 1):
        i = r + 1 - j
        A, B, C, D = D, A, B, C
        u_temp = (D * (2 * D + 1)) % modulo
        u = ROL(u_temp, lgw, 32)
        t_temp = (B * (2 * B + 1)) % modulo
        t = ROL(t_temp, lgw, 32)
        tmod = t % 32
        umod = u % 32
        C = (ROR((C - s[2 * i + 1]) % modulo, tmod, 32) ^ u)
        A = (ROR((A - s[2 * i]) % modulo, umod, 32) ^ t)
    D = (D - s[1]) % modulo
    B = (B - s[0]) % modulo
    return [A, B, C, D]

# Función principal para ejecutar el programa
# Función principal para ejecutar el programa
# Función principal para ejecutar el programa
# Función principal para ejecutar el programa
def main():
    print("Algoritmo RC6 - Cifrado y Descifrado")
    
    encoded_sentence = None  # Variable para almacenar la oración cifrada

    while True:
        option = input("Selecciona una opción:\n1. Cifrar\n2. Descifrar\n3. Salir\n")

        if option == '1':
            key = input("Ingresa la clave (16 caracteres): ")
            sentence = input("Ingresa la oración a cifrar: ")

            key = key + " " * (16 - len(key))
            key = key[:16]
            sentence = sentence + " " * (16 - len(sentence))
            sentence = sentence[:16]

            s = generateKey(key)
            encoded_sentence = encrypt(sentence, s)
            print("Oración cifrada:", encoded_sentence)
        elif option == '2':
            if encoded_sentence is not None:
                # encoded_sentence = 0
                print("Oración descifrada:", encoded_sentence)
                key = input("Ingresa la clave (16 caracteres): ")
                key = key + " " * (16 - len(key))
                key = key[:16]
                s = generateKey(key)
                # encoded_sentence = input("Ingresa la oración a cifrada: ")
                decoded_sentence = decrypt(encoded_sentence, s)
                print("Oración descifrada:", deBlocker(decoded_sentence))
            else:
                print("Primero cifra una oración antes de descifrar.")
        elif option == '3':
            print("¡Hasta luego!")
            break
        else:
            print("Opción no válida.")

if __name__ == "__main__":
    main()

