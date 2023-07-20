import MotleyScrape as motley


# Define a function to extract stock ticker symbols using regex

def exportToCSV(dataFr):
    dataFr.to_csv("file.csv")
    pass

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    motley.motleyFoolScrape()
