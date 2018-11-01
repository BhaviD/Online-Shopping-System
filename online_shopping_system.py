import pickle
import getpass
import utilities as utils

EXIT=-1
CUSTOMER=0
ADMIN=1

MAX_ADMIN_COUNT=2

main_menu = {
               1: 'Admin',
               2: 'Customer',
               3: 'Guest'
            }

customer_menu = {}
customer_functions = {}

class Products:
    products_dict = {}

    def __init__(self, id, name = "None", price = 0.0, group = "None", subgroup = "None"):
        self.id = id
        self.name = name
        self.price = price
        self.group = group
        self.subgroup = subgroup
        Products.products_dict[self.id] = self

    def __str__(self):
        return "\033[1;{0}m|{1:^10}|{2:^15}|{3:^15.2f}|{4:^15}|{5:^15}|\033[0m".format(utils.PURPLE,
                                                                                      self.id,
                                                                                      self.name,
                                                                                      self.price,
                                                                                      self.group,
                                                                                      self.subgroup)
                                                                                      #(float)("{:,}".format(self.price)),

    def Read():
        try:
            with open("products.file", "rb") as products_file:
                Products.products_dict = pickle.load(products_file)

        except FileNotFoundError:
            pass

    def HeadingPrint():
        utils.BoldPrint ("\n|{0:^10}|{1:^15}|{2:^15}|{3:^15}|{4:^15}|\n".format("Prod ID",
                                                                                "Name",
                                                                                "Price (Rs.)",
                                                                                "Group",
                                                                                "Subgroup"))

    def Modify(self):
        print ("\nProvide Details (press \"Enter\" to skip.)")
        name = input("Enter product name: ")
        price = utils.FloatingPointInputGet("Enter product's price: ")
        group = input("Enter product group: ")
        subgroup = input("Enter product subgroup: ")
        self.name = name if name != "" else self.name
        self.price = price if price > 0.0 else self.price
        self.group = group if group != "" else self.group
        self.subgroup = subgroup if subgroup != "" else self.subgroup


    HeadingPrint = staticmethod(HeadingPrint)
    Read = staticmethod(Read)


