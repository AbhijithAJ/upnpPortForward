from clrprint import clrprint
from intimations import telegram, push
from sys import platform
import subprocess,argparse

hostIP,externalIP='',''
upnp_cmd = 'upnpc.exe' if platform == 'win32' else 'upnpc'

def errorHandle(data_):     
    data_ = data_.decode() if type(data_) is bytes else data_
    if 'failed with code : 714' in data_: 
        clrprint(f'Specified port is not exposed to Internet.', clr='y')
    elif 'Found a (not connected?) IGD :' in data_: 
        clrprint('No valid Gateway found. Are you connected to the internet?\n','\nPlease retry after checking your internet connection. Please ask your ISP provider to enable UPnP service if the issue persists.', clr='r,y')
    else:
        clrprint('Please establish an internet connection, enable UPnP on your router, and try again.', clr='r')
    exit()

def updateIPs():
    '''
    Updates current public IP and private IP
    '''
    try:
        global hostIP,externalIP
        data = subprocess.check_output(f'{upnp_cmd} -e ajs -l', shell=True, universal_newlines=True, text=True)
        data = data.split('\n')
        for line in data: # get local and public ips
            if 'Local LAN ip address' in line: hostIP=(line.strip().split(' ')[-1])
            elif 'ExternalIPAddress' in line: externalIP=(line.strip().split(' ')[-1])
    except subprocess.CalledProcessError as exc: errorHandle(exc.output)
    except Exception as error: clrprint('Un expended error: ',error, clr='r')

def addPortForward(internal_port, external_port, protocol='tcp'):
    updateIPs()
    try:
        clrprint('Adding UPnP Port forward rule...', clr='p')
        data = subprocess.check_output(f'{upnp_cmd} -e ajs -a {hostIP} {internal_port} {external_port} {protocol}').decode()
        data = data.strip().split('\n')[-1]
        clrprint(data, clr='g')
    except Exception as e: clrprint('')

def removePortForward(external_port,  protocol):
    clrprint('Removing UPnP Port forward rule...', clr='p')
    updateIPs()
    try:
        data = subprocess.check_output(f'{upnp_cmd} -e ajs -d {external_port} {protocol}').decode()
        data = data.strip().split('\n')[-1]
        if 'returned : 0' in data: clrprint(f'Port {external_port} is removed from port forwarding table.',clr='g')
    except subprocess.CalledProcessError as exc:
        errorHandle(exc.output)

def listTable():
    clrprint('Getting Port forward table list.',clr='p')
    data = subprocess.check_output(f'{upnp_cmd} -e ajs -l').decode()
    if '->' in data:
        clrprint('UPNP Port Forward Table: ', clr='y')
        for line in data.split('\n'):
            if '->' in line:clrprint(f'  {line}', clr='r')
    else: clrprint('UPNP Port Forward Table:', '\n  EMPTY', clr='y,g')

def _argsFilter(args):
    '''
    Take args  
    '''
    if args.command == 'add':
        addPortForward(args.internalPort, args.externalPort, args.protocol)
    elif args.command == 'remove':
        removePortForward(args.externalPort, args.protocol)
    elif args.command == 'list':
        listTable()

if __name__=='__main__':
    parser = argparse.ArgumentParser(
        prog='upnpPortForward', 
        description='''
Description:
    - UPnP based portForwarding.
    - Easy to add/remove port Forward rules with a single command.
  Know more at https://github.com/AbhijithAJ/upnpPortForward''',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''\
DEVELOPED BY:
    Abhijith Boppe
    See more at https://bio.link/abhijithboppe
    Support me: https://www.buymeacoffee.com/abhijithboppe
    Thanks for using my code.
         '''
    )
    sub_cmds = parser.add_subparsers(dest='command') #add dest to get sub command when parsing
    
    cmd_add = sub_cmds.add_parser("add", help='add port forward rule.')  # adding sub command 'add'
    cmd_add.add_argument('internalPort', help='Internal port that application is listening on.')
    cmd_add.add_argument('externalPort', help='External port to be exposed to internet.')
    cmd_add.add_argument('protocol', default='tcp', help='Specify tcp or upd protocol.')
   
    cmd_remove = sub_cmds.add_parser("remove", help='Remove port forward rule.')  # adding sub command 'remove'
    cmd_remove.add_argument('externalPort', help='External port to be removed. Ex: 8888')
    cmd_remove.add_argument('protocol', default='tcp', help='Specify tcp or upd protocol.')

    cmd_remove = sub_cmds.add_parser("list", help='List port forward table.')  # adding sub command 'remove'
    _argsFilter(parser.parse_args())