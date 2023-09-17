import socket
import ssl
import os
import binascii
import falcon
import pickle
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential

#########################################################
#Set system parameters:
# os.environ['KEY_VAULT_NAME'] = 'cryptography-project'
# keyVaultName = os.environ["KEY_VAULT_NAME"]
keyVaultName = "cryptography-project"
KVUri = f"https://{keyVaultName}.vault.azure.net"
credential = DefaultAzureCredential()
secrets = SecretClient(vault_url=KVUri, credential=credential)

#Load SecretKey
str_client_f = secrets.get_secret("f-client").value
f = list(map(int, str_client_f.split(", ")))

str_client_g = secrets.get_secret("g-client").value
g = list(map(int, str_client_g.split(", ")))

str_client_F = secrets.get_secret("fF-client").value
F = list(map(int, str_client_F.split(", ")))

str_client_G = secrets.get_secret("gG-client").value
G = list(map(int, str_client_G.split(", ")))

polys = [f, g, F, G] 
sk = falcon.SecretKey(128,polys)
# create pk
pk = falcon.PublicKey(sk)

#########################################################

#merchant -> client:
M = b'' #Khai báo biến message
print("Step 3: Waiting for bill information from merchant....")
# init socket and create connection
context_merchant_client = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context_merchant_client.load_cert_chain('./server.crt', './server.key')
with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as sock:
        sock.bind(("127.0.0.1", 8448))
        sock.listen(5)
        print ('Client is listening...')
        with context_merchant_client.wrap_socket(sock, server_side=True) as ssock:
            conn, addr = ssock.accept()
            with conn:
                print('Connected by', addr)
                # sen pk
                pk_bytes = pickle.dumps(pk)
                conn.sendall(pk_bytes)
                
                # recv pk
                key_buffer_size = 4096
                merchant_pk_bytes = b''
                while True:
                    c_pk_bytes = conn.recv(key_buffer_size)
                    merchant_pk_bytes += c_pk_bytes
                    if len(c_pk_bytes) < key_buffer_size:
                        break
                merchant_pk = pickle.loads(merchant_pk_bytes)
                #print("Merchant public key:",merchant_pk)

                # recv mess + sig
                buffer_size = 4096
                data = b''
                while True:
                    dt = conn.recv(buffer_size)
                    data += dt
                    if len(dt) < buffer_size:
                        break
                received_data = data.split(b'0x3')
                response = b''
                rtn = False
                if len(received_data) == 2:
                    received_msg = received_data[0]
                    received_sig = received_data[1]
                    #print(received_msg.decode())
                    
                    # verify mess + sig
                    rtn = merchant_pk.verify(received_msg, received_sig)
                    print ("\nSignature verification: ", rtn)
                    
                    if rtn:
                        response = sk.sign(b'Success')
                        M = received_msg
                    else:
                        response = sk.sign(b'Failure')
                conn.sendall(response)
                
            
            

# client -> server:
#########################################################
#Message (Xử lý M vừa nhận được kết hợp với id_client để gửi đi cho server)
M = M.decode()
Client_ID = input("Input Client ID: ")
M = M + '0x2' + Client_ID
M = M.encode()
print("Step 4: Send request voucher to server....")
#init socket and create connection with SSL/TLS
context_client_server = ssl.create_default_context()
context_client_server.check_hostname = False
context_client_server.load_verify_locations('./server.crt')
with socket.create_connection(("127.0.0.1",8440)) as sock:
    with context_client_server.wrap_socket(sock, server_hostname="127.0.0.1") as ssock:
        ## receive public key from server
        key_buffer_size = 4096
        server_pk_bytes = b''
        while True:
            s_pk_bytes = ssock.recv(key_buffer_size)
            server_pk_bytes += s_pk_bytes
            if len(s_pk_bytes) < key_buffer_size:
                break
        server_pk = pickle.loads(server_pk_bytes)
        #print("Server public key:", server_pk)

        # send public key to server
        pk_bytes = pickle.dumps(pk)
        ssock.sendall(pk_bytes)
        
        # sig and send
        sig = sk.sign(M)
        data = M + b'0x3' + sig
        ssock.sendall(data)
        
        # receive response from server
        buffer_size = 4096
        data = b''
        while True:
            dt = ssock.recv(buffer_size)
            data += dt
            if len(dt) < buffer_size:
                break
        #print(data)
        rtn = server_pk.verify(b'Success', data)
        if rtn:
            print("\nSignature verification: Success")
        else:
            print("\nSignature verification: Failure")
        
