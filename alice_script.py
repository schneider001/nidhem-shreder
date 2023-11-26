import socket
import random
from aes_encrypt_decrypt import encrypt_aes, decrypt_aes

Alice_Trent_AES_key = b'0123456789abcdef0123456789abcdef'

Alice_id = 'Alice123'
Bob_id = 'Bob321'
Alice_random_num = random.randint(1, 100000)
print(f'Hi, I am Alice! My id is {Alice_id}, Bob id is {Bob_id}, My random num is {Alice_random_num}')

HOST = 'localhost'
PORT_ALICE_TRENT = 12345
PORT_ALICE_BOB = 12346

alice_socket_trent = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
alice_socket_trent.connect((HOST, PORT_ALICE_TRENT))

message_to_trent = f'{Alice_id}<{Bob_id}<{Alice_random_num}'.encode('utf-8')
alice_socket_trent.sendall(message_to_trent)

encrypted_message_from_trent = alice_socket_trent.recv(1024).decode('utf-8')
Alice_random_num, Bob_id, secret_key, encrypted_secret_key_and_Alice_id = decrypt_aes(Alice_Trent_AES_key, encrypted_message_from_trent)
print(f'The message from Trent: Alice_random_num={Alice_random_num} Bob_id={Bob_id} secret_key={secret_key} encrypted_secret_key_and_Alice_id={encrypted_secret_key_and_Alice_id}')

alice_socket_trent.close()

alice_socket_bob = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
alice_socket_bob.connect((HOST, PORT_ALICE_BOB))

message_to_bob = encrypted_secret_key_and_Alice_id.encode('utf-8')
alice_socket_bob.sendall(message_to_bob)

message_from_bob = alice_socket_bob.recv(1024).decode('utf-8')
Bob_random_num = decrypt_aes(secret_key.encode('utf-8'), message_from_bob)[0]
print(f'The message from Bob: Bob_random_num={Bob_random_num}')

message_to_bob = encrypt_aes(secret_key.encode('utf-8'), str(int(Bob_random_num)-1)).encode('utf-8')
alice_socket_bob.sendall(message_to_bob)

alice_socket_bob.close()