class Admin:
    login_menu = {}
    login_functions = {}

    option_menu = {}
    option_functions = {}

    admin_dict = {}

    def __init__(self, id, name, passwd):
        "constructor for Admin class"
        self.id = id
        self.name = name
        self.passwd = passwd
        Admin.admin_dict[self.id] = self

    def Read():
        try:
            with open("admins.file", "rb") as admins_file:
                Admin.admin_dict = pickle.load(admins_file)

        except FileNotFoundError:
            pass


    def LoginMenuPrint():
        print ("\n==============================================")
        utils.BoldPrint ("Admin Login\n")
        print ("==============================================")
        return utils.DictPrintAndInputGet(Admin.login_menu)


    def OptionMenuPrint():
        print ("\n==============================================")
        utils.BoldPrint ("Admin Options\n")
        print ("==============================================")
        return utils.DictPrintAndInputGet(Admin.option_menu)


    def Run():
        Admin.login_menu[1] = "Login"
        Admin.login_menu[2] = "Register New Admin"

        Admin.login_functions[1] = Admin.Login
        Admin.login_functions[2] = Admin.Register

        Admin.option_menu[1] = "View Products"
        Admin.option_menu[2] = "Add Products"
        Admin.option_menu[3] = "Delete Products"
        Admin.option_menu[4] = "Modify Products"
        #Admin.option_menu[5] = "Make Shipment"
        #Admin.option_menu[6] = "Confirm Delivery"

        Admin.option_functions[1] = Admin.ViewProducts
        Admin.option_functions[2] = Admin.AddProducts
        Admin.option_functions[3] = Admin.DelProducts
        Admin.option_functions[4] = Admin.ModifyProducts
        #Admin.option_functions[5] = Admin.MakeShipment
        #Admin.option_functions[6] = Admin.ConfirmDelivery

        while(True):
            x = Admin.LoginMenuPrint()
            if (EXIT == x):
                break

            utils.ColorTextPrint(utils.BLUE, "\n>> {0} <<\n".format(Admin.login_menu[x]))
            Admin.login_functions[x]()


    def Login():
        if (len(Admin.admin_dict) == 0):
            utils.ErrorPrint("No record of admins... please register a few!!\n")
            return

        id = (int)(input("Enter admin id: "))
        if id not in Admin.admin_dict:
            utils.ErrorPrint("Admin ID: {0} doesn't exist!!... please try again\n".format(id))
            return

        pswd = utils.PasswdInputMatch("Enter password: ", Admin.admin_dict[id].passwd)
        if (pswd == ""):
            return

        while(True):
            x = Admin.OptionMenuPrint()
            if (EXIT == x):
                break

            utils.ColorTextPrint(utils.BLUE, "\n>> {0} <<\n".format(Admin.option_menu[x]))
            Admin.option_functions[x]()


    def Register():
        admin_num = len(Admin.admin_dict)
        if(admin_num == MAX_ADMIN_COUNT):
            utils.ErrorPrint("\nMax number of admins already created!!\n")
            return

        while(True):
            id = (int)(input("Enter Admin id: "))
            if id in Admin.admin_dict:
                utils.ErrorPrint("Admin ID: {0} already exist!!... please try again\n".format(id))
                continue

            name = input("Enter admin name: ")
            pswd = utils.NewPasswdGet("Enter password: ")
            
            Admin(id, name, pswd)       # constructor inserts the new admin object in the dict

            with open("admins.file", "wb") as admins_file:
                pickle.dump(Admin.admin_dict, admins_file)

            utils.SuccessPrint("Admin ID: {0} successfully registered!!\n".format(id))
            break


    def ViewProducts():
        utils.screen_clear()
        if len(Products.products_dict) == 0:
            utils.ErrorPrint("No products available... Please add some!!\n")
            return

        utils.BoldPrint ("\nAvailable Products:\n")
        Products.HeadingPrint()
        for p in Products.products_dict:
            print (Products.products_dict[p])


    def AddProducts():
        while True:
            id = (int)(input("Enter product id: "))
            if id in Products.products_dict:
                utils.ErrorPrint("Product ID: {0} already exists!!... try again.\n".format(id))
                continue

            new_product = Products(id)

            Products.HeadingPrint()
            print (new_product)
            new_product.Modify()

            #Products.products_dict[id] = new_product

            with open("products.file", "wb") as products_file:
                pickle.dump(Products.products_dict, products_file)

            utils.SuccessPrint("Product ID: {0} successfully added!!\n\n".format(id))

            r = utils.YesNoGet("Add another product")

            if r != "y":
                break


    def DelProducts():
        while True:
            id = (int)(input("Enter product id to be deleted: "))
            print ("")
            if id not in Products.products_dict:
                utils.ErrorPrint ("Product ID: {0} doesn't exist!!\n".format(id))
            else:
                Products.HeadingPrint()
                print (Products.products_dict[id])
                print ("")
                r = utils.YesNoGet("Delete this product")
                if(r == "y"):
                    del Products.products_dict[id]

                    with open("products.file", "wb") as products_file:
                        pickle.dump(Products.products_dict, products_file)

                    utils.SuccessPrint ("Product ID: {0} deleted!!\n".format(id))
                else:
                    utils.ErrorPrint ("Product ID: {0} not deleted!!\n".format(id))

            r = utils.YesNoGet("\nDelete another product")

            if r != "y":
                break


    def ModifyProducts():
        while True:
            id = (int)(input("Enter product id to be modified: "))
            print ("")
            if id not in Products.products_dict:
                utils.ErrorPrint ("Product ID: {0} doesn't exist!!\n".format(id))
            else:
                Products.HeadingPrint()
                print (Products.products_dict[id])
                Products.products_dict[id].Modify()

                with open("products.file", "wb") as products_file:
                    pickle.dump(Products.products_dict, products_file)

            r = utils.YesNoGet("\nModify another product")

            if r != "y":
                break

    Read = staticmethod(Read)
    LoginMenuPrint = staticmethod(LoginMenuPrint)
    OptionMenuPrint = staticmethod(OptionMenuPrint)
    Run = staticmethod(Run)
    Login = staticmethod(Login)
    Register = staticmethod(Register)
    ViewProducts = staticmethod(ViewProducts)
    AddProducts = staticmethod(AddProducts)
    DelProducts = staticmethod(DelProducts)
    ModifyProducts = staticmethod(ModifyProducts)



