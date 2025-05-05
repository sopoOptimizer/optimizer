import os
import sys
import subprocess

class ScriptManager:
    """
    Gestiona la carga, ejecución e importación de scripts externos (.ps1, .bat, .py, .reg)
    para las optimizaciones del sistema.
    """
    def __init__(self):
        self.scripts = {}
        self.script_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts")
        if not os.path.exists(self.script_dir):
            os.makedirs(self.script_dir)
        self.load_scripts()

    def load_scripts(self):
        """Carga todos los scripts válidos de la carpeta scripts."""
        self.scripts = {}
        if os.path.exists(self.script_dir):
            for filename in os.listdir(self.script_dir):
                if filename.endswith((".py", ".ps1", ".bat", ".reg")):
                    script_path = os.path.join(self.script_dir, filename)
                    self.scripts[filename] = script_path

    def execute_script(self, script_name):
        """
        Ejecuta un script .py, .ps1, .bat o .reg.
        Retorna (True, salida_stdout) si éxito, o (False, error) si falla.
        """
        # DEBUG: Mostrar los scripts cargados y el nombre buscado
        print(f"[DEBUG] Scripts cargados: {list(self.scripts.keys())}")
        print(f"[DEBUG] Buscando script: {script_name}")
        if script_name not in self.scripts:
            return False, f"Script {script_name} no encontrado en {self.script_dir}"
        script_path = self.scripts[script_name]
        try:
            if script_path.endswith('.py'):
                result = subprocess.run([sys.executable, script_path], capture_output=True, text=True, shell=True)
            elif script_path.endswith('.ps1'):
                print(f"[EXEC] Ejecutando PowerShell como admin: {script_path}")
                # Lanzar el script sin esperar a que termine
                subprocess.Popen([
                    "powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-WindowStyle", "Hidden", "-File", script_path
                ], shell=True)
                return True, "Script lanzado"
            elif script_path.endswith('.bat'):
                result = subprocess.run([script_path], capture_output=True, text=True, shell=True)
            elif script_path.endswith('.reg'):
                result = subprocess.run([
                    "reg", "import", script_path
                ], capture_output=True, text=True, shell=True)
            else:
                return False, "Tipo de script no soportado"
            # Manejo de reinicio requerido
            if result.returncode == 3010:
                return True, result.stdout
            if result.returncode != 0:
                return False, f"Error al ejecutar script: {result.stderr}"
            return True, result.stdout
        except Exception as e:
            return False, f"Error al ejecutar script: {str(e)}"

    def import_script(self, file_path):
        """Importa un script externo a la carpeta scripts."""
        if not os.path.exists(file_path):
            return False, f"El archivo {file_path} no existe"
        filename = os.path.basename(file_path)
        destination = os.path.join(self.script_dir, filename)
        try:
            with open(file_path, 'rb') as src_file:
                with open(destination, 'wb') as dst_file:
                    dst_file.write(src_file.read())
            self.scripts[filename] = destination
            return True, f"Script {filename} importado correctamente"
        except Exception as e:
            return False, f"Error al importar script: {str(e)}"

    def create_restore_point(self, description="SOPO Punto de Restauración"):
        """
        Crea un punto de restauración usando WMI directamente en Python.
        Retorna (True, mensaje) o (False, error).
        """
        try:
            import win32com.client
            srv = win32com.client.Dispatch("WbemScripting.SWbemLocator").ConnectServer('.', 'root\\default')
            params = srv.Get("SystemRestore").Methods_("CreateRestorePoint").InParameters.SpawnInstance_()
            params.Properties_.Item('Description').Value = description
            params.Properties_.Item('RestorePointType').Value = 12  # MODIFY_SETTINGS
            params.Properties_.Item('EventType').Value = 100  # BEGIN_NESTED_SYSTEM_CHANGE
            result = srv.ExecMethod_('SystemRestore', 'CreateRestorePoint', params)
            code = result.Properties_.Item('ReturnValue').Value
            if code == 0:
                return True, "Punto de restauración creado correctamente."
            else:
                return False, f"Fallo WMI al crear restore point, código {code}."
        except Exception as e:
            return False, f"Error al crear punto de restauración: {e}"
