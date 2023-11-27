# MADE FOR GITHUB ACITONS 
import time
import os
import discord
from  random import randint
from requests import get
from bs4 import BeautifulSoup
import asyncio
# from dotenv import load_dotenv  #inLocalHost
# load_dotenv() #inLocalHost
# DISCORD_TOKEN = os.getenv('DISCORD_TOKEN') #inLocalHost

DISCORD_TOKEN = os.environ['DISCORD_TOKEN'] #githubRepo

f_w=open('BuildConfig.txt', 'w') # file to save f_w to
totalSum=0
totalmrp=0
HEADERS = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.50', 'Accept-Language': 'en-US, en;q=0.5',}
async def fetchPriceBefore(component, url):
    global f_w, totalmrp
    r = get(url, headers=HEADERS)
    soup = BeautifulSoup(r.text, 'html.parser')
    # FULL NAME OF THE COMPONENT PASSED
    componentName = (soup.find('h1')).string.strip()
    wordtrim = componentName.split(' ')[:8]
    componentName = ' '.join(wordtrim)

    # CURRENT PRICE
    p_now = ((soup.find('div', 'js-product-price')).contents[0]).string.strip()
    mrp = (soup.find('span', 'price-old')).string.strip()
    # LOWEST AND HIGHEST PRICES EVER
    l_pr = (soup.find('div', class_='label lowest').find_next_sibling('div')).string.strip()
    h_pr = (soup.find('div', class_='label highest').find_next_sibling('div')).string.strip()
    # LAST UPDATED PRICE OF THE COMPONENT
    last = ((soup.find('div', 'info js-product-price-updated-at')).contents[0]).string.strip()
    link = soup.find('a', attrs={'title': 'Go to shop'})

    fetched_data = f'''
{component}: {componentName}
Price: **{p_now}** | MRP: {mrp}
'''
    
    """ 
    # Additional information: Just put it inside above 'fetched_data' variable
        # Lowest: {l_pr} | Highest: {h_pr}
        # {last}
        # Check at: {link.get('href')}
    """
    # print(fetched_data)
    f_w.write(fetched_data)

    # String processing; conversion to int
    p_now = p_now[1:]
    p_now = p_now.replace(',', '')
    mrp = mrp[1:]
    mrp = mrp.replace(',', '')
    totalmrp+=int(mrp)
    p_now=int(p_now)

    # yesterdayPrices - Price tracking
    # with open(f"yesterdayPrices/{component}.txt" , "r") as cr:
    #     trackRecord = int(cr.read()) 
    #     if trackRecord<p_now: # Price rose 
    #         f_w.write(f"Change `+{p_now-trackRecord}`\n")
    #         print(f"{component} Price Changed by `+{p_now-trackRecord}` ")

    #     elif trackRecord==p_now: # Price equal
    #         print(f"{component} price is same.")

    #     elif trackRecord>p_now: # Price fell
    #         f_w.write(f"Change `{p_now-trackRecord}` \n")

    #         print(f"Price rose by {p_now-trackRecord} ")
    #         with open(f"yesterdayPrices/{component}.txt" , "w") as trackRecordWrite:
    #             trackRecordWrite.write(str(p_now)) # writing today's prpice to compare tomorrow
    return int(p_now)


async def fetchPriceHistory(component, url):
    global f_w
    r = get(url, headers=HEADERS)
    soup = BeautifulSoup(r.text, 'html.parser')

    data=[]
    name= (soup.find('h1')).string.strip()
    wordtrim = name.split(' ')[:8]
    name = ' '.join(wordtrim)
    data.append(name)

    table = soup.find('table', class_='text-center ph-table-offer')
    if table:
        rows = table.find_all('tr')
        for row in rows:
            # th = row.find('th', scope='row')
            td = row.find('td')
            for _ in range(2):
                # if th and td:
                if td:
                    # key = th.text.strip()
                    data.append(td.text.strip())
                    # data[key] = value`
    name =data[0]
    price=data[1]
    fetched_data= f"""

{name}
Price: {price}
"""
    price = price[1:]
    price = price.replace(',', '')
    price=int(price)
    return price
# unicode space ```ㅤㅤㅤㅤㅤㅤ```
    f_w.write(fetched_data)
    
    # Calls
