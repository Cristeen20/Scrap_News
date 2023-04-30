

import openai
import logging
import re
import time
import ast

#from nltk.tokenize import word_tokenize

# Set your OpenAI API key
openai.api_key = "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"

def trim_limit(content):
    w = content.split(" ")#word_tokenize(content)
    print(f'len of tokenised content {len(w)}')
    if(len(w)>1400):
        print(len(w[:1400]))
        content_limited = ''.join(w[:1400])
    else:
        content_limited = ''.join(w)
    return content_limited

def summarize(detail_list):
    summary = {}
    try:
        
        for detail in detail_list:
            for key,value in detail.items():
                if key == 'title':
                    title = value
                if key == 'content':
                    answers = {}
                    time.sleep(15)
                    logging.info("Summary openAI api call")
                    #logging.info(f'content to summarise {value}')
                    # Use OpenAI's GPT API to generate a summary of the news article
                    try:
                        response = openai.Completion.create(
                        engine="text-davinci-003",#"text-ada-001",#"text-davinci-003",#"davinci",
                        prompt = f'Summarise the article in less than 150 words\
                            \n article : {trim_limit(value)} \n \n',
                        max_tokens=200,
                        temperature= 0.2,
                        n=1,
                        stop=None
                        )

                        summary_content = response.choices[0].text
                        #summary_content = summary_content.replace('\n'," ")
                        summary_content = re.sub('[^.,a-zA-Z0-9 \n\.]', ' ', summary_content)  #re.sub('[\W_]+', ' ', summary_content)
                        print("Summary API return")
                        print(f'summary_content is {summary_content}')
                        summary[title] = summary_content
                        
                    except Exception as e:
                        print(f'error in openai summary api {e}')
                        continue
    except Exception as e:
        logging.error(e)
        logging.info("Error in Summarize openai")
    
    return summary


def question_answer(detail_list,questions):

    # Use OpenAI's GPT API to answer a set of questions related to the news article
    answer_list = {}
    try:

        for detail in detail_list:
            for key,value in detail.items():
                if key == 'title':
                    title = value
                if key == 'content':
                    content = value
                    try:
                        answers = {}  # key value pair of question and answer

                        print(questions)
                        time.sleep(10)
                        response = openai.Completion.create(
                            engine="text-davinci-003",
                            prompt = f'Answer these questions in less than 10 words based on the article \n {questions} \n \
                                    Give the full output in json format \n \
                                    Keep question as key and answer as value\n \
                                    \n article : {trim_limit(value)} \n \n',
                            max_tokens=256,
                            n=1,
                            temperature=0.2,
                            stop=None
                        )
                        answer_content = response.choices[0].text
                        print(f'answer content {answer_content}')
                        sum_split = ast.literal_eval(answer_content)

                        answer_key = ['not','no','mention','mentioned','none','n/a']
                        invalid_cnt = 0
                        for key,value in sum_split.items():
                            value_lis = value.lower().split(" ")
                            invalid_lis = [value for value in value_lis if value in answer_key]
                            print(f'no mention in answer {invalid_lis}')
                            if(len(invalid_lis) > 0):
                                invalid_cnt = invalid_cnt + 1
                        
                        if(invalid_cnt  >= len(questions)/2):
                            print(f'invalid aswer count is greater {invalid_cnt}')
                            answer_list[title] = {}
                        else:
                            answer_list[title] = sum_split
                        '''
                        answer_content = answer_content.replace('\n'," ")
                        answer = answer_content
                        '''

                        
                    except Exception as e:
                        print(f'error in openai answer api {e}')
                        continue
    except Exception as e:
        logging.error(e)
        logging.info("error in question answer")

    return answer_list
