import csv
import datetime
import sys
from PyQt5.QtGui import QPdfWriter, QPageSize, QPainter, QFont
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog
from PyQt5.QtCore import Qt, QStringListModel

from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QLabel, QPushButton, QCompleter, QVBoxLayout, QListWidget, \
    QDialog, QMessageBox, QFormLayout, QGroupBox, QTextEdit, QHBoxLayout
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Spacer
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.platypus.para import Paragraph


class MainWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Calculate Total Price")
    def get_stylesheet(self):
        return '''
            QWidget {
                background-color: #e8f4fc; /* Light blueish background color */
            }
            QLabel {
                color: #254e70; /* Dark blue text color */
                font-size: 18px;
            }
            QLineEdit, QTextEdit, QListWidget {
                border: 2px solid #357ca5; /* Dark blueish border color */
                border-radius: 12px;
                padding: 10px;
                font-size: 16px;
                background-color: #f0f8fd; /* Light blueish background color */
            }
            QPushButton {
                background-color: #357ca5; /* Dark blueish button color */
                color: #f5f5f5; /* Light greyish text color */
                border: none;
                border-radius: 12px;
                padding: 10px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #2d6a8a; /* Slightly darker blueish button color on hover */
            }
            QLineEdit:hover, QTextEdit:hover, QListWidget:hover {
                border-color: #417fb0; /* Darker blueish border color on hover */
            }
            QLineEdit:focus, QTextEdit:focus, QListWidget:focus {
                border-color: #357ca5; /* Dark blueish border color on focus */
                background-color: #f5fbff; /* Lighter blueish background color on focus */
            }
            QGroupBox {
                border: 2px solid #357ca5; /* Dark blueish border color */
                border-radius: 12px;
                margin-top: 10px;
            }
            QGroupBox:title {
                subcontrol-origin: margin;
                subcontrol-position: top center;
                padding: 0 3px;
                color: #254e70; /* Dark blue text color */
            }
        '''

    def init_ui(self):
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        form_layout = QFormLayout()

        self.client_name_edit = QLineEdit()
        form_layout.addRow("ΟΝΟΜΑ ΠΕΛΑΤΗ:", self.client_name_edit)

        self.product_name_edit = QLineEdit()
        self.product_name_edit.setPlaceholderText("Εισαγωγή προϊόντος...")
        completer = QCompleter(self.get_product_names())
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        completer.setFilterMode(Qt.MatchContains)
        self.product_name_edit.setCompleter(completer)
        form_layout.addRow("ΠΡΟΪΟΝ:", self.product_name_edit)

        self.amount_edit = QLineEdit()
        self.amount_edit.setPlaceholderText("Εισαγωγή τεμαχίων...")
        form_layout.addRow("ΤΕΜΑΧΙΑ:", self.amount_edit)

        layout.addLayout(form_layout)

        self.calculate_button = QPushButton("ΥΠΟΛΟΓΙΣΜΟΣ ΠΟΣΟΥ")
        self.calculate_button.clicked.connect(self.calculate_total_price)
        layout.addWidget(self.calculate_button)

        group_box = QGroupBox("ΑΠΟΤΕΛΕΣΜΑΤΑ")
        group_box_layout = QVBoxLayout()

        self.output_list = QTextEdit()
        self.output_list.setReadOnly(True)
        group_box_layout.addWidget(self.output_list)

        remove_item_layout = QHBoxLayout()
        self.remove_item_btn = QPushButton("ΑΦΑΙΡΕΣΗ ΠΡΟΪΟΝΤΟΣ")
        self.remove_item_btn.clicked.connect(self.remove_item)
        remove_item_layout.addWidget(self.remove_item_btn)

        self.total_price_label = QLabel("ΤΕΛΙΚΟ ΠΟΣΟ:")
        self.total_price_edit = QLineEdit()
        self.total_price_edit.setReadOnly(True)
        remove_item_layout.addWidget(self.total_price_label)
        remove_item_layout.addWidget(self.total_price_edit)

        group_box_layout.addLayout(remove_item_layout)
        group_box.setLayout(group_box_layout)
        layout.addWidget(group_box)

        self.generate_invoice_btn = QPushButton("ΑΠΟΘΗΚΕΥΣΗ ΤΙΜΟΛΟΓΙΟΥ")
        self.generate_invoice_btn.clicked.connect(self.generate_invoice)
        layout.addWidget(self.generate_invoice_btn)

    def get_product_names(self):
        product_names = []
        with open("UpperCaseProducts - Φύλλο1.csv", "r", encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile, delimiter=",")
            for row in reader:
                product_names.append(row[0])
        return product_names



    def calculate_total_price(self):
        if not self.product_name_edit.text() or not self.amount_edit.text():
            return

        product_name = self.product_name_edit.text()
        amount = int(self.amount_edit.text())

        if not self.price_edit.text():  # price field is empty, use csv to get price
            with open("UpperCaseProducts - Φύλλο1.csv", "r", encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile, delimiter=",")
                for row in reader:
                    if row[0] == product_name:
                        price = float(row[1])
                        break
        else:
            price = float(self.price_edit.text())
            self.price_edit.clear()  # clear field

        total_price = round(price * amount, 2)
        output_text = "{} :  {} x {}  = {}\n".format(product_name, price, amount, total_price)
        self.output_list.addItem(output_text)
        self.total_price += total_price
        self.total_price_edit.setText(str(self.total_price))
        self.total_price_edit.setText(str(self.total_price))

        # clear fields
        self.product_name_edit.clear()
        self.amount_edit.clear()

    def remove_item(self):
        item_id = self.output_list.currentRow()
        item_price = float(self.output_list.item(item_id).text().split("=")[-1])
        self.output_list.takeItem(item_id)
        self.total_price -= item_price

        current_total = round(float(self.total_price_edit.text()) - item_price, 2)
        self.total_price_edit.setText(str(current_total))

    def generate_invoice(self):
        """
        This function generates the invoice and saves it as a PDF.
        """
        products = [self.output_list.item(prod_id).text() for prod_id in range(self.output_list.count())]
        story = []

        try:
            filename = f"{self.client_name_edit.text()}_{datetime.datetime.now().date()}.pdf"
            doc = SimpleDocTemplate(filename, pagesize=letter, rightMargin=0)
            styles = getSampleStyleSheet()

            # Add title
            title_style = ParagraphStyle('Title')
            title_style.size = 8
            title = Paragraph(f"{self.client_name_edit.text()}, {datetime.datetime.now().date()}", title_style)
            story.append(title)

            # Add two empty rows
            story.append(Spacer(1, 20))
            story.append(Spacer(1, 20))

            # Add invoice text, each f-string in a new paragraph
            for product in products:
                # Add an empty line before the product
                story.append(Spacer(1, 4))
                story.append(Paragraph(product, styles['Normal']))
                # Add an empty line after the product
                story.append(Spacer(1, 4))

            # Add the total price with an empty line before it
            story.append(Spacer(1, 20))
            invoice_total_text = f"ΣΥΝΟΛΟ: {self.total_price} EUR\n"
            story.append(Paragraph(invoice_total_text, styles['Normal']))

            doc.build(story)

            # Show success message
            QMessageBox.information(self, "Success", f"PDF file '{filename}' has been created.")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")




if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())