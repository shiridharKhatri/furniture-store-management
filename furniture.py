"""
Plannings ::
First : display the details option to customer like
        1. Show available furniture with its details
        2. Purchase furniture
        3. Order furniture
        4. Exit
Second : If user clicks 2 then it should show them a available furniture details by reading furnitureName.txt file
"""

filePath = "coursework-real/furnitureName.txt"

# Function to retrieve furniture details from file
def furnitureDetails():
    try:
        file = open(filePath, 'r')  # Open file in read mode
        names = []
        # Reading each line and extracting details
        for data in file:
            # Splitting each line by comma and creating a dictionary for each furniture
            splitData = data.split(",")
            names.append({
                "id": splitData[0],
                "companyName": splitData[1],
                "furnitureName": splitData[2],
                "qty": splitData[3],
                "price": splitData[4]
            })
        return names  # Return list of dictionaries containing furniture details
    except FileNotFoundError:
        print("File not found!! ")

# Function to display furniture details
def furnitureDisplay():
    print(f"{'='*75}")
    print(f"| {'ID':^3} | {'Company':^30} | {'Furniture':^15} | {'Stock':^7} | {'Price':^5}")
    print(f"{'='*75}")
    for elements in furnitureDetails():
        # Formatting and printing each furniture's details
        print(f"| {elements['id']:^3} | {elements['companyName']:^30} | {elements['furnitureName']:^15} | {elements['qty']:^7} | {elements['price']}", end='')
    print(f"{'='*75}")

# Function to update the file after purchase
def updateFile(selectedFurniture, quantity):
    try:
        with open(filePath, 'r') as file:
            fileData = file.readlines()  # Reading all lines of file into list
    except FileNotFoundError:
        print("File not found")
    content = fileData[int(selectedFurniture[0]['id']) - 1].split(',')
    content[3] = str(float(selectedFurniture[0]['availableQty']) - quantity)  # Updating quantity in selected furniture
    fileData[int(selectedFurniture[0]['id']) - 1] = ",".join(content)  # Joining content back to form updated line
    if float(selectedFurniture[0]['availableQty']) <=0:
        print("Out of stock")
    else:
        selectedFurniture[0]['availableQty'] = str(float(selectedFurniture[0]['availableQty']) - quantity)  # Updating available quantity
        try:
            with open(filePath, 'w') as file:
                file.writelines(fileData)  # Writing updated lines back to file
        except FileNotFoundError:
            print("Second file not found")
    print(selectedFurniture)  # Printing selected furniture after update
def optionsToBuy(option):
    print('\n')
    print('='*25)
    print(f"{'CHOOSE OPTIONS':^25}")
    print('='*25)
    print(f"{'1. Add more quantity'}\n{'2.'} {option} {'more items'}\n{'3. Exit with bill'}")
    print('='*25)
    print('\n')
# Function to handle furniture purchase
def purchaseFurniture():
    furnitureDisplay()  # Display available furniture
    furnitureDetailList = furnitureDetails()
    while True:
        furnitureChoice = input('Enter id of the furniture that you want to buy or type exit >> ')
        if furnitureChoice.upper() == "EXIT":
            break
        else:
            try:
                furnitureChoiceCasted = int(furnitureChoice)
                if furnitureChoiceCasted <= 0 or furnitureChoiceCasted > len(furnitureDetails()):
                    print("Enter an id that is available in the table")
                    continue
                if float(furnitureDetailList[int(furnitureChoice)-1]['qty']) == 0.0:
                    print(f"😔 Sorry to say, but {furnitureDetailList[int(furnitureChoice)-1]['furnitureName'].upper()} is out of stock. However, you can buy other items available! 🛋️🛒")
                    continue
            except ValueError:
                print("❌ Invalid input! Please enter a valid furniture ID. 🪑🔢")
                continue
            selectedFurniture = []     
            for i in range(len(furnitureDetailList)):
                if int(furnitureDetailList[i]['id']) == furnitureChoiceCasted:
                    # Creating dictionary for selected furniture
                    selectedFurniture.append({
                        "id": furnitureDetailList[i]['id'],
                        "company": furnitureDetailList[i]['companyName'],
                        "name": furnitureDetailList[i]['furnitureName'],
                        "availableQty": furnitureDetailList[i]['qty'],
                        "selectedQty": None,
                        "price": furnitureDetailList[i]['price']
                    })
            isValidQuantity = False
            while not isValidQuantity:
                try:
                    qty = float(input("Enter quantity that you want to buy >> "))
                    if qty <= 0:
                        print("You have to buy at least one quantity")
                    else:
                        if float(selectedFurniture[0]['availableQty'])>= qty:
                            selectedFurniture[0]['selectedQty'] = qty
                            updateFile(selectedFurniture, qty)  # Updating file after purchase
                            isValidQuantity = True
                        else:
                            print(f"❌ {qty} Quantity is not available. Only {float(selectedFurniture[0]['availableQty'])} are available in stock.")
                            isValidQuantity = False
                except ValueError:
                    print("Please enter quantity as a number only!!")
            isQuantityAvailable = False
            while not isQuantityAvailable:
                optionsToBuy("Purchase")
                try:
                    afterPurchaseOption = int(input('Are you thinking of 🤔 >> '))
                    if afterPurchaseOption == 1:
                        while True:
                            try:
                                reQty = float(input("How many quantity you want to add >> "))
                                if reQty <= 0:
                                    print("You have to buy at least one quantity")
                                elif float(selectedFurniture[0]['availableQty']) <=0:
                                    print("Out of stock!!")
                                    break
                                else:
                                    if float(selectedFurniture[0]['availableQty'])>= reQty:
                                        selectedFurniture[0]['selectedQty'] += reQty
                                        updateFile(selectedFurniture, reQty)
                                        break
                                    else:
                                        print(f"❌ {reQty} Quantity is not available. Only {float(selectedFurniture[0]['availableQty'])} are available in stock.")
                            except ValueError:
                                print("Quantity must be a number!!")
                    elif afterPurchaseOption == 2:
                        furnitureDisplay()
                        furnitureChoice = input('Enter id of the furniture that you want to buy or type exit >> ')
                        if furnitureChoice.upper() == "EXIT":
                            break
                        else:
                            try:
                                furnitureChoice = int(furnitureChoice)
                            except:
                                print('Invalid option!! Enter your choice in number only!!')
                    elif afterPurchaseOption == 3:
                        break
                    else:
                        print("Please enter choice from above options")
                except ValueError:
                    print('Invalid option!! Enter your choice in number only!!')
        break
# Main program loop
while True:
    try:
        # Displaying the options to user 
        print(f"\n{'=' * 35}\n{'Choose options from below '.upper():^35}\n{'=' * 35}\n{'1️⃣  Show available furnitures.\n2️⃣  Purchase furniture.\n3️⃣  Order furniture.\n4️⃣  Exit'}\n{'=' * 35}")
        # Getting user choice in number 
        option = int(input("\nEnter your choice >> "))
        
        if option == 1:
            furnitureDisplay()  # Displaying available furniture
        elif option == 2:
            purchaseFurniture()  # Handling furniture purchase
        elif option == 3:
            pass  # Placeholder for future functionality
        elif option == 4:
            break  # Exiting the program
        else:
            print("Please enter a value from 1 to 4 only !!")
    except ValueError:
        print("Please choose an option in number from 1 to 4 shown.")