from forall import prstd , array_methods , HostList , proxy_domain
from flask  import Flask , request , send_from_directory , g

import random , threading , time ,  requests , urllib3 , json , socket , ssl , os , certifi , select

# -----------------------------------------------
urllib3.disable_warnings ()
# -----------------------------------------------

http_proxy = 8080
https_port = 8443

HostLista = HostList ( [ ] , True )

# EXAMPLE for KEEP-ALL : HostLista = HostList ( [ ]                  , True  )
# EXAMPLE for ROUTING  : HostLista = HostList ( [ 'www.google.com' ] , False )

# --------------------------------------------------------

pub_root_pem = '/root/Samael/static/root.samael.pem' ;

priv_crt = '/root/Crown/cert/crown.crt' ;
priv_key = '/root/Crown/cert/crown.key' ;

# --------------------------------------------------------

def SSLsocks ( ) :
    global http_proxy , HostLista

    host_name = '0.0.0.0'
    limit_clients = 20
    var_timeout = 1

    # ----------------------------------------------------------------------------------------
    # ----------------------------------------------------------------------------------------

    prstd ( 'set socket ssl\'s port: '  + str ( http_proxy    ) )
    prstd ( 'set socket ssl\'s host: '  + str ( host_name     ) )
    prstd ( 'set socket ssl\'s limit: ' + str ( limit_clients ) )
    prstd ( '' )

    context = ssl.SSLContext ( ssl.PROTOCOL_TLS_SERVER )
    context.load_cert_chain  ( priv_crt   ,   priv_key )

    context.load_verify_locations ( certifi.where () )
    prstd ( 'set socket ssl\'s CA and Certifications' )

    prstd ( '' )
    prstd ( 'show available ciphers: ' + str ( context.get_ciphers () ) )

    # https://stackoverflow.com/questions/49774366/how-to-set-ciphers-in-ssl-python-socket#49776964
    cipher = 'ECDHE-ECDSA-AES256-GCM-SHA384'
    context.set_ciphers ( cipher )
    prstd ( 'set socket ssl\'s CIPHERS ' ) # + str ( context.get_ciphers () ) )
    # How to see list of curl ciphers -> curl https://www.howsmyssl.com/a/check

    # SOCK_STREAM means that it is a TCP socket . SOCK_DGRAM means that it is a UDP socket .
    TCP_sock = socket.socket ( type=socket.SOCK_STREAM )
    prstd ( 'init socket ssl\'s STREAM' )

    TCP_sock.setsockopt ( socket.SOL_SOCKET , socket.SO_REUSEADDR , 1 )
    TCP_sock.bind ( ( host_name , http_proxy ) )

    prstd ( 'made socket ssl binding with host: ' + str ( host_name  ) )
    prstd ( 'made socket ssl binding with port: ' + str ( http_proxy ) )

    TCP_sock.listen ( limit_clients ) # number that the system will allow before refusing new connections

    prstd ( 'limited socket ssl for max X clients where X is: ' + str ( limit_clients ) )
    prstd ( '' )

    caPython = certifi.where ()
    caSSL = '/etc/ssl/certs/ca-certificates.crt'
    customca = None
    
    prstd ( 'show python certifi location: ' + str ( certifi.where () ) )
    prstd ( 'show ssl default CA paths: ' + str ( ssl.get_default_verify_paths () ) )
    prstd ( 'show short ssl default CA paths: ' + caSSL )

    # ----------------------------------------------------------------------------------------
    # ----------------------------------------------------------------------------------------

    hashCrown = 'hcNdisOut8W6nNckb9GMpkkk9/qfqncV1sqh308Cpd/JG4y436PGBaRpP48OD3YE'

    with open ( caPython , 'r' ) as infile :

         Python_hashCrown_count = infile.read ().count ( hashCrown )
         prstd ( 'certifi count the hash of Crown: ' + str ( Python_hashCrown_count ) )

         if Python_hashCrown_count == 0 :

            prstd ( 'Adding custom certs to Python\'s Certifi store' )
            with open ( pub_root_pem , 'rb' ) as infile : customca = infile.read ()

            with open ( caPython , 'ab' ) as outfile: outfile.write ( customca )

            prstd ( 'That might have worked for Python!' )
            
    # https://incognitjoe.github.io/adding-certs-to-requests.html

    with open ( caSSL , 'r' ) as infile :

         SSL_hashCrown_count = infile.read ().count ( hashCrown )
         prstd ( 'SSL ca-certificates count the hash of Crown: ' + str ( SSL_hashCrown_count ) )

         if SSL_hashCrown_count == 0 :

            prstd ( 'Adding custom certs to SSL\'s Certifi store' )
            with open ( pub_root_pem , 'rb' ) as infile : customca = infile.read ()

            with open ( caSSL , 'ab' ) as outfile: outfile.write ( customca )

            prstd ( 'That might have worked for caSSL!' )

    # ----------------------------------------------------------------------------------------
    # ----------------------------------------------------------------------------------------

    # Python ssl server reporting TLSV1_ALERT_UNKNOWN_CA
    # The TLv1 unknown CA alert is sent by some clients if,
    # they cannot verify the certificate of the server because it is signed by an unknown issuer CA.

    while True :

      prstd ( '' )
      socket_wrap , addr , data , internet_adress = None , None , None , None
      socket_internet , step , problems , socket_list = None , None , False , []

      # https://github.com/inaz2/proxy2/blob/master/proxy2.py

      # ----------------------------------------------------------------------------------------A

      step = 0
      try:
             # Return Value: An object of type ssl.SSLSocket
             TCP_sock = context.wrap_socket ( TCP_sock , server_side=True )
             prstd ( 'made socket ssl wrap -> get new TCP_sock for https' )
             step += 1

             socket_wrap , addr = TCP_sock.accept ()
             step += 1
             data  = socket_wrap.recv ( 2048 ).decode () # from bytes to string
             step += 1

             prstd ( 'socket wrap receive data: {}'.format ( data [ :-3 ] ) )
             step += 1

             bool_one = data.count ( 'GET http://' ) and data.count ( 'HTTP' )
             bool_two = data.count ( 'CONNECT'     ) and data.count ( 'HTTP' )
             problems = not ( bool_one or bool_two )

             if not problems : addr , step = addr [ 0 ] , step + 1
             if     bool_one :

                prstd ( 'accepted socket without ssl request from: ' + str ( addr ) )

                request = data.replace ( 'GET ' , '' )
                request = request [ : request.index ( ' HTTP' ) ]
                prstd ( 'from addr: ' + addr + ' GET : ' + request )
                step += 1

                response = requests.get ( request , verify = False , allow_redirects = False )
                prstd ( 'received response from requests.' )
                prstd ( 'status of response: ' + str ( response.status_code ) )
                step += 1

                if response.status_code >= 200 and response.status_code < 400:

                      reply = "HTTP/1.1 " + str ( response.status_code ) + " OK"
                      for ( key , value ) in response.headers.items () : reply += '\n' + str ( key ) + ': '  + str ( value )
                      reply += '\n\n'
                      step += 1

                      socket_wrap.sendall ( reply.encode  () )
                      step += 1
                      socket_wrap.sendall ( response.content )
                      step += 1

                      prstd ( 'to addr: ' + addr + ' send headers data: '           + reply [ :-3 ] )
                else: prstd ( 'to addr: ' + addr + ' bugs: response.status_code ! ( >= 200 & < 400' )

             step += 1

             if bool_one or problems : 99 / 0

             prstd ( 'accepted socket ssl request from: ' + str ( addr ) )

      except:
             socket_wrap , addr , data , problems = None , None , None , True
             prstd ( 'Had problems on step A: ' + str ( step ) )

      # ----------------------------------------------------------------------------------------B

      step = 0
      if not problems :
         try :
                 internet_adress = data [ : data.index ( ' HTTP' ) ].replace ( 'CONNECT ' , '' )
                 prstd ( 'from addr: ' + addr + ' internet_adress: ' + internet_adress         )
                 step += 1

                 problems = not data.count ( ':' )
                 if not problems: step += 1
                 else:              99  / 0

                 host = str ( internet_adress [ : internet_adress.index ( ':' )       ] )
                 port = int ( internet_adress [   internet_adress.index ( ':' ) + 1 : ] )
                 prstd ( 'from addr: ' + addr + ' collect host , port: ' +  str ( [ host , port ] ) )
                 step += 1

                 # host = 'http' + ( 's' if port == 443 else '' ) + '://' + host
                 # Not use with SOCKETs

                 problems = not HostLista.auto_add_host ( host )

                 if not problems: step += 1
                 else:              99  / 0

                 socket_internet = socket.create_connection         ( ( host , port ) , timeout=var_timeout )
                 prstd ( 'from server create connection to: ' + str ( [ host , port ] ) )
                 step += 1

                 reply = 'HTTP/1.1 200 Connection established\n\n'
                 socket_wrap.send ( reply.encode () ) # from string to bytes
                 prstd ( 'to addr: ' + addr + ' send data: ' + str ( reply [ :-2 ] ) )
                 step += 1
         except :
                 internet_adress , data , socket_internet , problems = None , None , None , True
                 prstd ( 'Had problems on step B: ' + str ( step ) )

      # ----------------------------------------------------------------------------------------C

      step = 0
      if    not problems : socket_list = [ socket_wrap , socket_internet ]
      while not problems :
                readable_list , writable_list , errors = select.select ( socket_list , [] , socket_list , var_timeout )
                step += 1

                if errors or not readable_list : break
                for r     in     readable_list :

                    other = socket_internet if r is socket_wrap else socket_wrap
                    prstd ( 'set other to: ' + 'socket internet' if r is socket_wrap else 'socket wrap    ' )
                    prstd ( 'found readable == ' + 'socket wrap' if r is socket_wrap else 'socket internet' )
                    step += 1

                    data = None

                    try:
                        data  = r.recv ( 50 * 1024 )
                    except:
                        data = None

                    step += 1

                    if not data :
                           problems = True
                           prstd   ( 'had problems inside While function, reading data: ' + str ( problems ) )
                           break

                    else : other.sendall ( data )

      prstd ( 'Had problems to execute While function, for reading data on step C: ' + str ( step ) )
      if socket_wrap : socket_wrap.close ()
      prstd ( 'socket wrap was closed   ' )

