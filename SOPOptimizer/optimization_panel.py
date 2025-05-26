from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QCheckBox, QHBoxLayout, QGroupBox, QMessageBox, QFrame, QSizePolicy
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QObject, QTimer
from .script_manager import ScriptManager
from .translations import TRANSLATIONS
import os

class ModernButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setMinimumHeight(40)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setStyleSheet("""
            QPushButton {
                background-color: #232e40;
                color: white;
                font-weight: bold;
                border-radius: 8px;
                padding: 10px 15px;
                border: none;
            }
            QPushButton:hover {
                background-color: #2D3748;
            }
            QPushButton:pressed {
                background-color: #0D1420;
            }
        """)

class AccentButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setMinimumHeight(40)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setStyleSheet("""
            QPushButton {
                background-color: #3B82F6;
                color: white;
                font-weight: bold;
                border-radius: 8px;
                padding: 10px 15px;
            }
            QPushButton:hover {
                background-color: #2563EB;
            }
            QPushButton:pressed {
                background-color: #1D4ED8;
            }
        """)

class OptimizationPanel(QWidget):
    def change_language(self, lang):
        self.lang = lang
        self.set_texts()

    def set_texts(self):
        t = TRANSLATIONS[self.lang]
        try:
            self.title.setText(t["optimization"])
            self.desc.setText(t.get("optimization_desc", "Panel de optimización del sistema."))
            # Botó de la memòria tècnica
            self.docs_btn.setText(t.get("docs_btn", "📄 Veure Memòria Tècnica dels Scripts"))
            # Botones de perfil
            self.daily_btn.setText(t.get("daily_profile", "Uso Diario"))
            self.work_btn.setText(t.get("work_profile", "Trabajo"))
            self.gaming_btn.setText(t.get("gaming_profile", "Gaming"))
            # Título del grupo
            self.optim_group.setTitle(t.get("profile_optimizations_group", "Profile Optimizations"))
            # Botones de acción
            self.execute_profile_btn.setText(t.get("execute_profile_btn", "Ejecutar Optimizaciones de Perfil"))
            self.execute_selected_btn.setText(t.get("execute_selected_btn", "Ejecutar Todas las Optimizaciones Seleccionadas"))
            # Nota
            self.note.setText(t.get("optim_note", "Cree un punto de restauración antes de realizar cambios importantes. Si pasamos el ratón por encima de la optimización, contiene información adicional."))
            # Actualizar optimizaciones mostradas (checkboxes y tooltips)
            self.update_profile_checkboxes()
        except KeyError as e:
            print(f"[ERROR i18n] Falta la clave de traducción: {e} para el idioma {self.lang}")

    def update_profile_checkboxes(self):
        t = TRANSLATIONS[self.lang]
        profile_key = self.current_profile_key
        # Limpia los checkboxes anteriores
        for cb in self.checkboxes:
            cb.deleteLater()
        self.checkboxes = []
        # Añade los checkboxes traducidos
        for opt_key, tooltip_key in self.optimization_profiles[profile_key]:
            cb = QCheckBox(t.get(opt_key, opt_key))
            cb.setStyleSheet("""
                QCheckBox {
                    font-size: 18px;
                    color: #e0e7ef;
                    margin-bottom: 10px;
                    background: #181f2a;
                    border: none;
                }
                QCheckBox::indicator {
                    width: 24px;
                    height: 24px;
                    border-radius: 3px;
                    border: 1px solid #4B5563;
                }
                QCheckBox::indicator:unchecked {
                    background-color: #1E293B;
                }
                QCheckBox::indicator:checked {
                    background-color: #3B82F6;
                    border: 1px solid #3B82F6;
                }
                QCheckBox::indicator:hover {
                    border: 1px solid #3B82F6;
                }
            """)
            cb.setToolTip(t.get(tooltip_key, tooltip_key))
            cb.optim_key = opt_key  # --- NUEVO: Guarda la clave interna ---
            self.optim_layout.addWidget(cb)
            self.checkboxes.append(cb)

    def __init__(self, lang="es"):
        super().__init__()
        self.lang = lang
        self.setStyleSheet("background-color: #181f2a;")
        from PyQt6.QtWidgets import QScrollArea
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Panel central envuelto en QScrollArea para responsividad
        self.central = QWidget()
        self.central.setStyleSheet("background: #121A2B; border-radius: 10px; border: 2px solid #1E293B;")
        self.central.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.central_layout = QVBoxLayout(self.central)
        self.central_layout.setSpacing(24)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setWidget(self.central)
        main_layout.addWidget(scroll)
        self._set_central_margins()

        # Título
        self.title = QLabel()
        self.title.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.title.setStyleSheet("font-size: 26px; color: #60a5fa; font-weight: bold; margin-bottom: 8px; background: transparent; border: none;")
        self.central_layout.addWidget(self.title)

        # Subtítulo/descripción
        self.desc = QLabel()
        self.desc.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.desc.setStyleSheet("font-size: 13px; color: #94a3b8; margin-bottom: 8px; background: transparent; border: none;")
        self.desc.setWordWrap(True)
        self.central_layout.addWidget(self.desc)

        # Guardar clave interna del perfil actual
        self.current_profile_key = "daily_profile"

        # Separador
        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setStyleSheet("background-color: #1E293B; min-height: 2px; margin: 16px 0px; border: none;")
        self.central_layout.addWidget(sep)

        # Botones de perfil
        profile_layout = QHBoxLayout()
        self.daily_btn = ModernButton("Uso Diario")
        self.work_btn = ModernButton("Trabajo")
        self.gaming_btn = ModernButton("Gaming")
        for btn in [self.daily_btn, self.work_btn, self.gaming_btn]:
            btn.setCheckable(True)
            btn.setStyleSheet("background: #232e40; color: #e0e7ef; font-size: 16px; padding: 10px 32px; margin: 0 8px; border-radius: 8px; border: none;")
            profile_layout.addWidget(btn)
        self.daily_btn.setChecked(True)
        self.central_layout.addLayout(profile_layout)

        # Caja de optimizaciones igual a benchmark
        self.optim_group = QGroupBox("Optimizaciones por Perfil")
        self.optim_group.setStyleSheet("QGroupBox { background-color: #181f2a; border-radius: 8px; border: 1px solid #232e40; margin-top: 18px; font-weight: bold; color: white; font-size: 15px; } QGroupBox::title { subcontrol-origin: margin; subcontrol-position: top center; padding: 0 16px; background-color: #181f2a; color: white; font-size: 15px; }")
        self.optim_layout = QVBoxLayout(self.optim_group)
        self.optim_layout.setSpacing(10)
        self.central_layout.addWidget(self.optim_group)

        # Diccionario de optimizaciones por perfil y tooltips (usando claves de traducción)
        # Diccionario de optimizaciones por clave interna de perfil
        self.optimization_profiles = {
            "daily_profile": [
                ("energy_plan_daily", "energy_plan_daily_desc"),
                ("windows_appearance_daily", "windows_appearance_daily_desc"),
                ("windows_performance_daily", "windows_performance_daily_desc"),
                ("system_power_daily", "system_power_daily_desc"),
                ("peripherals_daily", "peripherals_daily_desc"),
                ("network_daily", "network_daily_desc"),
                ("regtweaks_daily", "regtweaks_daily_desc")
            ],
            "work_profile": [
                ("energy_plan_work", "energy_plan_work_desc"),
                ("windows_appearance_work", "windows_appearance_work_desc"),
                ("windows_performance_work", "windows_performance_work_desc"),
                ("secure_network_work", "secure_network_work_desc"),
                ("regtweaks_work", "regtweaks_work_desc"),
            ],
            "gaming_profile": [
                ("energy_plan_gaming", "energy_plan_gaming_desc"),
                ("windows_appearance_gaming", "windows_appearance_gaming_desc"),
                ("windows_performance_gaming", "windows_performance_gaming_desc"),
                ("gaming_disable_gamebar", "gaming_disable_gamebar_desc"),
                ("gaming_mode", "gaming_mode_desc"),
                ("gpu_optimization_gaming", "gpu_optimization_gaming_desc"),
                ("system_power_gaming", "system_power_gaming_desc"),
                ("peripherals_gaming", "peripherals_gaming_desc"),
                ("bonus_gaming", "bonus_gaming_desc"),
                ("privacidad_windows", "privacidad_windows_desc")
            ]
        }
        # --- NUEVO: Diccionario de scripts por clave interna de optimización ---
        self.optimization_scripts = {
            # Daily
            "energy_plan_daily": "importar_uso_diario_powerplan.ps1",
            "windows_appearance_daily": "adjust_appearance_timeout.bat",
            "windows_performance_daily": "advanced_windows_settings.reg",
            "system_power_daily": "system_power_optimization.reg",
            "peripherals_daily": "peripheral_tweaks.reg",
            "network_daily": "network_security_daily.reg",
            "regtweaks_daily": "regtweaks_combined.reg",
            "privacy_daily": "privacy_uso_diario.ps1",
            # Work
            "energy_plan_work": "importar_trabajo_powerplan.ps1",
            "windows_appearance_work": "adjust_appearance_timeout.bat",
            "windows_performance_work": "advanced_windows_settings.reg",
            "secure_network_work": "network_secure_work.reg",
            "regtweaks_work": "regtweaks_extra_work.reg",
            # Gaming
            "energy_plan_gaming": "importar_gaming_powerplan.ps1",
            "windows_appearance_gaming": "adjust_appearance_timeout.bat",
            "windows_performance_gaming": "advanced_windows_settings.reg",
            "gaming_disable_gamebar": "desactivar_grabacion_gamebar.ps1",
            "gaming_mode": "modo_juego.ps1",
            "gpu_optimization_gaming": "gpu_optimization_gaming.reg",
            "system_power_gaming": "system_power_optimization.reg",
            "peripherals_gaming": "peripheral_tweaks.reg",
            "bonus_gaming": "bonus_gaming.bat",
            "privacidad_windows": "privacidad_windows.ps1"
        }
        self.checkboxes = []

        # --- Enllaç a la memòria tècnica de scripts ---
        from PyQt6.QtWidgets import QPushButton
        import webbrowser
        # Text traduïble per al botó de la memòria tècnica
        self.docs_btn = QPushButton("")
        self.docs_btn.setStyleSheet("font-size: 14px; padding: 8px 0; border-radius: 6px; margin-top: 12px; background-color: #fffffff;")
        self.docs_btn.clicked.connect(lambda: webbrowser.open('https://docs.google.com/document/d/1vUjwdvWUlWO2fp7RCwsHfRe-b6GY3ineJIRGMr1rMpw/edit?tab=t.0#heading=h.cvgjx7ji6w9n'))
        self.central_layout.addWidget(self.docs_btn)
        # NO LLAMAR a set_profile aquí, lo hará set_texts al final
        self.daily_btn.clicked.connect(lambda: self.set_profile("daily_profile"))
        self.work_btn.clicked.connect(lambda: self.set_profile("work_profile"))
        self.gaming_btn.clicked.connect(lambda: self.set_profile("gaming_profile"))

        # Botones de acción
        self.execute_profile_btn = AccentButton("")
        self.execute_profile_btn.setStyleSheet("font-size: 15px; padding: 12px 0; border-radius: 8px; margin-top: 18px;")
        self.execute_profile_btn.clicked.connect(self.execute_profile_optimizations)
        self.central_layout.addWidget(self.execute_profile_btn)

        self.execute_selected_btn = AccentButton("")
        self.execute_selected_btn.setStyleSheet("font-size: 15px; padding: 12px 0; border-radius: 8px; margin-top: 8px;")
        self.execute_selected_btn.clicked.connect(self.execute_selected_optimizations)
        self.central_layout.addWidget(self.execute_selected_btn)


        # Nota
        self.note = QLabel()
        self.note.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.note.setStyleSheet("font-size: 13px; color: #f59e42; margin-top: 12px; background: transparent; border: none;")
        self.central_layout.addWidget(self.note)

        # Llama a set_texts SOLO al final, cuando todos los widgets existen
        self.set_texts()

    def resizeEvent(self, event):
        self._set_central_margins()
        super().resizeEvent(event)

    def _set_central_margins(self):
        width = self.width()
        if width > 1400:
            m = 64
        elif width > 1100:
            m = 32
        elif width > 900:
            m = 16
        else:
            m = 6
        self.central_layout.setContentsMargins(m, m, m, m)

    def set_profile(self, profile_key):
        self.current_profile_key = profile_key
        self.daily_btn.setChecked(profile_key == "daily_profile")
        self.work_btn.setChecked(profile_key == "work_profile")
        self.gaming_btn.setChecked(profile_key == "gaming_profile")
        self.set_texts()

    def execute_profile_optimizations(self):
        selected = [cb.optim_key for cb in self.checkboxes if cb.isChecked()]
        if not selected:
            QMessageBox.warning(self, "Nada seleccionado", "Selecciona al menos una optimización.")
            return
        scripts = []
        errors = []
        for opt_key in selected:
            script_name = self.optimization_scripts.get(opt_key)
            if not script_name:
                errors.append(f"No se encontró script para: {opt_key}")
                continue
            scripts.append(script_name)
        if not scripts:
            QMessageBox.warning(self, "Errores al ejecutar", "\n".join(errors))
            return
        self.execute_scripts(scripts, errors)

    def execute_scripts(self, scripts, errors):
        self.execute_profile_btn.setEnabled(False)
        self.execute_selected_btn.setEnabled(False)

        class ScriptRunner(QObject):
            finished = pyqtSignal(list)
            show_message = pyqtSignal(str, str)
            def __init__(self, scripts):
                super().__init__()
                self.scripts = scripts
            def run(self):
                local_errors = errors.copy()
                try:
                    for script_name in self.scripts:
                        print(f"[DEBUG] Ejecutando script: {script_name}")
                        success, output = ScriptManager().execute_script(script_name)
                        if not success:
                            local_errors.append(f"{script_name}: {output}")
                except Exception as e:
                    local_errors.append(f"Excepción inesperada: {str(e)}")
                self.finished.emit(local_errors)

        self.thread = QThread()
        self.runner = ScriptRunner(scripts)
        self.runner.moveToThread(self.thread)
        self.thread.started.connect(self.runner.run)
        self.runner.finished.connect(self.on_scripts_finished)
        self.runner.finished.connect(self.thread.quit)
        self.runner.finished.connect(self.runner.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.start()


    def execute_selected_optimizations(self):
        self.execute_profile_optimizations()

    def on_scripts_finished(self, errors):
        self.execute_profile_btn.setEnabled(True)
        self.execute_selected_btn.setEnabled(True)
        if errors:
            QMessageBox.warning(self, "Errors", "\n".join(errors))
        else:
            QMessageBox.information(self, "Optimització completada", "Totes les optimitzacions s'han executat correctament!")

    def get_script_filename(self, opt_text):
        # Ya no se usa, pero se mantiene para compatibilidad
        return None