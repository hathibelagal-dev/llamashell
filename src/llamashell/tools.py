import os
import subprocess
import shlex
import importlib.metadata
import importlib.util
import dns.resolver
import dns.rdatatype
import sys
import json
import platform


def tool_get_current_directory() -> str:
    """Get the current working directory.

    Returns:
        str: The current working directory.
    """
    return os.getcwd()

def tool_change_directory(absolute_path: str) -> bool:
    """Change the current working directory to the given absolute path.

    Args:
        absolute_path: The absolute path of the directory to change to.

    Returns:
        True if the directory was changed successfully, False otherwise.
    """
    try:
        os.chdir(absolute_path)
        return True
    except OSError:
        return False
    

def tool_make_directory(absolute_path: str) -> bool:
    """Create a directory at the given absolute path.

    Args:
        absolute_path: The absolute path of the directory to create.

    Returns:
        True if the directory was created successfully, False otherwise.
    """
    try:
        os.makedirs(absolute_path)
        return True
    except OSError:
        return False
    
def tool_write_file(absolute_path: str, contents: str) -> bool:
    """Create a file at the given absolute path with the given contents.

    Args:
        absolute_path: The absolute path of the file to create.
        contents: The contents of the file to create.

    Returns:
        True if the file was created successfully, False otherwise.
    """
    try:
        with open(absolute_path, "w") as f:
            f.write(contents)
        return True
    except OSError:
        return False
    
def tool_read_file(absolute_path: str) -> str:
    """Read the contents of a file at the given absolute path.

    Args:
        absolute_path: The absolute path of the file to read.

    Returns:
        The contents of the file.
    """
    try:
        with open(absolute_path, "r") as f:
            return f.read()
    except OSError:
        return ""
    
def tool_list_directory(absolute_path: str) -> list:
    """List the contents of a directory at the given absolute path.

    Args:
        absolute_path: The absolute path of the directory to list.

    Returns:
        A list of the contents of the directory.
    """    
    try:
        return os.listdir(absolute_path)
    except OSError:
        return []
    
def tool_rename_file(old_path: str, new_path: str) -> bool:
    """Rename a file from the old path to the new path.

    Args:
        old_path: The old path of the file to rename.
        new_path: The new path of the file to rename.

    Returns:
        True if the file was renamed successfully, False otherwise.
    """
    try:
        os.rename(old_path, new_path)
        return True
    except OSError:
        return False
    
def tool_delete_file(absolute_path: str) -> bool:
    """Delete a file at the given absolute path.

    Args:
        absolute_path: The absolute path of the file to delete.

    Returns:
        True if the file was deleted successfully, False otherwise.
    """
    try:
        os.remove(absolute_path)
        return True
    except OSError:
        return False
    
def tool_run_python_file(absolute_path: str) -> str:
    """Run a Python file at the given absolute path.

    Args:
        absolute_path: The absolute path of the Python file to run.

    Returns:
        The combined stdout and stderr output of the Python file.
    """
    if not os.path.isfile(absolute_path):
        raise FileNotFoundError(f"No file found at {absolute_path}")
    
    try:
        result = subprocess.run(
            ["python", absolute_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False
        )
        output = result.stdout + result.stderr
        return output.strip()
    except subprocess.SubprocessError as e:
        raise ""
    
def tool_run_command(command: str, shell: bool = False) -> str:
    """Run a command and return the combined stdout and stderr output.

    Args:
        command: The command to run.
        shell: If True, run the command through the shell. Defaults to False.

    Returns:
        The combined stdout and stderr output of the command.
    """
    try:
        if shell:
            cmd = command
        else:
            cmd = shlex.split(command)
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            shell=shell,
            check=False
        )

        output = result.stdout + result.stderr
        return output.strip()
    except:
        return ""
    
def tool_get_python_package_version(package_name: str) -> str:
    """Check if a Python package is installed and return its version.

    Args:
        package_name: The name of the package to check.

    Returns:
        The version of the package if installed, or an empty string if not installed.
    """
    try:
        if importlib.util.find_spec(package_name) is not None:
            return importlib.metadata.version(package_name)
        return ""
    except (importlib.metadata.PackageNotFoundError, ModuleNotFoundError):
        return ""
    
def tool_install_python_package(package_name: str, version: str = None) -> bool:
    """Install a Python package using pip.

    Args:
        package_name: The name of the package to install.
        version: The specific version to install (e.g., '2.28.1'). If None, installs the latest version.

    Returns:
        True if the package was installed successfully or is already installed with the correct version, False otherwise.
    """
    package_spec = f"{package_name}=={version}" if version else package_name

    try:
        if tool_get_python_package_version(package_name) == version:
            return True
        
        if not version:
            if tool_get_python_package_version(package_name):
                return True                            

        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", package_spec],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        print(result.stdout.strip())
        print(result.stderr.strip())

        if tool_get_python_package_version(package_name) == version:
            return True
        
        if not version and tool_get_python_package_version(package_name):
            return True
        
        return False

    except:
        return False
    