# --------------------------------------------------------
# --------------------------------------------------------
# --------------------------------------------------------

app = Flask ( __name__ , static_folder = None )

prstd ( '' , True )

@app.route ( '/' , methods=array_methods )
def root   (     ):
    newHost   =   request.host
    while  newHost.count ( ':' + str ( https_port ) ) > 0: newHost = newHost.replace ( ':' + str ( https_port ) , '' )

    if     newHost == 'main.crown.proxy.ka' : return  send_from_directory ( 'static' , 'Crown.jpg'    )
    elif   newHost == 'logs.crown.proxy.ka' : return  send_from_directory ( 'static' , 'HackLogs.txt' )
    elif   newHost == 'deep.crown.proxy.ka' : return '<br>'.join          (     HostLista.content     )

    else : return 'route root switched to default.'

# --------------------------------------------------------

@app.before_request
def callme_before_every_request ():
    g.id = str ( random.randint ( 0 , 9 ) )
    for i in range ( 8 ): g.id += str ( random.randint ( 0 , 9 ) )
    request_detail = """


    ******************************************
    Before Request id: {g_id}
    Before URL:        {url}
    Before Methods:    {methods}
    Before Headers:    {headers} """

    newHost   =   request.host

    while  newHost.count ( ':' + str ( https_port ) ) > 0: newHost = newHost.replace ( ':' + str ( https_port ) , '' )
    if not newHost == 'logs.crown.proxy.ka' :

           prstd ( request_detail.format ( g_id = g.id , url = request.url , methods = request.method , headers = str ( request.headers ) [:-4] ) )

@app.after_request
def callme_after_every_response ( response ) :
    request_response = """
    ******************************************
    After request id:  {g_id}
    Response:          {response} """

    newHost   =   request.host

    while  newHost.count ( ':' + str ( https_port ) ) > 0: newHost = newHost.replace ( ':' + str ( https_port ) , '' )
    if not newHost == 'logs.crown.proxy.ka' :

           prstd ( request_response.format ( g_id = g.id , response = str ( response ) ) )
    return                 response

# --------------------------------------------------------

def runHttps (): app.run ( host="0.0.0.0" , debug=False , port=https_port , ssl_context = ( priv_crt , priv_key ) )
if  __name__ == "__main__":

    x = threading.Thread ( target = runHttps )
    y = threading.Thread ( target = SSLsocks )

    print ( "before running runHttps and SSLsocks" )

    x.start    (     )
    time.sleep ( 0.5 )
    y.start    (     )
