from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QGroupBox, QCheckBox, QPushButton, QHBoxLayout, QMessageBox, QComboBox
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from .custom_widgets import ModernButton, AccentButton, ModernGroupBox, ModernCheckBox
from .script_manager import ScriptManager  # Importar gestor de scripts
from .translations import TRANSLATIONS

class SettingsPanel(QWidget):
    def __init__(self, lang="es"):
        super().__init__()
        self.lang = lang
        self.script_manager = ScriptManager()  # Instanciar gestor de scripts
        self.setStyleSheet("background-color: #181f2a;")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 30, 40, 30)
        layout.setSpacing(20)
        self.title = QLabel()
        self.title.setStyleSheet("font-size: 20px; color: #60a5fa; font-weight: bold; margin-bottom: 4px;")
        layout.addWidget(self.title)
        self.desc = QLabel()
        self.desc.setStyleSheet("font-size: 13px; color: #94a3b8; margin-bottom: 16px;")
        self.desc.setWordWrap(True)
        layout.addWidget(self.desc)
        self.group = ModernGroupBox("")
        group_layout = QVBoxLayout(self.group)
        
        # Botón para buscar actualizaciones de Windows Update (primera opción)
        self.update_btn = AccentButton("")
        self.update_btn.clicked.connect(self.on_check_windows_update)
        group_layout.addWidget(self.update_btn)
        
        # Checkbox para modo oscuro
        self.cb_darkmode = ModernCheckBox("")
        group_layout.addWidget(self.cb_darkmode)
        
        # Checkbox para desactivar OneDrive
        self.cb_oneDrive = ModernCheckBox("")
        self.cb_oneDrive.stateChanged.connect(self.toggle_oneDrive)
        group_layout.addWidget(self.cb_oneDrive)
        
        # Checkbox para desactivar Microsoft Edge
        self.cb_edge = ModernCheckBox("")
        self.cb_edge.stateChanged.connect(self.toggle_edge)
        group_layout.addWidget(self.cb_edge)
        
        # Checkbox para desactivar seguimiento de ubicación
        self.cb_location = ModernCheckBox("")
        self.cb_location.stateChanged.connect(self.toggle_location)
        group_layout.addWidget(self.cb_location)
        
        # Checkbox para desactivar notificaciones
        self.cb_notifications = ModernCheckBox("")
        self.cb_notifications.stateChanged.connect(self.toggle_notifications)
        group_layout.addWidget(self.cb_notifications)
        
        # Checkbox para eliminar archivos temporales
        self.cb_temp_files = ModernCheckBox("")
        self.cb_temp_files.stateChanged.connect(self.toggle_temp_files)
        group_layout.addWidget(self.cb_temp_files)
        
        # Checkbox para desactivar apps en segundo plano
        self.cb_bg_apps = ModernCheckBox("")
        self.cb_bg_apps.stateChanged.connect(self.toggle_bg_apps)
        group_layout.addWidget(self.cb_bg_apps)
        
        # Selector de idioma
        self.language_label = QLabel()
        self.language_label.setStyleSheet("color: #60a5fa; font-weight: bold; margin-top: 10px;")
        group_layout.addWidget(self.language_label)
        self.language_combo = QComboBox()
        self.language_combo.addItems(["Català", "Español", "English"])
        lang_to_idx = {"ca": 0, "es": 1, "en": 2}
        self.language_combo.setCurrentIndex(lang_to_idx.get(self.lang, 1))
        self.language_combo.currentIndexChanged.connect(self._on_language_changed)
        group_layout.addWidget(self.language_combo)
        
        # Opción de crear punto de restauración
        self.cb_restore = ModernCheckBox("")
        group_layout.addWidget(self.cb_restore)
        self.cb_restore.stateChanged.connect(self.on_restore_toggled)
        
        layout.addWidget(self.group)
        btns = QHBoxLayout()
        self.save_btn = AccentButton("")
        self.save_btn.clicked.connect(self.save_settings)
        btns.addWidget(self.save_btn)
        self.reset_btn = ModernButton("")
        self.reset_btn.clicked.connect(self.reset_settings)
        btns.addWidget(self.reset_btn)
        layout.addLayout(btns)
        self.set_texts()

    def set_texts(self):
        t = TRANSLATIONS[self.lang]
        try:
            self.title.setText(t["settings"])
            self.desc.setText(t.get("settings_desc", "Ajusta la configuración de la aplicación según tus preferencias."))
            self.group.setTitle(t.get("general_options", "Opciones generales"))
            self.update_btn.setText(t["windows_update"])
            self.cb_darkmode.setText(t["dark_mode"])
            self.cb_oneDrive.setText(t.get("disable_oneDrive", "Desactivar OneDrive"))
            self.cb_edge.setText(t.get("disable_edge", "Desactivar Microsoft Edge"))
            self.cb_location.setText(t.get("disable_location", "Desactivar seguimiento de ubicación"))
            self.cb_notifications.setText(t.get("disable_notifications", "Desactivar notificaciones de Windows"))
            self.cb_temp_files.setText(t.get("delete_temp_files", "Eliminar archivos temporales"))
            self.cb_bg_apps.setText(t.get("disable_bg_apps", "Desactivar apps de Microsoft en segundo plano"))
            self.language_label.setText(t["language"])
            self.cb_restore.setText(t["restore_point"])
            self.save_btn.setText(t["save_settings"])
            self.reset_btn.setText(t["reset_settings"])
        except KeyError as e:
            print(f"[ERROR i18n] Falta la clave de traducción: {e} para el idioma {self.lang}")

    def toggle_notifications(self, state):
        import os, sys
        t = TRANSLATIONS[self.lang]
        script_path = os.path.join(os.path.dirname(sys.argv[0]), "scripts", "noNotifications.ps1")
        from PyQt6.QtWidgets import QMessageBox
        import subprocess
        try:
            completed = subprocess.run(["powershell", "-ExecutionPolicy", "Bypass", "-File", script_path], 
                                     capture_output=True, text=True, shell=True)
            if completed.returncode == 0:
                msg = "Notificaciones desactivadas" if state else "Notificaciones activadas"
                QMessageBox.information(self, t.get("success", "Éxito"), msg)
            else:
                QMessageBox.warning(self, t.get("error", "Error"), 
                                  f"No se pudieron {'desactivar' if state else 'activar'} las notificaciones\n{completed.stderr}")
                self.cb_notifications.setChecked(not state)  # Revertir el cambio
        except Exception as e:
            QMessageBox.critical(self, t.get("error", "Error"), 
                               f"Error al {'desactivar' if state else 'activar'} notificaciones\n{e}")
            self.cb_notifications.setChecked(not state)  # Revertir el cambio

    def toggle_oneDrive(self, state):
        import os, sys
        t = TRANSLATIONS[self.lang]
        script_path = os.path.join(os.path.dirname(sys.argv[0]), "scripts", "noOneDrive.ps1")
        from PyQt6.QtWidgets import QMessageBox
        import subprocess
        
        try:
            completed = subprocess.run(["powershell", "-ExecutionPolicy", "Bypass", "-File", script_path], 
                                     capture_output=True, text=True, shell=True)
            if completed.returncode == 0:
                QMessageBox.information(self, t.get("success", "Éxito"), 
                                      t.get("oneDrive_disabled", "OneDrive ha sido desactivado correctamente"))
            else:
                QMessageBox.warning(self, t.get("error", "Error"), 
                                  f"{t.get('oneDrive_disable_failed', 'Error al desactivar OneDrive')}\n{completed.stderr}")
                self.cb_oneDrive.setChecked(False)
        except Exception as e:
            QMessageBox.critical(self, t.get("error", "Error"), 
                               f"{t.get('oneDrive_disable_failed', 'Error al desactivar OneDrive')}\n{e}")
            self.cb_oneDrive.setChecked(False)

    def toggle_edge(self, state):
        import os, sys
        t = TRANSLATIONS[self.lang]
        script_path = os.path.join(os.path.dirname(sys.argv[0]), "scripts", "noEdge.ps1")
        from PyQt6.QtWidgets import QMessageBox
        import subprocess
        
        try:
            completed = subprocess.run(["powershell", "-ExecutionPolicy", "Bypass", "-File", script_path], 
                                     capture_output=True, text=True, shell=True)
            if completed.returncode == 0:
                QMessageBox.information(self, t.get("success", "Éxito"), 
                                      t.get("edge_disabled", "Microsoft Edge ha sido desactivado correctamente"))
            else:
                QMessageBox.warning(self, t.get("error", "Error"), 
                                  f"{t.get('edge_disable_failed', 'Error al desactivar Microsoft Edge')}\n{completed.stderr}")
                self.cb_edge.setChecked(False)
        except Exception as e:
            QMessageBox.critical(self, t.get("error", "Error"), 
                               f"{t.get('edge_disable_failed', 'Error al desactivar Microsoft Edge')}\n{e}")
            self.cb_edge.setChecked(False)

    def toggle_location(self, state):
        import os, sys
        t = TRANSLATIONS[self.lang]
        script_path = os.path.join(os.path.dirname(sys.argv[0]), "scripts", "noLocationTracking.ps1")
        from PyQt6.QtWidgets import QMessageBox
        import subprocess
        
        try:
            completed = subprocess.run(["powershell", "-ExecutionPolicy", "Bypass", "-File", script_path], 
                                     capture_output=True, text=True, shell=True)
            if completed.returncode == 0:
                QMessageBox.information(self, t.get("success", "Éxito"), 
                                      t.get("location_disabled", "Seguimiento de ubicación desactivado correctamente"))
            else:
                QMessageBox.warning(self, t.get("error", "Error"), 
                                  f"{t.get('location_disable_failed', 'Error al desactivar seguimiento de ubicación')}\n{completed.stderr}")
                self.cb_location.setChecked(False)
        except Exception as e:
            QMessageBox.critical(self, t.get("error", "Error"), 
                               f"{t.get('location_disable_failed', 'Error al desactivar seguimiento de ubicación')}\n{e}")
            self.cb_location.setChecked(False)

    def toggle_temp_files(self, state):
        import subprocess, os
        script_path = os.path.join(os.path.dirname(__file__), "..", "scripts", "DeleteTempFiles.ps1")
        try:
            result = subprocess.run(
                ["powershell", "-ExecutionPolicy", "Bypass", "-File", script_path],
                capture_output=True,
                text=True,
                shell=True,
                cwd=os.path.dirname(script_path)
            )
            print(f"[DEBUG] STDOUT: {result.stdout}\nSTDERR: {result.stderr}\nRETURNCODE: {result.returncode}")
            if result.returncode == 0:
                QMessageBox.information(self, "Éxito", TRANSLATIONS[self.lang].get("temp_files_deleted", "Archivos temporales eliminados correctamente"))
            else:
                QMessageBox.warning(self, "Error", f"{TRANSLATIONS[self.lang].get('temp_files_error', 'Error al eliminar temporales')}:\n{result.stderr}\n{result.stdout}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"{TRANSLATIONS[self.lang].get('temp_files_error', 'Error al eliminar temporales')}:\n{str(e)}")

    def toggle_bg_apps(self, state):
        import subprocess, os
        script_path = os.path.join(os.path.dirname(__file__), "..", "scripts", "DisableBackgroundApps.ps1")
        try:
            result = subprocess.run(
                ["powershell", "-ExecutionPolicy", "Bypass", "-File", script_path],
                capture_output=True,
                text=True,
                shell=True
            )
            if result.returncode == 0:
                QMessageBox.information(self, "Éxito", TRANSLATIONS[self.lang].get("bg_apps_disabled", "Apps en segundo plano desactivadas correctamente"))
            else:
                QMessageBox.warning(self, "Error", f"{TRANSLATIONS[self.lang].get('bg_apps_error', 'Error al desactivar apps en segundo plano')}:\n{result.stderr}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"{TRANSLATIONS[self.lang].get('bg_apps_error', 'Error al desactivar apps en segundo plano')}:\n{str(e)}")

    def change_language(self, lang):
        self.lang = lang
        self.set_texts()
        idx = {"ca": 0, "es": 1, "en": 2}.get(lang, 1)
        if self.language_combo.currentIndex() != idx:
            self.language_combo.blockSignals(True)
            self.language_combo.setCurrentIndex(idx)
            self.language_combo.blockSignals(False)

    def _on_language_changed(self, idx):
        lang_map = {0: "ca", 1: "es", 2: "en"}
        lang = lang_map.get(idx, "es")
        parent = self.parent()
        while parent and not hasattr(parent, "change_language"):
            parent = parent.parent()
        if parent and hasattr(parent, "change_language"):
            if getattr(parent, 'lang', None) != lang:
                parent.change_language(lang)
        else:
            if self.lang != lang:
                self.change_language(lang)

    class UpdateCheckWorker(QThread):
        finished = pyqtSignal(str)
        def __init__(self, script_path):
            super().__init__()
            self.script_path = script_path
        def run(self):
            import subprocess
            result = subprocess.run([
                "powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", self.script_path
            ], capture_output=True, text=True)
            salida = result.stdout.strip()
            self.finished.emit(salida)

    def on_check_windows_update(self):
        import os, sys
        t = TRANSLATIONS[self.lang]
        script_path = os.path.join(os.path.dirname(sys.argv[0]), "scripts", "windows_update.ps1")
        self.worker = self.UpdateCheckWorker(script_path)
        self.worker.finished.connect(lambda salida: self.show_update_result(salida, t))
        self.worker.start()

    def show_update_result(self, salida, t):
        from PyQt6.QtWidgets import QMessageBox, QPushButton
        if not salida:
            salida = t.get("no_updates", "No hay actualizaciones pendientes.")
        msg = QMessageBox(self)
        msg.setWindowTitle(t["windows_update"])
        msg.setText(salida)
        btn_open = QPushButton("Abrir Windows Update")
        def open_winupdate():
            import os
            os.system("start ms-settings:windowsupdate")
        btn_open.clicked.connect(open_winupdate)
        msg.addButton(btn_open, QMessageBox.ButtonRole.ActionRole)
        msg.addButton(t.get("ok", "OK"), QMessageBox.ButtonRole.AcceptRole)
        msg.exec()

    def save_settings(self):
        t = TRANSLATIONS[self.lang]
        if self.cb_darkmode.isChecked():
            success, output = self.script_manager.execute_script("modo_oscuro.ps1")
            if success:
                QMessageBox.information(self, t["dark_mode"], t.get("dark_mode_success", "Modo oscuro activado correctamente."))
            else:
                QMessageBox.critical(self, t["error"], t.get("dark_mode_error", f"No se pudo activar el modo oscuro:\n{output}"))
        if self.cb_oneDrive.isChecked():
            self.toggle_oneDrive(True)
        if self.cb_edge.isChecked():
            self.toggle_edge(True)
        if self.cb_location.isChecked():
            self.toggle_location(True)
        if self.cb_notifications.isChecked():
            self.toggle_notifications(True)
        if self.cb_temp_files.isChecked():
            self.toggle_temp_files(True)
        if self.cb_bg_apps.isChecked():
            self.toggle_bg_apps(True)
        QMessageBox.information(self, t["settings"], t["config_saved"])

    def reset_settings(self):
        t = TRANSLATIONS[self.lang]
        from PyQt6.QtWidgets import QMessageBox
        reply = QMessageBox.question(self, t["warning"], t["confirm_restore"], QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            # Aquí restablecerías los valores predeterminados
            QMessageBox.information(self, t["success"], t["values_restored"])

    def on_restore_toggled(self, state):
        """Crea un punto de restauración usando un script PowerShell externo si la casilla está activada."""
        import subprocess, os, sys
        if state == 2:
            try:
                script_path = os.path.join(os.path.dirname(sys.argv[0]), "scripts", "create_restore_point.ps1")
                result = subprocess.run([
                    "powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", script_path
                ], capture_output=True, text=True)
                salida = f"STDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}\nReturn code: {result.returncode}"
                if result.returncode == 0:
                    QMessageBox.information(self, "Punto de Restauración", salida)
                else:
                    QMessageBox.critical(self, "Error Punto de Restauración", salida)
            except Exception as e:
                QMessageBox.critical(self, "Error inesperado", str(e))
