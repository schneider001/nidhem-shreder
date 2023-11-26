import socket
from aes_encrypt_decrypt import encrypt_aes, generate_aes_key

Alice_Trent_AES_key = b'0123456789abcdef0123456789abcdef'
Bob_Trent_AES_key = b'qazwoiu789aasdef0123456kjhabokmn'

print('Hi, I am Trent!')

HOST = 'localhost'
PORT_ALICE_TRENT = 12345

trent_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
trent_socket.bind((HOST, PORT_ALICE_TRENT))
trent_socket.listen()

print('Waiting a message from Alice...')
alice_socket_trent, addr = trent_socket.accept()
message_from_alice = alice_socket_trent.recv(1024).decode('utf-8').split('<')
Alice_id, Bob_id, Alice_random_num = message_from_alice
print(f'The message from Alice: Alice_id={Alice_id} Bob_id={Bob_id}  Alice_random_num={Alice_random_num}')

secret_key = generate_aes_key()
print(f'Generated secret key is {secret_key}')
message_to_alice = encrypt_aes(Alice_Trent_AES_key, Alice_random_num, Bob_id, secret_key, encrypt_aes(Bob_Trent_AES_key, secret_key, Alice_id)).encode('utf-8')
alice_socket_trent.sendall(message_to_alice)

alice_socket_trent.close()
trent_socket.close()
