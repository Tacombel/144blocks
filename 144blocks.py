from urllib.request import Request, urlopen
import json

current_address = '502E8B71CFBDF5A92CF4DAACE154F83721BA016304339BEA6A9A9FDC5A6CEB0534CDA1B78E8F'
url = 'https://explorer.scpri.me/navigator-api/hash/' + current_address
req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
response = urlopen(req)
data = response.read()
data = data.decode("utf-8")
data = json.loads(data)

transactions = []
for e in data[1]['last100Transactions']:
    transactions.append(e)
transactions.reverse()

url = 'https://explorer.scpri.me/navigator-api/status'
req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
response = urlopen(req)
data = response.read()
data = data.decode("utf-8")
data = json.loads(data)
current_block = data[0]['lastblock']

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

if current_block > last_valid_bid_block + 144:
    competion_on = False

if competion_on:
    print()
    print(f'Last valid block will be {last_valid_bid_block + 144}.')
    print(f'There are still {last_valid_bid_block + 144 - current_block} blocks to come before the end of the competition. Aproximately {(last_valid_bid_block + 144 - current_block) / 6} hours')
    print(f'Valid bids between {(current_bid + 1e27) / 1e27} and {(current_bid + 100e27) / 1e27} scp, both included')
else:
    print()
    print(f'The competition ended')