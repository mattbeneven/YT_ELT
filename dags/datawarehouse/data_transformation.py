from datetime import timedelta, datetime

# 
# Example: duration_str = "P1DT2H30M45S"
def parse_duration(duration_str):

    # Replacing "P" and "T" with "", as they are not needed for our purpose.
    duration_str = duration_str.replace("P", "").replace("T", "")

    components = ['D', 'H', 'M', 'S']
    values = {"D": 0, "H": 0, "M": 0, "S": 0}

    for component in components:
        # splitting duration_str by the component ('D', 'H', 'M', or 'S'), 
        # and returning the preceding number as value, and the remaining string as the new duration_str
        if component in duration_str:
            value, duration_str = duration_str.split(component)
            # assigning the correct values into the dictionary values
            values[component] = int(value)

    total_duration = timedelta(
        days=values["D"], hours=values["H"], minutes=values["M"], seconds=values["S"]
    )

    return total_duration

def transform_data(row):

    duration_td = parse_duration(row['Duration'])

    # updating 'Duration' column to give a readable value
    # datetime.min is the earliest possible datetime in python. This is used so that we can return in the form "HH:MM:SS"
    row['Duration'] = (datetime.min + duration_td).time()

    # adding column Video_Type
    # defining Youtube Shorts as videos of duration 60 seconds or less. Anything else as a normal YT video
    row['Video_Type'] = "Shorts" if duration_td.total_seconds() <= 60 else "Normal"

    return row