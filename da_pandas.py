"""
        US Congress Financial Disclosure Analysis Python File by Benjamin Riseman, 2021

        As a few functions built around searching for tickers in excel documents provided
        by other algorithms of the database.

"""




import pandas, os, pathlib

""" Simply debug for the console, lets me see more of the dataframes """

pandas.set_option('display.max_rows', 500)
pandas.set_option('display.max_columns', 20)
pandas.set_option('display.width', 1000)


def search_tickers_disclosures(df : pandas.DataFrame, ticker_list : list, ignore_index: bool = True, add_median: bool = True, add_net_worth: bool = True, add_percent: bool = True) -> pandas.DataFrame:
    """
        Master function that generates a new DataFrame with asked-for tickers.
        Important parameters are the input DataFrame, and a ticker list, like ["AMZN", "AAPL", "GOOG"].

        Rest of the parameters add / modify columns of the newly-generated DataFrame.
        Recommended to be kept enabled.
        
    """

    if add_net_worth:
        cols = ["last_name", "filing_year",
               "min_value", "max_value", "net_worth", "ticker"]
    else:
        cols = ["last_name", "filing_year",
               "min_value", "max_value", "ticker"]
    mega_frame = pandas.DataFrame(columns = cols)
    
    for index, row in df.iterrows():
        for tick in ticker_list:
            if tick in row.values:
                if add_net_worth:
                    row["net_worth"] = get_net_worth(row["last_name"])[2]
                mega_frame = mega_frame.append(row, ignore_index = ignore_index)

    
    mega_frame = create_median(mega_frame) if add_median else None
    mega_frame = create_percent_total(mega_frame) if add_percent else None

    return mega_frame


def create_median(df : pandas.DataFrame) -> pandas.DataFrame:
    """ Generates a median column in the provided DataFrame. Returns a modified copy. """

    df2 = df.copy()

    try:

        df2["min_value"] = df2["min_value"].str.replace(r'\D', '')
        df2["max_value"] = df2["max_value"].str.replace(r'\D', '')

    except Exception as ex:
        print(ex)

    else:

        df2["min_value"] = df2["min_value"]
        df2["max_value"] = df2["max_value"]

    df2.insert(4, "median_value", (pandas.to_numeric(df2["min_value"]) +
                           pandas.to_numeric(df2["max_value"])) / 2)

    return df2


def create_percent_total(df : pandas.DataFrame) -> pandas.DataFrame:
    """ Generates a 'percent of net worth' column for the requested asset for the requested person.
        Returns a modified copy. """

    df2 = df.copy()

    df2.insert(6, "percent_of_total", (pandas.to_numeric(df2["median_value"]) / pandas.to_numeric(df2["net_worth"]) * 100))

    return df2

def get_person(last_name : str) -> tuple:
    """ Returns an unfiltered DataFrame with a person's holdings, given by last name. """
    
    person_frame = da_doc[new_data["last_name"] == last_name]
    
    return person_frame

def get_net_worth(last_name : str) -> tuple:
    """ Calculates net worth based on last name in the form of a string.
        Return a tuple in the form (min_value, max_value, median_value)."""

    total = 0

    person_frame = new_data[new_data["last_name"] == last_name]

    person_frame.loc[person_frame['min_value'] == "BLANK", 'min_value'] = 0
    person_frame.loc[person_frame['max_value'] == "BLANK", 'max_value'] = 0

    person_frame["min_value"] = person_frame["min_value"].str.replace(r'\D', '')
    person_frame["max_value"] = person_frame["max_value"].str.replace(r'\D', '')

    min_value = pandas.to_numeric(person_frame["min_value"]).sum()
    max_value = pandas.to_numeric(person_frame["max_value"]).sum()
    median_value = (min_value + max_value) / 2
            
    return (min_value, max_value, median_value)

def run():
    """ Automatically runs search_tickers w/ a file and ticker list input. """
    

    while True:

        print("Disclosure Analysis by Benjamin Riseman, 2021")

        fileLoc = input("Enter file location, 'h' for house, 's' for senate, or 'q' for quit: ")

        cur_path = os.getcwd() # Changed method of getting cwd

        if fileLoc == ("s" or "'s'"):
            fileLoc = os.path.join(cur_path,"Senate-Annual-Master.csv") #Changed Path Construction to be more universal

        elif fileLoc == ("h" or "'h'"):
            fileLoc = os.path.join(cur_path,"House-Annual-Master.csv") #Changed Path Construction to be more universal

        elif fileLoc == ("q" or "'q'"):
            break

        try:
            x = os.path.join(fileLoc)
            global da_doc
            da_doc = pandas.read_csv(x,encoding='iso-8859-1') # Changed encoding format
            global new_data

            new_data = da_doc.filter(items = ["last_name", "filing_year",
                                          "min_value", "max_value", "ticker"])

        except:
            print("File not readable / doesn't exist, try again")


        ticker_list = input("Enter tickers w/ spaces (ex. AMZN AAPL GOOG): ")
        

        t = ticker_list.split(" ")
        print(t)

        try:

            parsed_data = search_tickers_disclosures(new_data, t)

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


