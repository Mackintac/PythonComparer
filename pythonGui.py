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
        self.setWindowTitle("OER Comparer")
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

        self.similar_label = QLabel("0% Similar", self)
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
        url1 = self.url1_input.text()
        url2 = self.url2_input.text()

        first_version_list, second_version_list, ratio, html_diff = comparerBackend.compare_urls(url1, url2)

        self.html_diff_display.setHtml(html_diff)

        if "Error" in first_version_list[0] or "Error" in second_version_list[0]:
            self.similar_label.setText("Error fetching URLs")
        else:
            self.similar_label.setText(f"{ratio}% Similar")

    def showHelp(self):
        help_message = "This is a help message."
        help_message = '''How to use: 

1. Insert the URL of the first page you would like to compare into the text area with the placeholder "Enter URL#1".
2. Insert the URL of the second page you would like to compare (to the first page) into the text area with the placeholder "Enter URL#2".
3. Once both URLs have been provided, click on the "Compare" button near the bottom of the window to begin the process to compare the text contents of the two pages.
4. View your results in the center application window OR open the folder where this program is stored and view the document itself named "diff.html" in a browser (or rename the file in order to save it for later viewing!).
5. Repeat process to compare another set of webpages.

Legend:

Similarity Percentage = A percentage value for how similar the entirety of the two pages are to each other. 
Green Highlights = Added text that is less than 40% similar between pages.
Yellow Highlights = Modified text between pages.
Red Highlights = Removed text that is than 40% similar between pages.'''
        QMessageBox.information(self, "Help", help_message)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
