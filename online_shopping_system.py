import pickle

EXIT=-1
CUSTOMER=0
ADMIN=1

BLACK=30
RED=31
GREEN=32
PURPLE=34
PURPLE=35

main_menu = {
               1: 'Admin',
               2: 'Customer'
            }

admin_menu = {}
admin_functions = {}

customer_menu = {}
customer_functions = {}

def admin_run():
    a = Admin(1, "admin")

    admin_menu[1] = "View Products"
    admin_functions[1] = a.ViewProducts

    admin_menu[2] = "Add Products"
    admin_functions[2] = a.AddProducts

    admin_menu[3] = "Delete Products"
    admin_functions[3] = a.DelProducts

    admin_menu[4] = "Modify Products"
    admin_functions[4] = a.ModifyProducts
 
    # admin_menu[5] = "Make Shipment"
    # admin_functions[5] = a.MakeShipment
    #
    # admin_menu[6] = "Confirm Delivery"
    # admin_functions[6] = a.ConfirmDelivery

    while(1):
        x = AdminMenuPrint()
        if (EXIT == x):
            break

        admin_functions[x]()


#def customer_run():
#    a = 

main_functions = {
                    1: admin_run
                    #2: customer_run
                 }

products_dict = {}

def cursor_move(x, y):
    print ("\033[{0};{1}H".format(x, y))

def screen_clear():
    print (chr(27) + "[2J")
    cursor_move(0, 0)

def ErrorPrint(msg):
    print ("\033[1;{0}m{1}\033[0m".format(RED, msg), end='')

def SuccessPrint(msg):
    print ("\033[1;{0}m{1}\033[0m".format(GREEN, msg), end='')

def ColorTextPrint(color, msg):
    print ("\033[1;{0}m{1}\033[0m".format(color, msg), end='')

def BoldPrint(msg):
    print ("\033[1;{0}m{1}\033[0m".format(BLACK, msg), end='')

def YesNoGet(question):
    r = input("{0} (y/n) ? ".format(question))
    while(r != "y" and r != "n"):
        ErrorPrint("Invalid Input!!\n")
        r = input("{0} (y/n) ? ".format(question))
    return r

def FloatingPointInputGet(msg):
    f=0.0
    while True:
        try:
            ff = input(msg)
            if ff == "":
                break
            f = float(ff)
            break
        except ValueError:
            ErrorPrint("Only Floating Point values accepted... please try again!!\n")
    return f



class Products:
    def __init__(self, id, name, price, group, subgroup):
        self.id = id
        self.name = name
        self.price = price
        self.group = group
        self.subgroup = subgroup

    def HeadingPrint():
        BoldPrint ("\n|{0:^10}|{1:^15}|{2:^15}|{3:^15}|{4:^15}\n".format("Prod ID", "Name", "Price (Rs.)", "Group", "Subgroup"))

    HeadingPrint = staticmethod(HeadingPrint)

    def Modify(self):
        print ("\nProvide Details (press \"Enter\" to skip.)")
        name = input("Enter product name: ")
        price = FloatingPointInputGet("Enter product's price: ")
        group = input("Enter product group: ")
        subgroup = input("Enter product subgroup: ")
        self.name = name if name != "" else self.name
        self.price = price if price > 0.0 else self.price
        self.group = group if group != "" else self.group
        self.subgroup = subgroup if subgroup != "" else self.subgroup

    def __str__(self):
        return "\033[1;{0}m|{1:^10}|{2:^15}|{3:^15.2f}|{4:^15}|{5:^15}\033[0m".format(PURPLE, self.id,
                                                                                              self.name,
                                                                                              self.price,
                                                                                              self.group,
                                                                                              self.subgroup)

