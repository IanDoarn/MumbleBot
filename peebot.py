from twisted.python.rebuild import rebuild
import mumble_client as mc
import mumble_protocol as mp
import peebot
import sys
import random

users = ['Mrs.Santos',
         'zab',
         'Dartrunner',
         'Razz',
         'Tot',
         'Ghost',
         'Johnny',
         'Canadia',
         'Sammy',
         'Duke',
         'Kaz',
         'Timmy',
         'baxterhusky',
         'Batboy272']
prefixes = ['Its-me-',
            'I-am-the-real-',
            'Small-boy-',
            'Little-',
            'Not-actually-',
            'Bot-',
            'fuccboi-',
            'Sad-',
            'Literally-cancer-',
            'Large-boy-',
            'Gay-']
musicPre = ['Why not ',
            'Try ',
            'Maybe some ',
            'You should try ',
            'I like ',
            'What would be really calming is ',
            'What always gets me going is ']     
ball = ['It is certain',
         'It is decidedly so',
         'Without a doubt',
         'Yes, definitely',
         'You may rely on it',
         'As I see it, yes',
         'Most likely',
         'Outlook good',
         'Yes',
         'Signs point to yes',
         'Reply hazy try again',
         'Ask again later',
         'Better not tell you now',
         'Cannot predict now',
         'Concentrate and ask again',
         'Dont count on it',
         'My reply is no',
         'My sources say no',
         'Outlook not so good',
         'Very doubtful']
myName = random.choice(users)
myPrefix = random.choice(prefixes)
OWNER = "baxterhusky"  # Your mumble nickname
SERVER_IP = "cultofcaprisun.murmur.nfoservers.com"  # Server IP
SERVER_PORT = 3220  # Server PORT
#USERNAME = myName + "." # Bot's name
USERNAME = myPrefix + myName


# Use empty string for optional fields to remove
PASSWORD = ""  # Optional password
CERTIFICATE = ""  # Optional certificate

helptxt = """
<!DOCTYPE html>
<html>
<body>

<h2>I am the Capri Sun Corner Bot.</h2>
<h>Avalibale commands:</h>
<ul>
  <li>/insult [username] - Insult a user</li>
  <li>/feeling           - Random emotion</li>
  <li>/whoami            - Give yourself a backstory</li>
  <li>/rtd [dice number] - Roll the dice</li>
  <li>/tf2               - tf2 meymeys</li>
  <li>/givememusic       - random music genre</li>  
  <li>/8ball             - magic 8-ball</li>    
  <li>/howdoi:[question] - how do I do something?</li>    
</ul>
<h>Russian Roulette:</h>
<h>Only one person can play at a time (for now)</h>
<ul>
  <li>/rr:rr     - Start a game of Russian Roullete</li>
  <li>/rr:rr     - Pull the trigger</li>
  <li>/rr:rrs    - Leave the game</li>
  <li>/rr:rrstatus - Game Status</li>
</ul>

</body>
</html>
"""
          
