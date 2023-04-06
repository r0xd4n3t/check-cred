import socket
import subprocess
import getpass
import shlex


def check_host(host, port):
    """Check if a host and port are available."""
    try:
        socket.create_connection((host, port), timeout=5)
        return True
    except socket.error as e:
        print(f"Unable to connect to {host}:{port}. Error: {e}")
        return False


def mysql_cred_check(host, user, password):
    """Check if MySQL credentials are valid."""
    try:
        subprocess.run(f"mysql -h {host} -u {user} -p{password} -e 'select version();'",
                       shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"Credentials are valid for host: {host}")
    except subprocess.CalledProcessError as e:
        print(f"Credentials are invalid for host: {host} with error: {e}")


def mssql_cred_check(host, user, password, database):
    """Check if MSSQL credentials are valid."""
    try:
        subprocess.run(f"sqlcmd -S {host} -U {user} -P {password} -d {database} -Q 'SELECT @@VERSION'",
                       shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"Credentials are valid for host: {host}")
    except subprocess.CalledProcessError as e:
        print(f"Credentials are invalid for host: {host} with error: {e}")


def ssh_cred_check(host, port, user, password, sudo):
    """Check if SSH credentials are valid and if user has sudo access if specified."""
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
        subprocess.run(["ssh", "-o", "StrictHostKeyChecking=no", f"{user}@{host}", "-p", str(port), "exit"],
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE, input=f"{password}\n")


def smb_cred_check(host, user, password):
    """Check if SMB credentials are valid."""
    try:
        subprocess.run(f"smbclient \\\\{host}\\admin$ -U {user}%{shlex.quote(password)} -c \"ls\"",
                       shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"Credentials are valid for host: {host}")
    except subprocess.CalledProcessError:
        print(f"Credentials are invalid for host: {host}")

        
def menu():
    while True:
        print("\n1. MySQL Credentials Check")
        print("2. MSSQL Credentials Check")
        print("3. SSH Credentials Check")
        print("4. SMB Credentials Check")
        print("5. Exit")

        choice = None
        while choice not in range(1, 6):
            try:
                choice = int(input("Enter your choice: "))
                if choice not in range(1, 6):
                    print("Invalid choice. Please enter a number between 1 and 5.")
            except ValueError:
                print("Invalid input. Please enter a number between 1 and 5.")

        if choice == 1:
            host = input("Enter host: ")
            user = input("Enter username: ")
            password = input("Enter password: ")
            if check_host(host, 3306):  # Check if the host and port are available
                mysql_cred_check(host, user, password)
            else:
                print("Unable to connect to host or port is closed")
        elif choice == 2:
            host = input("Enter host: ")
            user = input("Enter username: ")
            password = input("Enter password: ")
            database = input("Enter database name: ")
            if check_host(host, 1433):  # Check if the host and port are available
                mssql_cred_check(host, user, password, database)
            else:
                print("Unable to connect to host or port is closed")
        elif choice == 3:
            host = input("Enter host: ")
            port = int(input("Enter port: "))
            user = input("Enter username: ")
            password = getpass.getpass()  # Obfuscate password input
            sudo = input("Check for Sudo? (y/n)")
            if check_host(host, port):  # Check if the host and port are available
                ssh_cred_check(host, port, user, password, sudo == 'y')
            else:
                print("Unable to connect to host or port is closed")
        elif choice == 4:
            host = input("Enter host: ")
            user = input("Enter username: ")
            password = getpass.getpass()  # Obfuscate password input
            if check_host(host, 445):  # Check if the host and port are available
                smb_cred_check(host, user, password)
            else:
                print("Unable to connect to host or port is closed")
        elif choice == 5:
            break


if __name__ == '__main__':
    menu()
