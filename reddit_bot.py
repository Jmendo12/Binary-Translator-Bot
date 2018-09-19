import praw
import config
import time
import os.path

#Log into reddit, and print to the console upon successful login
def botLogin():
    
    print "Logging in..."
   
    r = praw.Reddit(username = config.username,
                    password = config.password,
                    client_id = config.client_id,
                    client_secret = config.client_secret,
                    user_agent = "Binary_TranslatorBot V0.1")
    
    print "Logged in"
    return r

def runBot(r, commentsRepliedTo, binaryToDecimal, replyString):
    
    
    for comment in r.subreddit('test').comments(limit = 25):
       
        #Create a string of the comment body 
        commentString = comment.body
        i = 0
       
        #Break string up into sections of 8 bits, assuming there is a space between each 8 bit sequence
        while i <= len(commentString) - 8 and comment.id not in commentsRepliedTo and not comment.author == r.user.me:
            currentKey = commentString[i : i + 8]
            i = i + 9
           
            #Compare the 8 bit sequence to the key's in our dictionary; if a key matches, pass that key's value to chr()            # to construct a string based on the ascii value 
            for k , v in binaryToDecimal.items():
                if k in currentKey:
                    currentChar = chr(v)
                    replyString = replyString + currentChar
                    print replyString
      
        #If a replyString exists after cycling through the comment and comparing it to the key's in our dictionary reply        # to the comment with the translated string     
        if replyString and comment.id not in commentsRepliedTo and not comment.author == r.user.me:
            comment.reply("Translation: " + replyString)
            commentsRepliedTo.append(comment.id)
            #Write the comment ID to our file so that upon execution, we don't reply to comments we've already replied
            # to
            with open("comments_replied_to.txt", "a") as f:
                f.write(comment.id + "\n")
            # Reset the replyString to an empty string
            replyString = ""
   
    print "Sleeping for ten seconds"    
    time.sleep(10);

#This function gets comments that the bot has replied to from a text file, and puts them into the commentsRepliedTo list, so that the bot knows what comments it has already responded to
def getSavedComments():
    
    if not os.path.isfile("comments_replied_to.txt"):
        commentsRepliedTo = []
    else:
        with open("comments_replied_to.txt", "r") as f:
            commentsRepliedTo = f.read()
            commentsRepliedTo = commentsRepliedTo.split("\n")
            commentsRepliedTo = filter(None, commentsRepliedTo)
        
    return commentsRepliedTo

r = botLogin()

#Create a list of comments we have responded to, so we don't respond to them
#multiple times
commentsRepliedTo = getSavedComments()
#print commentsRepliedTo

#Create a Python Dictionary for Binary-Decimal key value pairs
binaryToDecimal = dict({"01000001": 65, "01000010": 66, "01000011": 67, "01000100": 68, "01000101": 69, "01000110": 70, 
    "01000111": 71, "01001000": 72, "01001001": 73, "01001010": 74, "01001011": 75, "01001100": 76, "01001101": 77, "01001110": 78, "01001111": 79, "01010000": 80, "01010001": 81, "01010010": 82, "01010011": 83, "01010100": 84, "01010101": 85, "01010110": 86, "01010111": 87, "01011000": 88, "01011001": 89, "01011010": 90, "01100001": 97, "01100010": 98, "01100011": 99, "01100100": 100, "01100101": 101, "01100110": 102, "01100111": 103, "01101000": 104, "01101001": 105, "01101010": 106, "01101011": 107, "01101100": 108, "01101101": 109, "01101110": 110, "01101111": 111, "01110000": 112, "01110001": 113, "01110010": 114, "01110011":115, "01110100": 116, "01110101": 117, "01110110": 118, "01110111": 119, "01111000": 120, "01111001": 121, "01111010": 122})

replyString = ""

while True:
    runBot(r, commentsRepliedTo, binaryToDecimal, replyString)