class Admin:
    def __init__(self, id, name):
        "constructor for Admin class"
        self.id = id
        self.name = name

    def ViewProducts(self):
        screen_clear()
        if len(products_dict) == 0:
            ErrorPrint("No products available... Please add some!!\n")
            return

        BoldPrint ("\nAvailable Products:\n")
        Products.HeadingPrint()
        for p in products_dict:
            print (products_dict[p])

    def AddProducts(self):
        while True:
            id = (int)(input("\nEnter product id: "))
            if id in products_dict:
                ErrorPrint("Product ID: {0} already exists!!... please try again\n".format(id))
                continue

            new_product = Products(id, "None", 0.0, "None", "None")

            Products.HeadingPrint()
            print (new_product)
            new_product.Modify()

            products_dict[id] = new_product

            with open("products.txt", "wb") as products_file:
                pickle.dump(products_dict, products_file)

            r = YesNoGet("Add another product")

            if r != "y":
                break

    def DelProducts(self):
        while True:
            id = (int)(input("Enter product id to be deleted: "))
            print ("")
            if id not in products_dict:
                ErrorPrint ("Product ID: {0} doesn't exist!!\n".format(id))
            else:
                Products.HeadingPrint()
                print (products_dict[id])
                print ("")
                r = YesNoGet("Delete this product")
                if(r == "y"):
                    del products_dict[id]

                    with open("products.txt", "wb") as products_file:
                        pickle.dump(products_dict, products_file)

                    SuccessPrint ("Product ID: {0} deleted!!\n".format(id))
                else:
                    ErrorPrint ("Product ID: {0} not deleted!!\n".format(id))

            r = YesNoGet("\nDelete another product")

            if r != "y":
                break

    def ModifyProducts(self):
        while True:
            id = (int)(input("Enter product id to be modified: "))
            print ("")
            if id not in products_dict:
                ErrorPrint ("Product ID: {0} doesn't exist!!\n".format(id))
            else:
                Products.HeadingPrint()
                print (products_dict[id])
                products_dict[id].Modify()

                with open("products.txt", "wb") as products_file:
                    pickle.dump(products_dict, products_file)

            r = YesNoGet("\nModify another product")

            if r != "y":
                break
                

class Customer:
    def __init__(self, id, name, addr, phone):
        "constructor for Admin class"
        self.id = id
        self.name = name
        self.addr = addr
        self.phone = phone



def DictPrintAndInputGet(_dict):
    l = len(_dict)
    for a in sorted(_dict):
        BoldPrint (a)
        print (" : {0}".format(_dict[a]))

    BoldPrint("-1")
    print (": Return")
    print ("==============================================")

    str_x = input(">> ")
    x = 0
    if(str_x == "-1" or str_x.isdigit()):
        x = (int)(str_x)

    while(x != -1 and (1 > x or x > l)):
        ErrorPrint("Invalid Input... Please try again!!\n\n")
        for a in sorted(_dict):
            BoldPrint (a)
            print (" : {0}".format(_dict[a]))

        BoldPrint("-1")
        print (": Return")
        print ("==============================================")

        str_x = input(">> ")
        if(str_x == "-1" or str_x.isdigit()):
            x = (int)(str_x)

    return x


def MainMenuPrint():
    print ("\n==============================================")
    BoldPrint ("Online Shopping System Menu\n")
    print ("==============================================")
    BoldPrint ("Identify yourself?\n")
    return DictPrintAndInputGet(main_menu)

def AdminMenuPrint():
    print ("\n==============================================")
    BoldPrint ("Admin Options\n")
    print ("==============================================")
    return DictPrintAndInputGet(admin_menu)

def ProductsRead():
    try:
        with open("products.txt", "rb") as products_file:
            global products_dict
            products_dict = pickle.load(products_file)

    except FileNotFoundError:
        pass
        

if __name__ == '__main__':
    screen_clear()

    ProductsRead()

    while(1):
        screen_clear()
        x = MainMenuPrint()
        if(EXIT == x):
            break

        screen_clear()
        main_functions[x]()

    screen_clear()