class Cart:
    def __init__(self):
        self.num_of_products = 0
        self.products_price_dict = {}
        self.total_price = 0.0

    def AddProduct(self, prod_id):
        if prod_id in self.products_price_dict:
            utils.ErrorPrint("Product ID {0} already exists in your cart!!\n".format(prod_id))
            return False

        self.products_price_dict[prod_id] = Products.products_dict[prod_id].price
        self.total_price += self.products_price_dict[prod_id]
        utils.SuccessPrint("Product ID {0} added to your cart!!".format(prod_id))
        return True


    def DeleteProduct(self, prod_id):
        if prod_id not in self.products_price_dict:
            utils.ErrorPrint("Product ID {0} doesn't exist in your cart!!\n".format(prod_id))
            return False

        self.total_price -= self.products_price_dict[prod_id]
        del self.products_price_dict[prod_id]
        utils.SuccessPrint("Product ID {0} deleted from your cart!!".format(prod_id))
        return True


    def Print(self):
        if len(self.products_price_dict) == 0:
            utils.ErrorPrint("Your Cart is Empty!!\n")
            return

        Products.HeadingPrint()
        for prod_id in sorted(self.products_price_dict):
            print (Products.products_dict[prod_id])

        utils.BoldPrint ("\nTotal Price: {0:.2f}\n".format(self.total_price))



class Customer:
    login_menu = {}
    login_functions = {}

    option_menu = {}

    customer_dict = {}

    def __init__(self, id, name = "None", addr = "None", phone = "None", passwd = "None"):
        "constructor for Admin class"
        self.id = id
        self.name = name
        self.addr = addr
        self.phone = phone
        self.passwd = passwd
        self.products_bought_dict = {}
        self.cart = Cart()
        Customer.customer_dict[self.id] = self

        self.option_functions = {}
        self.option_functions[1] = Admin.ViewProducts
        self.option_functions[2] = self.MakePayment
        self.option_functions[3] = self.AddToCart
        self.option_functions[4] = self.DeleteFromCart
        self.option_functions[5] = self.ViewCart


    def __str__(self):
        return "\033[1;{0}m{1:<15}: {2}\n{3:<15}: {4}\n{5:<15}: {6}\n\
                    \r{7:<15}: {8}\033[0m".format(utils.PURPLE,
                                                  "Customer ID", self.id,
                                                  "Name",    self.name,
                                                  "Address", self.addr,
                                                  "Phone",   self.phone)

    def LoginMenuPrint():
        print ("\n==============================================")
        utils.BoldPrint ("Customer Login\n")
        print ("==============================================")
        return utils.DictPrintAndInputGet(Customer.login_menu)


    def OptionMenuPrint():
        print ("\n==============================================")
        utils.BoldPrint ("Customer Options\n")
        print ("==============================================")
        return utils.DictPrintAndInputGet(Customer.option_menu)


    def Run():
        Customer.login_menu[1] = "Login"

        Customer.login_functions[1] = Customer.Login

        Customer.option_menu[1] = "View Products"
        Customer.option_menu[2] = "Make Payment"
        Customer.option_menu[3] = "Add to Cart"
        Customer.option_menu[4] = "Delete from Cart"
        Customer.option_menu[5] = "View Cart"


        while(True):
            x = Customer.LoginMenuPrint()
            if (EXIT == x):
                break

            utils.ColorTextPrint(utils.BLUE, "\n>> {0} <<\n".format(Customer.login_menu[x]))
            Customer.login_functions[x]()


    def Login():
        if (len(Customer.customer_dict) == 0):
            utils.ErrorPrint("No record of customers... please register!!\n")
            return

        id = (int)(input("Enter customer id: "))
        if id not in Customer.customer_dict:
            utils.ErrorPrint("Customer ID: {0} doesn't exist!!... please try again\n".format(id))
            return

        current_customer = Customer.customer_dict[id]
        if ( (current_customer.passwd != "None") and
             (False == utils.PasswdInputMatch("Enter password: ", current_customer.passwd)) ):
            return

        while(True):
            x = Customer.OptionMenuPrint()
            if (EXIT == x):
                break

            utils.ColorTextPrint(utils.BLUE, "\n>> {0} <<\n".format(Customer.option_menu[x]))
            current_customer.option_functions[x]()


    def Modify(self):
        print ("\nProvide Details (press \"Enter\" to skip.)")
        name = input("Enter customer name: ")
        addr = input("Enter customer address: ")
        phone = utils.MobileNumberGet("Enter customer mobile number: ")
        passwd = utils.NewPasswdGet("Enter password: ")

        self.name = name if name != "" else self.name
        self.addr = addr if addr != "" else self.addr
        self.phone = phone if phone != "" else self.phone
        self.passwd = passwd if passwd != "" else self.passwd


    def Read():
        try:
            with open("customer.file", "rb") as customer_file:
                Customer.customer_dict = pickle.load(customer_file)

            Guest.guest_number = len(Customer.customer_dict)

        except FileNotFoundError:
            pass



    def MakePayment(self):
        print("Make Payment")


    def AddToCart(self):
        while True:
            id = (int)(input("Enter product id: "))
            print ("")
            if id not in Products.products_dict:
                utils.ErrorPrint ("Product ID: {0} doesn't exist!!\n".format(id))
            else:
                if True == self.cart.AddProduct(id):
                    with open("customer.file", "wb") as customer_file:
                        pickle.dump(Customer.customer_dict, customer_file)

            r = utils.YesNoGet("\nAdd another product to cart?")

            if r != "y":
                break


    def DeleteFromCart(self):
        while True:
            id = (int)(input("Enter product id: "))
            print ("")
            if id not in Products.products_dict:
                utils.ErrorPrint ("Product ID: {0} doesn't exist!!\n".format(id))
            else:
                if True == self.cart.DeleteProduct(id):
                    with open("customer.file", "wb") as customer_file:
                        pickle.dump(Customer.customer_dict, customer_file)

            r = utils.YesNoGet("\nDelete another product from cart?")

            if r != "y":
                break



    def ViewCart(self):
        self.cart.Print()
        

    Read = staticmethod(Read)