class PeeBotClient(mp.MumbleClient):
    def connectionMade(self):
        mp.MumbleClient.connectionMade(self)
        
        self.currentUsers = []
        self.currentChannels = []
        self.inProgress = False
        self.gameList = []
        self.chamber = 0
        self.users = {}
        self.channels = {}
        self.session = 0
        self.channel = 0
        self.shutup = []
        self.follow = OWNER
        self.c_order = []
        for key, value in self.users.iteritems():
            self.currentUsers.append(str(key) + ":" + str(value))
        for key, value in self.channels.iteritems():
            self.currentChannels.append(str(key) + ":" + str(value))
    
    def scan(self):
        self.currentUsers = []
        self.currentChannels = []
        for key, value in self.users.iteritems():
            self.currentUsers.append(str(key) + ":" + str(value))
        for key, value in self.channels.iteritems():
            self.currentChannels.append(str(key) + ":" + str(value))

    def reload(self):
        rebuild(mp)
        rebuild(peebot)

    def reply(self, p, msg):
        if p.channel_id:
            self.send_textmessage("""<b><span style="color:#e70000">""" + msg + "</span></b>", channels=p.channel_id)
        else:
            self.send_textmessage("""<b><span style="color:#e70000">""" + msg + "</span></b>", users=[p.actor])

    def handle_udptunnel(self, p):
        if self.users[p.session] in self.shutup:
            self.move_user(self.shutup_channel, p.session)

    def handle_channelstate(self, p):
        if p.name:
            self.channels[p.channel_id] = p.name

    def handle_userremove(self, p):
        # Remove user from userlist
        del self.users[p.session]

    def handle_userstate(self, p):
        # Add user id to the userlist
        if p.name:
            self.users[p.session] = p.name

        # Stores own session id
        if p.name == self.factory.nickname:
            self.session = p.session

        if p.session == self.session:
            self.channel = p.channel_id

        # Follows user around
        if self.users[p.session] == self.follow:
            if p.channel_id:
                self.move_user(p.channel_id, self.session)
            elif p.self_mute:
                self.mute_or_deaf(self.session, True, True)
            else:
                self.mute_or_deaf(self.session, False, False)
    def handle_textmessage(self, p):
       if p.message == "/help":
           self.reply(p, helptxt)

       if p.message == "How are you?":
           self.reply(p, "Im splendid, how are you "+str(self.users[p.actor])+"?")
            
       if p.message == "/leave":
            if self.users[p.actor] != OWNER:
                if self.users[p.actor] != OWNER:
                    self.reply(p, "Why? Do you not love me?")
            else:
                self.reply(p, "Ok, goodbye for now!")
                sys.exit()
       if "/insult" in p.message:
            name = p.message.split(' ')[-1]
            line = random.choice(open('insults.txt').readlines())
            self.reply(p, name + " " +  line)
       if p.message == "/tf2":
            tf2 = random.choice(open('tf2.txt').readlines())
            self.reply(p, tf2)

       if "/me=" in p.message:
            txt = p.message.split('=')[1]
            self.reply(p, "<i>*"+ str(self.users[p.actor]) + " " + txt + "*</i>")

       if p.message == "/feeling":
            emo = random.choice(open('emotions.txt').readlines())
            self.reply(p, str(self.users[p.actor])+ " is feeling " +emo)
            
       if "/rtd" in p.message:
           rollNumber = random.randint(6,int(p.message.split(' ')[-1]))
           self.reply(p, "You rolled a " + str(rollNumber))
           
       if "/rr:" in p.message:
           cmd = p.message.split(':')[-1]
           if cmd == "rr" and self.inProgress == False:           
               self.chamber = 0
               self.inProgress = True
               self.gameList = []
               self.gameList.append(str(self.users[p.actor]))
               self.reply(p, str(self.users[p.actor]) + " is now playing Russian Roulette")
           if cmd == "rrstatus":
               if self.inProgress == True:
                   self.reply(p, self.gameList[0] + " is currently playing")
               elif self.inProgress != True:
                   self.reply(p, "No one is playing Russian Roulette")
           elif cmd == "rr" and self.inProgress == True:
               if str(self.users[p.actor]) != self.gameList[0]:
                   self.reply(p, self.gameList[0] + " is currently playing")
               elif str(self.users[p.actor]) == self.gameList[0]:
                   chamber = [1,2,3,4,5,6]
                   bullet = random.choice(chamber)
                   trigger = random.choice(chamber)
                   if int(trigger) == int(bullet):
                       self.reply(p, str(self.users[p.actor])+" pulled the trigger and shot themselves." )
                       self.inProgress = False
                       self.gameList.remove(str(self.users[p.actor]))
                       self.gameList = []
                       self.chamber = 0
                       if len(self.gameList) == 0:
                           self.reply(p, str(self.users[p.actor])+" Has left Russian Roulette")
                   elif int(trigger) != int(bullet) and self.chamber != 6:
                       self.reply(p, str(self.users[p.actor])+" pulled the trigger. *click* Nothing happens" )
                       self.chamber += 1
                   elif int(trigger) != int(bullet) and self.chamber == 6:
                       self.reply(p, str(self.users[p.actor])+" pulled the trigger and shot themselves." )
                       self.inProgress = False
                       self.gameList.remove(str(self.users[p.actor]))
                       self.gameList = []   
                       if len(self.gameList) == 0:
                           self.reply(p, str(self.users[p.actor])+" Has left Russian Roulette")
           elif cmd == "rrs" and self.inProgress == True:
                if str(self.users[p.actor]) == self.gameList[0]:
                   self.reply(p, str(self.users[p.actor])+" is weak and stopped playing")
                   self.inProgress = False
                   self.gameList.remove(str(self.users[p.actor]))
                   self.gameList = []
                   self.chamber = 0
                   if len(self.gameList) == 0:
                       self.reply(p, str(self.users[p.actor])+" Has left Russian Roulette")

               

       if p.message == "/reload":
            if self.users[p.actor] == OWNER:
                self.reload()
                self.scan()
                print "Reloaded!"
                
       if p.message in open('badwords.txt').read():
           self.reply(p, "Who are you calling " + p.message + " " +str(self.users[p.actor])+"?")
       if "I love you" in p.message:
           self.reply(p, "Aww. I love you too " +str(self.users[p.actor]))
       if "who is that?" in p.message:
           self.reply(p, "I am a bot. What are you?")
       if p.message == "/givememusic":
              genre = random.choice(open('music.txt').readlines())
              self.reply(p, random.choice(musicPre) + " <i>" + genre + "</i> music.")
       if p.message == "/8ball":
              ballR = random.choice(ball)
              self.reply(p, "<i>" + ballR + "</i>")
       
       if "/howdoi:" in p.message:
           how = []
           how = p.message.split(':')
           qu = []
           qu = how[1].split(' ')
           quJ = '+'.join(qu)
           string = "http://lmgtfy.com/?q="+quJ
           self.reply(p, "like this! " + string)
