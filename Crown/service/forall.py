import re

# -----------------------------------------------------------------------------------------------------------
def prstd ( message , back = False ):
    with open ( '/root/Crown/static/HackLogs.txt', 'w' if back else 'a' ) as f: f.write ( message + '\n' )
# -----------------------------------------------------------------------------------------------------------

proxy_domain  =   '.crown.proxy.ka'

filter_point  =   '(http)s*:\/\/([a-z_A-Z_0-9\-\.]+)[^a-z_A-Z_0-9]*'

array_methods = [ 'GET' ]
# ----------------------------------------------------------

class HostList:
    def __init__    ( self  , lista , auto ) :
        self.content        = lista
        self.automatic      = auto

  # --------------------------------------

    def auto_add_host ( self , http_host ) :

        if not http_host in self.content :

            if    self.automatic :
                  self.content += [ http_host ]

                  prstd ( 'auto_add_host executed for host: {} => added.'.format ( http_host ) )
            else: prstd ( 'auto_add_host can\'t be added for host: {}.  '.format ( http_host ) )
        else :    prstd ( 'auto_add_host is present for host: {}.       '.format ( http_host ) )

        da_ritorno = True if http_host in self.content else False
        prstd ( 'auto_add_host for host: {} results: {}.'.format ( http_host , str ( da_ritorno ) ) )

        return da_ritorno

# ----------------------------------------------------------

def regxMatch ( stringa ) :
    if  ( not   stringa ) : return ''

    da_ritorno   = []    
    for    match in re.findall ( filter_point , stringa ):

           match = match [ 1 ] # only match for one group, match [ x ] is not necessary
        
           da_ritorno += [ match ]
    return da_ritorno

# ----------------------------------------------------------
