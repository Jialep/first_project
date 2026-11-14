'''
purpose of this core is to refactor code, converting hard coded checks
into functions which can be accessed by every interface through importing
'''

def get_events(calendar_data,date_key): #takes in dict and key
    return calendar_data.get(date_key,[]) #return value else [] if not key
