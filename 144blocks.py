from urllib.request import Request, urlopen
import json

url = 'https://explorer.scpri.me/navigator-api/hash/17F62043BF2B3A777C96110FA28C77FC0C0A183334F642D1300993EF6709008938F2E3918BE6'
req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
response = urlopen(req)
data = response.read()
data = data.decode("utf-8")
data = json.loads(data)

transactions = []
for e in data[1]['last100Transactions']:
    transactions.append(e)
transactions.reverse()

first_bid = True
current_bid = 0
last_valid_bid_block = 0
competion_on =  True
for e in transactions:
    if first_bid:
        first_bid = False
        current_bid = e["ScChange"]
        last_valid_bid_block = e['Height']
        print(f'Initial bid: {current_bid} scp')
    else:
        if e['Height'] > last_valid_bid_block + 144:
            print(last_valid_bid_block)
            print(f'The competition has ended')
            competion_on = False
           # break
        else:
            if e["ScChange"] >= current_bid + 1e27:
                if e["ScChange"] >= current_bid+ 100e27:
                    current_bid += 100e27
                else:
                    current_bid = e["ScChange"]
                print(f'Block:{e["Height"]}, bid: {e["ScChange"] / 1e27} SCP --> Valid bid. New winning bid: {current_bid / 1e27}scp')
                last_valid_bid_block = e["Height"]
            else:
                print(f'Block:{e["Height"]}, bid: {e["ScChange"] / 1e27} SCP --> Bid must be between {(current_bid+ 1e27 / 1e27)} and {(current_bid + 100e27) / 1e27} SCP. Current winning bid: {current_bid / 1e27}scp')

url = 'https://explorer.scpri.me/navigator-api/status'
req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
response = urlopen(req)
data = response.read()
data = data.decode("utf-8")
data = json.loads(data)
current_block = data[0]['lastblock']

if competion_on:
    print()
    print(f'Last valid block will be {last_valid_bid_block + 144}. There are {last_valid_bid_block + 144 - current_block} blocks to come before the end of the competition')
    print(f'There are still {last_valid_bid_block + 144 - current_block} blocks to come before the end of the competition. Aproximately {(last_valid_bid_block + 144 - current_block) / 6} hours')
    print(f'Valid bids between {(current_bid + 1e27) / 1e27} and {(current_bid + 100e27) / 1e27} scp, both included')