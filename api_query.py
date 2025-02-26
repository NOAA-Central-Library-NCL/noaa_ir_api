import os, csv, sys, re, json, math
import toml
from itertools import accumulate, chain
from datetime import datetime
import requests

""" 
Class used to query IR and export output:
- RepositoryQuery

"""


class RepositoryQuery():
    """Query class used to interact with NOAA Repository JSON API"""

    item_url = "https://repository.library.noaa.gov/view/noaa/"
    today = f"{datetime.now().strftime('%Y-%m-%d')}T00:00:00Z"
    date_info = datetime.now().strftime("%Y_%m_%d")
    col_fname = f"noaa_collection_{date_info}"

    # dictionary containing NOAA Repository collections and associated PIDS
    pid_dict = { 
                "NOAA IR collection":"noaa",
                "National Environmental Policy Act (NEPA)" : "1",
                "Weather Research and Forecasting Innovation Act" : "23702",
                "Coral Reef Conservation Program (CRCP)" : "3",
                "Ocean Exploration Program (OER)" : "4",
                "National Marine Fisheries Service (NMFS)" : "5",
                "National Weather Service (NWS)": "6",
                "Office of Oceanic and Atmospheric Research (OAR)" : "7",
                "National Ocean Service (NOS)" : "8",                
                "National Environmental Satellite and Data Information Service (NESDIS)" : "9",
                "Sea Grant Publications" : "11",
                "Education and Outreach" : "12",
                "NOAA General Documents" : "10031",
                "NOAA International Agreements" : "11879",
                "Office of Marine and Aviation Operations (OMAO)" : "16402",
                "Integrated Ecosystem Assessment (IEA)":"22022",
                "NOAA Cooperative Institutes": "23649",
                "Cooperative Science Centers": "24914"
            }

    def __init__(self, fields):

        self.api_url =  "https://repository.library.noaa.gov/fedora/export/view/collection/"
        self.fields = fields
        self.pid = ''
        self.collection_data = []
        self.date_params = None

    def add_date_filtering(self):
        """
        Method adds date params dictionary to empty date params 
        """

        self.date_params = create_date_filter_params(data['date_params'])

        
    def get_single_collection(self,pid):
        """
        IR collection dataset is queried via REST API.
        
        Multiple functions are utilized to generate information in order
        JSON, including: row_total and API URL(s). This info is
        passed into a function a final function collection_data which 
        returns JSON.

        Parameters: 
            pid: collection pid
        
        Returns:
            Response header and Documents from an IR collection in JSON.
        """
        
        self.pid = str(pid)

        check_pid(self.pid_dict, self.pid)
        row_total = get_row_total(self.api_url, self.pid, self.date_params) 
        api_url_info = iterate_rows(self.api_url, self.pid, row_total, self.date_params)

        # call concat_json function
        self.collection_data = concat_json(api_url_info)


    def get_all_items(self):
        """
        Entire IR dataset is queried via REST API.

        'noaa' serves as the endpoint for entire IR collection.

        Multiple functions are utilized to generate information in order
        JSON, including: row_total and API URL(s). This info is
        passed into a function a final function collection_data which 
        returns JSON.

        Returns:
            Resonse header and entire Dataset collection in JSON.
        """

        all_ir_json = 'noaa'
        row_total = get_row_total(self.api_url, all_ir_json, self.date_params)
        api_url_info = iterate_rows(self.api_url, all_ir_json, row_total, self.date_params)

        # call concat_json function
        self.collection_data = concat_json(api_url_info)
        

    def filter_on_fields(self):
        """
        Filters JSON based on fields list passed into function.        

        Returns:
            Documents of from an IR collection in JSON
        """

        filtered_data = []

        for doc in self.collection_data:
            filtered_data.append(
                field_iterator(doc, self.fields))
             
        self.collection_data = filtered_data


    def convert_multivals_to_one(self, field, delimiter='~'):
        """
        Converts multivalued column values into a single value, 
        generating a new row, carrying over associated value to 
        newly created row.

        Default delimiter is a tilda symbol.

        Parameters:
            field: collection data field

        Returns: 
            Updates RepositoryQuery collection_data attribute
            with new values.
        """

        data = []

        for item in self.collection_data:
            if ';' in item[field]:
                for multi_item in item[field].split(delimiter):
                    data.append({
                        'PID': item['PID'],
                        field : multi_item
                        })
            else:
                data.append({
                        'PID': item['PID'],
                        field: item[field]
                        })

        # remove entries where fields equal ''    
        data = [x for x in data if x[field] != '']

        self.collection_data = data


    def search_field(self, field, search_value):
        """ 
        Search on collection data. 

        Collection data must already be pull and stored in 
        collection data instance variable. Exception will be thrown if not.

        Simple search is performed on selected field. 
        Search is converted to lower lower as is field to be searched on.

        Parameters:
            field: field to be searched on
            search_value: value that searches against field

        Returns:
            list of dicts.
        """
        
        if len(self.collection_data) == 0:
            raise Exception('No Collection data present. Make sure to pull data (single collection or entire dataset)')

        result_list = []

        for record in self.collection_data:
            try:
                if search_value.lower() in record[field].lower():
                    result_list.append(record)
            except KeyError:
                raise Exception('field not present. Check your RepositoryQuery instance fields')

        return result_list     
    

    def export_single_collection(self,
        pid, filetype='csv',export_path='.',
        col_fname=col_fname):
        
        """
        Export single repository collection data to CSV or JSON.

        Parameters:
            pid: collection pid. can also be 'noaa' if entire colleciton.
            filetype: 'csv' by default arg. 'json' as optional output.
            export_path: '.', or current path is default arg.
            col_fname: filename. 'noaa_collection_YYYY_MM_DD' is default arg.

        Returns:
            CSV or JSON of a single IR collection.
        """
        # creates directory if it doesn't exists
        make_dir(export_path)
        
        # repository_query.get_single_collection_json(collection_pid)
        self.get_single_collection(pid)
        self.filter_on_fields()

        collection_full_path = os.path.join(export_path, f"{col_fname}.{filetype}")
        print(collection_full_path)

        #export data
        # as CSV
        if filetype == 'csv':
            delimiter = '\t'
            write_dict_list_to_csv(self.collection_data,
                collection_full_path,
                delimiter, self.fields)
        
        # as JSON
        elif filetype == 'json':
            with open(collection_full_path, 'w') as f:
                json.dump(self.collection_data,
                    f,indent=4)
                
        else:
            print('filetype not accepted')

    
    def export_all_items(self,
        filetype='csv',export_path='.',
        col_fname=col_fname):
        """
        Exports all repository items data to CSV or JSON.

        Parameters:
            pid: collection pid. can also be 'noaa' if entire colleciton.
            filetype: 'csv' by default arg. 'json' as optional output.
            export_path: '.', or current path is default arg.
            col_fname: filename. 'noaa_collection_YYYY_MM_DD' is default arg.

        Returns:
            CSV or JSON of all items.
        """

        # creates directory if it doesn't exists
        make_dir(export_path)
        
        # repository_query.get_all_items
        self.get_all_items()
        self.filter_on_fields()

        collection_full_path = os.path.join(export_path, f"{col_fname}.{filetype}")
        print(collection_full_path)

        #export data
        # as CSV
        if filetype == 'csv':
            delimiter = '\t'
            write_dict_list_to_csv(self.collection_data,
                collection_full_path,
                delimiter, self.fields)
        
        # as JSON
        elif filetype == 'json':
            with open(collection_full_path, 'w') as f:
                json.dump(self.collection_data,
                    f,indent=4)
                
        else:
            print('filetype not accepted')

    ############################
    ####### Functions ##########
    ############################

