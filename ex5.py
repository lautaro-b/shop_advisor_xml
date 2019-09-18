#############################################################
# FILE : ex5.py
# WRITERS : lautaro_borrovinsky , lautaro , 33783538
#           liel
# EXERCISE : intro2cs ex5 2015-2016
# DESCRIPTION: A program that given items that we want to buy,
# tells us the best option for the purchase among the
# biggest supermarkets in the country.
# contains several functions with different usages
# using loops, deep copy, lists,dictionaries,
# files, importing files, among others.
#############################################################
import xml.etree.ElementTree as ET
import re
import copy


def get_attribute(store_db, ItemCode, tag):
    '''
    Returns the attribute (tag) 
    of an Item with code: Itemcode in the given store

    '''
    return store_db[ItemCode][tag]


def string_item(item):
    '''
    Textual representation of an item in a store.
    Returns a string in the format of '[ItemCode] (ItemName)'

    '''
    return '[' + item['ItemCode'] + ']'+"\t"+'{' + item['ItemName'] + '}'


def string_store_items(store_db):
    '''
    Textual representation of a store.
    Returns a string in the format of:
    string representation of item1
    string representation of item2
    '''
    lst = []
    for item in store_db.keys():
        lst.append(string_item(store_db[item]))
    return "\n".join([str(i) for i in lst]) + '\n'



def read_prices_file(filename):
    '''
    Read a file of item prices into a dictionary.  The file is assumed to
    be in the standard XML format of "misrad haclcala".
    Returns a tuple: store_id and a store_db, 
    where the first variable is the store name
    and the second is a dictionary describing the store. 
    The keys in this db will be ItemCodes of the different items and the
    values smaller  dictionaries mapping attribute names to their values.
    Important attributes include 'ItemCode', 'ItemName', and 'ItemPrice'
    '''
    tree = ET.parse(filename)
    root = tree.getroot()
    store_id = root.find("StoreId").text
    store_db = {}
    for item in root.getiterator('Item'):
        # Goes through each of the items
        item_code = item.find("ItemCode")
        for sub_item in item:                   # Goes through each sub-item
             store_db[item_code.text] = { sub_item.tag : sub_item.text
                                            for sub_item in item}
    return store_id, store_db


def filter_store(store_db, filter_txt):  
    '''
    Create a new dictionary that includes only the items 
    that were filtered by user.
    I.e. items that text given by the user is part of their ItemName. 
    Args:
    store_db: a dictionary of dictionaries as created in read_prices_file.
    filter_txt: the filter text as given by the user.
    '''
    filtered_dictionary = dict()
    for item in store_db:
        if filter_txt in store_db[item]['ItemName']:
            filtered_dictionary[item] = {
                attribute: store_db[item][attribute]
                for attribute in store_db[item]}
    return filtered_dictionary


def create_basket_from_txt(basket_txt): 
    '''
    Receives text representation of few items (and maybe some garbage 
      at the edges)
    Returns a basket- list of ItemCodes that were included in basket_txt

    '''
    # Find words in [] using Regular expression operations
    my_string = basket_txt
    basket = re.findall(r"\[([A-Za-z0-9_]+)\]", my_string)
    return basket


def get_basket_prices(store_db, basket):
    '''
    Arguments: a store - dictionary of dictionaries and a basket - 
       a list of ItemCodes
    Go over all the items in the basket and create a new list 
      that describes the prices of store items
    In case one of the items is not part of the store, 
      its price will be None.

    '''
    price_list = []
    for index_2 in basket:
        if index_2 not in store_db:
            price_list.append(None)
        for index in store_db:
            if index_2 in index:
                price = float(store_db[index_2]["ItemPrice"])
                price_list.append(price)

    return price_list


def sum_basket(price_list):
    '''
    Receives a list of prices
    Returns a tuple - the sum of the list (when ignoring Nones) 
      and the number of missing items (Number of Nones)

    '''
    missing_items = 0
    sum_price_list = 0
    for index in price_list:
        if index is None:
            missing_items += 1
        else: sum_price_list += index
    return sum_price_list, missing_items

 
def basket_item_name(stores_db_list, ItemCode):
    '''
    stores_db_list is a list of stores (list of dictionaries of
      dictionaries)
    Find the first store in the list that contains the item and return its
    string representation (as in string_item())
    If the item is not avaiable in any of the stores return only [ItemCode]

    '''
    for store in stores_db_list:
        if ItemCode in store:
            return string_item(store[ItemCode])

    return "["+ItemCode+"]"


def save_basket(basket, filename):
    ''' 
    Save the basket into a file
    The basket representation in the file will be in the following format:
    [ItemCode1] 
    [ItemCode2] 
    ...
    [ItemCodeN]
    '''
    open_file = open(filename, 'w')
    for item in basket:
        open_file.write('[' + item + ']' + "\n")


def load_basket(filename):
    ''' 
    Create basket (list of ItemCodes) from the given file.
    The file is assumed to be in the format of:
    [ItemCode1] 
    [ItemCode2] 
    ...
    [ItemCodeN]
    '''
    lst_of_items = []
    open_file = open(filename, 'r')
    lines = open_file.readlines()
    for line in lines:
        line = str(line.rstrip("\n"))
        lst_of_items.append(str(line))
    for item in lst_of_items:
        left_bracket = item.replace("[", "")
        lst_of_items[lst_of_items.index(item)] = left_bracket
    for item_2 in lst_of_items:
        right_bracket = item_2.replace("]", "")
        lst_of_items[lst_of_items.index(item_2)] = right_bracket
    return lst_of_items


def best_basket(list_of_price_list):
    '''
    Arg: list of lists, where each inner list is list of prices as created
    by get_basket_prices.
    Returns the cheapest store (index of the cheapest list) given that a 
    missing item has a price of its maximal price in the other stores *1.25

    '''

    lst_same_number = copy.deepcopy(list_of_price_list)

    final_list = []
    for my_list in lst_same_number:
        for product in my_list:
            if product is None:
                index_of_lst = lst_same_number.index(my_list)
                # Index of current list
                index_of_num = lst_same_number[index_of_lst].index(product)
                # Index of current number in list
                temporary_lst = []
                for lists_index in range(len(lst_same_number)):
                    # Goes through all the numbers in the different list that
                    # are on the same index as the one with the None found
                    num_in_lists = lst_same_number[lists_index][index_of_num]
                    # Returns the number that are in the same index through the
                    # different lists
                    if num_in_lists is not None:
                        temporary_lst.append(num_in_lists)
                        lst_same_number[index_of_lst][index_of_num] = \
                            max(temporary_lst) * 1.25
    for new_list in lst_same_number:
        final_list.append(sum(new_list))
    the_min = min(final_list)
    min_index = final_list.index(the_min)
    # Selects the index of the store with the lowest sum

    return min_index







