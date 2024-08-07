import socket
import signal
import sys
import threading



message_list=[]                         #mesajları tutacak listemiz.
condition=threading.Condition()         #cv kullanacağız...


# Mesajları listeye ekleyen iş parçacığı
def message_receiver(sock):
    while True:
        try:
            connection, address = sock.accept()
            buf = connection.recv(1024)
            if buf:
                print(f"Received: {buf}")
                with threading.Lock():  # Listeye erişim sırasında eşzamanlılık sağlamak için
                    message_list.append(buf)
            connection.send(buf)
            connection.close()
        except socket.timeout:
            continue
        except OSError:
            break

# Mesajları işleyen iş parçacığı
def message_processor():
    while True:
        with threading.Lock():  # Listeye erişim sırasında eşzamanlılık sağlamak için
            if message_list:
                message = message_list.pop(0)
                # Burada mesaj üzerinde işlem yapabilirsiniz
                print(f"Processing: {message}")



# Sunucuyu düzgün kapatmak için bir sinyal işleyicisi 
def signal_handler(sig, frame):
    print('Sunucu kapatılıyor...')
    sock.close()

signal.signal(signal.SIGINT, signal_handler)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('127.0.0.1', 12345))
sock.listen(5)
sock.settimeout(1)  # Accept çağrısına zaman aşımı eklendi

print("Sunucu çalışıyor... (Ctrl+C ile kapatabilirsiniz)")

while True:
    try:
        connection, address = sock.accept()
        buf = connection.recv(1024)
        print(f"Received: {buf}")
        message_list.append(buf)        #mesaj listeye eklendi.
        connection.send(buf)
        connection.close()
    except socket.timeout:
        continue                        #Zaman aşımında döngüye devam edin
    except OSError:
        break

print("Sunucu kapandı.")

#print(message_list)                     liste atıyor mu diye deneme

sys.exit(0)

