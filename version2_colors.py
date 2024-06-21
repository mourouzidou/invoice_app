import csv
import datetime
import sys
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
import locale
from PyQt5.QtGui import QDoubleValidator
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
                background-color: #9cd9d8; /* Light blueish background color */
            }
            QLabel {
                color: #080808; /* Dark blue text color */
                font-size: 26px;
                font-weight: bold;
            }
            QLineEdit, QListWidget {
                border: 2px solid #080808; /* Dark blueish border color */
                border-radius: 12px;
                padding: 14px;
                font-size: 24px;
                background-color: #f7ffe6; /* Light blueish background color */
            }
            QPushButton {
                background-color: #cedead; /* Dark blueish button color */
                color: #080808; /* Light greyish text color */
                border: none;
                border-radius: 12px;
                padding: 18px;
                font-size: 24px;
            }
            QPushButton:hover {
                background-color:  	#84d19a; /* Slightly darker blueish button color on hover */
            }
            QLineEdit:hover, QListWidget:hover {
                border-color: #417fb0; /* Darker blueish border color on hover */
            }
            QLineEdit:focus, QListWidget:focus {
                border-color: #357ca5; /* Dark blueish border color on focus */
                background-color: #f5fbff; /* Lighter blueish background color on focus */
            }
        ''')

        doubles_validator = QDoubleValidator(self)
        doubles_validator.setDecimals(6)

        self.client_label = QLabel("ΟΝΟΜΑ ΠΕΛΑΤΗ")
        self.client_name_edit = QLineEdit()
        self.product_name_label = QLabel("ΠΡΟΪΌΝ")
        self.product_name_edit = QLineEdit()
        self.amount_label = QLabel("ΤΕΜΑΧΙΑ")
        self.amount_edit = QLineEdit()

        self.price_label = QLabel("ΤΙΜΗ ΤΕΜΑΧΙΟΥ")
        self.price_edit = QLineEdit()
        self.price_edit.setValidator(doubles_validator)
        self.amount_edit.setValidator(doubles_validator)
        self.price_edit.returnPressed.connect(self.calculate_total_price)
        self.amount_edit.returnPressed.connect(self.handle_amount_entered)

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
        self.output_list.setMinimumHeight(240)
        self.setLayout(self.layout)

        # Create a list of product names
        product_names = []
        with open("products_prices.csv", "r", encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile, delimiter=",")
            for row in reader:
                product_names.append(row[0])

        # Create an autocompleter with the list of product names
        self.completer = QCompleter(product_names)
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.completer.setFilterMode(Qt.MatchContains)
        self.product_name_edit.setCompleter(self.completer)


    def keyPressEvent(self, event):
        if event.key() in (Qt.Key_Return, Qt.Key_Enter):
            self.focusNextChild()
        else:
            super().keyPressEvent(event)


    def handle_amount_entered(self):
        # If the price edit is empty, try to fetch the price from the CSV
        if not self.price_edit.text():
            product_name = self.product_name_edit.text()
            price = None
            with open("products_prices.csv", "r", encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile, delimiter=",")
                for row in reader:
                    if row[0] == product_name:
                        price = float(row[1])
                        break
            if price is not None:
                self.price_edit.setText(str(price))
                self.calculate_total_price()
            else:
                self.price_edit.setFocus()
        else:
            self.calculate_total_price()


    def calculate_total_price(self):
        try:
            product_name = self.product_name_edit.text()
            amount_text = self.amount_edit.text()
            price_text = self.price_edit.text()

            if not product_name or not amount_text:
                QMessageBox.warning(self, "Invalid Input", "Product name and amount must be provided.")
                return

            # Validate the amount input
            try:
                amount = int(amount_text)
            except ValueError:
                QMessageBox.warning(self, "Invalid Input", "Amount must be a valid integer.")
                self.amount_edit.clear()
                return

            price = None
            # Validate the price input
            try:
                if not price_text:
                    with open("products_prices.csv", "r", encoding='utf-8') as csvfile:
                        reader = csv.reader(csvfile, delimiter=",")
                        for row in reader:
                            if row[0] == product_name:
                                price = float(row[1])
                                break
                    if price is None:
                        QMessageBox.warning(self, "Invalid Input", "Price must be provided for new products.")
                        return
                else:
                    price = float(price_text)
            except ValueError:
                QMessageBox.warning(self, "Invalid Input", "Price must be a valid number.")
                self.price_edit.clear()
                return

            total_price = round(price * amount, 2)
            output_text = "{} :  {} x {}  = {}\n".format(product_name, amount, price, total_price)
            self.output_list.addItem(output_text)
            self.total_price += total_price
            self.total_price_edit.setText(str(self.total_price))

            # Clear fields
            self.product_name_edit.clear()
            self.amount_edit.clear()
            self.price_edit.clear()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"An unexpected error occurred: {str(e)}")


    def remove_item(self):
        item_id = self.output_list.currentRow()
        if item_id == -1:  # No item selected
            QMessageBox.warning(self, "Invalid Action", "Please select an item to remove.")
            return

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
            # products.sort()

            # Populate the table data
            for product in products:
                parts = product.split("=")
                product_name = parts[0].split(":")[0].strip()
                amount, price = parts[0].split(":")[1].strip().split("x")
                total_price = parts[1].strip()
                table_data.append([product_name, amount, locale.format("%.2f", float(price), grouping=True),
                                   locale.format("%.2f", float(total_price), grouping=True)])

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