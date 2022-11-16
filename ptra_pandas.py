"""
        PTR Analysis Python File by Benjamin Riseman for FinePrint Data, 2021

        As a few functions built around searching for tickers in excel documents provided
        by other algorithms of the database.

"""




import pandas
import os
import pathlib

""" Simply debug for the console, lets me see more of the dataframes """

pandas.set_option('display.max_rows', 500)
pandas.set_option('display.max_columns', 20)
pandas.set_option('display.width', 1000)

def search_tickers_ptr(df : pandas.DataFrame, ticker_list : list, ignore_index: bool = True, add_median: bool = True) -> pandas.DataFrame:
    """
        Master function that generates a new DataFrame with asked-for tickers.
        Important parameters are the input DataFrame, and a ticker list, like ["AMZN", "AAPL", "GOOG"].

        Rest of the parameters add / modify columns of the newly-generated DataFrame.
        Recommended to be kept enabled.
        
    """

    cols = ["name", "transaction_date", "transaction_type",
           "amount_min", "amount_max", "ticker", "asset_line1"]
    
    mega_frame = pandas.DataFrame(columns = cols)
    
    for index, row in df.iterrows():
        for tick in ticker_list:
            if tick in row.values:
                mega_frame = mega_frame.append(row, ignore_index = ignore_index)

    
    mega_frame = create_median(mega_frame) if add_median else None

    return mega_frame

def create_median(df : pandas.DataFrame) -> pandas.DataFrame:
    """ Generates a median column in the provided DataFrame. Returns a modified copy. """

    df2 = df.copy()

    try:

        df2["amount_min"] = df2["amount_min"].str.replace(r'\D', '')
        df2["amount_max"] = df2["amount_max"].str.replace(r'\D', '')

    except Exception as ex:
        print(ex)

    else:

        df2["amount_min"] = df2["amount_min"]
        df2["amount_max"] = df2["amount_max"]

    df2.insert(5, "amount_median", (pandas.to_numeric(df2["amount_min"]) +
                           pandas.to_numeric(df2["amount_max"])) / 2)

    return df2

def get_person(name : str) -> tuple:
    """ Returns an unfiltered DataFrame with a person's transactions, given by full name. """
    
    person_frame = da_doc[new_data["name"] == name]
    
    return person_frame

def run():
    """ Automatically runs search_tickers w/ a file and ticker list input. """
    

    while True:

        print("PTR Analysis by Benjamin Riseman for FinePrint Data, 2021")
        
        fileLoc = input("Enter file location, 'h' for house, 's' for senate, or 'q' for quit: ")

        cur_path = os.getcwd() # Changed method of getting cwd

        if fileLoc == ("s" or "'s'"):
            fileLoc = os.path.join(cur_path,"Senate-PTR_2020-2021.csv") #Changed Path Construction to be more universal
            # fileLoc = str(cur_path) + "/Senate-PTR_2020-2021.csv"

        elif fileLoc == ("h" or "'h'"):
            fileLoc = os.path.join(cur_path,"House-PTR_2020-2021.csv") #Changed Path Construction to be more universal

        elif fileLoc == ("q" or "'q'"):
            break

        try:
            x = os.path.join(fileLoc)
            global da_doc
            da_doc = pandas.read_csv(x,encoding='iso-8859-1') # Changed encoding format
            global new_data

            new_data = da_doc.filter(items = ["name", "transaction_date", "transaction_type",
                                            "amount_min", "amount_max", "ticker", "asset_line1"])

        except:
            print("File not readable / doesn't exist, try again")


        ticker_list = input("Enter tickers w/ spaces (ex. AMZN AAPL GOOG): ")

        t = ticker_list.split(" ")
        print(t)

        try:

            parsed_data = search_tickers_ptr(new_data, t)

            option = input("Done parsing! Enter 's' to save or 'p' to print: ")

            if option == ("s" or "'s'"):
                saveAs = input("Enter location to save: ")

                parsed_data.to_csv(saveAs, index = False)

                print("Saved to " + saveAs)

            elif option == ("p" or "'p'"):
                print(parsed_data)
                
            break
        
        except Exception as ex:
            print("Error in parsing? Try again:")
            print(ex)

    

if __name__ == "__main__":
    run()
