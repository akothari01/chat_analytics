import re

MESSAGE_REG = r'^(\d{4}-\d{2}-\d{2}), (\d{2} h \d{2}) - (.*?): (.*)'


def parse_chat():
    data = []
    with open('chat.txt', 'r', encoding='utf-8') as f:
        for line in f:
            cleanLine = line.strip()
            if not cleanLine:
                continue
            match = re.match(MESSAGE_REG, cleanLine)
            if match:
                newMessage = {
                    'date': match.group(1),
                    'time': match.group(2),
                    'user': match.group(3),
                    'text': match.group(4)
                }
                data.append(newMessage)
            elif data:
                data[-1]['text'] += " " +  cleanLine
            else:
                continue
    return data

if __name__ == "__main__":
    chats = parse_chat()
    leaderboard = {}
    for i in chats:
        name = i['user']
        leaderboard[name] = leaderboard.get(name, 0) + 1
    for name,count in leaderboard.items():
        print(f"{name} : {count}")
        
