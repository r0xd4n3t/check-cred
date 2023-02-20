import socket
import subprocess
import getpass
import shlex

def check_host(host, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(5)
            result = sock.connect_ex((host, port))
            if result == 0:
                return True
            else:
                return False
    except Exception as e:
        print(f"An error occurred while checking host: {e}")
        return False

def mysql_cred_check(host, user, password):
    try:
        subprocess.run(f"mysql -h {host} -u {user} -p{password} -e 'select version();'", shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"Credentials are valid for host: {host}")
    except subprocess.CalledProcessError as e:
        print(f"Credentials are invalid for host: {host} with error: {e}")

def mssql_cred_check(host, user, password, database):
    try:
        subprocess.run(f"sqlcmd -S {host} -U {user} -P {password} -d {database} -Q 'SELECT @@VERSION'", shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"Credentials are valid for host: {host}")
    except subprocess.CalledProcessError as e:
        print(f"Credentials are invalid for host: {host} with error: {e}")

def ssh_cred_check(host, port, user, password, sudo):
    try:
        cmd = [
            "ssh",
            "-o", "StrictHostKeyChecking=no",
            f"{user}@{host}",
            "-p", str(port),
        ]
        if sudo:
            cmd.append("sudo echo test")
            result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, input=f"{password}\n".encode())
            print(f"Credentials are valid for host: {host} with sudo access")
        else:
            cmd.append("echo test")
            result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, input=f"{password}\n".encode())
            print(f"Credentials are valid for host: {host}")
    except subprocess.CalledProcessError as e:
        print(f"Credentials are invalid for host: {host} with error code: {e.returncode}")
        print(f"Output: {e.output}")
        subprocess.run(["ssh", "-o", "StrictHostKeyChecking=no", f"{user}@{host}", "-p", str(port), "exit"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, input=f"{password}\n")
        
def smb_cred_check(host, user, password):
    try:
        subprocess.run(f"smbclient \\\\{host}\\admin$ -U {user}%{shlex.quote(password)} -c \"ls\"", shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"Credentials are valid for host: {host}")
    except subprocess.CalledProcessError:
        print(f"Credentials are invalid for host: {host}")

def menu():
    while True:
        try:
            print("\n1. MySQL Credentials Check")
            print("2. MSSQL Credentials Check")
            print("3. SSH Credentials Check")
            print("4. SMB Credentials Check")
            print("5. Exit")
            choice = int(input("Enter your choice: "))
            if choice == 1:
                host = input("Enter host: ")
                user = input("Enter username: ")
                password = input("Enter password: ")
                if check_host(host, 3306): # Check if the host and port are available
                    mysql_cred_check(host, user, password)
                else:
                    print("Unable to connect to host or port is closed")
            elif choice == 2:
                host = input("Enter host: ")
                user = input("Enter username: ")
                password = input("Enter password: ")
                database = input("Enter database name: ")
                if check_host(host, 1433): # Check if the host and port are available
                    mssql_cred_check(host, user, password, database)
                else:
                    print("Unable to connect to host or port is closed")
            elif choice == 3:
                host = input("Enter host: ")
                port = int(input("Enter port: "))
                user = input("Enter username: ")
                password = getpass.getpass() # Obfuscate password input
                sudo = input("Check for Sudo? (y/n)")
                if check_host(host, port): # Check if the host and port are available
                    ssh_cred_check(host, port, user, password, sudo == 'y')
                else:
                    print("Unable to connect to host or port is closed")
            elif choice == 4:
                host = input("Enter host: ")
                user = input("Enter username: ")
                password = getpass.getpass() # Obfuscate password input
                if check_host(host, 445): # Check if the host and port are available
                    smb_cred_check(host, user, password)
                else:
                    print("Unable to connect to host or port is closed")
            elif choice == 5:
                break
            else:
                print("Invalid choice")
        except ValueError:
            print("Invalid input")

if __name__ == '__main__':
    menu()
