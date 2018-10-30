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

    # admin_menu[4] = "Modify Products"
    # admin_functions[4] = a.ModifyProducts
    #
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

class Products:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __str__(self):
        return "\033[1;{0}mProduct ID: {1}, Name: {2}\033[0m".format(PURPLE, self.id, self.name)


class Admin:
    def __init__(self, id, name):
        "constructor for Admin class"
        self.id = id
        self.name = name

    def ViewProducts(self):
        if len(products_dict) == 0:
            ErrorPrint("No products available... Please add some!!\n")
            return

        BoldPrint ("\nAvailable Products:\n")
        for p in products_dict:
            print (products_dict[p])

    def AddProducts(self):
        while True:
            id = (int)(input("\nEnter product id: "))
            if id in products_dict:
                ErrorPrint("Product ID: {0} already exists!!... please try again\n".format(id))
                continue
            name = input("Enter product name: ")
            products_dict[id] = Products(id, name)

            with open("products.txt", "a") as products_file:
                products_file.write("{0} {1}\n".format(id, name))

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
                print (products_dict[id])
                r = YesNoGet("Delete above product")
                if(r == "y"):
                    del products_dict[id]

                    with open("products.txt", "w") as products_file:
                        for p in products_dict:
                            products_file.write("{0} {1}\n".format(p, products_dict[p].name))

                    SuccessPrint ("Product ID: {0} deleted!!\n".format(id))
                else:
                    ErrorPrint ("Product ID: {0} not deleted!!\n".format(id))

            r = YesNoGet("\nDelete another product")

            if r != "y":
                break


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
        with open("products.txt", "r") as products_file:
            for line in products_file:
                info = line.split()
                products_dict[(int)(info[0])] = Products((int)(info[0]), info[1])
    except FileNotFoundError:
        pass
        

if __name__ == '__main__':
    screen_clear()

    ProductsRead()

    while(1):
        x = MainMenuPrint()
        if(EXIT == x):
            break

        main_functions[x]()
