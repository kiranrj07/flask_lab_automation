import paramiko
import csv
import time
from scp import SCPClient

def CreatePod(hostname,uname,passwd,commands,allscripts="EMPTY"):
    final_output=[]
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname, username=uname, password=passwd)
        print("Connected to %s" % hostname)
    except paramiko.AuthenticationException:
        print("Failed to connect to % s due to wrong username / password" % hostname)
        final_output.append("<br/>Failed to connect to % s due to wrong username / password<br/>" % hostname)
        return final_output
    except:
        print("Failed to connect to % s" % hostname)
        final_output.append("<br/>Failed to connect to % s<br/>" % hostname)
        return final_output

    mcommands = commands.split("#")
    try:
        for cmd in mcommands:
            print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% <br/>"
                  "  Executing the command: {} <br/>"
                  "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%".format(cmd))
            final_output.append("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% <br/>"
                  "  Executing the command: {} <br/>"
                  "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%".format(cmd))
            stdin, stdout, stderr = ssh.exec_command(cmd)

            err = ''.join(stderr.readlines())
            out = ''.join(stdout.readlines())
            final_output.append(str(out) + str(err))

            print(err, out, final_output)

    except Exception as e:
            print(e.message)

    scripts = allscripts.split('#')
    if scripts != "EMPTY":
        try:
            for script in scripts:
                print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% <br/>"
                      "  Executing the command: {} <br/>"
                      "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%".format(script))
                final_output.append("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% <br/>"
                      "  Executing the command: {} <br/>"
                      "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%".format(script))
                with SCPClient(ssh.get_transport()) as scp:
                    scp.put('{}.ps1'.format(script), '/')
               # client.disconnect()
                print("File deployed")
                final_output.append("File deployed<br/>")

                stdin, stdout, stderr = ssh.exec_command("cd /")
                err = ''.join(stderr.readlines())
                out = ''.join(stdout.readlines())
                final_output.append(str(out) + str(err))
                print(err, out, final_output)
                print("Comamnd line:", "powershell invoke-command -command { C:/%s.ps1 }"%(script))
                final_output.append("<br/>Comamnd line:", "powershell invoke-command -command { C:/%s.ps1 }"%(script))
                print("Moved to / directory")
                final_output.append("<br/>Moved to / directory")
                time.sleep(5)

                stdin, stdout, stderr = ssh.exec_command("powershell invoke-command -command { C:/%s.ps1 }"%(script))
                err = ''.join(stderr.readlines())
                out = ''.join(stdout.readlines())
                final_output.append(str(out) + str(err))
                print(err, out, final_output)
                final_output.append("<br/>Script executed successfully")
                print("Script executed successfully")
        except:
            print("Exception occured @ script block")
            final_output.append("<br/>Exception occured @ script block<br/>")

    # if allscripts == "EMPTY":
    #     return final_output.append('endofprogramcompletion')

    print("I am the last line of the execution")
    yield final_output

def csv_file(filename):
    data_buffer=[]
    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 1
        for row in csv_reader:
            data_buffer.append(row[0]+" "+row[1]+" "+row[2]+" "+row[3]+""+row[4])
            data_buffer.append("<br/> <br/><br/>Start of {} Task".format(line_count))
            data_buffer.append("<br/><br/>################################################### <br/> ")
            try:
                #print("I am printing ++++++++++++++++++ createPod outupr in list:",CreatePod(row[0],row[1],row[2],row[3],row[4]))
                data_buffer.append(CreatePod(row[0],row[1],row[2],row[3],row[4]))
                line_count += 1
            except:
                data_buffer.append("<br/><br/>End of task no {} executed Unsuccessfully".format(line_count))
                data_buffer.append("<br/><br/>################################################### <br/><br/>")
                data_buffer.append("<br/><br/>Task no {} executed Unsuccessfully <br/>".format(line_count))
                line_count += 1
            # else:
            #     data_buffer.append("End of task no {} executed successfully".format(line_count))
            #     data_buffer.append("################################################### <br/><br/>")
            #     data_buffer.append("Task no {} executed successfully <br/>".format(line_count))
            #     line_count += 1

        data_buffer.append("endofprogramcompletion")
    return data_buffer