def tool_uninstall_python_package(package_name: str) -> bool:
    """Uninstall a Python package using pip.

    Args:
        package_name: The name of the package to uninstall.

    Returns:
        True if the package was uninstalled successfully, False otherwise.
    """
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pip", "uninstall", "-y", 
             package_name, "--quiet"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        print(result.stdout.strip())
        print(result.stderr.strip())
        return True
    except:
        return False
    
def tool_get_current_user() -> str:
    """Get the current user.

    Returns:
        The current user.
    """
    return os.getlogin()

def tool_get_current_time() -> str:
    """Get the current time.

    Returns:
        The current time.
    """
    return os.popen("date").read().strip()

def tool_get_current_day() -> str:
    """Get the current day.

    Returns:
        The current day.
    """
    return os.popen("date +'%A'").read().strip()

def tool_get_current_month() -> str:
    """Get the current month.

    Returns:
        The current month.
    """
    return os.popen("date +'%B'").read().strip()

def tool_get_current_year() -> str:
    """Get the current year.

    Returns:
        The current year.
    """
    return os.popen("date +'%Y'").read().strip()

def tool_get_dns_records(domain: str, record_types: list[str] = None) -> str:
    """Retrieve DNS records for a given domain.

    Args:
        domain: The domain name to query (e.g., 'example.com').
        record_types: List of DNS record types to query (e.g., ['A', 'MX', 'NS']).
                                           If None, queries common types: A, MX, NS, TXT, CNAME, AAAA.

    Returns:
        A dictionary mapping record types to lists of record values.
              Returns an empty list for a record type if no records are found or if an error occurs.
    """
    if record_types is None:
        record_types = ['A', 'MX', 'NS', 'TXT', 'CNAME', 'AAAA']

    result = {rtype: [] for rtype in record_types}

    for rtype in record_types:
        try:
            rdtype = getattr(dns.rdatatype, rtype.upper(), None)
            if rdtype is None:
                result[rtype] = []
                continue

            answers = dns.resolver.resolve(domain, rdtype)
            for answer in answers:
                if rtype == 'MX':
                    result[rtype].append(f"{answer.preference} {answer.exchange}")
                elif rtype in ['NS', 'CNAME']:
                    result[rtype].append(str(answer.target))
                elif rtype == 'TXT':
                    result[rtype].append(' '.join(s.decode('utf-8') for s in answer.strings))
                else:
                    result[rtype].append(str(answer))
        except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer, dns.resolver.NoNameservers,
                dns.resolver.LifetimeTimeout, dns.exception.DNSException):
            result[rtype] = []

    return json.dumps(result)

def tool_list_python_packages(pattern: str = None) -> list:
    """Lists all installed python packages that match the given pattern.
    If no pattern is provided, lists all installed python packages.

    Args:
        pattern: The pattern to search for in the package names
    
    Returns:
        A list of all installed python packages
    """
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pip", "list"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        packages = [line.split()[0] for line in result.stdout.strip().split("\n")]
        return [pkg for pkg in packages if pattern in pkg] if pattern else packages
    except:
        return []
    
def tool_get_system_information() -> str:
    """Return system information equivalent to the 'uname -a' command.

    Returns:
        A string containing system information including OS, hostname, kernel version, release, and architecture.

    Example:
        On Linux: 'Linux hostname 5.15.0-73-generic #80-Ubuntu SMP x86_64 GNU/Linux'
        On macOS: 'Darwin hostname 22.6.0 Darwin Kernel Version 22.6.0 x86_64 macOS'
        On Windows: 'Windows hostname 10.0.22621 AMD64 Windows'
    """
    try:
        system = platform.system()
        hostname = platform.node()
        release = platform.release()
        version = platform.version()
        machine = platform.machine()

        if system == "Linux":
            version = version.split("#")[0].strip() if "#" in version else version
            return f"{system} {hostname} {release} {version} {machine} {system}"
        elif system == "Darwin":
            return f"{system} {hostname} {release} {version} {machine} macOS"
        elif system == "Windows":
            return f"{system} {hostname} {release} {version} {machine} {system}"
        else:
            return f"{system} {hostname} {release} {version} {machine} {system}"

    except Exception as e:
        return f"Error retrieving system information: {str(e)}"