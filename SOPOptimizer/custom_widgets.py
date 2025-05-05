from PyQt6.QtWidgets import QPushButton, QCheckBox, QGroupBox
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainter, QColor, QPainterPath, QLinearGradient

class RoundedIconButton(QPushButton):
    def __init__(self, icon_name, text="", parent=None):
        super().__init__(text, parent)
        self.icon_name = icon_name
        self.setMinimumHeight(40)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        path = QPainterPath()
        path.addRoundedRect(0, 0, self.width(), self.height(), 10, 10)
        if self.isDown():
            painter.fillPath(path, QColor("#0D1420"))
        elif self.underMouse():
            painter.fillPath(path, QColor("#1E293B"))
        else:
            painter.fillPath(path, QColor("#121A2B"))
        painter.setPen(QColor("white"))
        painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, self.text())

class ModernButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setMinimumHeight(40)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setStyleSheet("""
            QPushButton {
                background-color: #1E293B;
                color: white;
                font-weight: bold;
                border-radius: 8px;
                padding: 10px 15px;
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

class ModernGroupBox(QGroupBox):
    def __init__(self, title, parent=None):
        super().__init__(title, parent)
        self.setStyleSheet("""
            QGroupBox {
                background-color: #1E293B;
                border-radius: 10px;
                border: 1px solid #2D3748;
                margin-top: 20px;
                font-weight: bold;
                color: white;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top center;
                padding: 0 10px;
                background-color: #1E293B;
                color: white;
            }
        """)

class ModernCheckBox(QCheckBox):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setStyleSheet("""
            QCheckBox {
                color: white;
                spacing: 0.5em;
                font-size: 1em;
                padding: 0.6em 0.3em 0.6em 0.3em;
            }
            QCheckBox::indicator {
                width: 1.3em;
                height: 1.3em;
                border-radius: 0.25em;
                border: 1.5px solid #4B5563;
            }
            QCheckBox::indicator:unchecked {
                background-color: #1E293B;
            }
            QCheckBox::indicator:checked {
                background-color: #3B82F6;
                border: 1.5px solid #3B82F6;
                image: url(data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxOCIgaGVpZ2h0PSIxOCIgdmlld0JveD0iMCAwIDI0IDI0IiBmaWxsPSJub25lIiBzdHJva2U9IiNmZmZmZmYiIHN0cm9rZS13aWR0aD0iMyIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIiBzdHJva2UtbGluZWpvaW49InJvdW5kIj48cG9seWxpbmUgcG9pbnRzPSIyMCA2IDkgMTIgMTUgMTggOSI+PC9wb2x5bGluZT48L3N2Zz4=);
            }
            QCheckBox::indicator:hover {
                border: 1.5px solid #3B82F6;
            }
        """)
