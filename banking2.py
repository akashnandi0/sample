import random
import sqlite3
import time
import pyttsx3

start, end = 0, 0
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
# engine.say('Welcome')
engine.runAndWait()


def talk(text):
    engine.say(text)
    engine.runAndWait()


def create_db():
    conn = sqlite3.connect("account.s3db")
    curr = conn.cursor()
    try:
        curr.execute(
            'create table if not exists card (number TEXT, pin TEXT, fname TEXT, lname Text, balance INTEGER default '
            '0);')
    except sqlite3.OperationalError:
        curr.execute('DROP TABLE card;')
        curr.execute(
            'create table if not exists card (number TEXT, pin TEXT, fname TEXT, lname Text, balance INTEGER default '
            '0);')
    finally:
        conn.commit()
        # print("WELCOME TO CRYPTO BANK")
        # talk("WELCOME TO CRYPTO BANK...CHOOSE THE FOLLOWING")


def create_card():
    def get_pin():
        pin = ""
        for each in random.sample(range(9), k=4):
            pin += str(each)
        return pin

    conn = sqlite3.connect("account.s3db")
    curr = conn.cursor()
    iin = [4, 0, 0, 0, 0, 0]
    random_acc_no = random.sample(range(9), 9)
    fname = input("First Name: ")
    lname = input("Last Name: ")
    luhn_card_no = []
    luhn_card_no.extend(iin)
    luhn_card_no.extend(random_acc_no)
    tmp_list = luhn_card_no.copy()
    for i in range(0, len(tmp_list), 2):
        tmp_list[i] *= 2
        if tmp_list[i] > 9:
            tmp_list[i] -= 9
    checksum = list(str(10 - sum(tmp_list) % 10))
    if len(checksum) != 1:
        checksum = [0]
    luhn_card_no.extend(checksum)
    del tmp_list
    card_no_for_db = ''.join(map(str, luhn_card_no))
    card_pin_for_db = get_pin()
    time.sleep(2)
    print(
        "-----------------------------------------\nACCOUNT CRREATION UNDER "
        "PROCESS\n-----------------------------------------")
    talk("ACCOUNT CREATION UNDER PROCESS...PLEASE WAIT FEW SECONDS")
    st = "."
    for i in range(0, 5):
        time.sleep(0.5)
        print(st * i * i)
    time.sleep(2)
    print(
        "\n-----------------------------------------\nACCOUNT CREATION "
        "SUCCESSFUL\n-----------------------------------------")
    talk("ACCOUNT CREATION SUCCESSFULL")
    time.sleep(0.5)
    print("\n-----------------\nACCOUNT DETAILS\n-----------------\nWELCOME {} {}".format(fname, lname))
    talk("YOUR CARD AND PIN IS GETTING GENERATED")
    time.sleep(1)
    print("\nYour card has been created")
    print("Your card number:\n{}\nYour card PIN:\n{}\n".format(card_no_for_db, card_pin_for_db))
    curr.execute('SELECT number from card;')
    # db_return = curr.fetchall()
    # try:
    #     listofrows = (lambda l: [item for sublist in l for item in sublist])(db_return)
    #     myid = max(listofrows)
    # except ValueError:
    #     myid = 0
    sqlinjectme = (card_no_for_db, card_pin_for_db, fname, lname)
    curr.execute('INSERT INTO card (number, pin, fname, lname) VALUES (?, ?, ?, ?);', sqlinjectme)
    conn.commit()


def check_algo(checkme):
    converting_to_int_list = []
    for item in list(checkme):
        converting_to_int_list.append(int(item))
    luhn_card_no = converting_to_int_list[:-1]
    tmp_list = luhn_card_no.copy()
    for i in range(0, len(tmp_list), 2):
        tmp_list[i] *= 2
        if tmp_list[i] > 9:
            tmp_list[i] -= 9
    checksum = list(str(10 - sum(tmp_list) % 10))
    if len(checksum) != 1:
        checksum = [0]
    luhn_card_no.extend(checksum)
    del tmp_list
    card_no_for_db = ''.join(map(str, luhn_card_no))
    if card_no_for_db == checkme:
        return True
    else:
        return False


