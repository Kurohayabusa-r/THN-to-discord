import requests
from bs4 import BeautifulSoup
from discord_webhook import DiscordWebhook, DiscordEmbed
import time
import os

webhook_urls = ['Your webhook url']
webhook = DiscordWebhook(url=webhook_urls)
limit = 5

def hackernews_reader():
    try:
        r = requests.get('https://thehackernews.com/')
        if r.status_code == 200:
            soup = BeautifulSoup(r.content, 'html.parser')
            posts = soup.findAll('div',class_='body-post')

            for post in posts[:limit]:
                check = str(post.find('a',class_='story-link')['href'])
                if check not in blacklist:
                    title = post.find('h2',class_='home-title').text

                    published = post.find('div',class_='item-label').text

                    link = post.find('a',class_='story-link')['href']

                    find_image = post.find('img',class_='home-img-src')
                    image = find_image['data-src']

                    description = post.find('div',class_='home-desc').text
                    description = description[:200] + '...'

                    embed = DiscordEmbed(title=title, url=link, description='{}'.format(description), color=29183)
                    embed.set_image(url=image)
                    embed.add_embed_field(name='Published', value=published)
                    embed.set_timestamp()

                    webhook.add_embed(embed)
                    response = webhook.execute()
                    webhook.remove_embed(0)

                    blacklist.append(str(check))

                    with open("hackernews.txt", "a") as f:
                        f.write(str(check) + "\n")
                        f.close()

                    time.sleep(10)

        time.sleep(10)
        return

    except Exception as e:
        print(e)

def blacklisted_posts():
    if not os.path.isfile("hackernews.txt"):
        blacklist = []
    else:
        with open("hackernews.txt", "r") as f:
            blacklist = f.read()
            blacklist = blacklist.split("\n")
            f.close()

    return blacklist

blacklist = blacklisted_posts()
while True:
    hackernews_reader()