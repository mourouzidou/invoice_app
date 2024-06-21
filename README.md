Appodeikseis_v2 is an advanced application designed to streamline and enhance the process of calculating and generating invoices for products and clients. It offers a user-friendly interface with robust features aimed at improving efficiency and accuracy in managing invoices.



How to Use

    Client and Product Entry:
        Enter the client's name and product details (name, amount, and price). If the product exists in the predefined list, the price will auto-populate.

    Calculations and Error Handling:
        Press <Enter> to navigate between fields. The application will handle errors such as missing prices or invalid amounts to ensure data accuracy.

    Invoice Generation:
        Once all entries are complete, generate the invoice in PDF format. The invoice will include all products, quantities, prices, and the total amount, formatted according to the selected locale.

    Data Management:
        Easily manage products and clients through intuitive controls, with upcoming features to reload and edit product details on the fly.

Appodeikseis_v2 is your comprehensive solution for efficient invoice management, ensuring accuracy, and enhancing productivity. Stay tuned for version 3, bringing even more powerful features and improvements!


# Version 2 Changes

- **Raise error** in case price is not given for non-recorded product
- **Raise error** in case user will try to remove a product without having selected one
- **Do not allow characters** other than digits (integers) and (".") in the amount box
- **Navigate through boxes** by pressing `<enter>`
- `pyinstaller --windowed` to not include terminal window (this allows opening multiple dashboards)
- **PDF output** not sorted alphabetically

---

# To Do for Version 3

- **Reload the products** and edit them given the file
- **Use enter** to click and save the price button as well 
- **Create a list** of all clients and choose them from a drop down menu
- **Automatically create** a different directory for each client

 
