import os, sys, csv, json
from datetime import datetime
from api_query import RepositoryQuery, DataExporter

"""
Menu provides interactive command-line menu for api_query.py

"""


class Menu:

    data_info_json = datetime.now().strftime("%Y_%m_%d") + ".json"
    date_info_csv = datetime.now().strftime("%Y_%m_%d") + ".csv"

    """
    Display a menu and respond to choices when run method is executed.
    """
    def __init__(self):
        self.query = RepositoryQuery(default_fields)
        self.export = DataExporter()
        self.choices = {
                "1": self.get_csv_of_collection_titles,
                "2": self.get_csv_of_all_items,
                "3": self.exit_menu
                }

    def display_menu(self):
        print("""
Query NOAA Resposistory JSON REST API

    1. Get CSV of collection
    2. Get CSV of all items
    3. Quit
    """)

    def run(self):
        """
        Call method on Menu class to display the menu and respond to choices.
        """
        while True:
            self.display_menu()
            choice = input("Enter an option: ")
            action = self.choices.get(choice)
            if action:
                action()
            else:
                print("{0} is not a valid choice".format(choice))

    @staticmethod
    def collections():
        print("")
        print("Enter the number associated with collection to retrieve data:")
        print("")
        print("NEPA : 1")
        print("Coral Reef Conservation Program: 3")
        print("Ocean Exploration Program: 4")
        print("National Marine Fisheries Service : 5")
        print("National Weather Service: 6")
        print("Office of Oceanic and Atmospheric Research: 7")
        print("National Ocean Service: 8")
        print("National Environmental Satellite and Data Information Service: 9")
        print("Sea Grant Publications: 11")
        print("Education and Outreach: 12")
        print("NOAA General Documents: 10031")
        print("NOAA International Agreements: 11879")
        print("Office of Marine and Aviation Operations (OMAO): 16402")
        print("Integrated Ecosystem Assessment (IEA): 22022")
        print("NOAA Cooperative Institutes: 23649")
        print("Cooperative Science Centers : 24914")
        print("")

    def get_csv_of_collection_titles(self):
        """
        Returns selected collection as CSV
        """

        # call filter_by_date function
        filter_by_date(self.query.date_filter)

        self.collections()
        collection_pid = input("Select a collection: ")

        # export collection
        self.export.export_collection_as_csv(self.query, collection_pid)

        clear_screen()
        for name, pid in self.query.pid_dict.items():
            if collection_pid == pid:
                print('')
                print(f'File printed: {name}')


    def get_csv_of_all_items(self):
        """
        Returns a CSV of all titles from IR.
        """

        # call filter_by_date function
        filter_by_date(self.query.date_filter)

        # export all collections
        self.export.export_all_collections_as_csv(self.query,
            self.query.get_all_collections_json())

        clear_screen()
        print('')
        print(f'All collections file printed')


    def exit_menu(self):
        print("")
        print("Bye Bye.")
        print("")
        os._exit(0)


def filter_by_date(date_filter):
    """
    Used to create date filter.

    Parameters:
        date_filter: api_query method
    """

    while True:

        # filter by date
        filter_by = input('Filter by date [y/n]? ')

        if filter_by == 'y' or filter_by == 'Y':

            from_date = input('From [YYYY-MM-DD]: ')
            if date_format(from_date):

                until_date = input('OPTIONAL: Until [YYYY-MM-DD/n]: ')
                if date_format(until_date):

                    # call date filter method
                    date_filter(from_date, until_date)
                    break

                elif until_date == 'n' or until_date == 'N':

                    date_filter(from_date)
                    break

        elif filter_by == 'n' or filter_by == 'N':
            break
        else:
            print('Filter by date [y/n]')


def clear_screen():

    if sys.platform == "linux" or sys.platform == "linux2":
        os.system('clear')
    elif sys.platform == "darwin":
        os.system('clear')
    elif sys.platform == "win32":
        os.system('cls')


def date_format(date):
    """
    Check if date param format is valid.

    format: 'YYYY-MM-DDT00:00:00Z'

    """
    try:
        datetime.strptime(date, '%Y-%m-%d')
        return date
    except ValueError:
       print("Incorrect data format, should be YYYY-MM-DD")


def update_columns():
    """
    Use function to update default column options within menu.py while
    script is running.
    """
    pass



if __name__ == "__main__":
    default_fields =  ['PID', 'mods.title','mods.type_of_resource',
    'fgs.createdDate','mods.sm_digital_object_identifier',
    'mods.related_series']
    m = Menu()
    m.run()
