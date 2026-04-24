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


if __name__ == "__main__":
    run_analysis()
