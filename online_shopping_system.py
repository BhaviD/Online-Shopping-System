import pickle
import getpass
import utilities as utils

EXIT=-1
CUSTOMER=0
ADMIN=1

main_menu = {
               1: 'Admin',
               2: 'Customer',
               3: 'Guest'
            }

customer_menu = {}
customer_functions = {}

class Products:
    products_dict = {}

    def __init__(self, id, name, price, group, subgroup):
        self.id = id
        self.name = name
        self.price = price
        self.group = group
        self.subgroup = subgroup

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

    def __str__(self):
        return "\033[1;{0}m|{1:^10}|{2:^15}|{3:^15.2f}|{4:^15}|{5:^15}|\033[0m".format(utils.PURPLE,
                                                                                      self.id,
                                                                                      self.name,
                                                                                      self.price,
                                                                                      self.group,
                                                                                      self.subgroup)

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
        return DictPrintAndInputGet(Admin.login_menu)


    def OptionMenuPrint():
        print ("\n==============================================")
        utils.BoldPrint ("Admin Options\n")
        print ("==============================================")
        return DictPrintAndInputGet(Admin.option_menu)


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

            utils.ColorTextPrint(utils.BLUE, "\n>> {0} <<".format(Admin.login_menu[x]))
            Admin.login_functions[x]()


    def Login():
        if (len(Admin.admin_dict) == 0):
            utils.ErrorPrint("No record of admins... please register a few!!\n")
            return

        id = (int)(input("\nEnter admin id: "))
        if id not in Admin.admin_dict:
            utils.ErrorPrint("Admin ID: {0} doesn't exist!!... please try again\n".format(id))
            return

        try_count = 1
        max_try_count = 3
        pswd = getpass.getpass("Enter password: ")
        while (pswd != Admin.admin_dict[id].passwd):
            try_count += 1
            if (try_count > max_try_count):
                utils.ErrorPrint ("Max number of tries reached!!\n")
                break
            utils.ErrorPrint("Incorrect Password... please try again!!\n")
            pswd = getpass.getpass("Enter password: ")

        if(try_count > max_try_count):
            return

        while(True):
            x = Admin.OptionMenuPrint()
            if (EXIT == x):
                break

            utils.ColorTextPrint(utils.BLUE, "\n>> {0} <<".format(Admin.option_menu[x]))
            Admin.option_functions[x]()


    def Register():
        admin_num = len(Admin.admin_dict)
        if(admin_num == MAX_ADMIN_COUNT):
            utils.ErrorPrint("Max number of admins already created!!\n")
            return

        while(True):
            id = (int)(input("\nEnter Admin id: "))
            if id in Admin.admin_dict:
                utils.ErrorPrint("Admin ID: {0} already exist!!... please try again\n".format(id))
                continue

            name = input("Enter admin name: ")
            pswd = getpass.getpass("Enter password: ")
            while (len(pswd) < 8):
                utils.ErrorPrint("Minimum length of password should be 8... please try again!!\n")
                pswd = getpass.getpass("Enter password:")

            Admin.admin_dict[id] = Admin(id, name, pswd)

            with open("admins.file", "ab") as admins_file:
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
            id = (int)(input("\nEnter product id: "))
            if id in Products.products_dict:
                utils.ErrorPrint("Product ID: {0} already exists!!... try again.\n".format(id))
                continue

            new_product = Products(id, "None", 0.0, "None", "None")

            Products.HeadingPrint()
            print (new_product)
            new_product.Modify()

            Products.products_dict[id] = new_product

            with open("products.file", "wb") as products_file:
                pickle.dump(Products.products_dict, products_file)

            utils.SuccessPrint("Product ID: {0} successfully added!!\n\n".format(id))

            r = utils.YesNoGet("Add another product")

            if r != "y":
                break


    def DelProducts():
        while True:
            id = (int)(input("\nEnter product id to be deleted: "))
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
            id = (int)(input("\nEnter product id to be modified: "))
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

    Run = staticmethod(Run)
    Login = staticmethod(Login)
    Register = staticmethod(Register)
    ViewProducts = staticmethod(ViewProducts)
    AddProducts = staticmethod(AddProducts)
    DelProducts = staticmethod(DelProducts)
    ModifyProducts = staticmethod(ModifyProducts)



class Customer:
    def __init__(self, id, name, addr, phone):
        "constructor for Admin class"
        self.id = id
        self.name = name
        self.addr = addr
        self.phone = phone

class Guest:
    guest_number = 0
    option_menu = {}
    option_functions = {}

    def __init__(self):
        Guest.guest_number += 1
        self.guest_number = Guest.guest_number


    def Run():
        Guest.option_menu[1] = "View Products"
        Guest.option_menu[2] = "Get Registered"

        Guest.option_functions[1] = Admin.ViewProducts
        Guest.option_functions[2] = Guest.Register

        while(True):
            x = Guest.OptionMenuPrint()
            if (EXIT == x):
                break

            utils.ColorTextPrint(utils.BLUE, "\n>> {0} <<".format(Guest.option_menu[x]))
            Guest.option_functions[x]()


    def OptionMenuPrint():
        print ("\n==============================================")
        utils.BoldPrint ("Guest Options\n")
        print ("==============================================")
        return DictPrintAndInputGet(Guest.option_menu)


    def Register():
        


def DictPrintAndInputGet(_dict):
    l = len(_dict)
    for a in sorted(_dict):
        utils.BoldPrint (a)
        print (" : {0}".format(_dict[a]))

    utils.BoldPrint("-1")
    print (": Return")
    print ("==============================================")

    str_x = input(">> ")
    x = 0
    if(str_x == "-1" or str_x.isdigit()):
        x = (int)(str_x)

    while(x != -1 and (1 > x or x > l)):
        utils.ErrorPrint("Invalid Input... Please try again!!\n\n")
        for a in sorted(_dict):
            utils.BoldPrint (a)
            print (" : {0}".format(_dict[a]))

        utils.BoldPrint("-1")
        print (": Return")
        print ("==============================================")

        str_x = input(">> ")
        if(str_x == "-1" or str_x.isdigit()):
            x = (int)(str_x)

    return x


def MainMenuPrint():
    utils.screen_clear()
    print ("\n==============================================")
    utils.BoldPrint ("Online Shopping System Menu\n")
    print ("==============================================")
    utils.BoldPrint ("Identify yourself?\n")
    return DictPrintAndInputGet(main_menu)


main_functions = {
                    1: Admin.Run,
                    3: Guest.Run
                    #2: customer_run
                 }


if __name__ == '__main__':
    utils.screen_clear()

    Admin.Read()
    Products.Read()

    while(1):
        x = MainMenuPrint()
        if(EXIT == x):
            break

        main_functions[x]()

    utils.screen_clear()
