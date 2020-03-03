# Part 1.: Data Exploration
# 1.1 : Can be found in exam.sh, under #1.1
# 1.2.
def read_year_to_anomaly_data(filename):
    """ Reads year and temperature anomaly data into a dictionary """
    openfile = open(filename, 'r') # Opens the file in read mode
    lines = openfile.readlines() # Return all lines in the file, as a list where each line is an item in the list object
    log_dict = {} # Creates dictionary
    for line in lines:
        if line[0] == ' ': # All pre-column lines star with %, so we can use whitespace as identifier
            year = int(line[2:6]) # Extracts the year by indexing as a float
            temperature = float(line[12:18]) # Extracts the temperature value by indexing as a float
            log_dict[year] = temperature # Appends the year as key with temperature as value to the dictionary
        else:
            continue
    return log_dict # Returns the dictionary

# 1.3.
import matplotlib.pylab as plt
def create_line_plot(data, out_filename):
    """Creates a line plot of the key,value pairs in a data set, set to a dictionary"""
    fig, ax = plt.subplots()
    dict = data # Defines dict as input data
    x = list(dict.keys()) # takes dict's keys as X-values
    y = list(dict.values()) # takes dict's values as Y-values
    plt.plot(x,y)
    plt.savefig(out_filename)
    return fig, ax

#Part 2.: Stripes:
# 2.1
from matplotlib.pyplot import get_cmap
class ColorMapper():
    def __init__(self, values, cmap_str='RdBu_r'):
        self.max_abs_value = max(values)
        self.cmap = get_cmap(cmap_str)

    def get_color(self, temp_value):
        """Normalises a given value to a range between 0 and 1, and returns the corresponding color in the color map """
        normalized_value = temp_value - (-self.max_abs_value)/(self.max_abs_value-(-(self.max_abs_value)))
        return self.cmap(normalized_value)

# 2.2.1
def construct_blocks(data, bottom=0.0, height=1.0):
    """returns a list of tuples with 5 elements, from a dictionary, with default width and height"""
    list_of_blocks = []
    for key in data:
        years = key
        anomaly = data.get(key)
        width = 1
        list_of_blocks.append((years, bottom, height, width, anomaly))
    return list_of_blocks

# 2.2.2 
def plot_blocks(list_of_blocks, color_mapper,
                colorbar=True,
                figure_width=20, figure_height=5):
    '''
    Visualize list of blocks, where each block is specified in the format
    (x-coordinate, y-coordinate, width, height, value). The color_mapper is
    used to look up colors corresponding to the values provided in each block.

    :param list_of_blocks: List of (x-coordinate, y-coordinate, width, height, value) tuples
    :param color_mapper: Used to lookup values for each block
    :param colorbar: Whether to include a color bar
    :param figure_width: Width of figure
    :param figure_height: Height of figure
    :return: None
    '''

    fig, ax = plt.subplots(1, figsize=(figure_width, figure_height))
    x_values = []
    y_values = []
    for block in list_of_blocks:
        rect = matplotlib.patches.Rectangle(block[:2], block[2], block[3],
                                            linewidth=1, edgecolor='none',
                                            facecolor=color_mapper.get_color(block[-1]))
        ax.add_patch(rect)
        x_values += [block[0], block[0]+block[2]]
        y_values += [block[1], block[1]+block[3]]

    ax.set_xlim(min(x_values), max(x_values))
    ax.set_ylim(min(y_values), max(y_values))

    if colorbar:
        from mpl_toolkits.axes_grid1 import make_axes_locatable
        divider = make_axes_locatable(plt.gca())
        ax_cb = divider.new_horizontal(size="1%", pad=0.1)
        matplotlib.colorbar.ColorbarBase(ax_cb, cmap=color_mapper.cmap,
                                         orientation='vertical',
                                         norm=matplotlib.colors.Normalize(
                                             vmin=-color_mapper.max_abs_value,
                                             vmax=color_mapper.max_abs_value))
    plt.gcf().add_axes(ax_cb)
    plt.show()

# 2.3
def calculate_anomalies_per_decade(dict):
    """calculates average anomalies per decade"""
    start = list(dict.keys())[0] # lists dict keys as start
    end = list(dict.keys())[len(dict) - 1] # lists the amount of keys, minus one, as end
    decade_to_avg_anomaly = {} # creates final output dict
    average_anomaly_per_decade =  [] #creates a list, used for calculus later
    for key in dict:
        average_anomaly_per_decade.append(dict[key]) # appends every dict key to list
        if key % 10 == 0 and key is not start: # if key value isn't modulo 0 and is not start
            decade_to_avg_anomaly[(key -10, key)] = round(sum(average_anomaly_per_decade) / float(len(average_anomaly_per_decade)), 3) # calculates average of the list
            del average_anomaly_per_decade[:] # resets the list before next iteration
            average_anomaly_per_decade.append(dict[key])
    if end % 10 != 0 : # makes it so last end decade is 2019 (which is not modulo 0)
        decade_to_avg_anomaly[(key -8, end + 1)] = round(sum(average_anomaly_per_decade) / float(len(average_anomaly_per_decade)), 3) #same calculation as before, but -8 to start 2010
    return decade_to_avg_anomaly

