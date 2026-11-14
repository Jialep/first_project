def get_events(calendar_data,date_key): #takes in dict and key
    return calendar_data.get(date_key,[]) #return value else [] if not key
