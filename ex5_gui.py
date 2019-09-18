import ex5
from tkinter import filedialog
from tkinter import *
import sys

MAX_STORES = 3
CANVAS_WIDTH = 650
CANVAS_HEIGHT = 200
STORE_TEXT_WIDTH = 50
STORE_TEXT_HEIGHT = 20
NAME_COL_W = 40
NUM_COL_W = 8
BEST_COLOR = 'red'
REG_COLOR = 'black'


class ex5GUI:
    '''
    An object that create a gui for ex5 using tkinter
    '''
    def __init__(self, top):

        self.top = top
        # --- Datastructures --
        self.DB_list = [{} for i in range(MAX_STORES)]
        self.basket_list = [[] for i in range(MAX_STORES)]
        self.item_list = [{} for i in range(MAX_STORES)]
        self.store_names = [[] for i in range(MAX_STORES)]
        self.basket = []
        self.full_DB = {}

        self.file_xml_opt = options = {}
        options['defaultextension'] = '.xml'
        options['initialdir'] = '.'

        self.file_txt_opt = options = {}
        options['defaultextension'] = '.txt'
        options['initialdir'] = '.'

        # --- main frames --
        self.left_frame = Frame(self.top)
        self.right_frame = Frame(self.top)
        self.left_frame.grid(column=0, row=0)
        self.right_frame.grid(column=1, row=0, sticky=W)
        self.sys = sys.platform



        # -- Left Frame -----
        self.load_frame = Frame(self.left_frame)
        self.load_frame.grid(column=0, row=0, columnspan=1)

        self.filter_frame = Frame(self.left_frame)
        self.filter_frame.grid(column=0, row=1, columnspan=1)
        self.store_name_label = Label(self.left_frame)
        self.store_name_label.grid(column=0, row=3)
        self.store_items_panel = Text(self.left_frame,
                height=STORE_TEXT_HEIGHT, width=STORE_TEXT_WIDTH,
                highlightbackground='black')
        self.store_items_panel.grid(column=0, row=4, rowspan=1)
        self.store_to_basket_frame = Frame(self.left_frame)
        self.store_to_basket_frame.grid(column=1, row=4, sticky=W)

        # --- load frame ---
        self.store_idx_GUI = IntVar()
        self.store_idx_GUI.set(1)
        self.load_file_button = Button(self.load_frame, text='Load file',
                command=lambda: self.read_prices_GUI())
        self.load_file_button.grid(column=1, row=0)
        self.load_file_button_new = Button(self.load_frame, text='Load demo',
                command=lambda: self.load_demo_GUI())
        self.load_file_button_new.grid(column=0, row=0)
        self.store_idx_option_list = (1, 2, 3)
        self.store_idx_option_menu = OptionMenu(self.load_frame,
          self.store_idx_GUI, *self.store_idx_option_list)
        self.store_idx_option_menu.grid(column=2, row=0)
        self.show_store_button = Button(self.load_frame, text='Show',
                 command=lambda: self.print_to_screen())
        self.show_store_button.grid(column=3, row=0)

        # --- filter frame ---
        self.filter_entry = Entry(self.filter_frame)
        self.filter_entry.pack(side=LEFT)
        self.filter_button = Button(self.filter_frame,
                text="Filter", command=lambda: self.filterGUI())
        self.filter_button.pack(side=RIGHT)

        # --- store to basket frame ---
        self.add_basket = Button(self.store_to_basket_frame,
                text='Add Selected', command=lambda: self.add_basket_GUI())
        self.add_basket.grid(column=0, row=3, columnspan=2)
        self.delete_basket_button = Button(self.store_to_basket_frame,
                text='Clear basket', command=lambda: self.delete_all())
        self.delete_basket_button.grid(column=0, row=4, columnspan=2)

        # --- right frame ---
        self.basket_file_frame = Frame(self.right_frame)
        self.basket_file_frame.grid(column=0, row=0, sticky=N)
        self.basket_names_frame = Frame(self.right_frame)
        self.basket_names_frame.grid(column=0, row=1, rowspan=2, sticky=W)
        self.basket_table_frame = Frame(self.right_frame)
        self.basket_table_frame.grid(column=0, row=3)
        self.basket_frame_sum = Frame(self.right_frame)
        self.basket_frame_sum.grid(column=0, row=4, sticky=W)

        # --- basket file frame ---       
        self.add_basket_button = Button(self.basket_file_frame,
                 text='Load basket',
                 command=lambda: self.add_basket_from_file_GUI())
        self.add_basket_button.grid(column=0, row=0)
        self.save_basket_button = Button(self.basket_file_frame,
                 text='Save basket',
                 command=lambda: self.save_basket_to_file_GUI())
        self.save_basket_button.grid(column=1, row=0)

        # --- basket table ---
        self.create_basket_canvas()


    def configure_scrollbar(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        self.basket_canvas.configure(
                scrollregion=self.basket_canvas.bbox("all"))


    def load_demo_GUI(self):
        '''
        Load the demo into the GUI
        '''
        item_idx = self.store_idx_GUI.get()-1 
        [store, db] = get_demo_store()
        self.add_store_to_DB_GUI(store, db, item_idx)  


    def read_prices_GUI(self):
        '''
        Calls the user function read_prices_file
        and print its output to the screen
        '''
        item_idx = self.store_idx_GUI.get()-1
        try: 
            
            filename = filedialog.askopenfilename(**self.file_xml_opt)
            if filename:
                
                [store, db] = ex5.read_prices_file(filename) 
                self.add_store_to_DB_GUI(store, db, item_idx)
        except:
            print("error in read_prices_file")
        

        
        
    def add_store_to_DB_GUI(self, store, db, item_idx):
        ''' Update the DB and the GUI with the arguments'''
        self.DB_list[item_idx] = db
        self.item_list[item_idx] = db
        self.store_names[item_idx] = store
        self.print_to_screen()
        


    def filterGUI(self):
        '''
        Calls the users filter function
        and update the store frame with its output
        '''
        for store_ix in range(MAX_STORES):
            self.item_list[store_ix] = ex5.filter_store(self.DB_list[store_ix],
                    self.filter_entry.get())
            assert type(self.item_list[store_ix]) == dict, \
                    "filter didn't return a dictionary"

        self.print_to_screen()


    def print_to_screen(self):
        '''
        print a srote in the store frame
        '''
        idx = self.store_idx_GUI.get()-1
        db = self.item_list[idx]
        if self.store_names[idx]:
            self.store_name_label.config(text="Store "+self.store_names[idx],
                    font="TkDefaultFont 14 bold")
        else:
            self.store_name_label.config(text="Empty store",
                    font="TkDefaultFont 14 bold")
        self.store_items_panel.delete('1.0', END)
        try:

            txt = ex5.string_store_items(db)
            if txt:
                if self.sys == 'linux':
                    txt = self.right_to_left(txt)
                ix = txt.index(']')
                self.store_items_panel.insert(END, txt[:ix])    
                self.store_items_panel.insert(END, txt[ix:])
        except:
            print("error in string_store_items")
        self.print_basket()


    def right_to_left(self, txt):
        ''' Handle right to left conversion in linux '''
        left_par = [i for i, ltr in enumerate(txt) if ltr == '{']
        right_par = [i for i, ltr in enumerate(txt) if ltr == '}']
        for i in range(len(left_par)):
            txt = txt[:left_par[i]+1]+txt[left_par[i]+1:right_par[i]][::-1]+ \
                    txt[right_par[i]:]
        return txt


    def delete_all(self):
        ''' delete the current basket'''
        self.basket = []
        self.refresh_basket()


    def create_basket_canvas(self):
        '''
        Create a canvas for the basket table -
        needs to be re-created for every new basket
        '''

        self.basket_canvas = Canvas(self.basket_table_frame, borderwidth=0,
                background="#ffffff", width=CANVAS_WIDTH, height=CANVAS_HEIGHT)
        self.basket_frame = Frame(self.basket_canvas, background="#ffffff")
        self.basket_scrollbar = Scrollbar(self.basket_table_frame,
                orient="vertical", command=self.basket_canvas.yview)
        self.basket_canvas.configure(yscrollcommand=self.basket_scrollbar.set)

        self.basket_scrollbar.pack(side=RIGHT, fill="y")
        self.basket_canvas.create_window((0, 0), window=self.basket_frame,
                anchor="w", tags="self.basket_frame")
        self.basket_canvas.pack(side="left", fill="both", expand=True)
        self.basket_frame.bind("<Configure>", self.configure_scrollbar)


    def refresh_basket(self):
        '''Delete the current basket canvas and create a new one '''
        self.basket_canvas.destroy()
        self.basket_scrollbar.destroy()
        self.basket_frame.destroy()
        self.create_basket_canvas()


    def get_prices_counts_best_GUI(self):
        '''
        Calls the user functions sum_baskets and best_basket
        Refresh the table sums based on their output
        '''
        prices_GUI = [0]*MAX_STORES
        counts_GUI = [0]*MAX_STORES
        
        for store_ix in range(MAX_STORES):
            
            self.basket_list[store_ix] = ex5.get_basket_prices(
                    self.DB_list[store_ix], self.basket)
            
            try:
                prices_GUI[store_ix], counts_GUI[store_ix] = \
                        ex5.sum_basket(self.basket_list[store_ix])
            except:
                prices_GUI[store_ix] = 0
                counts_GUI[store_ix] = 0

        best_GUI = ex5.best_basket(self.basket_list)
        return (prices_GUI, counts_GUI, best_GUI)


    def add_basket_GUI(self):
        '''
        Calls the user function create_basket_from_txt
        update the basket based on its output
        '''
        try:
            selectedItems = self.store_items_panel.selection_get()
        except:
            return
        try:
            self.basket.extend(ex5.create_basket_from_txt(selectedItems))
        except:
            print("error in create_basket_from_txt")
        try:
            self.print_basket()
        except:
            print("error in get_basket_prices or another function"+ 
                " that you didn't implement yet (q7-q12)")
        


    def add_basket_from_file_GUI(self):
        '''
        Calls the user function add_basket_from_file and and
        print the basket table
        '''
        self.basket = []
        try:
            filename = filedialog.askopenfilename(**self.file_txt_opt)
            if filename:
                self.basket = ex5.load_basket(filename)
                if self.basket is None: self.basket =[] # in case load basket return None
                self.print_basket()
        except:
            print("error in load_basket")

            
           

        


    def save_basket_to_file_GUI(self):
        '''Calls the user function: save_basket_to_file'''
        try:
            filename = filedialog.asksaveasfilename(**self.file_txt_opt)
            if filename:
                ex5.save_basket(self.basket, filename)
        except:
            print("error in save_basket")


    def print_basket_names(self):
        ''' Print store names in the basket panel'''
        Label(self.basket_names_frame, text="Store IDs",
                font="TkDefaultFont 14 bold").grid(row=0, column=0,
                columnspan=MAX_STORES+1)
        Label(self.basket_names_frame, text="List of items", width=NAME_COL_W,
                borderwidth="1", relief="solid").grid(row=1, column=0)

        for store_ix in range(MAX_STORES):
            if self.store_names[store_ix]:
                Label(self.basket_names_frame, text=self.store_names[store_ix],
                        width=NUM_COL_W, borderwidth="1",
                        relief="solid").grid(row=1, column=store_ix+1)
            else:
                Label(self.basket_names_frame, text='empty', width=NUM_COL_W,
                        borderwidth="1",
                        relief="solid").grid(row=1, column=store_ix+1)


    def print_basket(self):
        '''print the baskets table in the basket canvas'''
        self.print_basket_names()
        if not self.basket:
            return    
        self.refresh_basket() 
        prices, counts, best_ix = self.get_prices_counts_best_GUI()
        
        # print the different items in the basket
        for item_ix, item in enumerate(self.basket):
            item_name = ex5.basket_item_name(self.DB_list, 
                                self.basket[item_ix])
            if item_name:
                if self.sys == 'linux':
                    item_name = self.right_to_left(item_name)
                Label(self.basket_frame, anchor="w", text=item_name,
                        width=NAME_COL_W, borderwidth="1", 
                        relief="solid").grid(row=item_ix, column=0)
            else:
                Label(self.basket_frame, text=item, width=NAME_COL_W,
                        borderwidth="1", anchor="w",
                        relief="solid").grid(row=item_ix, column=0)

            # print the item price in the different stores
            for store_ix in range(MAX_STORES):
                Label(self.basket_frame,
                        text=str(self.basket_list[store_ix][item_ix]),
                        width=NUM_COL_W, borderwidth="1", 
                        relief="solid").grid(row=item_ix, column=store_ix+1)

        # print the summary frame with the best one indictae by color
        Label(self.basket_frame_sum, text="", width=NAME_COL_W,
                borderwidth="0").grid(row=0, column=0, columnspan=2)
        Label(self.basket_frame_sum, text="Total price", width=NAME_COL_W,
                borderwidth="1",
                relief="solid").grid(row=1, column=0, sticky=W)
        Label(self.basket_frame_sum, text="Missing items",
                width=NAME_COL_W, borderwidth="1",
                relief="solid").grid(row=2, column=0)

        for store_ix in range(MAX_STORES):
            if store_ix == best_ix:
                c = BEST_COLOR
            else:
                c = REG_COLOR
            Label(self.basket_frame_sum, text='%.2f' % prices[store_ix],
                    width=NUM_COL_W, borderwidth="1", relief="solid",
                    fg=c).grid(row=1, column=store_ix+1, sticky=W)

            Label(self.basket_frame_sum, text='%.0d' % counts[store_ix],
                    width=NUM_COL_W, borderwidth="1", relief="solid",
                    fg=c).grid(row=2, column=store_ix+1, sticky=W)



def get_demo_store():
    '''
    loads a demo store into the program
    '''
    store_id = '001'
    store_db = {'59907': {'ManufacturerName': 'מעדנות בע"מ',
      'ManufactureCountry': 'IL', 'Quantity': '500.00','ItemCode': '59907',
      'ItemPrice': '26.10', 'PriceUpdateDate': '2014-07-22 08:09',
      'UnitOfMeasure': '100 גרם', 'ItemName': 'פיצה משפחתית'},
      '66196': {'ManufacturerName': 'אסם',
      'ManufactureCountry': 'IL', 'Quantity': 
      '200.00', 'ItemCode': '66196', 'ItemPrice': '3.80',
      'PriceUpdateDate': '2015-05-19 08:34',
      'UnitOfMeasure': '100 גרם', 'ItemName': 'ביסלי גריל'},
      '30794': {'ManufacturerName': 'תנובה',
      'ManufactureCountry': 'IL', 'Quantity': '1.00',  'ItemCode': '30794',
      'ItemPrice': '10.90', 'PriceUpdateDate': '2013-12-08 13:48',
      'UnitOfMeasure': 'ליטר', 'ItemName': 'משקה סויה'},  
      '13520': {'ManufacturerName': 'יוניליוור',
      'ManufactureCountry': 'IL', 'Quantity': '75.00', 'ItemCode': '13520',
      'ItemPrice': '4.90', 'PriceUpdateDate': '2015-07-07 08:26',
      'UnitOfMeasure': '100 גרם', 'ItemName': 'קליק קורנפלקס'}, 
      '84316': {'ManufacturerName': 'החברה המרכזית לייצור משקאות',
      'ManufactureCountry': 'IL', 'Quantity': '1.50', 'ItemCode': '84316',
      'ItemPrice': '7.20', 'PriceUpdateDate': '2013-12-31 07:28',
      'UnitOfMeasure': 'ליטר', 'ItemName': 'קוקה קולה בקבוק 1.5 ליטר'}}
    return (store_id, store_db) 

# ----Initate the  GUI ------
if __name__== "__main__":
    top = Tk()
    GUI = ex5GUI(top)
    top.mainloop()

