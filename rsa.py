import tkinter as tk
import random

#generar numeros primos aleatorios

def generarPrimo(bits):
    while True:
        primo = random.getrandbits(bits)
        if validarPrimo(primo):
            return primo
        
# verificar numero primo
def validarPrimo(n, k=5):
    for _ in range(k):
        a = random.randint(2, n - 2)
        if pow(a, n - 1, n) != 1:
            return False

    return True

# calcular mcd
def mcd(e, phi):
    while phi:
        e, phi = phi, e % phi
    return e

# calcular inverso modular
def inversoModular(e, phi):
    originalValue, tempValueOne, tempValueTwo = phi, 0, 1
    while e > 1:
        q = e // phi
        phi, e = e % phi, phi
        tempValueOne, tempValueTwo = tempValueTwo - q * tempValueOne, tempValueOne
    return tempValueTwo + originalValue if tempValueTwo < 0 else tempValueTwo

# generar claves
def generaClaves(bits):
    p = generarPrimo(bits)
    q = generarPrimo(bits)
    n = p * q
    phi = (p - 1) * (q - 1)
    e = random.randint(2, phi - 1)
    while mcd(e, phi) != 1:
        e = random.randint(2, phi - 1)
    d = inversoModular(e, phi)
    publicKey = (n, e)
    privateKey = (n, d)
    return publicKey, privateKey

# cifrar un mensaje
def cifrar(mensaje, publicKey):
    n, e = publicKey
    mensajeCifrado = [pow(ord(char), e, n) for char in mensaje];
    print("mensaje cifrado:",mensajeCifrado)
    return mensajeCifrado

# descifrar un mensaje
def descifrar(mensajeCifrado, privateKey):
    n, d = privateKey
    mensajeDescifrado = [chr(pow(char, d, n)) for char in mensajeCifrado]
    print("mensaje descifrado:",''.join(mensajeDescifrado))
    return ''.join(mensajeDescifrado)



#configuracion inicial
ventana = tk.Tk()
ventana.title("ALGORITMO RSA")
bits = 1024
publicKey, privateKey = generaClaves(bits)
print("clave publica")
print(publicKey)
print("clave privada")
print(privateKey)

# interfaz grafica
label_mensaje = tk.Label(ventana, text="Mensaje:")
label_mensaje.pack()
entrada_mensaje = tk.Entry(ventana)
entrada_mensaje.pack()

#cifrar
def cifrar_mensaje():
    mensaje = entrada_mensaje.get()
    mensaje_cifrado = cifrar(mensaje, publicKey)
    resultado_cifrado.config(text="Mensaje Cifrado: " + ' '.join(map(str, mensaje_cifrado)))
    
boton_cifrar = tk.Button(ventana, text="Cifrar", command=cifrar_mensaje)
boton_cifrar.pack()

resultado_cifrado = tk.Label(ventana, text="")
resultado_cifrado.pack()

#descifrar
def descifrar_mensaje():
    mensaje_cifrado = resultado_cifrado.cget("text").split(": ")[1].split()
    mensaje_descifrado = descifrar([int(x) for x in mensaje_cifrado], privateKey)
    resultado_descifrado.config(text="Mensaje Descifrado: " + mensaje_descifrado)

boton_descifrar = tk.Button(ventana, text="Descifrar", command=descifrar_mensaje)
boton_descifrar.pack()

resultado_descifrado = tk.Label(ventana, text="")
resultado_descifrado.pack()

ventana.mainloop()