#!/bin/bash

if (( ${#@} > 0 )) ;
then
     if (( ${#@} > 1 )) && [[ $1 == 's' ]] && [[ $2 == 'trace' ]] ;
     then
          curl -x https://crown.proxy.ka:8080/  --trace-ascii  /dump.txt  https://duckduckgo.com/ ;

     elif [[ $1 == 's' ]] ;
     then
          curl -x https://crown.proxy.ka:8080/  "https://duckduckgo.com/?q=past&t=ffab&ia=web" ;

     elif [[ $1 == 'trace' ]] ;
     then
          curl -x http://crown.proxy.ka:8080/  --trace-ascii  ./dump.txt  https://duckduckgo.com/ ;
     fi
else
     curl -x http://crown.proxy.ka:8080/  https://duckduckgo.com/ ;
fi

# https://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html