async def main():
    global totalSum
    C = await asyncio.gather(
        fetchPriceBefore('CPU','https://www.pricebefore.com/amd-5000-series-ryzen-5-5600x-desktop-processor-6-cores-m20417.html'),
        fetchPriceBefore('GPU','https://www.pricebefore.com/asus-dual-radeon-rx-6600-8-gb-gddr6-ram-pcie-m178093.html'),
        #  I HAD TO THIS BECASUE 1x8GB WAS ONLY AVAILABLE THERE
        fetchPriceBefore('RAM','https://www.pricebefore.com/corsair-vengeance-lpx-8gb-1x8gb-ddr4-3200mhz-c16-desktop-ram-m5956.html'),
        fetchPriceBefore('RAM','https://www.pricebefore.com/corsair-vengeance-lpx-8gb-1x8gb-ddr4-3200mhz-c16-desktop-ram-m5956.html'),
        # fetchPriceBefore('MOB Asus B550F','https://www.pricebefore.com/asus-rog-strix-b550-f-gaming-wifi-ii-amd-am4-m103100.html'),
        fetchPriceHistory('MOB','https://price-history.in/product/msi-mag-b550-tomahawk-max-wifi-Ps08jmce'),

        # MOBO for intel use case
        # fetchPriceHistory('MOB','https://price-history.in/product/msi-mag-b560m-mortar-wifi-micro-l6uinaw8'),

        fetchPriceBefore('SSD','https://www.pricebefore.com/samsung-970-evo-plus-1tb-pcie-nvme-m-2-2280-m6200.html'),
        fetchPriceBefore('PSU','https://www.pricebefore.com/cooler-master-mwe-550-bronze-v2-230v-80-plus-bronze-m50037.html'),
        fetchPriceBefore('CASE','https://www.pricebefore.com/galax-revolution-01-rev-01w-mid-tower-gaming-case-4-m19447.html'),
        fetchPriceHistory('Monitor','https://price-history.in/product/msi-modern-md272qpw-27-inch-wqhd-11UsYyyp'),
        
    )
    print(C)
    
# Appending total build cost, also under main() 
    totalSum = 0
    for i in range(len(C)):
        totalSum += C[i]
    print(totalSum)
    f_w.writelines(f'''

```Fetched: ₹{totalSum} | MRP: ₹{totalmrp}```

> Memory Modules''')

    R = await asyncio.gather(
                fetchPriceBefore('Corsair 16GB', 'https://www.pricebefore.com/corsair-vengeance-lpx-16gb-16gb-ddr4-3200mhz-udimm-c16-desktop-m1869.html'),
                fetchPriceBefore('XPG 16GB', 'https://www.pricebefore.com/xpg-adata-gammix-d30-ddr4-6gb-1x16gb-3200mhz-u-dimm-m21623.html'),
        )
    f_w.writelines(f'''
Final sum with 16GB Modules = Standard fetched Sum + Current Module Price - (Hardcoded) previous RAM price: 
''')
    for i in range(0,len(R)):
        sumWith_16Gigs=0
        sumWith_16Gigs+=(totalSum + 2*R[i] - 2*1809)
        f_w.writelines(f'''{i}. `{sumWith_16Gigs}` = {totalSum} + {2*R[i]} - {2*1816}
''')
asyncio.run(main())
f_w.close()


# Discord starts
f_r=open('BuildConfig.txt', 'r')
intent=discord.Intents.default()
client=discord.Client(intents=intent)
msg=(f_r.read())
print(msg)

@client.event
async def on_ready():
    print(f'Logged in As {client.user}')
    try:
        await send_message()
    except Exception as e:
        print(e)
    finally:
        await client.close() # To close the connection after out job is done whether successfully or not 

async def send_message():
    global totalSum
    mention='everyone'
    embed_colors=[0x64748b, 0xfed7aa, 0xf97316, 0xfef3c7, 0xfbbf24, 0x22c55e, 0x0d9488, 0x22d3ee, 0x0ea5e9, 0x8b5cf6, 0xf9a8d4, 0xf472b6, 0xfda4af]
    channel_id=1136610536256192542 #pc-config
    channel = client.get_channel(channel_id)
    choice = randint(0, len(embed_colors)-1)
    embedtry=discord.Embed(title=f"₹{totalSum}", description=f"{msg} @{mention}", color=embed_colors[choice])
    embedtry.set_footer(text=f"Embed Hex: {hex(embed_colors[choice])}", icon_url=None)
    await channel.send(embed=embedtry)

client.run(DISCORD_TOKEN)
print("Success!")
