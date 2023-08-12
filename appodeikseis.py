import csv
import datetime
import sys
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
import locale
from reportlab.lib.pagesizes import landscape, portrait, A4


from PyQt5.QtGui import QPdfWriter, QPageSize, QPainter, QFont
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog
from PyQt5.QtCore import Qt, QStringListModel

from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QLabel, QPushButton, QCompleter, QVBoxLayout, QListWidget, \
    QDialog, QMessageBox
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Spacer
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.platypus.para import Paragraph


class MainWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Calculate Total Price")
        self.setStyleSheet('''
            QWidget {
                background-color: #e8f4fc; /* Light blueish background color */
            }
            QLabel {
                color: #254e70; /* Dark blue text color */
                font-size: 26px;
                font-weight: bold;
            }
            QLineEdit, QListWidget {
                border: 2px solid #357ca5; /* Dark blueish border color */
                border-radius: 12px;
                padding: 14px;
                font-size: 24px;
                background-color: #f0f8fd; /* Light blueish background color */
            }
            QPushButton {
                background-color: #357ca5; /* Dark blueish button color */
                color: #f5f5f5; /* Light greyish text color */
                border: none;
                border-radius: 12px;
                padding: 18px;
                font-size: 24px;
            }
            QPushButton:hover {
                background-color: #2d6a8a; /* Slightly darker blueish button color on hover */
            }
            QLineEdit:hover, QListWidget:hover {
                border-color: #417fb0; /* Darker blueish border color on hover */
            }
            QLineEdit:focus, QListWidget:focus {
                border-color: #357ca5; /* Dark blueish border color on focus */
                background-color: #f5fbff; /* Lighter blueish background color on focus */
            }
        ''')

        self.client_label = QLabel("ΟΝΟΜΑ ΠΕΛΑΤΗ")
        self.client_name_edit = QLineEdit()
        self.product_name_label = QLabel("ΠΡΟΪΌΝ")
        self.product_name_edit = QLineEdit()
        self.amount_label = QLabel("ΤΕΜΑΧΙΑ")
        self.amount_edit = QLineEdit()

        self.price_label = QLabel("ΤΙΜΗ ΤΕΜΑΧΙΟΥ")
        self.price_edit = QLineEdit()

        self.remove_item_btn = QPushButton("ΑΦΑΙΡΕΣΗ ΠΡΟΙΟΝΤΟΣ")
        self.remove_item_btn.clicked.connect(self.remove_item)

        self.calculate_button = QPushButton("ΥΠΟΛΟΓΙΣΜΟΣ ΠΟΣΟΥ")
        self.output_list = QListWidget()
        self.total_price = 0
        self.total_price_label = QLabel("ΤΕΛΙΚΟ ΠΟΣΟ")
        self.total_price_edit = QLineEdit()
        self.generate_invoice_btn = QPushButton("ΑΠΟΘΗΚΕΥΣΗ ΤΙΜΟΛΟΓΙΟΥ")
        self.generate_invoice_btn.clicked.connect(self.generate_invoice)

        # LAYOUT
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.client_label)
        self.layout.addWidget(self.client_name_edit)
        self.layout.addWidget(self.product_name_label)
        self.layout.addWidget(self.product_name_edit)
        self.layout.addWidget(self.amount_label)
        self.layout.addWidget(self.amount_edit)
        self.layout.addWidget(self.price_label)
        self.layout.addWidget(self.price_edit)
        self.layout.addWidget(self.calculate_button)
        self.layout.addWidget(self.output_list)
        self.layout.addWidget(self.remove_item_btn)
        self.layout.addWidget(self.total_price_label)
        self.layout.addWidget(self.total_price_edit)
        self.layout.addWidget(self.generate_invoice_btn)

        self.calculate_button.clicked.connect(self.calculate_total_price)

        self.setLayout(self.layout)

        # Create a list of product names
        product_names = []
        with open("UpperCaseProducts - Φύλλο1.csv", "r", encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile, delimiter=",")
            for row in reader:
                product_names.append(row[0])

        # Create an autocompleter with the list of product names
        self.completer = QCompleter(product_names)
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.completer.setFilterMode(Qt.MatchContains)
        self.product_name_edit.setCompleter(self.completer)

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
        output_text = "{} :  {} x {}  = {}\n".format(product_name, amount, price, total_price)
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
        # Set the locale to Greek format with EUR currency
        locale.setlocale(locale.LC_ALL, ('el_GR', 'UTF-8'))

        products = [self.output_list.item(prod_id).text() for prod_id in range(self.output_list.count())]
        story = []

        try:
            filename = f"{self.client_name_edit.text()}_{datetime.datetime.now().date()}.pdf"
            doc = SimpleDocTemplate(filename, pagesize=portrait(A4))
            styles = getSampleStyleSheet()

            # Add title
            title_style = ParagraphStyle('Title')
            title_style.size = 17
            title_style.fontName = 'Helvetica-Bold'  # Make the title bold
            title = Paragraph(f"{self.client_name_edit.text()}, {datetime.datetime.now().date()}", title_style)
            story.append(title)

            # Add two empty rows
            story.append(Spacer(1, 20))

            # Create a list to hold the data for the table
            table_data = [['ΠΡΟΙΟΝ', 'ΤΕΜΑΧΙΑ', 'ΤΙΜΗ ΤΜΧ', 'ΣΥΝΟΛΙΚΗ ΤΙΜΗ']]
            products.sort()

            # Populate the table data
            for product in products:
                parts = product.split("=")
                product_name = parts[0].split(":")[0].strip()
                amount, price = parts[0].split(":")[1].strip().split("x")
                total_price = parts[1].strip()
                table_data.append([product_name, amount, locale.format("%.2f", float(price), grouping=True), locale.format("%.2f", float(total_price), grouping=True)])

            # Add a separator row
            table_data.append(['', '', '', ''])

            # Add the total invoice row
            total_price_text = f"ΣΥΝΟΛΟ: {locale.currency(self.total_price, grouping=True)}"
            table_data.append(['', '', '', total_price_text])

            # Create the table
            table = Table(table_data, colWidths=[200, 100, 100, 100])  # Adjust the colWidths as needed
            table_style = TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.black),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('ALIGN', (0, 0), (0, -1), 'LEFT'),  # Align "Product" column to the left
                ('ALIGN', (1, 0), (-1, -1), 'CENTER'),  # Align other columns to the center
            ])
            table.setStyle(table_style)

            story.append(table)

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





if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())