# MADE FOR GITHUB ACITONS 
import time
import os
import discord
from  random import randint
from requests import get
from bs4 import BeautifulSoup
import asyncio
# from dotenv import load_dotenv
# load_dotenv()
# DISCORD_TOKEN = os.environ('DISCORD_TOKEN')
DISCORD_TOKEN = os.environ['DISCORD_TOKEN']

f_w=open('BuildConfig.txt', 'w') # file to save f_w to
# My Browser's Header
HEADERS = ({'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.50', 'Accept-Language': 'en-US, en;q=0.5'})
async def fetch(component, url):
    global f_w, data
    r = get(url, headers=HEADERS)
    soup = BeautifulSoup(r.text, 'html.parser')

    data=[]
    name= (soup.find('h1'))
    data.append(name.string.strip())
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
    fetched_data= (f"""
```{name}```
Price: {price}
""")

    # print(fetched_data)
    # print(fetched_data)
    f_w.write(fetched_data)

    # String processing conversion to int 
    price =price[1:]
    price=price.replace(',', '')
    return int(price)

async def main():
    L = await asyncio.gather(
            fetch('CPU', 'https://price-history.com/product/amd-5000-series-ryzen-5-5600x-7o5pfhce'),
            fetch('GPU', 'https://price-history.com/product/asus-dual-radeon-rx-6600-8-gHeLVdmb'),
            fetch('MOBO', 'https://price-history.com/product/asus-b550-rog-strix-b550-f-afVbQaG5'),
            fetch('RAM', 'https://price-history.com/product/corsair-vengeance-lpx-16gb-2x8gb-ddr4-p5Jfhhce'),
            fetch('SSD', 'https://price-history.com/product/samsung-970-evo-plus-1tb-pcie-xDT82vyp'),
            fetch('PSU', 'https://price-history.com/product/cooler-master-mwe-550-bronze-v2-rBRCfoSj'),
    )
    totalSum=0
    for i in range(5):
        totalSum+=L[i]
    f_w.writelines(f"""
Total Sum: Rs.{str(totalSum).strip()}
""")

    M = await asyncio.gather(
                fetch('Archer', 'https://price-history.com/product/archer-tech-lab-astra-m200-mechanical-3NMVBcw8'),
                # fetch('CB-GK 34', 'https://price-history.com/product/renewed-cosmic-byte-cb-gk-34-LUB7wmce'),
        )
    

asyncio.run(main())
f_w.writelines(f"""
via CronJobs - Github Actions {time.strftime('%H:%M:%S')}
""")

f_w.close()


f_r=open('BuildConfig.txt', 'r')
# Discord starts
intent=discord.Intents.default()
client=discord.Client(intents=intent)
msg=(f_r.read())
# print(msg)

@client.event
async def on_ready():
    print(f'Logged in As {client.user}')
    try:
        await send_message()
    except Exception as e:
        print(e)
    finally:
        await client.close() # To clso the connection after out job is done

async def send_message():
    mention='everyone'
    embed_colors=[0xf8fafc, 0x64748b, 0xfed7aa, 0xf97316, 0xfef3c7, 0xfbbf24, 0xecfccb, 0x22c55e, 0x0d9488, 0x22d3ee, 0x0ea5e9, 0x8b5cf6, 0xf9a8d4, 0xf472b6, 0xfda4af]
    channel_id=1136610536256192542 #pc-config
    channel = client.get_channel(channel_id)
    embedtry=discord.Embed(description=f"@{mention} {msg}", color=embed_colors[randint(0, len(embed_colors)-1)])
    await channel.send(embed=embedtry)

client.run(DISCORD_TOKEN)
print("Success!")



# async def fetch(component, url):
#     global f_w

#     r = get(url, headers=HEADERS)

#     soup = BeautifulSoup(r.text, 'html.parser')
#     name= (soup.find('h1')).string.strip()
#     price_now = ((soup.find('div','js-product-price')).contents[0]).string.strip()
#     mrp = (soup.find('span','price-old')).string.strip()
#     lowest_price=((soup.find('div', class_='label lowest').find_next_sibling('div')).string.strip())
#     last_update = ((soup.find('div','info js-product-price-updated-at')).contents[0]).string.strip()
#     link= soup.find('a', attrs={'title':"Go to shop"})

#     fetched_data = f'''
# **{name}**
# **Price**: {price_now} | **MRP**: {mrp} | **Lowest**: {lowest_price}
# View at: {link.get('href')}
# {last_update}
# '''
#     # print(fetched_data)
#     f_w.write(fetched_data)

#     # String processing conversion to int 
#     price_now =price_now[1:]
#     price_now=price_now.replace(',', '')
#     return int(price_now)

# async def main():
#     L = await asyncio.gather(
#             fetch('CPU', 'https://www.pricebefore.com/amd-5000-series-ryzen-5-5600x-desktop-processor-6-cores-m20417.html'),
#             fetch('GPU', 'https://www.pricebefore.com/asus-dual-radeon-rx-6600-8-gb-gddr6-ram-pcie-m178093.html'),
#             fetch('MOBO', 'https://www.pricebefore.com/asus-rog-strix-b550-f_w-gaming-wifi-ii-amd-am4-m103100.html'),
#             fetch('SSD', 'https://www.pricebefore.com/samsung-970-evo-plus-1tb-pcie-nvme-m-2-2280-m6200.html'),
#             fetch('PSU', 'https://www.pricebefore.com/cooler-master-mwe-550-bronze-v2-230v-80-plus-bronze-m50037.html'),
# # MK Mechanical Keyboard
#             fetch('EvoFox Katana Pro RGB MK Red', 'https://www.pricebefore.com/evofox-katana-pro-rgb-mechanical-keyboard-silent-red-switches-16-m180782.html'),
#             fetch('MK', 'https://www.pricebefore.com/cooler-master-mwe-550-bronze-v2-230v-80-plus-bronze-m50037.html'),
#     )
#     # print(L)
#     totalSum=0
#     for i in range(5):
#         totalSum+=L[i]

#     # print(totalSum)
#     f_w.writelines(f"""Total Sum: Rs.{str(totalSum).strip()}
# via CronJobs - Github Actions
# {time.strftime('%H:%M:%S')}
# """)
#     # f_w.writelines(f"Total Sum: Rs.{str(totalSum).strip()} Test")

# asyncio.run(main())
# f_w.close()


# f_r=open('BuildConfig.txt', 'r')
# # Discord starts
# intent=discord.Intents.default()
# client=discord.Client(intents=intent)
# msg=(f_r.read())
# # print(msg)

# @client.event
# async def on_ready():
#     print(f'Logged in As {client.user}')
#     try:
#         await send_message()
#     except Exception as e:
#         print(e)
#     finally:
#         await client.close() # To clso the connection after out job is done

# async def send_message():
#     mention='everyone'
#     embed_colors=[0xf8fafc, 0x64748b, 0xfed7aa, 0xf97316, 0xfef3c7, 0xfbbf24, 0xecfccb, 0x22c55e, 0x0d9488, 0x22d3ee, 0x0ea5e9, 0x8b5cf6, 0xf9a8d4, 0xf472b6, 0xfda4af]
#     channel_id=1136610536256192542 #pc-config
#     channel = client.get_channel(channel_id)
#     embedtry=discord.Embed(description=f"@{mention} {msg}", color=embed_colors[randint(0, len(embed_colors)-1)])
#     await channel.send(embed=embedtry)

# client.run(DISCORD_TOKEN)
# print("Success!")