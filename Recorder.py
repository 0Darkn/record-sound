import sys
import subprocess
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout,
    QFileDialog, QMessageBox
)

class VLCRecorder(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gravador de Som VLC (Qt)")
        self.setGeometry(500, 300, 300, 200)

        self.process = None
        self.output_file = None

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

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

    def start_recording(self):
        self.output_file, _ = QFileDialog.getSaveFileName(
            self,
            "Guardar gravação",
            "",
            "WAV (*.wav)"
        )

        if not self.output_file:
            QMessageBox.warning(self, "Erro", "Nome do ficheiro não selecionado!")
            return

        self.btn_record.setEnabled(False)
        self.btn_stop.setEnabled(True)

        vlc_command = [
            "vlc",
            "dshow://",
            "--sout",
            f"#transcode{{acodec=s16l,channels=2,samplerate=44100}}:"
            f"std{{access=file,mux=wav,dst={self.output_file}}}",
            "--run-time=10",
            "--stop-time=10",
            "vlc://quit"
        ]

        self.process = subprocess.Popen(
            vlc_command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        QMessageBox.information(
            self,
            "Gravação",
            "Gravação iniciada.\nSerá guardada automaticamente após 10 segundos."
        )

    def stop_recording(self):
        if self.process:
            self.process.terminate()
            self.process = None
            QMessageBox.information(self, "Parado", "Gravação terminada e guardada.")
        else:
            QMessageBox.warning(self, "Erro", "Nenhuma gravação em curso.")

        self.btn_record.setEnabled(True)
        self.btn_stop.setEnabled(False)

    def closeEvent(self, event):
        if self.process:
            self.process.terminate()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VLCRecorder()
    window.show()
    sys.exit(app.exec_())