# Part 3: Looking at latitudes
# 3.1.
def read_latitude_year_to_anomaly_data(filename):
    """reads data to a nested dictionary with latitude as outer keys, years as inner key and temperature anomaly as inner key"""
    openfile = open(filename,'r') # Opens the file in read mode
    dict_of_dicts = {} # Creates the dictionary-containing dictionary
    for line in openfile: # iterates over the items/lines in the list
        year = int(line[0:4]) # Extract the year-value and converts it into an integer
        latitude = float(line[5:9]) # Extract the latitude-value and converts it into a float
        anomaly = float(line[9:16]) # Extract the anomaly-value and converts it into a float
        if dict_of_dicts.get(latitude): # Checks for new key "latitude"-value in dict
            dict_of_dicts[latitude].update({year: anomaly}) # If it's there, update(!!) the outer key value with nested dict of year:anomaly
        else:
            dict_of_dicts[latitude] = {year: anomaly} # If it's not there, creates the key as outer dict key with inner dict of year:anomaly
    return dict_of_dicts

# 3.2
def get_values_from_nested_dict(nested_dict):
    """reads nested dictionary values into a list"""
    list_of_values = [] #creates a list
    for latitude in nested_dict.values(): #for each outer key in nested dictionary (name 'latitude' is optional, but indicative for this dataset)
        for year in latitude: # for each inner key for outer key
            list_of_values.append(latitude[year]) # appends inner values to the list
    return list_of_values


# 3.3
def construct_latitude_blocks(nested_dict):
    """reads a nested dictionary to a list of tuples with 5 elements, with default width and height"""
    list_of_tuples = [] #creates a list
    for latitude in nested_dict.keys(): #for each outer key in nested dict (variable name 'latitude' is optionally used for easier read for this specific dataset)
        for year in nested_dict[latitude].keys(): #for each inner key in outer key
           summary = (year, latitude, 1, 5, nested_dict[latitude][year]) #creates a tuple with the 5 elements, last being inner key in nested dictionary
           list_of_tuples.append(summary) #appends tuple to a list of tuples
    return list_of_tuples

# Part 4: Co2 emissions
# 4.1 is an Unix-task and can be found in exam.sh, beneath '#4.1'.
# 4.2.1
def sorting_first_index(tuple_selected):
    """sorts a tuple by first index"""
    return tuple_selected[1]
def find_top10_emitting_countries(filename):
    """returns the top ten countries, sorted by highest co2 emission"""
    openfile = open(filename,'r') # opens file in read mode
    country_list = [] # creates a list
    lines = openfile.readlines() # reads each line as string in a list
    for line in lines:
        naked_line = line.strip().split(',') # strips trailing characters, and splits the string by ','
        if 'Population' in naked_line or len(naked_line[1]) != 3: # if country code is not 3 characters, then move on
            continue
        else: # if country code is 3 characters, then
            country_list.append((naked_line[0],int(naked_line[2]),float(naked_line[3]))) # appends country name, year and emission to the list
    country_list = sorted(country_list,key= sorting_first_index, reverse= True)
    year_list = [] # creates a separate list for year
    for item in country_list:
        year_list.append(item[1]) # appends year-value to the year-list
    topten = [] # creates a list for the final output
    for item in country_list:
        if item[1] == max(year_list): # if year-value is equal to highest value of year-list, then
            topten.append((item[0],item[2])) # append country name and emission to final output list
        topten = sorted(topten,key = sorting_first_index, reverse= True)[0:10] # sort the already ascending list to descinding order, include only the top 10
    return topten

# 4.2.2
import matplotlib
def plot_emissions(list_of_tuples, population_dict=None, figure_width=15, figure_height=5):
    '''
    Create a bar plot of CO2 emissions. If population_dict is provided, resize
    bars so that width reflect population size and height denotes emission per
    capita.

    :param list_of_tuples: List of (country-name, value) tuples
    :param population_dict: Dictionary of (country-name, population) pairs
    :param figure_width: Width of figure
    :param figure_height: Height of figure
    :return:
    '''

    # Create new figure
    fig,ax = plt.subplots(1, figsize=(figure_width, figure_height))

    # Choose color map
    cmap = plt.get_cmap("Spectral")

    heights = []
    labels = []
    widths = []
    colors = []
    for i, entry in enumerate(list_of_tuples):
        heights.append(entry[1])
        # Scale down height of bar with population size
        if population_dict is not None:
            heights[-1] /= population_dict[entry[0]]
        labels.append(entry[0])
        colors.append(cmap(i/len(list_of_tuples)))
    if population_dict is None:
        x = range(len(list_of_tuples))
        widths = [0.9] * len(list_of_tuples)
    else:
        max_width = 0
        for entry in list_of_tuples[:-1]:
            max_width = max(max_width, population_dict[entry[0]])
        x = np.arange(len(list_of_tuples)) * max_width
        for entry in list_of_tuples:
             widths.append(population_dict[entry[0]])

    # Create bar plot and set tick values
    plt.bar(x, height=heights, width=widths, color=colors)
    plt.ylabel("Annual CO2 emissions (tonnes)")
    plt.xticks(x, labels, rotation=45, ha="right")
    plt.show()

# 4.3:
def read_population_data(data, year):
    """read co2 emission per capita into a dictionary"""
    new_dict = {} # creates a dictionary
    openfile = open(data,'r') # opens the file in read mode
    lines = openfile.readlines()[1:] # turns each line to list of strings, skipping the first (header) line
    for line in lines:
        line = line.rstrip() # strips trailing characters
        line = line.split(',') # splits each string in the list by ','
        if str(year) in line: # if the year-argument, turned into a string to compare, with value in line
            country, code, year, population = line # name the strings in string (line)
            country = line[0]  # country is the first string in line
            population = line[3] # population is fourth string in line
            new_dict[country] = population # append with country as key, with population as value
    return new_dict
