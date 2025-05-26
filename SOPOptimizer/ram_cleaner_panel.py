from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox
from PyQt6.QtCore import Qt
import subprocess
import os
from .translations import TRANSLATIONS

class RamCleanerPanel(QWidget):
    def __init__(self, lang="es"):
        super().__init__()
        self.lang = lang
        self.setStyleSheet("background-color: #181f2a;")
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.title = QLabel(TRANSLATIONS[self.lang]["ram_cleaner"])
        self.title.setStyleSheet("font-size: 22px; font-weight: bold; color: #60a5fa; margin-bottom: 12px;")
        layout.addWidget(self.title)
        self.desc = QLabel(TRANSLATIONS[self.lang].get("ram_cleaner_desc", "Libera la memoria RAM en caché para mejorar el rendimiento del sistema."))
        self.desc.setStyleSheet("font-size: 15px; color: #e0e7ef; margin-bottom: 18px;")
        self.desc.setWordWrap(True)
        layout.addWidget(self.desc)
        self.clean_btn = QPushButton(TRANSLATIONS[self.lang].get("clean_ram_now", "Liberar RAM ahora"))
        self.clean_btn.setStyleSheet("font-size: 18px; background: #2563eb; color: white; padding: 10px 0; border-radius: 8px;")
        self.clean_btn.clicked.connect(self.free_ram)
        layout.addWidget(self.clean_btn)

    def change_language(self, lang):
        self.lang = lang
        t = TRANSLATIONS[self.lang]
        try:
            self.title.setText(t["ram_cleaner"])
            self.desc.setText(t.get("ram_cleaner_desc", "Libera la memoria RAM en caché para mejorar el rendimiento del sistema."))
            self.clean_btn.setText(t.get("clean_ram_now", "Liberar RAM ahora"))
        except KeyError as e:
            print(f"[ERROR i18n] Falta la clave de traducción: {e} para el idioma {self.lang}")

    def free_ram(self):
        # Ruta al ejecutable de RAMMap
        def resource_path(relative_path):
            import sys, os
            if hasattr(sys, '_MEIPASS'):
                return os.path.join(sys._MEIPASS, relative_path)
            return os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', relative_path)

        rammap_path = resource_path(os.path.join('RAMMap', 'RAMMap.exe'))
        if not os.path.exists(rammap_path):
            QMessageBox.warning(self, "Error", f"No se encontró RAMMap.exe en: {rammap_path}\nPor favor, descárgalo y colócalo en la carpeta RAMMap.")
            return
        try:
            subprocess.run([rammap_path, "-Et"], check=True)
            QMessageBox.information(self, "Liberación de RAM", "La memoria caché del sistema ha sido liberada usando RAMMap.")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"No se pudo ejecutar RAMMap: {e}")
