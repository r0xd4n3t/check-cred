# Introduction:

This is a Python script that provides various functions to check if the provided credentials are valid for specific services, such as MySQL, MSSQL, SSH, and SMB.

## Functions and their purposes

Here is a brief overview of the functions and their purposes:

-   `check_host(host, port)`: This function checks if a host is reachable and a specific port is open or not.
-   `mysql_cred_check(host, user, password)`: This function checks if the provided MySQL credentials are valid for the specified host.
-   `mssql_cred_check(host, user, password, database)`: This function checks if the provided MSSQL credentials are valid for the specified host and database.
-   `ssh_cred_check(host, port, user, password, sudo)`: This function checks if the provided SSH credentials are valid for the specified host and port. It can also check for sudo access.
-   `smb_cred_check(host, user, password)`: This function checks if the provided SMB credentials are valid for the specified host.

The `menu()` function provides a simple user interface to choose which function to run and input the required parameters. It also calls the `check_host()` function to ensure that the host and port are available before running any of the credential check functions.

## Prerequisites:

Prerequisites for running this code include having Python 3 installed on your machine, as well as any necessary packages that are not included in the standard library (there are none in this case). You may also need to have appropriate access to the services being checked and their respective ports.
