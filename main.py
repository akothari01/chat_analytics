from parser import parse_chat

def run_analysis():
    file_name = 'chat.txt'
    chats = parse_chat(file_name)

    user_stats = {}

    for chat in chats:
        name = chat['user']
        if name == "Mon amie La Rose":
            name = "Sam Landry"

        if name not in user_stats:
            user_stats[name] = {
                'messages': 0,
                'words': 0,
                'questions': 0,
                'exclamations': 0
            }

        stats = user_stats[name]
        stats['messages'] += 1

        line = chat['text']
        stats['words'] += len(line.split())

        stats['questions'] += line.count('?')
        stats['exclamations'] += line.count('!')

    print("Total Messages")
    for name, stats in user_stats.items():
        print(f'{name} : {stats["messages"]}')

    print("\nEngagement Ratio")
    for name, stats in user_stats.items():
        ratio = stats['words'] / stats['messages'] if stats['messages'] > 0 else 0
        print(f'{name} : {ratio:.2f}')

    print("\nHype meter (Questions, Exclamations)")
    for name, stats in user_stats.items():
        print(f"{name} : {stats['questions']}, {stats['exclamations']}")

    # Find the 3-month window with the most texts
    from collections import defaultdict
    from datetime import datetime
    from dateutil.relativedelta import relativedelta

    monthly_counts = defaultdict(int)
    for chat in chats:
        # Extract year and month (YYYY-MM)
        month_key = chat['date'][:7]
        monthly_counts[month_key] += 1

    if monthly_counts:
        # Get sorted list of all months present in the data
        sorted_months = sorted(monthly_counts.keys())
        start_date = datetime.strptime(sorted_months[0], "%Y-%m")
        end_date = datetime.strptime(sorted_months[-1], "%Y-%m")

        max_messages = -1
        golden_age = (None, None)

        current_window_start = start_date
        while current_window_start <= end_date:
            window_messages = 0
            # Define the 3-month window
            window_months = []
            for i in range(3):
                m = (current_window_start + relativedelta(months=i)).strftime("%Y-%m")
                window_months.append(m)
            
            for m in window_months:
                window_messages += monthly_counts.get(m, 0)

            if window_messages > max_messages:
                max_messages = window_messages
                golden_age = (window_months[0], window_months[-1])
            
            current_window_start += relativedelta(months=1)

        print(f"\nGolden Age: {golden_age[0]} to {golden_age[1]} ({max_messages} messages)")

    # Find the 4-hour window with the most texts on average
    # Windows: 00-04, 04-08, 08-12, 12-16, 16-20, 20-00
    hourly_windows = {
        "00:00 - 04:00": 0,
        "04:00 - 08:00": 0,
        "08:00 - 12:00": 0,
        "12:00 - 16:00": 0,
        "16:00 - 20:00": 0,
        "20:00 - 00:00": 0
    }

    for chat in chats:
        # Time format is "HH h MM" based on MESSAGE_REG
        hour = int(chat['time'].split(' h ')[0])
        
        if 0 <= hour < 4:
            hourly_windows["00:00 - 04:00"] += 1
        elif 4 <= hour < 8:
            hourly_windows["04:00 - 08:00"] += 1
        elif 8 <= hour < 12:
            hourly_windows["08:00 - 12:00"] += 1
        elif 12 <= hour < 16:
            hourly_windows["12:00 - 16:00"] += 1
        elif 16 <= hour < 20:
            hourly_windows["16:00 - 20:00"] += 1
        else:
            hourly_windows["20:00 - 00:00"] += 1

    if hourly_windows:
        most_active_window = max(hourly_windows, key=hourly_windows.get)
        # Convert IST to MST (IST is UTC+5:30, MST is UTC-7:00)
        # Difference is 12 hours and 30 minutes. 
        # For simplicity in 4-hour blocks, we shift the window labels by -12.5 hours.
        mst_windows = {}
        for window, count in hourly_windows.items():
            start_hour = int(window.split(':')[0])
            # (start_hour - 12.5) % 24. We'll approximate to -12 for the block mapping.
            mst_start = (start_hour - 12) % 24
            mst_end = (mst_start + 4) % 24
            mst_label = f"{mst_start:02d}:00 - {mst_end:02d}:00 (MST)"
            mst_windows[mst_label] = count
        
        most_active_window = max(mst_windows, key=mst_windows.get)
        hourly_windows = mst_windows # Update for the print statement

        print(f"\nMost Active Time Window: {most_active_window} ({hourly_windows[most_active_window]} total messages)")


if __name__ == "__main__":
    run_analysis()
