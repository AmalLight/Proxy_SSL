
# https://letsencrypt.org/docs/certificates-for-localhost/
# https://docs.oracle.com/en/operating-systems/oracle-linux/6/admin/ol_self_cert.html
# https://www.udemy.com/course/ssltls-essentials-theory-and-implementation

if (( ${#@} == 1 )) && [[ $1 == 'install' ]] ;
then
     ssh root@192.168.31.2 -t " echo '' && sudo apt update        && sudo apt upgrade -y && echo '' ;
                                echo '' && sudo apt autoremove -y && sudo apt autoclean  && sudo history -c && echo '' ;
     echo ''
     sudo apt install -y ssh  iptables  ufw    genisoimage dnsutils ;
     sudo apt install -y curl wget nmap python3 python3-pip openssl ;
     echo ''
     echo '' ; pip3 install flask pyopenssl ; "
fi

# ----------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------

echo '' ;

if  [[ -f ./shortSV.conf ]]  ;  then  scp shortSV.conf root@192.168.31.2:/root/Crown/cert/shortSV.conf  ;  fi

# ----------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------

ssh root@192.168.31.2 -t " echo '' ;

   cd     /root/Crown/cert/                ;
   echo  '/root/Crown/cert/ <-- I am Here' ; echo '' ;

   rm -rf  *.key   &&   echo  'removed cert  key  files'  ;
   rm -rf  *.csr   &&   echo  'removed cert  csr  files'  ;
   rm -rf  *.crt   &&   echo  'removed cert  crt  files'  ;

# ----------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------

   echo ''  && for el in \$( ls /root/Samael/cert/ ) ; do echo \" Samael File: /root/Samael/cert/\$el \" ; done && echo '' ;

   cp  /root/Samael/cert/shortCA.conf         shortCA.conf        &&  chmod 755 shortCA.conf       ;
   cp  /root/Samael/cert/index.txt            index.txt           &&  chmod 755 index.txt          ;
   cp  /root/Samael/cert/serial.txt           serial.txt          &&  chmod 755 serial.txt         ;
   cp  /root/Samael/cert/private-ca-key.key   private-ca-key.key  &&  chmod 755 private-ca-key.key ;
   cp  /root/Samael/cert/public-ca-cert.crt   public-ca-cert.crt  &&  chmod 755 public-ca-cert.crt ;

            openssl genrsa -out private-server-key.key 2048 ;
   echo '' ;
            openssl req    -out private-server-csr.csr     -sha256 -new -key private-server-key.key                   -config shortSV.conf                         ;
   yes |    openssl ca     -out public-server-cert.crt  -md sha256       -in private-server-csr.csr -notext -days 365 -config shortCA.conf -extensions server_cert ;
   
# ----------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------

   cp  /root/Crown/cert/public-server-cert.crt  /root/Crown/cert/crown.crt  ;
   cp  /root/Crown/cert/private-server-key.key  /root/Crown/cert/crown.key  ;

   echo ''  && for el in \$( ls              --all ) ; do echo \" File: /root/Crown/cert/\$el   \" ; done && echo '' ;
               for el in \$( ls /root/Crown/static ) ; do echo \" File: /root/Crown/static/\$el \" ; done && echo '' ;

# ----------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------

   echo 'echo                         '' ; '  > /root/check.sh ;
   echo 'sudo iptables -t filter -L -v   ; ' >> /root/check.sh ;
   echo 'sudo iptables -t nat    -L -v   ; ' >> /root/check.sh ;
   echo 'sudo iptables -t mangle -L -v   ; ' >> /root/check.sh ;

   sudo ln -sf /root/check.sh /usr/bin/check && chmod 755 /root/* && check && echo '' ;
"

echo ''
