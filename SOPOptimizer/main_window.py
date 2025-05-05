import os
from PyQt6.QtWidgets import QMainWindow, QStackedWidget, QWidget, QHBoxLayout, QVBoxLayout, QLabel, QSizePolicy
from .benchmark_panel import BenchmarkPanel
from .optimization_panel import OptimizationPanel
from .ram_cleaner_panel import RamCleanerPanel
from .script_manager import ScriptManager
from .side_panel import EnhancedSidePanel
from .settings_panel import SettingsPanel
from .translations import TRANSLATIONS

class SOPOOptimizer(QMainWindow):
    """
    Ventana principal de la aplicación SOPO: navegación entre paneles y carga de recursos.
    """
    def __init__(self, logo_path, lang="es"):
        super().__init__()
        self.logo_path = logo_path
        self.lang = lang
        self.script_manager = ScriptManager()
        self.setWindowTitle(TRANSLATIONS[self.lang]["main_title"])
        self.setMinimumSize(900, 600)  # Más flexible para pantallas pequeñas
        self.setStyleSheet("""
            QWidget {
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 14px;
                color: #e6e6e6;
            }
            QPushButton {
                background-color: #232c3b;
                border-radius: 8px;
                padding: 8px 16px;
                font-size: 1em;
                color: #e6e6e6;
            }
            QPushButton:hover {
                background-color: #2a3650;
            }
            QScrollBar:vertical, QScrollBar:horizontal {
                background: #232c3b;
                border-radius: 5px;
            }
        """)
        self.init_ui()

    def change_language(self, lang):
        self.lang = lang
        self.setWindowTitle(TRANSLATIONS[self.lang]["main_title"])
        # Actualizar todos los paneles con el nuevo idioma
        self.settings_panel.change_language(lang)
        self.optimization_panel.change_language(lang)
        # Corrige el nombre del panel de benchmark si es necesario
        if hasattr(self, 'benchmark_visual_page'):
            self.benchmark_visual_page.change_language(lang)
        elif hasattr(self, 'benchmark_panel'):
            self.benchmark_panel.change_language(lang)
        self.side_panel.change_language(lang)
        self.ram_cleaner_panel.change_language(lang)

    def init_ui(self):
        # Layout principal con panel lateral y contenido central
        central_widget = QWidget()
        central_widget.setStyleSheet("background-color: #181f2a;")
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        self.setCentralWidget(central_widget)

        # Panel lateral
        self.side_panel = EnhancedSidePanel(self.logo_path)
        self.side_panel.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        main_layout.addWidget(self.side_panel)

        # Stack de páginas
        self.stack_widget = QStackedWidget()
        self.stack_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        main_layout.addWidget(self.stack_widget, 1)

        # Panel de benchmark visual
        self.benchmark_panel = BenchmarkPanel(lang=self.lang)
        self.benchmark_panel.set_texts()
        self.stack_widget.addWidget(self.benchmark_panel)
        # Panel de optimizaciones
        self.optimization_panel = OptimizationPanel(lang=self.lang)
        self.optimization_panel.set_texts()
        self.stack_widget.addWidget(self.optimization_panel)
        # Panel de liberador de RAM
        self.ram_cleaner_panel = RamCleanerPanel(lang=self.lang)
        self.stack_widget.addWidget(self.ram_cleaner_panel)
        # Panel de configuración
        self.settings_panel = SettingsPanel(lang=self.lang)
        self.stack_widget.addWidget(self.settings_panel)

        # Conectar navegación
        self.side_panel.nav_buttons[0].clicked.connect(lambda: self.stack_widget.setCurrentWidget(self.optimization_panel))
        self.side_panel.nav_buttons[1].clicked.connect(lambda: self.stack_widget.setCurrentWidget(self.ram_cleaner_panel))
        self.side_panel.nav_buttons[2].clicked.connect(lambda: self.stack_widget.setCurrentWidget(self.settings_panel))
        self.side_panel.nav_buttons[3].clicked.connect(lambda: self.stack_widget.setCurrentWidget(self.benchmark_panel))

        # Por defecto, mostrar el panel de optimizaciones
        self.stack_widget.setCurrentWidget(self.optimization_panel)
