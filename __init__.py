import datetime
import logging
import requests
import json
import asyncio

from .parseurl import generate_news_feed_url,sub_link_details
from .db import db_connect,write_db,read_db
from .openai_analyse import summarize,question_answer
from .mailer import send_mail,create_html

import azure.functions as func


async def main(mytimer: func.TimerRequest) -> None:
    
        utc_timestamp = datetime.datetime.utcnow().replace(
            tzinfo=datetime.timezone.utc).isoformat()

        if mytimer.past_due:
            logging.info('The timer is past due!')



        '''Connect to db '''
        db_service_return = db_connect()
        if db_service_return['statusCode'] == 200:
            topic,questions = read_db(db_service_return['service'])
        else:
             return db_service_return
        
        rss_url_return = generate_news_feed_url(topic)

        if(rss_url_return["statusCode"]==500):
            logging.error(rss_url_return)
    


        detail_list_return = sub_link_details(rss_url_return['rss_url'])
        if(detail_list_return['statusCode']==500):
            logging.error(detail_list_return)

        logging.info(f' The length of invalid_link list is {detail_list_return["invalid_link"]}')
        
        answer_list = question_answer(detail_list_return['detail_list'],questions)
        summary = summarize(detail_list_return['detail_list'])
        
        
        print("writing to db")
        if db_service_return['statusCode'] == 200:
            logging.info("write to DBB")
            write_db(db_service_return['service'],detail_list_return['detail_list'],summary,answer_list)
        
        html_content = create_html(detail_list_return,summary,answer_list)
        
        send_mail(topic,html_content) #detail_list_return['invalid_link']
        
        logging.info('Python timer trigger function ran at %s', utc_timestamp)


        
