
from azure.core.credentials import AzureNamedKeyCredential
from azure.data.tables import TableServiceClient
from azure.data.tables import TableClient
from azure.core.exceptions import ResourceExistsError, HttpResponseError,ResourceNotFoundError,ClientAuthenticationError
import logging
import uuid

def db_connect():
    try:
        print("Azure Blob Storage Python quickstart sample")
        account_url = "https://rssscrapdata.table.core.windows.net/" #"https://seleniumnews9706b8.table.core.windows.net/"

        credential = AzureNamedKeyCredential("rssscrapdata", "--add your credential--")

        service = TableServiceClient(endpoint=account_url, credential=credential)
        return {"service":service,
                "statusCode":200}

    except Exception as ex:
        print(f"error in db_connect function")
        error = {"error":str(ex),
                "statusCode":500}
        return error



def write_db(service,detail_list,summary,answer_list):
    table_client = service.get_table_client(table_name="NewsCollect") 
    answer_table_client =  service.get_table_client(table_name="AnswerCollect")

    for dict_val in detail_list:
        try:
            print("Summary while writing to db")
            logging.info(f" Date published to db {dict_val['date_published']}")
            #try:
            ans_col = len(answer_list[dict_val['title']])
            unique_id = uuid.uuid4()
            logging.info(f'unique id is {unique_id}')

            data = {
                "PartitionKey":str(dict_val['date_published']),
                "RowKey":str(unique_id),
                "Title":dict_val['title'],
                "Link":dict_val['news_link'],
                "Content":dict_val['content'],
                "Description":dict_val['descript'],
                "Summary":summary[dict_val['title']]
            }
            entity = table_client.create_entity(entity=data)

            for que,ans in answer_list[dict_val['title']].items():
                ans_data={
                    "PartitionKey":str(que),
                    "RowKey":str(unique_id),
                    "Answer":str(ans),
                    "Title":dict_val['title']
                }
                answer_entity = answer_table_client.create_entity(entity=ans_data)

            
            
        
        except ClientAuthenticationError as e:
            logging.error(e)
            print(e)

        except ResourceNotFoundError as e:
            logging.error(e)
            print(e)
        except ResourceExistsError as e:
            logging.error(e)
            print(e)

        except Exception as e:
            logging.error(e)
            print(e)
        
        

def read_db(service):
    try:
        topic = None
        question_set = []

        table_client = service.get_table_client(table_name="InputQueries") 
        got_entity = table_client.get_entity(partition_key="partialkey", row_key="rowkey")
        
        for items in got_entity:
            if(items == 'topic'):
                topic = got_entity[items]
            if('q' in str(items)):
                question_set.append(got_entity[items])  

    except Exception as e:
        logging.error(e)
    
    return topic,question_set


