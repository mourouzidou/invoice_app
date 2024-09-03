# Appodeikseis_v2 
### This is a desktop application developed in order to help my family business save time and effort by automating the invoice generation procedures. 
### Problems solved:
* No more calculation mistakes
* Speed up the bill calculations up to 4 times
* Keep track of client orders over time
* Warehouse management such as the storage of available products, prices etc.

Appodeikseis_v2 is a dekstop application designed to streamline and enhance the process of calculating and generating invoices for products and clients. It offers a user-friendly interface with robust features aimed at improving efficiency and accuracy in managing and generating invoices.


How to Use

    Client and Product Entry:
        Enter the client's name and product details (name, amount, and price). If the product exists in the predefined list, the price will auto-populate.

    Calculations and Error Handling:
        Press <Enter> to navigate between fields. The application will handle errors such as missing prices or invalid amounts to ensure data accuracy.

    Invoice Generation:
        Once all entries are complete, generate the invoice in PDF format. The invoice will include all products, quantities, prices, and the total amount, formatted according to the selected locale.

    Data Management:
        Easily manage products and clients through intuitive controls, with upcoming features to reload and edit product details on the fly.

Appodeikseis_v2 is a comprehensive solution for efficient invoice management, ensuring accuracy, and enhancing productivity. Stay tuned for version 3, bringing even more powerful features and improvements!


# Version 2 Changes

- **Raise error** in case price is not given for non-recorded product
- **Raise error** in case user will try to remove a product without having selected one
- **Do not allow characters** other than digits (integers) and (".") in the amount box
- **Navigate through boxes** by pressing `<enter>`
- `pyinstaller --windowed` to not include terminal window (this allows opening multiple dashboards)
- **PDF output** not sorted alphabetically

---

Step1: Select a product from the auto-complete dorp-down menu
       Each product has a default price unless the user sets a new price manually
       
Step2: Click "ΥΠΟΛΟΓΙΣΜΟΣ ΠΟΣΟΥ" button to store the entry and calculate the total price for this product

Step3: Add a new product (this time the product price is specified -optional- and the default price will be overwritten)
       The total price is automatically calculated and displayed in the field "ΤΕΛΙΚΟ ΠΟΣΟ"
       User adds the rest of the products and the quantity per item

Step4: The user can delete a product from the list and the entry will be removed. The price is subtracted from the total price (Optional)

Step5: Click the button "ΑΠΟΘΗΚΕΥΣΗ ΤΙΜΟΛΟΓΙΟΥ" to save the invoice and export it as a pdf in the format ClientName_Today's_Date.pdf

<p align="center">
  <img src="https://github.com/mourouzidou/invoice_app/blob/main/Screenshot%20from%202024-09-03%2013-26-02.png" alt="Enter the Client Name" width="400"/>
  <img src="Screenshot from 2024-09-03 13-26-34.png" alt="" width="400"/>
</p>


<p align="center">
  <img src="Screenshot from 2024-09-03 13-27-01.png" alt="Enter the Client Name" width="400"/>
  <img src="Screenshot from 2024-09-03 13-27-48.png" alt="Another Image" width="400"/>
</p>

<p align="center">
  <img src="Screenshot from 2024-09-03 13-28-09.png" alt="Third Image" width="400"/>
  <img src="Screenshot from 2024-09-03 13-28-22.png" alt="Fourth Image" width="400"/>
</p>

A .pdf file with the client name and the date is exported
<p align="center">
  <img src="Screenshot from 2024-09-03 13-34-58.png" alt="Third Image" width="400"/>
  
</p>




# To Do for Version 3

- **Reload the products** and edit them given the file
- **Use enter** to click and save the price button as well 
- **Create a list** of all clients and choose them from a drop down menu
- **Automatically create** a different directory for each client
 
