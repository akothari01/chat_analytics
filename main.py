from parser import parse_chat

def run_analysis():
    file_name = 'chat.txt'
    chats = parse_chat(file_name)
    messageDict = {}
    wordDict = {}
    for chat in chats:
        name = chat['user']
        if name == "Mon amie La Rose" : name = "Sam Landry"
        messageDict[name] = messageDict.get(name, 0) + 1
        line = chat['text']
        wordLine = line.split(' ')
        wordDict[name] = wordDict.get(name,0) + len(wordLine)
    print("Total Messages")
    for name, count in messageDict.items():
        print(f'{name} : {count}')
    print("Engagement Ratio")
    for name, count in messageDict.items():
        print(f'{name} : {wordDict[name] / count}')


if __name__ == "__main__":
    run_analysis()