def field_iterator(json_data, fields):
    """
    Helper function. 

    Return dict
    """

    data_dict = {}

    delimiter = '~'
    for field in fields:
        if json_data.get(field) is None:
            data_dict.update({field: ''})
        elif isinstance(json_data.get(field), list): 
            # delimter
            data_dict.update({field: clean_text(delimiter.join(json_data.get(field)))})
        else:
            data_dict.update({field: clean_text(json_data.get(field))})

    return data_dict


def make_request(url):
    """
    Make request. Check for 200 status code. If not exit
    script with sys.exit.  
    
    Parameters:
        url: api url string.
    
    Returns:
        Returns response, if not returns
        message and quit program.
    """

    r = requests.get(url)
    if r.status_code != 200:
        return 'status code did not return 200'
    return r


def get_row_total(api_url, pid, date_params):
    """
    Get row total from collection. 

    Parameters:
        api_url: api url string
        pid: collection pid. can also be 'noaa' if entire colleciton.
        date_parameters: string formatted as 
            'from=MMMM-YY-DDT00:00:00Z&until=MMMM-YY-DDT00:00:00Z'

    Returns row total for each collection, 
    including entire NOAA IR collection.
    """

    # conditional is based on whether the option
    # was selected to use class method of 'add filter'
    if date_params is None:
        r = requests.get(f'{api_url}{pid}')
    else:
        r = requests.get(f'{api_url}{pid}?{date_params}')

    if r.status_code != 200:
        return 'status code did not return 200'
    data = r.json()
    return data['response']['numFound']


