import discord
from nostr_sdk import  Client, NostrSigner, Keys, Event, Filter, \
HandleNotification, Timestamp, init_logger, LogLevel, Kind, PublicKey
from datetime import timedelta

import re


DISCORD_TOKEN = "MTI0NTc0NzQ2OTEzMzAyNTM5MQ.GiWA_1.x9cdIfbSSVRvn2fVzEMySm9-_BPaU8Wndiwsg4"
DISCORD_CHANNEL_ID = 1262414282742562846



# main 
class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged in as {self.user}')
        

    
    async def setup_hook(self) -> None:
        # create the background task and run it in the background
        self.bg_task = self.loop.create_task(self.my_background_task())


    async def my_background_task(self):
        await self.wait_until_ready()
        channel = self.get_channel(DISCORD_CHANNEL_ID)
        if channel is None:
            print(f"Channel with ID {DISCORD_CHANNEL_ID} not found.")
            return
        
        

        while not self.is_closed():
            init_logger(LogLevel.DEBUG)

            # sk = SecretKey.from_bech32("nsec1ufnus6pju578ste3v90xd5m2decpuzpql2295m3sknqcjzyys9ls0qlc85")
            # keys = Keys(sk)
            # OR
            keys = Keys.parse("nsec1ufnus6pju578ste3v90xd5m2decpuzpql2295m3sknqcjzyys9ls0qlc85")

            sk = keys.secret_key()
            pk = keys.public_key()
            print(pk)
            print(f"Bot public key: {pk.to_bech32()}")

            # npub1wz8v75sfhx2h0kggwp328ehr0aanl8c3uxzxqmxk4uvvzzm6xruqtc4qjt

            pk_ss = PublicKey.parse("npub1wz8v75sfhx2h0kggwp328ehr0aanl8c3uxzxqmxk4uvvzzm6xruqtc4qjt") 
            signer = NostrSigner.keys(keys)
            nostr_client = Client(signer)

            await nostr_client.add_relay("wss://nos.lol")
            await nostr_client.add_relay("wss://relay.damus.io")
            await nostr_client.connect()

            now = Timestamp.now()

            
            # filter = Filter()
            # filter.kind = [Event.kind]
            ss_filter = Filter().authors([pk_ss]).kind(Kind(1)) 
            events = await nostr_client.get_events_of([ss_filter], timedelta(seconds=10))
            await nostr_client.subscribe([ss_filter], None)
            print(f"Received {events.__len__()} events")
            
            

            # await client.subscribe([ss_filter], None)
            # print(f"53: {ss_filter}")

            class NotificationHandler(HandleNotification):
                async def handle(self, relay_url, subscription_id, event: Event):
                    print(f"Received new event from {relay_url}: {event.as_json}")
                    print(event)

                    
                    # Use regular expression to extract the content
                    content_pattern = re.compile(r'content: "([^"]+)"')
                    content_match = content_pattern.search(str(event))

                    # Check if a match was found and extract the content
                    if content_match:
                        content = content_match.group(1)
                        print(f"Content: {content}")
                        await channel.send(content)

                    else:
                        print("Content not found.")
                

                    

                async def handle_msg(self, relay_url, msg):
                    None

            await nostr_client.handle_notifications(NotificationHandler())




client = MyClient(intents=discord.Intents.default())
client.run(DISCORD_TOKEN) 



