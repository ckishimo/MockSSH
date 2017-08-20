
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

command_dir = MockSSH.TelnetCommand('dir', [do_dir], [do_dir_error])

#
# command show
#
def do_show(instance):
    print('debug function do_show')
    print('sshuser: %s' % settings.sshuser)

    # FIXME: Find > in the output it will stop the output
    if settings.sshuser == 'mx':
        cmd = ' '.join(instance.args)
        command = "%s | no-more\r" % cmd
        print('* command to send over telnet: %s' % command)
        settings.telnet_id.write(command)
        #out = settings.telnet_id.read_until(">", 5)
        out = settings.telnet_id.read_until(b">",5)
        # Do not display the first empty line
        out1 =  out[out.find('\n'):]
        # Do not display the command again (echo)
        out2 = out1[len(command):]
        # Do not display the prompt from the telnet session
        out3 = out2[:out2.rfind('\n')]
        instance.writeln(out3)

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

command_show = MockSSH.TelnetCommand('show', [do_show], *["vlan", "arp", "mac-address", 
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

print("* SSH server running on %s port %d" % (server,port))
print("* Use user: local, password: x (outputs from disk)")
print("* Use user: ROUTER_NAME, password: x (outputs directly from telnet router)")

settings.init()
MockSSH.runServer(commands, prompt="hostname#", interface='127.0.0.1', port=9999, **users)