def retrieve_from_db(user_enters_card_no, user_enters_pin):
    conn = sqlite3.connect("account.s3db")
    curr = conn.cursor()
    card_number = user_enters_card_no
    pin = user_enters_pin
    sqlinjectme = (card_number, pin)
    curr.execute('SELECT number, pin FROM card WHERE number = ? and pin = ?;', sqlinjectme)
    db_return = curr.fetchone()
    match = False
    try:
        if card_number in db_return and pin in db_return:
            match = True
            print("You have successfully logged in!")
            talk("Login Successfully")
    except sqlite3.OperationalError:
        print("\nWrong card number or PIN!\n")
        talk("Invalid Input")
    except TypeError:
        print("\nWrong card number or PIN!\n")
        talk("Invalid Input")
    while match:
        print("1. View Balance\n2. Deposit Amount\n3. Withdraw Amount\n4. Transfer Amount\n5. Close Account\n6.Log "
              "0ut\n7.View Account Details\n0.Exit")
        second_menu_choice = int(input())
        if second_menu_choice == 1:
            curr.execute('SELECT balance FROM card WHERE number = ? and pin = ?;', (card_number, pin))
            db_return = curr.fetchone()
            print("\nBalance: {}\n".format(db_return[0]))
            talk("Balance")
        elif second_menu_choice == 2:
            print("\nEnter Amount:")
            sqlinjectme = (int(input()), card_number, pin)
            curr.execute('UPDATE card SET balance = balance + ? WHERE number = ? and pin = ?;', sqlinjectme)
            conn.commit()
            print("Money Deposit Successful")
            talk("Money Deposited Successful")
            curr.execute('SELECT balance FROM card WHERE number = ? and pin = ?;', (card_number, pin))
            db_return = curr.fetchone()
            print("\nBalance: {}\n".format(db_return[0]))
            talk("Balance")
        elif second_menu_choice == 3:
            print("\nEnter amount to be withdrawn:")
            sqlinjectme = (int(input()), card_number, pin)
            curr.execute('UPDATE card SET balance = balance - ? WHERE number = ? and pin = ?;', sqlinjectme)
            conn.commit()
            curr.execute('SELECT balance FROM card WHERE number = ? and pin = ?;', (card_number, pin))
            db_return = curr.fetchone()
            print("Withdrawal Successfully")
            talk("Withdrawal Successful")
            print("\nBalance: {}\n".format(db_return[0]))
            talk("Balance")
        elif second_menu_choice == 4:
            # global transfer_destination
            transfer_destination = []
            print("Enter card number:")
            user_enters_transferdest = input()
            if len(user_enters_transferdest) != 16:
                print("\nProbably you made a mistake in the card number.\nPlease try again!\n")
                talk("Invalid Input")
                continue
            elif len(user_enters_transferdest) == 16:
                if user_enters_transferdest == card_number:
                    print("\nYou can't transfer money to the same account!\n")
                    talk("Sorry")
                    continue
                elif not check_algo(user_enters_transferdest):
                    '# IF CHECK LUHN ALGO RETURNS FALSE. NOT FALSE = TRUE AND THEN WE CONTINUE'
                    print("\nLUHN CHECK:Probably you made a mistake in the card number.\nPlease try again!\n")
                    talk("Invalid Card Number")
                    continue
                else:
                    transfer_destination = (int(user_enters_transferdest),)
            curr.execute('SELECT number FROM card WHERE number = ?;', transfer_destination)
            db_return = curr.fetchone()
            try:
                len(db_return)
                print("\nEnter how much money you want to transfer:\n")
                user_enters_transfermoney = int(input())
                curr.execute('SELECT balance FROM card WHERE number = ? and pin = ?', (card_number, pin))
                db_return = curr.fetchone()
                if user_enters_transfermoney > db_return[0]:
                    print("\nNot enough money!\n")
                    talk("Not enough money try again")
                    continue
                else:
                    curr.execute('UPDATE card SET balance = balance + ? WHERE number = ?;', (
                        user_enters_transfermoney, int(user_enters_transferdest)))
                    curr.execute('UPDATE card SET balance = balance - ? WHERE number = ?;', (
                        user_enters_transfermoney, card_number))
                    conn.commit()
                    print("\nSuccess!\n")
                    talk("Success")
                    curr.execute('SELECT balance FROM card WHERE number = ? and pin = ?;', (card_number, pin))
                    db_return = curr.fetchone()
                    print("\nBalance: {}\n".format(db_return[0]))
                    talk("Balance")
                    continue
            except TypeError:
                print("\nSuch a card does not exist.\n")
                talk("Invalid Card")
                continue

        elif second_menu_choice == 5:
            sqlinjectme = (card_number, pin)
            curr.execute('DELETE FROM card WHERE number = ? and pin = ?;', sqlinjectme)
            conn.commit()
            print("\nThe account has been closed!\n")
            talk("Account closed")
            break
        elif second_menu_choice == 6:
            print("You have successfully logged out!")
            talk("Logged out successfully")
            match = False
        elif second_menu_choice == 7:
            curr.execute("SELECT fname, lname, balance FROM card WHERE number = ? AND pin = ?;", (card_number, pin))
            db_return = curr.fetchmany()
            # print(db_return[0][0])
            print("\nName : {} {}\tBalance: Rs.{}\n".format(db_return[0][0], db_return[0][1], db_return[0][2]))
        elif second_menu_choice == 0:
            end1 = time.time()
            print("Bye!")
            talk("Have a nice day")
            talk("Happy to assist you...Thank you")
            print("process finished in {}".format(end1 - start))
            conn.close()
            # exit()
            main()


def main():
    program_is_running = True
    create_db()
    while program_is_running:
        global start
        start = time.time()
        print("\nWELCOME TO CRYPTO BANK")
        talk("WELCOME TO CRYPTO BANK...CHOOSE THE FOLLOWING")
        print("1. Create an account\n2. Log into account\n0. Exit\nOption : ")
        first_menu_choice = int(input())
        if first_menu_choice == 1:
            create_card()
        elif first_menu_choice == 2:
            print("Enter your card number:")
            user_enters_card_no = input()
            print("Enter your PIN:")
            user_enters_pin = input()
            retrieve_from_db(user_enters_card_no, user_enters_pin)
        elif first_menu_choice == 0:
            print("Bye!")
            talk("Happy to assist you...Thank you")
            end1 = time.time()
            print("process finished in {}".format(end1 - start))
            program_is_running = True


while True:
    main()