#           self.reply(p, r"""<a href=" """ + string + """">this is how you """ + how[1] + """</a>""")
               
     
       if p.message == "/whoami":
           if str(self.users[p.actor]) == "Mr.Santos":
               self.reply(p, "You're my <i>daddy</i>")
           else:
               fName = random.choice(open('names.txt').readlines())
               lName = random.choice(open('names.txt').readlines())
               country = random.choice(open('countries.txt').readlines())
               job = random.choice(open('job.txt').readlines())
               emotion1 = random.choice(open('emotions.txt').readlines())
               emotion2 = random.choice(open('emotions.txt').readlines())
               hobby = random.choice(open('hobby.txt').readlines())
               music = random.choice(open('music.txt').readlines())
               age = str(random.randint(1,110))
               self.reply(p, "You are " + fName + " " + lName + ", you are a " + job + " and you are from " + country + ". You are " + age + " years old." + " You often feel " + emotion1 + " and sometimes a little " + emotion2 + ". You often find joy in " + hobby + ". You love listening to " + music + " music.")
       if "/move" in p.message:
           if self.users[p.actor] == OWNER:
               chName = p.message.split(':')[-1]
               for item in self.currentChannels:
                   info = []
                   info = item.split(':')
                   num = int(info[0])
                   chan = info[1]
                   if chName == chan:
                       print chan + " " + str(num) 
                       self.channel = num
                       self.move_user(self.channel, self.session)
                       self.follow = 0
                   
                   

        # Moves user every time they talk
       elif p.message.startswith("/shutup"):
            if self.users[p.actor] == OWNER:
                name = p.message.split(' ')[-1]
                if name in self.users.values():
                    self.shutup_channel = 18
                    self.shutup.append(name)
                else:
                    self.reply(p, "Invalid name")

            elif p.message.startswith("/stop"):
                self.shutup = []

        # Follows user around different channels (and mute)
       elif p.message.startswith("/follow"):
            if self.users[p.actor] == OWNER:
                name = p.message.split(' ')[-1]
                
                if name in self.users.values():
                    if name == "Mr.Santos":
                        self.reply(p, "Following my daddy")
                        self.follow = name
                    self.follow = name
                else:
                    self.reply(p, "Invalid name")

       elif p.message.startswith("/unfollow"):
            if self.users[p.actor] == OWNER:

                self.follow = 0

        # List the channels in the console
       elif p.message.startswith("/channels"):
            if self.users[p.actor] == OWNER:
                self.currentChannels = []
                for key, value in self.channels.iteritems():
                    self.currentChannels.append(str(key) + ":" + str(value))
                for item in self.currentChannels:
                    print item

        # List the users in the console
       elif p.message.startswith("/users"):
            if self.users[p.actor] == OWNER:
                self.currentUsers = []
                for key, value in self.users.iteritems():
                    self.currentUsers.append(str(key) + ":" + str(value))
                for item in self.currentUsers:
                    print item

if __name__ == '__main__':
    while(True):
        factory = mc.create_client(peebot.PeeBotClient, USERNAME, PASSWORD)
        mc.start_client(factory, SERVER_IP, SERVER_PORT, certificate=CERTIFICATE)
