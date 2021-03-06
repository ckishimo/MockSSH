
import sys
import MockSSH
import settings
from twisted.python import log

#
# File based on examples/mock_cisco.py
#

def do_dir(instance):
    tmp = '-'.join(instance.args)
    name = configs + "/" + tmp + '.log'
    print("File name to open: %s" % name)
    with open(name) as f:
        for out in f:
            out = out.rstrip('\r\n')  # CK: Remove call_commandrriage return
            instance.writeln(out)

def do_dir_error(instance):
    instance.writeln("Unknown command")

command_dir = MockSSH.ArgumentValidatingCommand('dir', [do_dir], [do_dir_error])

#
# command show
#
def do_show(instance):
	# Instance
	# <class 'MockSSH.ArgumentValidatingCommand'>
    print('debug function do_show')
    print('sshuser: %s' % settings.sshuser)

    # FIXME: show chassis alarms does not give the same output when ran multiple times
    # FIXME: Find > in the output it will stop the output
    # FIXME: Remove the prompt returned from the telent output to the ssh output

    if settings.sshuser == 'mx':
        cmd = ' '.join(instance.args)
        command = "%s | no-more\r" % cmd
        print('* command to send over telnet: %s' % command)
        settings.telnet_id.write(command)
        out = settings.telnet_id.read_until('>', 5)
        
       	instance.writeln(out)
    elif settings.sshuser == "netiron":
        print('* netiron')
    	# Use netiron directory for outputs
    elif settings.sshuser == "fastiron":
        print('* fastiron')
    	# Use fastiron directory for outputs
    else:
    	print(instance.args)
    	tmp = '-'.join(instance.args)
    	aa = tmp.replace("/", "-")
    	name = configs + "/" + aa + '.log'
    	print("File name to open: %s" % name)
    	with open(name) as f:
        	for out in f:
	            out = out.rstrip('\r\n')
            	instance.writeln(out)

command_show = MockSSH.ArgumentValidatingCommand('show', [do_show], *["vlan", "arp", "mac-address", 
    "module", "version","ip bgp summary","ip bgp neighbors", "ipv6 neighbors", "lldp neighbors", 
    "lldp neighbors detail", "lldp neighbors detail ports eth 3/1", 
    "ip interface", "running begin ntp", "ip bgp summary", "ip bgp neighbors"])

commands = [ command_show, command_dir ]

port = 9999
server = '127.0.0.1'
users = {'mx': 'x', 'local' : 'x', 'testadmin': 'x'}
# Define location of all mocked outputs
outputs = 'netiron/'
tn = ''
print(type(MockSSH)) 		# module
print(type(command_show))	# <class 'MockSSH.ArgumentValidatingCommand'>

#print(super(command_show))
#print(type(p))
print("* SSH server running on %s port %d" % (server,port))
print("* Use user: local, password: x")

# ckishimo: less verbose
log.startLogging(sys.stderr)
settings.init()
MockSSH.runServer(commands, prompt="hostname#", interface='127.0.0.1', port=9999, **users)
