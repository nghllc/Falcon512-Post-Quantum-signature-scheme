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
N = 128
os.environ['KEY_VAULT_NAME'] = 'cryptography-project'
keyVaultName = os.environ["KEY_VAULT_NAME"]
KVUri = f"https://{keyVaultName}.vault.azure.net"
credential = DefaultAzureCredential()
secrets = SecretClient(vault_url=KVUri, credential=credential)

#Load SecretKey
str_merchant_f = secrets.get_secret("f-merchant").value
f = list(map(int, str_merchant_f.split(", ")))

str_merchant_g = secrets.get_secret("g-merchant").value
g = list(map(int, str_merchant_g.split(", ")))

str_merchant_F = secrets.get_secret("fF-merchant").value
F = list(map(int, str_merchant_F.split(", ")))

str_merchant_G = secrets.get_secret("gG-merchant").value
G = list(map(int, str_merchant_G.split(", ")))

polys = [f, g, F, G] 
sk = falcon.SecretKey(128,polys)

# create public key:
pk = falcon.PublicKey(sk)

#########################################################
# Message:
Merchant_ID = input("Input Merchant ID: ")
Order_ID = input("Input Order ID: ")
Amount = input("Input Amount: ")
M = Merchant_ID + '0x2' + Order_ID + '0x2' + Amount
M = M.encode()
print("Step 2: Send bill information to client....")
#########################################################
# init socket and create connection with SSL/TLS
context_merchant_client = ssl.create_default_context()
context_merchant_client.check_hostname = False
context_merchant_client.load_verify_locations('./server.crt')

# request connection and communicate
with socket.create_connection(("172.17.18.61",8448)) as sock:
    with context_merchant_client.wrap_socket(sock, server_hostname="172.17.18.61") as ssock:
        # receive public key from client
        key_buffer_size = 4096
        client_pk_bytes = b''
        while True:
            s_pk_bytes = ssock.recv(key_buffer_size)
            client_pk_bytes += s_pk_bytes
            if len(s_pk_bytes) < key_buffer_size:
                break
        client_pk = pickle.loads(client_pk_bytes)
        #print("Server public key:", server_pk)

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
        rtn = client_pk.verify(b'Success', data)
        if rtn:
            print("\nSignature verification: Success")
        else:
            print("\nSignature verification: Failure")
        # Close connection
        
        ssock.close()

#########################################################
#client -> merchant: 
print("Step 6: Waiting for voucher from server....")
# init socket and create connection
context_client_merchant = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context_client_merchant.load_cert_chain('./server.crt', './server.key')

# accept connection and communicate

with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as sock:
        sock.bind(("0.0.0.0", 8444))
        sock.listen(5)
        print ('Merchant is listening...')
        with context_client_merchant.wrap_socket(sock, server_side=True) as ssock:
            conn, addr = ssock.accept()
            with conn:
                print('Connected by', addr)
                # send public key to client
                pk_bytes = pickle.dumps(pk)
                conn.sendall(pk_bytes)
                
                # receive public key from client
                key_buffer_size = 4096
                client_pk_bytes = b''
                while True:
                    c_pk_bytes = conn.recv(key_buffer_size)
                    client_pk_bytes += c_pk_bytes
                    if len(c_pk_bytes) < key_buffer_size:
                        break
                client_pk = pickle.loads(client_pk_bytes)
                #print("Client public key:",client_pk)

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
                    rtn = client_pk.verify(received_msg, received_sig)
                    print ("\nSignature verification: ", rtn)
                
                    if rtn:
                        # response
                        response = sk.sign(b'Success')
                        M = received_msg
                    else:
                        response = sk.sign(b'Failure')
                conn.sendall(response)

#merchant -> server
#Request money
print("Step 8: Send request money to server....")
#########################################################
# init socket and create connection with SSL/TLS
context_merchant_client = ssl.create_default_context()
context_merchant_client.check_hostname = False
context_merchant_client.load_verify_locations('./server.crt')

# request connection and communicate
with socket.create_connection(("34.143.172.68",9090)) as sock:
    with context_merchant_client.wrap_socket(sock, server_hostname="34.143.172.68") as ssock:
        # receive public key from client
        key_buffer_size = 4096
        client_pk_bytes = b''
        while True:
            s_pk_bytes = ssock.recv(key_buffer_size)
            client_pk_bytes += s_pk_bytes
            if len(s_pk_bytes) < key_buffer_size:
                break
        client_pk = pickle.loads(client_pk_bytes)
        #print("Server public key:", server_pk)

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
        rtn = client_pk.verify(b'Success', data)
        if rtn:
            print("\nSignature verification: Success")
        else:
            print("\nSignature verification: Failure")
        # Close connection
        ssock.close()