class Guest:
    guest_number = 0
    option_menu = {}
    option_functions = {}

    def Run():
        Guest.guest_number += 1

        Guest.option_menu[1] = "View Products"
        Guest.option_menu[2] = "Get Registered"

        Guest.option_functions[1] = Admin.ViewProducts
        Guest.option_functions[2] = Guest.Register

        while(True):
            x = Guest.OptionMenuPrint()
            if (EXIT == x):
                break

            utils.ColorTextPrint(utils.BLUE, "\n>> {0} <<\n".format(Guest.option_menu[x]))
            Guest.option_functions[x]()


    def OptionMenuPrint():
        print ("\n==============================================")
        utils.BoldPrint ("Guest Options\n")
        print ("==============================================")
        return utils.DictPrintAndInputGet(Guest.option_menu)


    def Register():
        if Guest.guest_number in Customer.customer_dict:
            utils.ErrorPrint("Guest ID {0} is already registered!!\n".format(Guest.guest_number))
            return

        new_customer = Customer(Guest.guest_number)

        print (new_customer)
        new_customer.Modify()

        with open("customer.file", "wb") as customer_file:
            pickle.dump(Customer.customer_dict, customer_file)

        utils.SuccessPrint("Customer ID: {0} successfully added!!\n\n".format(new_customer.id))


    Run = staticmethod(Run)
    OptionMenuPrint = staticmethod(OptionMenuPrint)
    Register = staticmethod(Register)



def MainMenuPrint():
    utils.screen_clear()
    print ("\n==============================================")
    utils.BoldPrint ("Online Shopping System Menu\n")
    print ("==============================================")
    utils.BoldPrint ("Identify yourself?\n")
    return utils.DictPrintAndInputGet(main_menu)


main_functions = {
                    1: Admin.Run,
                    2: Customer.Run,
                    3: Guest.Run
                 }


if __name__ == '__main__':
    utils.screen_clear()

    Admin.Read()
    Products.Read()
    Customer.Read()

    while(1):
        x = MainMenuPrint()
        if(EXIT == x):
            break

        main_functions[x]()

    utils.screen_clear()
