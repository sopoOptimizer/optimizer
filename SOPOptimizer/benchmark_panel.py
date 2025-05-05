from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QGridLayout, QProgressBar, QTableWidget, QTableWidgetItem, QHeaderView, QGroupBox, QMessageBox, QPushButton
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QColor
from .translations import TRANSLATIONS
import psutil
try:
    import GPUtil
    HAS_GPUTIL = True
except ImportError:
    HAS_GPUTIL = False

class BenchmarkPanel(QWidget):
    def change_language(self, lang):
        self.lang = lang
        self.set_texts()

    def set_texts(self):
        t = TRANSLATIONS[self.lang]
        try:
            self.title.setText(t["benchmark"])
            self.desc.setText(t.get("benchmark_desc", "Panel de benchmark del sistema."))
            self.export_btn.setText(t.get("export_benchmark", "Exportar Benchmark"))
        except KeyError as e:
            print(f"[ERROR i18n] Falta la clave de traducción: {e} para el idioma {self.lang}")

    def __init__(self, lang="es"):
        super().__init__()
        self.lang = lang
        self.setStyleSheet("background-color: #181f2a;")
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(40, 30, 40, 30)
        main_layout.setSpacing(18)

        # Título
        self.title = QLabel()
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title.setStyleSheet("font-size: 20px; color: #60a5fa; font-weight: bold; margin-bottom: 4px;")
        main_layout.addWidget(self.title)

        # Descripción
        self.desc = QLabel()
        self.desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.desc.setStyleSheet("font-size: 13px; color: #94a3b8; margin-bottom: 16px;")
        self.desc.setWordWrap(True)
        main_layout.addWidget(self.desc)

        # Panel de métricas (Grid)
        metrics_layout = QGridLayout()
        metrics_layout.setContentsMargins(0, 0, 0, 0)
        metrics_layout.setHorizontalSpacing(18)
        metrics_layout.setVerticalSpacing(12)

        # CPU
        cpu_text = QLabel("CPU:")
        cpu_text.setStyleSheet("color: #64748b; font-size: 13px; font-weight: 500;")
        self.cpu_label = QLabel()
        self.cpu_label.setStyleSheet("color: #e0e7ef; font-size: 14px;")
        self.cpu_bar = QProgressBar()
        self.cpu_bar.setTextVisible(False)
        self.cpu_bar.setFixedHeight(6)
        self.cpu_bar.setStyleSheet("QProgressBar {height: 6px; border-radius: 3px; background: #232e40;} QProgressBar::chunk {background: #2563eb; border-radius: 3px;}")
        metrics_layout.addWidget(cpu_text, 0, 0)
        metrics_layout.addWidget(self.cpu_label, 0, 1)
        metrics_layout.addWidget(self.cpu_bar, 0, 2)

        # RAM
        ram_text = QLabel("RAM:")
        ram_text.setStyleSheet("color: #64748b; font-size: 13px; font-weight: 500;")
        self.ram_label = QLabel()
        self.ram_label.setStyleSheet("color: #e0e7ef; font-size: 14px;")
        self.ram_bar = QProgressBar()
        self.ram_bar.setTextVisible(False)
        self.ram_bar.setFixedHeight(6)
        self.ram_bar.setStyleSheet("QProgressBar {height: 6px; border-radius: 3px; background: #232e40;} QProgressBar::chunk {background: #2563eb; border-radius: 3px;}")
        metrics_layout.addWidget(ram_text, 1, 0)
        metrics_layout.addWidget(self.ram_label, 1, 1)
        metrics_layout.addWidget(self.ram_bar, 1, 2)

        # GPU
        gpu_text = QLabel("GPU:")
        gpu_text.setStyleSheet("color: #64748b; font-size: 13px; font-weight: 500;")
        self.gpu_label = QLabel()
        self.gpu_label.setStyleSheet("color: #e0e7ef; font-size: 14px;")
        self.gpu_mem_label = QLabel()
        self.gpu_mem_label.setStyleSheet("color: #94a3b8; font-size: 12px;")
        self.gpu_bar = QProgressBar()
        self.gpu_bar.setTextVisible(False)
        self.gpu_bar.setFixedHeight(6)
        self.gpu_bar.setStyleSheet("QProgressBar {height: 6px; border-radius: 3px; background: #232e40;} QProgressBar::chunk {background: #2563eb; border-radius: 3px;}")
        gpu_info_box = QVBoxLayout()
        gpu_info_box.addWidget(self.gpu_label)
        gpu_info_box.addWidget(self.gpu_mem_label)
        metrics_layout.addWidget(gpu_text, 2, 0)
        metrics_layout.addLayout(gpu_info_box, 2, 1)
        metrics_layout.addWidget(self.gpu_bar, 2, 2)

        # Disco
        disk_text = QLabel("Disco:")
        disk_text.setStyleSheet("color: #64748b; font-size: 13px; font-weight: 500;")
        self.disk_label = QLabel()
        self.disk_label.setStyleSheet("color: #e0e7ef; font-size: 14px;")
        self.disk_bar = QProgressBar()
        self.disk_bar.setTextVisible(False)
        self.disk_bar.setFixedHeight(6)
        self.disk_bar.setStyleSheet("QProgressBar {height: 6px; border-radius: 3px; background: #232e40;} QProgressBar::chunk {background: #2563eb; border-radius: 3px;}")
        metrics_layout.addWidget(disk_text, 3, 0)
        metrics_layout.addWidget(self.disk_label, 3, 1)
        metrics_layout.addWidget(self.disk_bar, 3, 2)

        # Red
        net_text = QLabel("Red:")
        net_text.setStyleSheet("color: #64748b; font-size: 13px; font-weight: 500;")
        self.net_label = QLabel()
        self.net_label.setStyleSheet("color: #e0e7ef; font-size: 14px;")
        self.net_bar = QProgressBar()
        self.net_bar.setTextVisible(False)
        self.net_bar.setFixedHeight(6)
        self.net_bar.setStyleSheet("QProgressBar {height: 6px; border-radius: 3px; background: #232e40;} QProgressBar::chunk {background: #2563eb; border-radius: 3px;}")
        metrics_layout.addWidget(net_text, 4, 0)
        metrics_layout.addWidget(self.net_label, 4, 1)
        metrics_layout.addWidget(self.net_bar, 4, 2)

        main_layout.addLayout(metrics_layout)

        # --- TOP 5 PROCESOS CPU Y RAM (MODO TABLA SIMPLE) ---
        proc_title = QLabel("Procesos principales (CPU y RAM)")
        proc_title.setStyleSheet("font-size: 14px; color: #60a5fa; margin-top: 16px; font-weight: bold;")
        main_layout.addWidget(proc_title)

        # Tabla para procesos CPU
        self.proc_cpu_table = QTableWidget()
        self.proc_cpu_table.setColumnCount(2)
        self.proc_cpu_table.setHorizontalHeaderLabels(["Proceso", "CPU %"])
        self.proc_cpu_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.proc_cpu_table.verticalHeader().setVisible(False)
        self.proc_cpu_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.proc_cpu_table.setStyleSheet("""
            QTableWidget {
                background-color: #1e293b;
                border: 1px solid #334155;
                color: #e2e8f0;
            }
            QHeaderView::section {
                background-color: #1e293b;
                padding: 4px;
                border: none;
                color: #94a3b8;
            }
        """)
        main_layout.addWidget(self.proc_cpu_table)

        # Tabla para procesos RAM
        self.proc_ram_table = QTableWidget()
        self.proc_ram_table.setColumnCount(2)
        self.proc_ram_table.setHorizontalHeaderLabels(["Proceso", "RAM MB"])
        self.proc_ram_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.proc_ram_table.verticalHeader().setVisible(False)
        self.proc_ram_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.proc_ram_table.setStyleSheet(self.proc_cpu_table.styleSheet())
        main_layout.addWidget(self.proc_ram_table)

        # Botón para exportar benchmark (ahora al final)
        self.export_btn = QPushButton("")
        self.export_btn.setStyleSheet("""
            QPushButton {
                background-color: #3B82F6;
                color: white;
                font-weight: bold;
                border-radius: 8px;
                padding: 10px 15px;
                margin-top: 15px;
            }
            QPushButton:hover {
                background-color: #2563EB;
            }
            QPushButton:pressed {
                background-color: #1D4ED8;
            }
        """)
        self.export_btn.clicked.connect(self.export_benchmark)
        main_layout.addWidget(self.export_btn)

        # Inicialización de variables para el seguimiento de red y disco
        self.last_net = psutil.net_io_counters()
        self.max_net_sent = 0
        self.max_net_recv = 0
        self.last_disk = psutil.disk_io_counters()

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_stats)
        self.timer.start(1000)
        self.update_stats()

    def update_stats(self):
        cpu = psutil.cpu_percent(interval=None)
        self.cpu_label.setText(f"{cpu:.1f}%")
        self.cpu_bar.setValue(int(cpu))

        mem = psutil.virtual_memory()
        self.ram_label.setText(f"{mem.percent:.1f}%")
        self.ram_bar.setValue(int(mem.percent))

        # GPU info universal (nombre y memoria)
        gpu_name = "No detectada"
        gpu_total = gpu_used = gpu_load = None
        gpu_found = False
        try:
            import wmi
            w = wmi.WMI()
            for gpu in w.Win32_VideoController():
                gpu_name = gpu.Name
                try:
                    gpu_total = round(int(gpu.AdapterRAM) / 1024 / 1024 / 1024, 2)
                except:
                    gpu_total = None
                gpu_found = True
                break
        except Exception:
            pass
        if HAS_GPUTIL:
            gpus = GPUtil.getGPUs()
            if gpus:
                g = gpus[0]
                gpu_name = g.name
                gpu_total = g.memoryTotal
                gpu_used = g.memoryUsed
                gpu_load = g.load * 100
                gpu_found = True
        if gpu_found:
            self.gpu_label.setText(gpu_name)
            if gpu_total is not None:
                if gpu_used is not None:
                    self.gpu_mem_label.setText(f"{gpu_used} MB / {gpu_total} MB")
                else:
                    self.gpu_mem_label.setText(f"Total: {gpu_total} MB")
            else:
                self.gpu_mem_label.setText("")
            if gpu_load is not None:
                self.gpu_bar.setValue(int(gpu_load))
            else:
                self.gpu_bar.setValue(0)
        else:
            self.gpu_label.setText("No detectada")
            self.gpu_mem_label.setText("")
            self.gpu_bar.setValue(0)

        # Red (Network)
        net = psutil.net_io_counters()
        sent = (net.bytes_sent - self.last_net.bytes_sent) / 1024
        recv = (net.bytes_recv - self.last_net.bytes_recv) / 1024
        self.max_net_sent = max(self.max_net_sent, sent)
        self.max_net_recv = max(self.max_net_recv, recv)
        percent_sent = (sent / self.max_net_sent * 100) if self.max_net_sent > 0 else 0
        percent_recv = (recv / self.max_net_recv * 100) if self.max_net_recv > 0 else 0
        self.net_label.setText(f"Enviado: {sent:.1f} KB/s | Recibido: {recv:.1f} KB/s")
        net_bar_value = int(max(percent_sent, percent_recv))
        self.net_bar.setValue(net_bar_value)
        self.last_net = net

        # Disco (Disk)
        disk = psutil.disk_io_counters()
        read = (disk.read_bytes - self.last_disk.read_bytes) / 1024
        write = (disk.write_bytes - self.last_disk.write_bytes) / 1024
        try:
            disk_usage = psutil.disk_usage('/')
            percent_disk = disk_usage.percent
            self.disk_bar.setValue(int(percent_disk))
            self.disk_label.setText(f"{percent_disk}% | Lectura: {read:.1f} KB/s | Escritura: {write:.1f} KB/s")
        except Exception:
            self.disk_bar.setValue(0)
            self.disk_label.setText("No disponible")
        self.last_disk = disk

        # --- TOP 5 PROCESOS CPU Y RAM OPTIMIZADO ---
        try:
            import time
            now = time.time()
            if not hasattr(self, '_last_proc_update') or now - self._last_proc_update > 2:
                self._last_proc_update = now
                for p in psutil.process_iter(['pid']):
                    try:
                        p.cpu_percent(interval=None)
                    except Exception:
                        pass
                time.sleep(0.2)
                cpu_list = []
                for p in psutil.process_iter(['name']):
                    try:
                        name = p.info['name']
                        val = p.cpu_percent(interval=None)
                        if name and 'idle' not in name.lower():
                            cpu_list.append((name, val))
                    except Exception:
                        pass
                cpu_list = sorted(cpu_list, key=lambda x: x[1], reverse=True)
                self._top_cpu = cpu_list[:5]
                ram_list = []
                for p in psutil.process_iter(['name', 'memory_info']):
                    try:
                        name = p.info['name']
                        val = p.info['memory_info'].rss / (1024*1024)
                        ram_list.append((name, val))
                    except Exception:
                        pass
                ram_list = sorted(ram_list, key=lambda x: x[1], reverse=True)
                self._top_ram = ram_list[:5]
            self.proc_cpu_table.setRowCount(len(self._top_cpu))
            for i, (name, cpu_val) in enumerate(self._top_cpu):
                self.proc_cpu_table.setItem(i, 0, QTableWidgetItem(str(name)[:18]))
                self.proc_cpu_table.setItem(i, 1, QTableWidgetItem(f"{cpu_val:.1f}%"))
            self.proc_ram_table.setRowCount(len(self._top_ram))
            for i, (name, ram_val) in enumerate(self._top_ram):
                self.proc_ram_table.setItem(i, 0, QTableWidgetItem(str(name)[:18]))
                self.proc_ram_table.setItem(i, 1, QTableWidgetItem(f"{ram_val:.1f} MB"))
        except Exception:
            self.proc_cpu_table.setRowCount(1)
            self.proc_cpu_table.setItem(0, 0, QTableWidgetItem("No disponible"))
            self.proc_cpu_table.setItem(0, 1, QTableWidgetItem("-"))
            self.proc_ram_table.setRowCount(1)
            self.proc_ram_table.setItem(0, 0, QTableWidgetItem("No disponible"))
            self.proc_ram_table.setItem(0, 1, QTableWidgetItem("-"))

    def export_benchmark(self):
        """Exporta los resultados del benchmark a un archivo TXT en C:\\benchmarkSOPO"""
        import os, platform, datetime, socket
        t = TRANSLATIONS[self.lang]
        
        try:
            # Crear carpeta si no existe
            output_dir = "C:\\benchmarkSOPO"
            os.makedirs(output_dir, exist_ok=True)
            
            # Nombre del archivo con timestamp
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            file_path = os.path.join(output_dir, f"benchmark_{timestamp}.txt")
            
            # Obtener datos del sistema
            cpu_info = f"{platform.processor()} ({psutil.cpu_count()} núcleos)" if hasattr(platform, 'processor') else "No disponible"
            ram_info = f"{round(psutil.virtual_memory().total / (1024**3), 1)}GB" if hasattr(psutil, 'virtual_memory') else "No disponible"
            
            # Obtener info de GPU (si está disponible)
            gpu_info = "No detectada"
            if HAS_GPUTIL:
                try:
                    gpus = GPUtil.getGPUs()
                    gpu_info = ", ".join([f"{g.name} ({g.memoryTotal}MB)" for g in gpus])
                except:
                    pass
            
            # Obtener info de disco
            disk_info = []
            for part in psutil.disk_partitions():
                try:
                    usage = psutil.disk_usage(part.mountpoint)
                    disk_info.append(f"{part.device} ({part.mountpoint}) - {usage.total/(1024**3):.1f}GB total, {usage.percent}% usado")
                except:
                    disk_info.append(f"{part.device} ({part.mountpoint}) - Error al leer")
            
            # Obtener info de red
            net_info = []
            for name, addrs in psutil.net_if_addrs().items():
                for addr in addrs:
                    if addr.family == socket.AF_INET:
                        net_info.append(f"{name}: {addr.address}")
                        break
            
            # Generar contenido del reporte
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(f"=== BENCHMARK SOPO - {timestamp} ===\n\n")
                
                # Sección 1: Especificaciones completas
                f.write("=== ESPECIFICACIONES DEL SISTEMA ===\n")
                f.write(f"[CPU] {cpu_info}\n")
                f.write(f"[RAM] {ram_info}\n")
                f.write(f"[GPU] {gpu_info}\n")
                f.write(f"[OS] {platform.system()} {platform.release()} {platform.version()}\n")
                
                # Info de discos
                f.write("\n[Discos]\n")
                f.write("\n".join(disk_info) + "\n")
                
                # Info de red
                f.write("\n[Red]\n")
                f.write("\n".join(net_info) + "\n\n")
                
                # Sección 2: Uso actual
                f.write("=== USO ACTUAL ===\n")
                cpu_percent = psutil.cpu_percent() if hasattr(psutil, 'cpu_percent') else "N/A"
                ram_percent = psutil.virtual_memory().percent if hasattr(psutil, 'virtual_memory') else "N/A"
                disk_percent = psutil.disk_usage('/').percent if hasattr(psutil, 'disk_usage') else "N/A"
                net_io = psutil.net_io_counters()
                f.write(f"CPU: {cpu_percent}% | RAM: {ram_percent}% | Disco: {disk_percent}%\n")
                f.write(f"Red: Enviando {net_io.bytes_sent/1024:.1f}KB/s | Recibiendo {net_io.bytes_recv/1024:.1f}KB/s\n\n")
                
                # Sección 3: Procesos
                f.write("=== TOP 5 PROCESOS CPU ===\n")
                for i, (name, cpu_val) in enumerate(getattr(self, '_top_cpu', [])):
                    f.write(f"{i+1}. {name} (CPU: {cpu_val:.1f}%)\n")
                
                f.write("\n=== TOP 5 PROCESOS RAM ===\n")
                for i, (name, ram_val) in enumerate(getattr(self, '_top_ram', [])):
                    f.write(f"{i+1}. {name} (RAM: {ram_val:.1f}MB)\n")
            
            QMessageBox.information(self, t.get("benchmark_exported", "Éxito"), 
                                  f"{t.get('benchmark_exported', 'Benchmark exportado a:')}\n{file_path}")
        except Exception as e:
            QMessageBox.critical(self, t.get("benchmark_export_error", "Error"), 
                               f"{t.get('benchmark_export_error', 'Error al exportar benchmark:')}\n{str(e)}")
