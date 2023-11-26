import socket
import random
from aes_encrypt_decrypt import encrypt_aes, decrypt_aes

Bob_Trent_AES_key = b'qazwoiu789aasdef0123456kjhabokmn'

Alice_id = 'Alice123'
Bob_id = 'Bob321'
Bob_random_num = random.randint(1, 100000)
print(f'Hi, I am Bob! My id is {Bob_id}, Alice id is {Alice_id}, My random num is {Bob_random_num}')

HOST = 'localhost'
PORT_ALICE_BOB = 12346

bob_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
bob_socket.bind((HOST, PORT_ALICE_BOB))
bob_socket.listen()

print('Waiting a message from Alice...')
alice_socket_bob, addr = bob_socket.accept()
message_from_alice = alice_socket_bob.recv(1024).decode('utf-8')
secret_key, Alice_id = decrypt_aes(Bob_Trent_AES_key, message_from_alice)
print(f'The message from Alice: secret_key={secret_key}, Alice_id={Alice_id}')

message_to_alice = encrypt_aes(secret_key.encode('utf-8'), Bob_random_num).encode('utf-8')
alice_socket_bob.sendall(message_to_alice)

message_from_alice = alice_socket_bob.recv(1024).decode('utf-8')
Bob_random_num_minus_one = decrypt_aes(secret_key.encode('utf-8'), message_from_alice)[0]
print(f'The message from Alice: Bob_random_num_minus_one={Bob_random_num_minus_one}')

alice_socket_bob.close()
bob_socket.close()
