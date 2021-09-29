import requests

# access token from facebook graph api explorer
access_token = ''

# gets all comments from instagram post id and puts them in "comments.txt"
def getComments():
    global access_token
    # giveaway post id from facebook graph api explorer
    post_id = str()
    # after string found in the "after" part in the fb stuff
    after_str = ''
    # limit of commments
    lim = '25'
    # original string
    final_str = ''

    while True:
        format = "https://graph.facebook.com/v12.0/" + post_id + "/comments?access_token=" + access_token + "&pretty=0&limit=" + lim + "&after=" + after_str
        req = requests.get(format)
        result = req.text
        final_str += result
        
        # get the "after" and put that into the "next" section of the code:
        after_str = getAfter(result)
        if after_str == '':
            print('All comments have been found')
            break
    
    resultFile = open("comments.txt", "w")
    resultFile.write(final_str)
    resultFile.close()
    print("Comments are: \n" + final_str)

def getAfter(str):
    afterStart = str.find('&after=') + 7
    afterEnd = str.find('"}}')
    if afterStart == -1 or afterEnd == -1:
        return ('')
    return str[afterStart:afterEnd]

# gets ids from .txt file of comments and puts them in "ids.txt"
# param: .txt file of all comments string
def getIds(str):
    file = open(str, "r")
    resultFile = file.read()
    file.close()

    # source: https://stackoverflow.com/questions/3873361/finding-multiple-occurrences-of-a-string-within-a-string-in-python
    ids = []
    idStart = 0
    while idStart < len(resultFile):
        idStart = resultFile.find('"id":"', idStart)
        idEnd = resultFile.find('"}', idStart)  
        if idStart == -1 or idEnd == -1:
            break
        ids.append(resultFile[idStart + 6:idEnd])
        idStart += 6
    
    idFile = open("ids.txt", "w")
    for id in ids:
        idFile.write(id + '\n')
    idFile.close()
    print("IDs are:")
    print(ids)

# returns names (up to a max num of instances) from .txt file of ids and puts them in "names.txt"
# param: .txt file of names, max num of name instances
def getNames(idFile, nameMax):
    names = []
    file = open(idFile, "r")
    ids = file.readlines()
    nameFile = open("names.txt", "w")

    for id in ids:
        format = "https://graph.facebook.com/v12.0/" + id.rstrip('\n') + "?fields=username&access_token=" + access_token
        req = requests.get(format)
        name = req.text
        nameStart = name.find('":"') + 3
        nameEnd = name.find('","')
        # only add to names + write to file if the number of names is less than the max
        if names.count(name[nameStart:nameEnd]) < nameMax:
            names.append(name[nameStart:nameEnd])
            nameFile.write(name[nameStart:nameEnd] + '\n')

    nameFile.close()
    print("Names are:")
    print(names)

# getComments()
# getIds("comments.txt")

# put number of instances you want to allow in max
# max = 
# getNames("ids.txt", max)