#########################################################
#server -> client: 
print("Step 5: Waiting for respone voucher from server....")
# init socket and create connection
context_server_client = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context_server_client.load_cert_chain('./server.crt', './server.key')

# accept connection and communicate

with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as sock:
        sock.bind(("127.0.0.1", 8443))
        sock.listen(5)
        print ('Client is listening...')
        with context_server_client.wrap_socket(sock, server_side=True) as ssock:
            conn, addr = ssock.accept()
            with conn:
                print('Connected by', addr)
                # send public key to server
                pk_bytes = pickle.dumps(pk)
                conn.sendall(pk_bytes)
                
                # receive public key from server
                key_buffer_size = 4096
                server_pk_bytes = b''
                while True:
                    c_pk_bytes = conn.recv(key_buffer_size)
                    server_pk_bytes += c_pk_bytes
                    if len(c_pk_bytes) < key_buffer_size:
                        break
                server_pk = pickle.loads(server_pk_bytes)
                #print("Server public key:",server_pk)

                # recv mess + sig
                buffer_size = 4096
                data = b''
                while True:
                    dt = conn.recv(buffer_size)
                    data += dt
                    if len(dt) < buffer_size:
                        break
                received_data = data.split(b'0x3')
                response = b''
                if len(received_data) == 2:
                    received_msg = received_data[0]
                    received_sig = received_data[1]
                    #print(received_msg.decode()) 
                    # verify mess + sig
                    rtn = server_pk.verify(received_msg, received_sig)
                    print ("\nSignature verification: ", rtn)
                
                    if rtn:
                        # response
                        response = sk.sign(b'Success')
                        M = received_msg
                    else:
                        response = sk.sign(b'Failure')
                conn.sendall(response)

#client -> merchant: 
print("Step 6: Forward voucher to merchant....")
##########################################################
# init socket and create connection with SSL/TLS
context_client_merchant = ssl.create_default_context()
context_client_merchant.check_hostname = False
context_client_merchant.load_verify_locations('./server.crt')

# request connection and communicate
with socket.create_connection(("127.0.0.1",8444)) as sock:
    with context_client_merchant.wrap_socket(sock, server_hostname="127.0.0.1") as ssock:
        # receive public key from merchant
        key_buffer_size = 4096
        merchant_pk_bytes = b''
        while True:
            s_pk_bytes = ssock.recv(key_buffer_size)
            merchant_pk_bytes += s_pk_bytes
            if len(s_pk_bytes) < key_buffer_size:
                break
        merchant_pk = pickle.loads(merchant_pk_bytes)


        # send public key to merchant
        pk_bytes = pickle.dumps(pk)
        ssock.sendall(pk_bytes)
        
        # sig and send message
        sig = sk.sign(M)
        data = M + b'0x3' + sig
        ssock.sendall(data)
        
        # receive response from client
        buffer_size = 4096
        data = b''
        while True:
            dt = ssock.recv(buffer_size)
            data += dt
            if len(dt) < buffer_size:
                break
        #print(data)
        rtn = merchant_pk.verify(b'Success', data)
        if rtn:
            print("\nSignature verification: Success")
        else:
            print("\nSignature verification: Failure")
        # Close connection
        
        ssock.close()

#print("final M: ", M.decode())
