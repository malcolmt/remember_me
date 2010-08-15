import socket

def load_external_settings(module_root, caller_globals):
    """
    Loads an external settings file, based on machine hostname, and pulls all
    the all-caps names into the passed-in namespace.
    """
    # Convert machine hostname to valid Python module name.
    hostname = socket.gethostname().replace(".", "_").replace("-", "_")
    try:
        module = __import__("%s.%s" % (module_root, hostname), caller_globals,
                {}, [])
        local_settings = getattr(module, hostname)
        for setting in dir(local_settings):
            if setting.upper() == setting:
                caller_globals[setting] = getattr(local_settings, setting)
    except ImportError:
        # File may not exist, so we ignore all import errors. If you make a
        # Python syntax error in the file, it will be swallowed silently. So
        # don't do that.
        pass

