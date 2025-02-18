import sys
import comparerBackend
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QTextEdit, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox, QSplitter
from PyQt6.QtCore import Qt

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initializeUI()

    def initializeUI(self):
        self.setGeometry(100, 100, 1200,800)
        self.setWindowTitle("PyQt GUI")
        self.setUpMainWindow()
        self.show()  

    def setUpMainWindow(self):
        layout = QVBoxLayout()

        self.url1_input = QLineEdit(self)
        self.url1_input.setPlaceholderText("Enter URL#1")
        layout.addWidget(self.url1_input)

        self.url2_input = QLineEdit(self)
        self.url2_input.setPlaceholderText("Enter URL#2")
        layout.addWidget(self.url2_input)

        self.html_diff_display = QTextEdit(self)
        self.html_diff_display.setReadOnly(True)
        self.html_diff_display.setStyleSheet("background-color: #f0f0f0; color: #000000")  # Set background color
        layout.addWidget(self.html_diff_display)


        compare_button = QPushButton("Compare", self)
        compare_button.setFixedSize(100, 30)  
        compare_button.clicked.connect(self.compareUrls)
        layout.addWidget(compare_button)

        self.similar_label = QLabel("90% Similar", self)
        layout.addWidget(self.similar_label)

        button_layout = QHBoxLayout()
        
        help_button = QPushButton("Help", self)
        help_button.clicked.connect(self.showHelp)
        button_layout.addWidget(help_button)

        exit_button = QPushButton("Exit", self)
        exit_button.clicked.connect(self.close)
        button_layout.addWidget(exit_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def compareUrls(self):
        # url1 = self.url1_input.text()
        # url2 = self.url2_input.text()
        
        # url1 = 'https://ecampusontario.pressbooks.pub/commbusprofcdn/chapter/the-evolution-of-digital-media/'
        # url2 = 'https://ecampusontario.pressbooks.pub/llsadvcomm/chapter/7-1-the-evolution-of-digital-media/'


        # url1 = 'https://pressbooks.palni.org/writingfordigitalmedia/chapter/best-practices-for-digital-writing-2/' 
        # url2 = 'https://ecampusontario.pressbooks.pub/multimediacomm/chapter/bestpractices-digitalwriting/'

        url1 = 'https://openstax.org/books/concepts-biology/pages/6-1-the-genome'
        url2 = 'https://ecampusontario.pressbooks.pub/personalizedhealthnursing/chapter/genome-cell-cycle/'

        # url1 = 'https://pressbooks.palni.org/writingfordigitalmedia/chapter/best-practices-for-digital-writing-2/' 
        # url2 = 'https://ecampusontario.pressbooks.pub/multimediacomm/chapter/bestpractices-digitalwriting/'

        # url1 = 'https://pressbooks.palni.org/writingfordigitalmedia/chapter/best-practices-for-digital-writing-2/' 
        # url2 = 'https://ecampusontario.pressbooks.pub/multimediacomm/chapter/bestpractices-digitalwriting/'

        first_version_list, second_version_list, ratio, html_diff = comparerBackend.compare_urls(url1, url2)

        self.html_diff_display.setHtml(html_diff)
        
        print(ratio)
        self.similar_label.setText(str(ratio))

    def showHelp(self):
        help_message = "This is a help message."
        QMessageBox.information(self, "Help", help_message)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
