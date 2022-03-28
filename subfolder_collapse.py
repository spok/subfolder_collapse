# Программа для переноса файлов из подпапок в корневую папку
# выполняется переименовывание файлов по маске "имя каталога + имя файла"


from PyQt5.QtWidgets import QPlainTextEdit, QWidget, QLabel, QPushButton, QVBoxLayout, QApplication, \
    QProgressBar, QHBoxLayout
import os
import pathlib
import shutil
import sys


class TextField(QPlainTextEdit):
    def __init__(self, ):
        super().__init__()
        self.path_list = []

    def dragEnterEvent(self, e):
        if e.mimeData().hasUrls():
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e):
        self.path_list = [u.toLocalFile() for u in e.mimeData().urls()]
        # Обработка списка с каталогами с выводом в элемент
        for f in self.path_list:
            for dir in os.walk(f):
                if len(dir[2]) > 0:
                    text = dir[0] + ' ->' + str(len(dir[2])) + '\n'
                    self.insertPlainText(text)


class MyWindow(QWidget):
    """Основной класс программы"""

    def __init__(self):
        # Инициализация родителей
        super().__init__()
        self.label = QLabel('Перетащить мышкой папку в текстовое поле')
        self.label.setAcceptDrops(False)
        self.text = TextField()
        self.text.setAcceptDrops(True)
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        self.hbox = QHBoxLayout()
        self.button = QPushButton('Выполнить')
        self.button.setAcceptDrops(False)
        self.button_clear = QPushButton('Очистить')
        self.button_clear.setAcceptDrops(False)
        self.hbox.addWidget(self.button)
        self.hbox.addWidget(self.button_clear)
        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.label)
        self.vbox.addWidget(self.text)
        self.vbox.addWidget(self.progress_bar)
        self.vbox.addLayout(self.hbox)
        self.setLayout(self.vbox)
        self.button.clicked.connect(self.move_file)
        self.button_clear.clicked.connect(self.clear_text)
        self.total = 0

    def move_file(self):
        if len(self.text.path_list) > 0:
            for path in self.text.path_list:
                count = 0
                total = 0
                # Опредление общего количества файлов
                for dir in os.walk(path):
                    if len(dir[2]) > 0:
                        total += len(dir[2])
                for dir in os.walk(path):
                    if len(dir[2]) > 0:
                        folder_name = pathlib.PureWindowsPath(dir[0]).parts[-1]
                        for i, file in enumerate(dir[2]):
                            # переименование файлов по маске
                            count += 1
                            new_name = folder_name + ' - ' + file
                            os.rename(os.path.join(dir[0], file), os.path.join(dir[0], new_name))
                            # перенос файлов
                            shutil.move(os.path.join(dir[0], new_name), os.path.join(path, new_name))
                            self.progress_bar.setValue(int(count / total * 100))

    def clear_text(self):
        """Очистка текстового поля"""
        self.text.clear()
        self.text.path_list = []


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    window.setWindowTitle('Обработка подпапок папок с файлами')
    window.resize(600, 800)
    window.show()
    sys.exit(app.exec_())
