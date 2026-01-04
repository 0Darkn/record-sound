import sys
import subprocess
import re
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout,
    QFileDialog, QMessageBox, QComboBox, QLabel
)

class VLCRecorder(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gravador de Som VLC (Qt)")
        self.setGeometry(500, 300, 350, 260)

        self.process = None
        self.output_file = None

        self.init_ui()
        self.load_audio_devices()

    def init_ui(self):
        layout = QVBoxLayout()

        layout.addWidget(QLabel("Dispositivo de Áudio:"))

        self.combo_audio = QComboBox()
        layout.addWidget(self.combo_audio)

        self.btn_refresh = QPushButton("Atualizar dispositivos")
        self.btn_refresh.clicked.connect(self.load_audio_devices)
        layout.addWidget(self.btn_refresh)

        self.btn_record = QPushButton("Gravar")
        self.btn_record.clicked.connect(self.start_recording)
        layout.addWidget(self.btn_record)

        self.btn_stop = QPushButton("Parar")
        self.btn_stop.setEnabled(False)
        self.btn_stop.clicked.connect(self.stop_recording)
        layout.addWidget(self.btn_stop)

        self.btn_exit = QPushButton("Sair")
        self.btn_exit.clicked.connect(self.close)
        layout.addWidget(self.btn_exit)

        self.setLayout(layout)

    # -------------------------------------------------
    # LISTAR DISPOSITIVOS DE ÁUDIO VIA VLC
    # -------------------------------------------------
    def load_audio_devices(self):
        self.combo_audio.clear()

        try:
            cmd = ["vlc", "-vvv", "dshow://"]
            result = subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=5
            )

            devices = set()

            for line in result.stderr.splitlines():
                match = re.search(r"audio device name\s*:\s*(.*)", line)
                if match:
                    devices.add(match.group(1).strip())

            if not devices:
                self.combo_audio.addItem("Dispositivo padrão")
            else:
                for dev in sorted(devices):
                    self.combo_audio.addItem(dev)

        except Exception as e:
            QMessageBox.warning(self, "Erro", f"Erro ao listar dispositivos:\n{e}")
            self.combo_audio.addItem("Dispositivo padrão")

    # -------------------------------------------------
    # INICIAR GRAVAÇÃO
    # -------------------------------------------------
    def start_recording(self):
        self.output_file, _ = QFileDialog.getSaveFileName(
            self, "Guardar gravação", "", "WAV (*.wav)"
        )

        if not self.output_file:
            return

        device = self.combo_audio.currentText()

        audio_option = []
        if device != "Dispositivo padrão":
            audio_option = [f":dshow-adev={device}"]

        vlc_command = [
            "vlc",
            "dshow://",
            *audio_option,
            "--sout",
            f"#transcode{{acodec=s16l,channels=2,samplerate=44100}}:"
            f"std{{access=file,mux=wav,dst={self.output_file}}}",
            "vlc://quit"
        ]

        self.process = subprocess.Popen(
            vlc_command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        self.btn_record.setEnabled(False)
        self.btn_stop.setEnabled(True)

        QMessageBox.information(self, "Gravação", "Gravação iniciada.")

    # -------------------------------------------------
    # PARAR GRAVAÇÃO
    # -------------------------------------------------
    def stop_recording(self):
        if self.process:
            self.process.terminate()
            self.process = None

        self.btn_record.setEnabled(True)
        self.btn_stop.setEnabled(False)

        QMessageBox.information(self, "Parado", "Gravação terminada.")

    # -------------------------------------------------
    # FECHAR APLICAÇÃO
    # -------------------------------------------------
    def closeEvent(self, event):
        if self.process:
            self.process.terminate()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = VLCRecorder()
    win.show()
    sys.exit(app.exec_())
