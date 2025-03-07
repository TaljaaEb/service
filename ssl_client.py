import socket, ssl, sys, os
import hashlib

clients = []
verified = None

sys.argv.append('172.29.n.n') #8900
sys.argv.append('127.0.0.1')

#HOST, PORT = 'localhost', 8900
AUTH, APORT = str(sys.argv[1]), 443
HOST, PORT, CERT, KEY = str(sys.argv[2]), 443, 'certificate.pem', 'private.key'

def auth():
    print('in auth-1')
    sock = socket.socket(socket.AF_INET)
    #context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
##    context = ssl.SSLContext()
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    context.minimum_version = ssl.TLSVersion.TLSv1_3
    context.maximum_version = ssl.TLSVersion.TLSv1_3
    #context.verify_mode = ssl.CERT_REQUIRED
    context.check_hostname = False

    context.load_verify_locations('C:\\Users\\TaljaaEb\\Desktop\\B1COB2\\k_cabundle.pem')

    # Wrap the socket with SSL/TLS (using TLSv1.3)
    conn = context.wrap_socket(
        sock,
        server_side=False,
        do_handshake_on_connect=True,
        suppress_ragged_eofs=True,
        server_hostname='127.0.0.1',
        session=None
    )




    try:
        conn.connect((AUTH, APORT))
        handle(conn, clients)
        code = conn.recv(4)
    finally:
        print(code)
        if code == 'CTRU':
            print(code)
            conn.close()
        else:
            conn.close()

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    IP = s.getsockname()[0]
    s.close()
    return IP

def get_username():
#    USER = os.getlogin()
    USER = 'user1-taljaaeb'
    return USER

def hashing(ctext):
    obj = hashlib.sha256()
    obj.update(bytes(ctext, 'utf-8'))
    return obj.hexdigest()
   
def handle(conn, clients):
    verify = False
    if len(clients) == 0:
        #conn.write(b'GET / HTTP/1.1\n')
        #conn.write(b'%s' % conn.getpeername()[0].encode())
        BSTRING = LOCAL_IP + LOCAL_USER
        BSTRING_ENC = hashing(BSTRING)
        print(BSTRING_ENC)
        ######conn.write(b'%s' % BSTRING_ENC.encode())
        conn.write(b'%s' % BSTRING_ENC.encode())
        print(BSTRING_ENC)
        clients.append(BSTRING_ENC)
        ASTRING = conn.recv().decode()
        ASTRING_ENC = hashing(ASTRING)
        print(ASTRING_ENC)
        clients.append(ASTRING_ENC)
        #print(conn.recv().decode())
    else:
        conn.write(b'%s' % clients[0].encode())
        conn.write(b'%s' % clients[1].encode())
        clients = []
        verify = True
        print(verify)

def main(args=None):
    sock = socket.socket(socket.AF_INET)
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    context.minimum_version = ssl.TLSVersion.TLSv1_3
    context.maximum_version = ssl.TLSVersion.TLSv1_3
    #context.verify_mode = ssl.CERT_REQUIRED
    context.check_hostname = False

    context.load_verify_locations('cabundle.pem')

    # Wrap the socket with SSL/TLS (using TLSv1.3)
    conn = context.wrap_socket(
        sock,
        server_side=False,
        do_handshake_on_connect=True,
        suppress_ragged_eofs=True,
        server_hostname='127.0.0.1',
        session=None
    )


    try:
        conn.connect((HOST, PORT))
        handle(conn, clients)
    finally:
        conn.close()

if __name__ == '__main__':
    REMOTE_IP = str(sys.argv[1])
    LOCAL_IP = get_ip()
    LOCAL_USER = get_username()
    main()
    if len(clients) == 2:
        auth()
