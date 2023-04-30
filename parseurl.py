import feedparser
import dateutil
from dateutil import parser
from operator import itemgetter
import re
import asyncio
import logging
import requests
import json
from datetime import datetime, timedelta





def generate_news_feed_url(topic):
    try:
        # Format the topic for use in the URL
        formatted_topic = topic.replace(" ", "+")
        day = datetime.today().strftime('%Y-%m-%d')
        prev_day = datetime.today() - timedelta(days=1)
        prev_day = prev_day.strftime('%Y-%m-%d')
        # Generate the Google News RSS feed URL for the topic
        print(f'prev day {prev_day} and day {day}')
        rss_url = f'https://news.google.com/rss/search?q={formatted_topic}+after:{prev_day}+before:{day}' #&hl=en-US&gl=US&ceid=US:en" after:2020-06-01+before:2020-06-02
        #rss_url = f'https://news.google.com/rss/search?q={formatted_topic}'
        #rss_url = f'https://news.google.com/rss/search?q=foreclosed+hotels+after:03-04-2023+before:04-04-2023'
        logging.info(f'the rss url is {rss_url}')
        
        return {"rss_url":rss_url,
                "statusCode":200}
    
    except Exception as e:
        logging.info(f'error in generate_news_feed_url function')
        error = {'error':str(e),
                'statusCode':500}
        return error

def sub_link_details(url):
    try:
        logging.info("calling pypeteer")
        detail_list = []
        feeds = feedparser.parse(url)
        feed = [feed for feed in feeds.entries]
        count = 0
        news = {}
        invalid_link = {}

        #newlist=sorted(feed,key=lambda x: parser.parse(x['published']), reverse=True)
        link_count = 0
        for entry in feed:
            
            link_count = link_count + 1
            if(link_count > 20):
                break

            content = None
            link = None

            entity_dict = {}

            try:
                url = "https://urlscrap.azurewebsites.net/api/HttpTrigger1"

                payload = json.dumps({
                "name": "Azure",
                "link": entry.link})
                headers = {
                'Content-Type': 'application/json'
                }
                response = requests.request("POST", url, headers=headers, data=payload)
            
                logging.info(f"got api resut {response.text}")
                
                result = response.text
                print(f'api results {result}')
                result = json.loads(result)
                content = result['content']
                link = result['link']
                logging.info(link)
            except Exception as e:
                logging.error(f'APi call error {e} in {entry.link}')
                

            date = entry.published
            logging.info(f" Date published is {date}")
            
            title = entry.title
            descript = entry.description

            
            if content ==None:
                if link != None:
                    invalid_link[title] = link
                else:
                    invalid_link[title] = entry.link
                print(f'continuess')
                continue
                


            entity_dict['news_link'] = link
            entity_dict['date_published'] = date
            entity_dict['title'] = title
            entity_dict['descript'] = descript
            entity_dict['content'] = content
            
            

            if len(content) > 10:
                print(f'content to summarise {content}')
                detail_list.append(entity_dict)
                news[title] = count
            else:
                invalid_link[title] = link
            
            
        logging.info(f'Valid content length {news}')
        logging.info(f'Invalid link {invalid_link}')
        return {"detail_list":detail_list,
                "invalid_link":invalid_link,
                "statusCode":200}
        
    except Exception as e:
        logging.error(f"error in sub_link_details function - {e}")
        error = {"error":str(e),
                "statusCode":500}
        return error

    




