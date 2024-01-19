import sqlite3
import pandas as pd
import os
import time

# db connectors and creation.
conn = sqlite3.connect('minidb.db')
cursor = conn.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS anime(
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               name TEXT NOT NULL,
               genre TEXT NOT NULL); """)

def menu():
    while True:
        os.system('clear')
        print('Menu:')
        print("1 - Show table")
        print("2 - Add record")
        print("3 - Remove record")
        print("4 - Export to csv")
        print("5 - Quit the program")

        while True:
            try:
                option = int(input("\nPlease enter your choice: "))
                break
            except ValueError:
                print("Invalid input. Please enter a number: ")

        if option in [1, 2, 3, 4]:
            match option:
                case 1:
                    show_table()
                    input('\nPress ENTER to go back.')
                case 2:
                    add_record()
                case 3:
                    remove_record()
                case 4:
                    export_to_csv()

        elif option == 5:
            print('\nQuitting the program...')
            break
        else:
            print('Invalid option, try again.')
            time.sleep(1)


def show_table():
    os.system('clear')
    query = 'SELECT * FROM anime'
    tbl_df = pd.read_sql_query(query, conn, index_col='id')
    print(tbl_df)


def add_record():
    new_anime_name = input('\nEnter the name of the anime: ')
    new_anime_genre = input('Enter the anime genre: ')
    data = {'name': new_anime_name, 'genre': new_anime_genre}
    new_row_df = pd.DataFrame(data, index=[0])
    new_row_df.to_sql('anime', conn, if_exists='append', index=False)
    print(f'\nThe anime "{new_anime_name}" has been added to the db.')
    this_usr_input = input('\nWrite "new" to add another record or press Enter to go back: ')
    if this_usr_input == 'new':
        os.system('clear')
        add_record()


def remove_record():
    show_table()
    print('\n')
    to_delete = input('Enter the index of the anime to delete: ')
    cursor.execute('DELETE FROM anime WHERE id = ?', to_delete)
    conn.commit()
    print('The anime has been removed from the db.')
    this_usr_input = input('\nWrite "del" to delete another or press Enter to go back: ')
    if this_usr_input == 'del':
        remove_record()


def export_to_csv():
    query = 'SELECT name, genre FROM anime'
    tbl_df = pd.read_sql_query(query, conn)
    tbl_df.to_csv('anime_db.csv')
    print('\nThe csv file has been created.')
    time.sleep(2)


menu()