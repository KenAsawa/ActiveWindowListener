import os
import pathlib
import subprocess
import sys

# Determine whether to use Windows CLI / PowerShell commands or *nix commands
_windows = sys.platform in ['Windows', 'win32', 'cygwin']
# Find location of MongoDB daemon process
_daemon_path = subprocess.check_output(['where' if _windows else 'which', 'mongod']).decode().strip()
# Define location of configuration file within this folder
_config_file = os.path.join(pathlib.Path(__file__).parent.absolute(), 'mongoServer.config')
# Current handle server instance's process
_server = None


def start_server():
    """
    Creates a new process for a local MongoDB server. Does nothing if
    the process exists (the server is already active).
    :return: None
    """

    global _server

    # Check if the 'db' directory exists. If not, make it, so MongoDB starts properly.
    db_path = os.path.join(pathlib.Path(__file__).parent.absolute(), 'db')
    if not os.path.isdir(db_path):
        try:
            os.mkdir(path=db_path)
        except OSError:
            raise Exception('Database directory creation failed.')

    if not _server:
        log_path = os.path.join(pathlib.Path(__file__).parent.absolute(), 'mongo.server.log')
        _server = subprocess.Popen([_daemon_path, '--config', _config_file, '--dbpath', db_path, '--logpath', log_path],
                                   text=True)


def close_server():
    """
    Terminates the current process of the local MongoDB server. Does nothing if
    the process does not exist (the server is already inactive).
    :return: None
    """

    global _server
    if _server:
        _server.terminate()
        _server.wait()
        _server = None


if __name__ == '__main__':
    start_server()
    while input('Press q to quit: ') != 'q':
        pass
    close_server()
