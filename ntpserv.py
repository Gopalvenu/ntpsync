import sys
import commands
import smtplib
import socket
import subprocess
import ntpsettings

def ntpchk(result,ip_addr):
    
    if int(result[0].replace('\n','')) == 0:
        print "success"
    else:
	sendingmail(ip_addr)

def sendingmail(ip_addr):
 
    try:
        smtpObj = smtplib.SMTP(ntpsettings.server, ntpsettings.port)
        smtpObj.starttls()
        smtpObj.sendmail(ntpsettings.fromaddr ,ntpsettings.to ,ntpsettings.msg%(ip_addr))
    except Exception, e:
            print "Unable to send email. Error: %s" % str(e)

if __name__ == '__main__':
    
    for ip_addr in ntpsettings.ip_list:
        try:
            for cmd in ntpsettings.cmd_list:
	        ssh = subprocess.Popen(["ssh", "%s"%ip_addr, '%s'%cmd],shell=False,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            result = ssh.stdout.readlines()
            if result == []:
    	        error = ssh.stderr.readlines()
                print >>sys.stderr, "ERROR: %s" % error
        except:
	    print "ntpd stop or server down"    
        ntpchk(result,ip_addr)

