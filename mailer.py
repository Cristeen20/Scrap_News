import azure.functions as function
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail,Email, To, Content

import logging

apikey = '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'

def send_mail(topic,html_content):

    try:
        sg = SendGridAPIClient(api_key=apikey)
        msg = Mail(
            Email('kokuljose@outlook.com'),
            [To('davidisraeli2023@gmail.com'),
            To('kokuljose@outlook.com'),
            To('d@israeliholdings.com')],
            f'Topic : {topic}',
            Content("text/html", html_content),
            is_multiple= True
        )
        print("sending mail")
        mail_json = msg.get()

        # Send an HTTP POST request to /mail/send
        response = sg.client.mail.send.post(request_body=mail_json)
        response = sg.send(msg)
        logging.info(response)
    except Exception as exe:
        logging.error(exe)
        logging.info("Error in send_mail function")



def create_html(detail_list,summary,answer_list):

    mail_content = ''
    invalid_link = ''
    
    for dic_item in detail_list['detail_list']:
        try:
            
            answer_content = ''
            for t,a in answer_list.items():
                if t == dic_item['title']:
                    
                    for k,v in a.items():
                        answer_content = answer_content+'''
                        <h5>'''+str(k)+'''?</h5>
                        <p>'''+str(v)+'''</p>'''
            if answer_content != '':
                mail_content = mail_content + '''\
                <h4>Headline :<a href='''+dic_item['news_link']+'''> '''+str(dic_item['title'])+'''</a></h4>
                <h4><i>Summary :</i></h4>
                <p>'''+str(summary[dic_item['title']])+'''</p>
                <hr>'''
                mail_content = mail_content +'''<h4><i>Answers</i></h4> '''+ answer_content
        except Exception as e:
            logging.error(e)
            logging.info("error in create_html function")

    for itm,link in detail_list['invalid_link'].items():
        try:
            invalid_link = invalid_link + '''
            <p><a href='''+str(link)+'''>'''+str(itm)+'''</a></p>'''
        except Exception as e:
            logging.error(e)
            logging.info("error in create_html function")

    
    

    if(mail_content == ''):
        html_content='''
        <!DOCTYPE html>  
        <html>  
        <head>  
        <title>News Today</title>  
        </head>  
        <body>  
        <p>Dear David,</p>
        <p>No major news for the day</p>
        <h4><i>Links Found</i></h4>
        <div>'''+invalid_link+'''</div>
        </body>  
        </html>
        '''
    else:
        html_content ='''
        <!DOCTYPE html>  
        <html>  
        <head>  
        <title>News Today</title>  
        </head>  
        <body>  
        <p>Dear David,</p>  
        <p>Attaching today's news highlights</p>
        <div>'''+mail_content+'''</div> 
        <h4><i>Other Links</i></h4>
        <div>'''+invalid_link+'''</div>
        </body>  
        </html>  
        '''
    logging.info("writing to html")
    return html_content

