import pandas as pd
from parser import parse_chat

def run_analysis():
    file_name = 'chat.txt'
    chats = parse_chat(file_name) #Use parse_chat to go through a file to make it a dictionary
    df = pd.DataFrame(chats) #Convert dictionary to dataframe (4 columns: date, time, user, text)
    finalDataDict = {} #After all the work is done, results will be stored here to export into JSON for react
    globalSubDict = {} #global sub dictionary for finalDataDict
    finalDataDict['global'] = globalSubDict
    globalNameSubDict = {} #name sub dictionary for global sub dictionary
    globalSubDict['names'] = globalNameSubDict
    



    if df.empty:
        print("No chat data found.")
        return

    # Normalize user names
    df['user'] = df['user'].replace("Mon amie La Rose", "Sam Landry") 

    # Extract metrics using pandas string operations
    df['word_count'] = df['text'].str.split().str.len() #Convert text column strings to array split by whitespace and get the length to get number of words for every text
    df['question_count'] = df['text'].str.count(r'\?') #Count the number of question marks in each text
    df['exclamation_count'] = df['text'].str.count('!') #Count the number of exclamations in each text

    # Aggregate per user global stats of message count, word count, question count, exclamation count
    user_stats = df.groupby('user').agg(
        messages=('user', 'count'),
        words=('word_count', 'sum'),
        questions=('question_count', 'sum'),
        exclamations=('exclamation_count', 'sum')
    )

    #Global total messages
    for name, count in user_stats['messages'].items():
        finalDataDict['global']['names']['msgCount'] = count
    print(finalDataDict)
    print("\nEngagement Ratio")
    engagement = user_stats['words'] / user_stats['messages']
    for name, ratio in engagement.items():
        print(f'{name} : {ratio:.2f}')

    print("\nHype meter (Questions, Exclamations)")
    for name, row in user_stats.iterrows():
        print(f"{name} : {int(row['questions'])}, {int(row['exclamations'])}")

    # Golden Age (3-month window)
    df['date'] = pd.to_datetime(df['date'])
    monthly = df.set_index('date').resample('ME').size()
    
    if not monthly.empty:
        # Calculate a 3-month rolling sum of messages
        rolling_3m = monthly.rolling(window=3).sum()
        max_msgs = rolling_3m.max()
        if pd.notna(max_msgs):
            end_date = rolling_3m.idxmax()
            start_date = end_date - pd.DateOffset(months=2)
            print(f"\nGolden Age: {start_date.strftime('%Y-%m')} to {end_date.strftime('%Y-%m')} ({int(max_msgs)} messages)")

    # Active Time Window Analysis (Approximating IST to MST shift of -12 hours)
    df['hour_ist'] = df['time'].str.split(' h ').str[0].astype(int)
    df['hour_mst'] = (df['hour_ist'] - 12) % 24
    
    bins = [0, 4, 8, 12, 16, 20, 24]
    labels = ["00:00 - 04:00", "04:00 - 08:00", "08:00 - 12:00", "12:00 - 16:00", "16:00 - 20:00", "20:00 - 00:00"]
    df['window'] = pd.cut(df['hour_mst'], bins=bins, labels=labels, right=False)
    
    window_counts = df['window'].value_counts()
    if not window_counts.empty:
        most_active = window_counts.idxmax()
        print(f"\nMost Active Time Window: {most_active} (MST) ({window_counts.max()} total messages)")

if __name__ == "__main__":
    run_analysis()
