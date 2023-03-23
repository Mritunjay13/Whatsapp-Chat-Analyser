import pandas as pd
import re

def preprocess(data):
    pattern= '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s[\w][\w][\s]-'
    messages= re.split(pattern, data)[1:]
    dates= re.findall(pattern, data)
    
    df= pd.DataFrame({'user_message': messages, 'message_date': dates})

    df['message_date']= pd.to_datetime(df['message_date'],format='%d/%m/%Y, %I:%M %p -')

    # df.rename(columns={'message_date': 'date'}, inplace=True)
    
    df['date']= df['message_date'].dt.date
    df['time']= df['message_date'].dt.time
    
    
    users= []
    messages=[]
    for message in df['user_message']:
        entry= re.split('([\w\W]+?):\s', message)
        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            for i in entry:
                entry2= re.split('([\w\W]+?)\sj', i)
                if entry2[1:]:
                    users.append(entry2[1])
                    messages.append('joined to group')
                else:
                    for i in entry2:
                        entry3= re.split('([\w\W]+?)\sadded',i)
                        if entry3[1:]:
                            users.append(entry3[2])
                            messages.append("added to group")
                        else:
                            users.append('group_notification')
                            messages.append(entry2[0])
    
                    
                    
    df['user']= users
    df['message']= messages
    df.drop(columns=['user_message'], inplace= True)

    df['year']= df['message_date'].dt.year
    df['month_num']= df['message_date'].dt.month
    df['month']= df['message_date'].dt.month_name()
    df['day']= df['message_date'].dt.day
    df['day_name']= df['message_date'].dt.day_name()
    df['hour']= df['message_date'].dt.hour
    df['minute']= df['message_date'].dt.minute
    df.drop(columns=['message_date'], inplace= True)

    return df