from scapy.all import *
import sys
import time

def enviar_paquetes_icmp(ip_destino, texto_cifrado):
    # Initialize sequence number
    seq_num = 0
    
    for char in texto_cifrado:

        # Timestamp
        timestamp = int(time.time())
        timestamp_bytes = struct.pack('<Q', timestamp)  # Convertir el timestamp a bytes en Little Endian
        timestamp_hex = ''.join([f'\\x{byte:02x}' for byte in timestamp_bytes])  # Formatear los bytes como '\xHH'
        # Construir el paquete ICMP
        paquete_icmp = IP(dst=ip_destino, ttl=64) / ICMP(type=8, code=0, id = os.getpid() & 0xFFFF, seq=seq_num) / bytes(timestamp_bytes)
        
        # seq number incremental por cada paquete que se envie
        seq_num += 1
        paquete_icmp.seq = seq_num

        # Payload con char cifrado
        paquete_icmp /= bytes(char, 'utf-8')
        paquete_icmp /= b'\x00' * 5
        paquete_icmp /= Raw(load=bytes.fromhex("101112131415161718191a1b1c1d1e1f202122232425262728292a2b2c2d2e2f3031323334353637"))
        # Enviar el paquete ICMP
        send(paquete_icmp)
        # Mantiene ejecucion de 1 segundo
        time.sleep(1)
 
ip_destino = "127.0.0.1"
texto_cifrado = input("")

enviar_paquetes_icmp(ip_destino, texto_cifrado)