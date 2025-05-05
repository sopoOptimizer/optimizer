from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame, QSizePolicy
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QPainter, QLinearGradient, QColor
from .custom_widgets import RoundedIconButton
from .translations import TRANSLATIONS

class EnhancedSidePanel(QWidget):
    """
    Panel lateral con logo, navegación y estilos personalizados.
    """
    def __init__(self, logo_path, lang="es", parent=None):
        super().__init__(parent)
        self.logo_path = logo_path
        self.lang = lang
        if not self.logo_path or not QPixmap(self.logo_path):
            self.logo = QPixmap()
        else:
            self.logo = QPixmap(self.logo_path)
        self.setMinimumWidth(250)
        self.setMaximumWidth(300)
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(15, 25, 15, 25)
        main_layout.setSpacing(20)
        # Fondo y color de letra uniforme para todo el panel lateral
        self.setStyleSheet("background-color: #181f2a; color: #e0e7ef;")
        # Panel superior con logo
        top_panel = QWidget()
        top_panel.setStyleSheet("background: transparent; border: none;")
        top_layout = QVBoxLayout(top_panel)
        top_layout.setContentsMargins(0, 0, 0, 0)
        top_layout.setSpacing(15)
        logo_label = QLabel()
        if not self.logo.isNull():
            logo_label.setPixmap(self.logo.scaled(
                180, 180,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            ))
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo_label.setStyleSheet("background: transparent; border: none;")
        top_layout.addWidget(logo_label)
        self.subtitle_label = QLabel()
        self.subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.subtitle_label.setStyleSheet("font-size: 14px; color: #94A3B8; margin-bottom: 10px;")
        self.subtitle_label.setWordWrap(True)
        top_layout.addWidget(self.subtitle_label)
        main_layout.addWidget(top_panel)
        # Separador
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setStyleSheet("background-color: #1E293B; min-height: 2px; margin: 10px 0px;")
        main_layout.addWidget(separator)
        # NAV
        self.nav_label = QLabel()
        self.nav_label.setStyleSheet("color: #64748B; font-size: 13px; font-weight: bold; letter-spacing: 1px; background: transparent;")
        main_layout.addWidget(self.nav_label)
        # Botones de navegación
        self.nav_buttons = []
        self.nav_btn_texts = ["optimization", "ram_cleaner", "settings", "benchmark"]
        self.nav_btn_tooltips = ["optimize_tooltip", "ram_cleaner_tooltip", "settings_tooltip", "benchmark_tooltip"]
        for i in range(4):
            btn = RoundedIconButton("", "")
            btn.setToolTip("")
            btn.setProperty("index", i)
            btn.setStyleSheet("background: #232e40; color: #e0e7ef; font-size: 15px; padding: 8px 0; border-radius: 8px; border: none; margin-bottom: 12px;")
            self.nav_buttons.append(btn)
            main_layout.addWidget(btn)
        main_layout.addStretch(1)
        # Pie de página
        self.version_label = QLabel()
        self.version_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.version_label.setStyleSheet("color: #94a3b8; font-size: 12px; margin-top: 15px; background: transparent;")
        main_layout.addWidget(self.version_label)
        self.copyright_label = QLabel()
        self.copyright_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.copyright_label.setStyleSheet("color: #64748B; font-size: 12px; background: transparent;")
        main_layout.addWidget(self.copyright_label)
        self.set_texts()

    def set_texts(self):
        t = TRANSLATIONS[self.lang]
        try:
            self.nav_label.setText(t["navigation"])
            for i, btn in enumerate(self.nav_buttons):
                btn.setText(t[self.nav_btn_texts[i]])
        except KeyError as e:
            print(f"[ERROR i18n] Falta la clave de traducción: {e} para el idioma {self.lang}")
        self.subtitle_label.setText(t.get("main_title", "Sistema de Optimización Profesional Operativo"))
        self.nav_label.setText(t.get("navigation", "NAVEGACIÓN"))
        nav_btn_labels = [
            t.get("optimization", "Optimizaciones"),
            t.get("ram_cleaner", "Liberador de RAM"),
            t.get("settings", "Configuración"),
            t.get("benchmark", "Benchmark SOPO")
        ]
        nav_btn_tooltips = [
            t.get("optimize_tooltip", "Accede a todas las optimizaciones del sistema"),
            t.get("ram_cleaner_tooltip", "Libera la memoria RAM en caché"),
            t.get("settings_tooltip", "Ajusta la configuración de la app"),
            t.get("benchmark_tooltip", "Visualiza el benchmark en tiempo real")
        ]
        for i, btn in enumerate(self.nav_buttons):
            btn.setText(nav_btn_labels[i])
            btn.setToolTip(nav_btn_tooltips[i])
        self.version_label.setText(t.get("version", "Versión 1.0"))
        self.copyright_label.setText(t.get("copyright", "2025 SOPO - Todos los derechos reservados"))

    def change_language(self, lang):
        self.lang = lang
        self.set_texts()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0, QColor("#0F172A"))
        gradient.setColorAt(1, QColor("#1E293B"))
        painter.fillRect(self.rect(), gradient)
