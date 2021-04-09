import os
import pandas as pd

# initialize the excel writer and output file
writer = pd.ExcelWriter('csv_merged.xlsx', engine='xlsxwriter')

# clear default header formatting
import pandas.io.formats.excel
pandas.io.formats.excel.ExcelFormatter.header_style = None

# create a list of .csv filenames
csv_file_list = [f for f in os.listdir('.') if f.endswith('.csv')]
# sort list
csv_file_list.sort()

# loop for merging of csv files
for i in csv_file_list:
    if 'objects' in i:
        objects_df = pd.read_csv(i, nrows=1) # read just the first line for columns
        objects_columns = objects_df.columns.tolist() # get the columns
        objects_cols_to_use = objects_columns[:len(objects_columns)-1] # drop the last empty column
        objects_df = pd.read_csv(i, usecols=objects_cols_to_use) # re-read csv without last empty column

    elif 'ztraces' in i:
        ztraces_df = pd.read_csv(i, nrows=1)
        ztraces_columns = ztraces_df.columns.tolist()
        ztraces_cols_to_use = ztraces_columns[:len(ztraces_columns)-1]
        ztraces_df = pd.read_csv(i, usecols=ztraces_cols_to_use)
        
        # since this elif is performed last based on sort, do these next three steps here
        # concatenate the list of dataframes
        log = []
        log_df = pd.DataFrame(log, columns = ['Log'])
        merged_df = pd.concat([log_df, objects_df, ztraces_df, traces_df], axis=1)
         
        # create sheet name
        str_split = i.split("ztraces")
        dend_sheet_name = str_split[0]
        dend_sheet_name = dend_sheet_name.upper()

        # write dataframe to xlsx file with sheetname
        merged_df.to_excel(writer, sheet_name = dend_sheet_name, index=False) 

    else:
        traces_df = pd.read_csv(i, nrows=1)
        traces_columns = traces_df.columns.tolist()
        traces_cols_to_use = traces_columns[:len(traces_columns)-1]
        traces_df = pd.read_csv(i, usecols=traces_cols_to_use)
        # reorder this dataframe so 'Trace' is the first column
        reorder = traces_df['Trace']
        traces_df.drop(labels=['Trace'], axis=1, inplace = True)
        traces_df.insert(0, 'Trace', reorder)

# close the pandas excel writer and output the excel file
writer.save()