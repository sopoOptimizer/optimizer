import os
import ctypes

def is_windows():
    """Devuelve True si el SO es Windows."""
    return os.name == "nt"

def is_admin():
    """Devuelve True si el proceso tiene privilegios de administrador (solo Windows)."""
    if not is_windows():
        return False
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception:
        return False

def relaunch_as_admin():
    """Reinicia el script actual con privilegios de administrador (solo Windows)."""
    if not is_windows():
        return
    import sys
    params = ' '.join([f'"{arg}"' for arg in sys.argv])
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, params, None, 1)
    sys.exit(0)
