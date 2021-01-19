import pandas as pd
import PySimpleGUI as sg

def read_data():
    
    #Get the json-file and read it into a dataframe
    url = "https://raw.githubusercontent.com/solita/dev-academy-2021/main/names.json"
    df = pd.read_json(url, orient='records')
    
    #Format the name and amount columns
    df['name'] = df['names'].apply(lambda x: x['name'])
    df['amount'] = df['names'].apply(lambda x: x['amount'])
    df = df[['name', 'amount']]
    
    #Sort names by the most popular
    df_most_popular = df.sort_values('amount', ascending=False).reset_index(drop=True)
    df_most_popular['fnames'] = df_most_popular.apply(lambda x: str(x['name'])+": "+str(x['amount']), axis=1)
    
    #Sort names in alphabetical order
    df_alphabetical = df.sort_values('name')
    
    #Sum the names for total value
    df_sum = df['amount'].sum()
    
    return df, df_most_popular, df_alphabetical, df_sum

def main():
    
    data = read_data()
    
    #Define column with charts
    name_list_column = [
        [
             sg.Listbox(values=[], enable_events=True, size=(40, 20), key="charts")
        ]
    ]
    
    #Define column with buttons and input box
    button_column = [
        [
             sg.Button("Order By Amount")
        ],
        [
             sg.Button("Alphabetical Order")
        ],
        [
             sg.Button("Total Amount")
        ],
        [
             sg.Text("Submit a Name")
        ],
        [
             sg.Input(size=(25, 1), enable_events=True, key="name_input"), sg.Button("Submit")
        ],
        [
             sg.Button("Exit")
        ]
    ]
    
    #Define the layout with vertical separation
    layout = [
        [
            sg.Column(name_list_column),
            sg.VSeparator(),
            sg.Column(button_column)
        ]
    ]
    
    #Define the GUI
    window = sg.Window("Name Application", layout, return_keyboard_events=True)
    
    #While event to open the GUI
    while True:
         event, values = window.read()
         
         #Order by amount button formats the column to list
         if event == "Order By Amount":
             fnames = data[1]['fnames'].tolist()
             
             #Update the text box
             window["charts"].update(fnames)
         
         #Alphabetical order button formats the column to a list
         elif event == "Alphabetical Order":
             fnames = data[2]['name'].tolist()
             
             #Update the text box
             window["charts"].update(fnames)
         
         #Total amount button formats the sum value to string
         elif event == "Total Amount":
             name_sum = ["Total amount of all the names: "+str(data[3])]
             
             #Update the text box
             window["charts"].update(name_sum)
          
         #Submit button checks the name given
         elif event == "Submit":
             
             #Variable for user input and check for match
             name_given = values['name_input'].capitalize()
             
             #Check if submit is empty
             if name_given == '':
                 name_check = ["Please enter a name"]
             else:
                 amount = data[0]['amount'].loc[data[0]['name']==name_given]
             
                 #If a match is found, get the amount as a string
                 if amount.size == 1:
                     name_check = ["Amount of persons with given name: "+str(amount.iloc[0])]
                 
                    #If no match is found, error text
                 else:
                     name_check = ["Submitted name not found"]
                 
             #Update the text box
             window["charts"].update(name_check)
             
             
         #Close the window   
         elif event == "Exit" or event == sg.WIN_CLOSED:
             break
    
    window.close()

main()