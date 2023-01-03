import key
import discord
import ItemManager as im
import asyncio
import exceptionRecorder as er
import scrape
import sortLogic as sl
import Channels
import TimeDif
import urllib3
import requests

key = key.GetKey()


try:
    intents = discord.Intents.all()
    client = discord.Client(intents=intents)
except:
    client = discord.Client()

@client.event
async def on_ready():
    print('we have logged in as {0.user}'.format(client))
    #channels = [605674655457476618, 919740114693931009, 1054781839803428864]
    
    try:
        await asyncio.sleep(3)
        HBchannel = client.get_channel(919740114693931009) #test channel 1056780369145380936
        #HBchannel = client.get_channel(1056780369145380936) 
        #channel = client.get_channel(HBchannel)
        await HBchannel.send("Banker awake. - This is a test-")
    except:
        er.basicHandler()
    #channel = client.get_channel(605674655457476618) #Do channel
    #1054781839803428864 Do test channel
    

    while True:
        #channels = Channels.getChannels()#[('Barter', 919740114693931009), ('FpickleDog', 919740114693931009),
        channels = Channels.getDicChannels() # returns dic like dic = {person : (channel1, channel2)}
        perList = list(channels)
        i = 1 #waits 5 seconds at startup to try
        while i > 0:
            await asyncio.sleep(1)
            i = i - 1
            print(i, end='\r\r\r\r')
        for per in perList:
            #print("\nTesting character {} and sending channel {}".format(per, x[1]))
            try:
                onhands = scrape.PullData(per)
            except Exception as err:
                tp = type(err)
                if tp == ValueError:
                    print(err)
                    continue
                if tp == AttributeError:
                    print(err)
                    continue
                if tp == requests.exceptions.ConnectionError:
                    print(tp)
                    pass
                if tp == OSError:
                    print(tp)
                    pass
                if tp == urllib3.exceptions.NewConnectionError:
                    print(tp)
                    pass
                if tp == urllib3.exceptions.MaxRetryError:
                    print(tp)
                    pass
                if tp == requests.exceptions.ConnectionError:
                    print(tp)
                    pass
                if tp == requests.exceptions.HTTPError:
                    print(tp)
                    continue
                else:
                    print(tp)
                    er.MessageHandler(per)
                    continue
            try:
                sl.MainSort(onhands)
            except:
                er.MessageHandler(per)
            chans = channels[per]
            if len(onhands.sendMsg) > 40 and len(onhands.sendMsg) < 2000:
                for chan in chans:
                    ch = client.get_channel(chan)
                    await ch.send(onhands.sendMsg)
                    print("Sent message on channel {}".format(chan))
                    await asyncio.sleep(3)
            if len(onhands.sendMsg) < 2000:
                pass # write output to file and post
            await asyncio.sleep(15)



        #i = 3585 #waits i seconds after running to run again
        i = TimeDif.getTimeDif() #gets dif between now and next hour in seconds
        while i > 0:
            await asyncio.sleep(1)
            i = i - 1
            print(i, end='\r\r\r\r')

client.run(key)
