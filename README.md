
---

## 1️⃣ O que o programa faz (resumo rápido)

O script original:

* Cria uma **janela GUI** **PyQt**
* Usa o **VLC via linha de comandos** para:

  * Gravar som do microfone
  * Guardar num ficheiro `.wav`
* Tem botões:

  * **Gravar**
  * **Parar**
  * **Sair**

---

## 2️⃣ Tecnologias usadas na versão Qt

* **PyQt5** (funciona também em Windows 10)
* `subprocess` para executar o VLC
* `QFileDialog` para escolher o ficheiro
* `QMessageBox` para mensagens

📦 Instalação (se ainda não tiveres):

```bash
pip install pyqt5
```

---


## 4️⃣ Explicação passo a passo

### 🔹 Classe principal

```python
class VLCRecorder(QWidget):
```

* Em Qt, a janela é uma **classe**
* Herdamos de `QWidget`

---

### 🔹 Interface gráfica

```python
QPushButton("Gravar")
QVBoxLayout()
```

* `QVBoxLayout` organiza os botões na vertical
* Cada botão liga a uma função (`clicked.connect`)

---

### 🔹 Escolher ficheiro

```python
QFileDialog.getSaveFileName()
```

* Substitui `filedialog` do Tkinter
* Retorna o caminho escolhido

---

### 🔹 Executar o VLC

```python
subprocess.Popen(vlc_command)
```

* Igual ao Tkinter
* O VLC grava áudio via `dshow://`
* Guarda em WAV

---

### 🔹 Encerrar correctamente

```python
def closeEvent(self, event):
```

* Garante que o VLC é fechado ao sair
* Muito importante em Qt

---

## 5️⃣ Melhorias possíveis (próximos passos)

Posso acrescentar facilmente:

- ✅ Duração configurável (SpinBox)
- ✅ Barra de progresso
- ✅ Escolha do dispositivo de áudio
- ✅ Gravação ilimitada (sem tempo fixo)
- ✅ Logs num ficheiro `.log`
- ✅ Integração com **VLC Python bindings**
