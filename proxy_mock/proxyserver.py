from subprocess import Popen
import subprocess
import pkg_resources
import os

# Creates a subprocess of proxy.py (pip package) and host a local proxy server.
# Pip package: https://pypi.org/project/proxy.py/
# Github: https://github.com/abhinavsingh/proxy.py/blob/develop/proxy/proxy.py
class ProxyServer():

    # public variables for the proxy server
    user : str = "test"
    password : str = "test"
    host : str = "127.0.0.1"
    port : str = "8080"

    # Private variables used throughout this class
    _serverProcess = None
    _isAuthenticated : bool = False

    def __init__(self, authenticated : bool):
        self._isAuthenticated = authenticated

        # Check if required pip package is installed
        try:
             pkg_resources.require("proxy.py")
        except pkg_resources.DistributionNotFound:
            assert False, "proxy.py pip package is not installed!"

    def start(self):
        ''' Starts the proxy server (Configuration depends on constructor) on the local workstation.'''

        proxyType : str = "Authenticated" if self._isAuthenticated else "Unauthenticated"
        print(f"Opening proxy server {self.host}:{self.port} ({proxyType})")

        script_dir = os.path.dirname(os.path.abspath(__file__))

        if self._isAuthenticated:
            self._serverProcess = subprocess.Popen([
                "proxy",
                "--hostname", self.host,
                "--port", self.port,
                "--basic-auth", f"{self.user}:{self.password}",
                # "--cert-file", script_dir + "/cert.pem",
                # "--key-file", script_dir  + "/key.pem"
                ])
        else:
            self._serverProcess = subprocess.Popen([
                "proxy",
                "--hostname", self.host,
                "--port", self.port,
                # "--cert-file", script_dir + "/cert.pem",
                # "--key-file", script_dir  + "/key.pem"
                ])

    def stop(self):
        ''' Stops the proxy server (Configuration depends on constructor) on the local workstation.'''
        
        print(f"Closing proxy server {self.host}:{self.port}")
        self._serverProcess.kill()
        self._serverProcess.terminate()

    def isRunning(self) -> bool:
        ''' Current state of the proxy server subprocess, returns true when the subprocess is stil active.'''
        return self._serverProcess.poll() is None

if __name__ == "__main__":
    import time

    # Change to True if you want authentication
    authenticated = True

    proxy = ProxyServer(authenticated)
    proxy.start()
    print("Proxy server started. Press Ctrl+C to stop.")

    try:
        while proxy.isRunning():
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping proxy server...")
        proxy.stop()
        print("Proxy server stopped.")
# ...existing code...