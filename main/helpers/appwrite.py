import datetime
from appwrite.client import Client
from appwrite.exception import AppwriteException
from appwrite.query import Query
from appwrite.services.databases import Databases
from . import level_helper


def get_database_conn():
    try:
        with open('./data/restricted/appwrite.txt') as f:
            conf = f.read().splitlines()

            client = Client()
            (client
             .set_endpoint(conf[0])  # Your API Endpoint
             .set_project(conf[1])  # Your project ID
             .set_key(conf[2])  # Your secret API key
             )

            databases = Databases(client)
    except AppwriteException as e:
        print(e)

    return databases


def create_guild_database(guild_id):
    databases = get_database_conn()
    databases.create(
        database_id=f"{guild_id}",
        name=f"{guild_id}",
    )
    databases.create_collection(database_id=f"{guild_id}", collection_id='guild_settings', name='guild_settings')
    databases.create_string_attribute(database_id=f"{guild_id}", collection_id='guild_settings', key='welcome_msg',
                                      required=True, size=256)
    databases.create_document(database_id=f"{guild_id}", collection_id='guild_settings', document_id='settings',
                              data={'welcome_msg': "Hi {user}, welcome to {server}!"})
    databases.create_collection(database_id=f"{guild_id}", collection_id='guild_users', name='guild_users')
    databases.create_datetime_attribute(database_id=f"{guild_id}", collection_id='guild_users', key='last_exp_drop',
                                        required=True)
    databases.create_integer_attribute(database_id=f"{guild_id}", collection_id='guild_users', key='lvl',
                                       required=True)
    databases.create_integer_attribute(database_id=f"{guild_id}", collection_id='guild_users', key='exp',
                                       required=True)
    databases.create_index(database_id=f"{guild_id}", collection_id='guild_users', key='exp_key', type='key',
                           attributes=['exp'])


def delete_guild_database(guild_id):
    databases = get_database_conn()
    databases.delete(
        database_id=f"{guild_id}"
    )


def add_member(guild_id, uid, join_date):
    databases = get_database_conn()
    databases.create_document(database_id=f"{guild_id}", collection_id='guild_users', document_id=f"{uid}",
                              data={'last_exp_drop': f"{join_date}",
                                    'lvl': 0,
                                    'exp': 0})


def delete_member(guild_id, uid):
    databases = get_database_conn()
    databases.delete_document(database_id=f"{guild_id}", collection_id='guild_users', document_id=f"{uid}")


def add_exp(guild_id, uid, msg_datetime, exp):
    databases = get_database_conn()
    user = databases.get_document(database_id=f"{guild_id}", collection_id='guild_users', document_id=f"{uid}")
    if datetime.datetime.fromisoformat(user['last_exp_drop']) <= msg_datetime - datetime.timedelta(minutes=1):
        new_exp = user['exp'] + exp

        if level_helper.has_lvl_up(user['lvl'], new_exp):
            new_lvl = user['lvl'] + 1

            databases.update_document(database_id=f"{guild_id}", collection_id='guild_users', document_id=f"{uid}",
                                      data={
                                          'last_exp_drop': f"{msg_datetime}",
                                          'lvl': new_lvl,
                                          'exp': new_exp
                                      })

            return True, new_lvl
        else:
            databases.update_document(database_id=f"{guild_id}", collection_id='guild_users', document_id=f"{uid}",
                                      data={
                                          'last_exp_drop': f"{msg_datetime}",
                                          'exp': new_exp
                                      })
            return False, user['lvl']


def set_welcome_msg(guild_id, msg):
    databases = get_database_conn()
    databases.update_document(database_id=f"{guild_id}", collection_id='guild_settings', document_id='settings',
                              data={
                                  'welcome_msg': msg
                              })


def get_welcome_msg(guild_id):
    databases = get_database_conn()
    welcome_msg = databases.get_document(database_id=f"{guild_id}", collection_id='guild_settings',
                                         document_id='settings')

    return welcome_msg['welcome_msg']


def get_top_5(guild_id):
    databases = get_database_conn()
    top_5 = databases.list_documents(database_id=f"{guild_id}", collection_id='guild_users',
                                     queries=[Query.orderDesc('exp'), Query.limit(5)])['documents']
    return top_5


def get_user_lvl(guild_id, uid):
    databases = get_database_conn()
    user = databases.get_document(database_id=f"{guild_id}", collection_id='guild_users', document_id=f"{uid}")
    return user
