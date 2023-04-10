<a id="top"></a>

#

<h1 align="center">
Credentials Checker
</h1>

<p align="center"> 
  <kbd>
<img src="https://raw.githubusercontent.com/r0xd4n3t/check-cred/main/img/pass.png"></img>
  </kbd>
</p>

<p align="center">
<img src="https://img.shields.io/github/last-commit/r0xd4n3t/check-cred?style=flat">
<img src="https://img.shields.io/github/stars/r0xd4n3t/check-cred?color=brightgreen">
<img src="https://img.shields.io/github/forks/r0xd4n3t/check-cred?color=brightgreen">
</p>

📜 Introduction:

This is a Python script that provides various functions to check if the provided credentials are valid for specific services, such as MySQL, MSSQL, SSH, and SMB.

It provides a menu with four options:

-    MySQL Credentials Check
-    MSSQL Credentials Check
-    SSH Credentials Check
-    SMB Credentials Check

## 🕹️ Functions and their purposes

Here is a brief overview of the functions and their purposes:

-   `check_host(host, port)`: This function checks if a given host and port are available by attempting to establish a connection using the `socket.create_connection(`) method. It returns `True` if the connection is successful and `False` otherwise.
-   `mysql_cred_check(host, user, password)`: This function checks if the provided MySQL credentials are valid by running a mysql command. It uses the `run_command()` function to execute the command and returns the result.
-   `mssql_cred_check(host, user, password, database)`: This function checks if the provided MSSQL credentials are valid by running an `sqlcmd` command. It uses the `run_command()` function to execute the command and returns the result.
-   `ssh_cred_check(host, port, user, password, sudo)`: This function checks if the provided SSH credentials are valid and if the user has sudo access if specified. It runs an `ssh` command and then calls the `print_result()` function to display the result.
-   `smb_cred_check(host, user, password`): This function checks if the provided SMB credentials are valid. Depending on the platform (Windows or Linux), it uses either the `net use` or `smbclient` command. It then calls the `run_command()` function to execute the command and returns the result.
-   `run_command(host, command, service_name)`: This function is a helper function that executes a given command using the `subprocess.run()` method. It returns `True` if the command is executed successfully and `False` otherwise.
-   `print_result(host, result, service_name)`: This function displays the result of a credentials check, including whether the check was successful or not, and the output and error messages from the process.
-   `menu()`: This function displays a menu for the user to select which credential check they want to perform (MySQL, MSSQL, SSH, or SMB). It takes user inputs for the required parameters and calls the corresponding function to perform the selected check. The menu loop continues until the user chooses to exit.

These functions work together to provide a comprehensive and user-friendly interface for checking the validity of various types of credentials.

## 📝 Prerequisites

Prerequisites for running this code include having Python 3 installed on your machine, as well as any necessary packages that are not included in the standard library (there are none in this case). You may also need to have appropriate access to the services being checked and their respective ports.

<p align="center"><a href=#top>Back to Top</a></p>