def iterate_rows(api_url, col_pid, row_total, date_params, row_num=5000): 
    """
    If total number of rows is less than 
    chunk val a list of URLS is generated with 
    a num appended with a query string
    """

    url_base = api_url_base_constructor(api_url, col_pid)

    if row_total < row_num:
        # conditional is based on whether the option
        # was selected to use class method of 'add filter'
        return f'{url_base}?rows={row_total}&{date_params}'
    else:
        chunk_array = split_equal(row_total, row_num)
        # insert 0 at beginning of list
        chunk_array.insert(0,0) 
        cumsum_chunk_array = list(accumulate(chunk_array))

        chunk_link_array = []

        for chunk in cumsum_chunk_array:
            if chunk != row_total:
                if date_params is None:
                    # chunk url conditional is based on whether the option
                    # was selected to use class method of 'add filter'
                    chunk_url = f'{url_base}?rows={str(row_num)}&start={str(chunk)}'
                    chunk_link_array.append(chunk_url)
                else:
                    chunk_url = f'{url_base}&rows={str(row_num)}&start={str(chunk)}'
                    chunk_link_array.append(chunk_url)
                continue

        return chunk_link_array

    
def split_equal(total, row_num):
    """
    Helper function for iterate_rows function
    """
    li = [row_num] * math.floor((total / row_num))
    return li


def concat_json(api_url_info):
    """
    Function utilized to handle multiple or single api URL requests.

    If multiple API URL requests are occur, requests are made
    using list comprehensions resulting in lists of dicts. Lists
    are combined using itertools chain. 

    If single API request is made, only list of dicts is returned.

    Returns:
        list of IR records. Response header is removed in the process. 
        Neccessary for concating JSON.  
    """
    
    # if api_url_info contains multiple links are present
    if isinstance(api_url_info, list):
        r = [make_request(url) for url in api_url_info]
        data = [x.json() for x in r]
        docs = [x['response']['docs'] for x in data]
        #use itertools chain to concat lists together
        docs = list(chain(*docs))
    
    # if a single link is present
    elif isinstance(api_url_info, str):
        r = make_request(api_url_info)
        data = r.json()
        docs = data['response']['docs']

    return docs


def check_pid(collection_info, pid):
    """
    Checks to see if pid is a valid pid repo collection pid.

    Parameters:
        pid: sting value

    Returns:
        Error message and exit program is value isn't valid; pid 
        passed in if value is valid.
    """
    for collection_pid in collection_info.values():
        if pid == collection_pid:
            return pid
    return f'{pid} is not a valid pid'


def make_dir(filepath):
    """
    Creates directory in current working
    directory if it doesn't exists

    Paramaters:
        filepath: filepath
    
    """
    if os.path.exists(filepath) == False:
        os.mkdir(filepath)


def clean_text(text):
    """
    Clean text data.
    """
    text = text.replace('\n', '').replace('\r','')
    return text


def write_dict_list_to_csv(dict_li,file_path, delimiter, fieldnames):
    """
    Write Python dict list to CSV

    Parameters:
        dict_li: Python list of dictionaries
        file_path: abs or relative file path. use to save CSV
        delimiter: choose type of delimiter
        fieldnames: function utilizes csv.DictWriter. Currently
        written to require header.
    """

    with open(file_path, 'w',
        newline='', encoding='utf-8') as fh:
        
        # list of dictionaries written to CSV
        csvfile = csv.DictWriter(fh,
            delimiter=delimiter,
            fieldnames=fieldnames
            )

        csvfile.writeheader()
        csvfile.writerows(dict_li) 

def api_url_base_constructor(api_url, col_pid):
    """
    helper function used to  
    construct an api_url base using api_url and col_pid

    returns an URL string
    """

    return f'{api_url}{col_pid}'


def create_date_filter_params(date_dict):
    """
    Create 'from' & 'until' date filter params that
    can be added to initial NOAA IR API request in order to filter on request. 
    Filter is applied to fgs.modifieddate field.
    """

    return f"from={date_dict['from']}T00:00:00Z&until={date_dict['until']}T00:00:00Z"


def read_toml_file(toml_file):
    """
    helper function to read toml file.
    Reads list of API fields.


    Parameters:
        toml_file: toml_file name
    """

    data = toml.load(toml_file)
    return data


if __name__ == "__main__":
    # command line arg takes in toml file
    # toml file contains api fields you wish to pull from api
    f_name = sys.argv[1]
    data = read_toml_file(f_name)
    # instantiate class 
    q = RepositoryQuery(data['fields'])
    
    # call method IF you want to create date params
    # date param information is stored in fields toml file.
    # do not use method if you want unfiltered report.
    q.add_date_filtering()

    #use class methods to either export single collection all items from IR
    #CSV is the default file format, but you can specify json for that format
    q.export_single_collection('5', 'csv') 
    
    # to export entire collection...
    # no args are required, but optional include args include filepath, filename,
    # and filetype (CSV, JSON) 
    #q.export_all_items('json')