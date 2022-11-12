from clrprint import clrprint
from intimations import telegram, push
import subprocess
import argparse

hostIP,externalIP='',''

def _argsFilter(args):
    '''
    Take args  
    '''
    if args.command == 'add':
        addPortForward(args.internalPort, args.externalPort, args.protocol)
    elif args.command == 'remove':
        if '-' in args.externalPorts:
            start_port,end_port = args.externalPorts.split('-')
        else:
            start_port,end_port=args.externalPorts,args.externalPorts
        removePortForward(start_port,end_port, args.protocol)

def errorHandle(data_):     
        data_ = data_.decode()
        clrprint(data_,clr='p')
        if 'failed with code' in data_:
            clrprint('No ports are exposed to external IP {externalIP}.', clr='y')
        elif 'Found a (not connected?) IGD :' in data_:
            clrprint('No valid Gateway found. Are you connected to the internet?\n','\nPlease retry after checking your internet connection. Please ask your ISP provider to enable UPnP service if the issue persists.', clr='r,y')
        else:
            clrprint('Please establish an internet connection, turn on UPnP on your router, and try again.', clr='r')
        exit()

def updateIPs() -> list:
    '''
    Updates current public IP and private IP
    '''
    try:
        global hostIP,externalIP
        data = subprocess.check_output('.\\upnpc.exe -e ajs -l', shell=True, universal_newlines=True, text=True)
        data = data.split('\n')
        for line in data: # get local and public ips
            if 'Local LAN ip address' in line: hostIP=(line.strip().split(' ')[-1])
            elif 'ExternalIPAddress' in line: externalIP=(line.strip().split(' ')[-1])
    except subprocess.CalledProcessError as exc:
        errorHandle(exc.output)
    except Exception as e:
        clrprint('Un expended error: ',e, clr='r')

def addPortForward(internal_port, external_port, protocol='tcp'):
    updateIPs()
    try:
        data = subprocess.check_output(f'.\\upnpc.exe -e ajs -a {hostIP} {internal_port} {external_port} {protocol}').decode()
        data = data.strip().split('\n')[-1]
        clrprint(data, clr='g')
    except Exception as e:
        clrprint('')

def removePortForward(external_port_start, external_port_end, protocol):
    updateIPs()
    try:
        data = subprocess.check_output(f'.\\upnpc.exe -e ajs -N {external_port_start} {external_port_end} {protocol}').decode()
        data = data.strip().split('\n')[-1]
        if 'returned : 0' in data:
            clrprint(f'Ports from {external_port_start} to {external_port_end} are removed from port forwarding.',clr='g')
    except subprocess.CalledProcessError as exc:
        errorHandle(exc.output)

def listTable():
    data = subprocess.check_output(f'.\\upnpc.exe -e ajs -l')
    if '->' in data:
        clrprint('UPNP Port Forward Table: ', clr='y')
        for line in data:
            if '->' in data:
                clrprint(f'  {line}', clr='r')
    else:
        clrprint('UPNP Port Forward Table:', '\n  EMPTY', clr='y,g')


if __name__=='__main__':
    parser = argparse.ArgumentParser(
        prog='upnp_port-Forward', 
        description='''
Description:
    - push/toast notifications with different icons
    - beep sound with different types of sound
    - telegram message (requires your botAPI and ChatID)
  Know more at https://github.com/AbhijithAJ/intimations''',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''\
DEVELOPED BY:
    Abhijith Boppe
    See more at https://bio.link/abhijithboppe
    Support me: https://www.buymeacoffee.com/abhijithboppe
    Thanks for using the module.
         '''
    )

    sub_cmds = parser.add_subparsers(dest='command') #add dest to get sub command when parsing
    
    cmd_add = sub_cmds.add_parser("add", help='add port forward rule in firewall')  # adding sub command 'add'
    cmd_add.add_argument('internalPort', help='Internal port that application is listening on.')
    cmd_add.add_argument('externalPort', help='external port to be exposed to internet.')
    cmd_add.add_argument('protocol', default='tcp', help='tcp/upd protocol.')
   
    cmd_remove = sub_cmds.add_parser("remove", help='remove port forward rule in firewall')  # adding sub command 'remove'
    cmd_remove.add_argument('externalPorts', help='external ports range to be removed. Ex: 8888-9999 or 5555 ')
    cmd_remove.add_argument('protocol', default='tcp', help='tcp/upd protocol.')

    _argsFilter(parser.parse_args())