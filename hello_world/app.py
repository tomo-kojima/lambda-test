import json
import psycopg2
from psycopg2 import Error
import psycopg2.errorcodes

check_version_query = 'SELECT version()'
table_name = "test1"
create_query = f'create table {table_name} (id integer, name varchar(100))'
insert_query = f'insert into {table_name} values(1,\'aiueo\')'
select_query = f'SELECT * FROM {table_name}'


def get_connect():
    try:
        # Todo: 要設定
        connector = psycopg2.connect('postgresql://{user}:{password}@{host}:{port}/{dbname}'.format(
            user="postgres",  # ユーザ
            password="???",  # パスワード
            host="???.ap-northeast-1.rds.amazonaws.com",  # RDSエンドポイント
            port="5432",  # ポート
            dbname="test"))  # データベース名

        # カーソル取得
        cursor = connector.cursor()
    except(Exception, Error) as error:
        print("PostgreSQLへの接続時のエラーが発生しました", error)
        return {
            "statusCode": 500,
            "body": json.dumps({
                "message": "db connected error",
            }),
        }

    return connector, cursor


def exec_query(connector, cursor, query):
    err_response = None
    re_connect = False
    try:
        print(query)
        cursor.execute(query)
    except Error as error:
        if error.pgcode == psycopg2.errorcodes.DUPLICATE_TABLE:
            cursor.close()
            connector.close()
            re_connect = True
        else:
            cursor.close()
            connector.close()
            print(f'{query} でExceptionが発生しました', error)
            err_response = {
                "statusCode": 500,
                "body": json.dumps({
                    "message": "Error",
                }),
            }
    except Exception as error:
        cursor.close()
        connector.close()
        print(f'{query} でExceptionが発生しました', error)
        err_response = {
            "statusCode": 500,
            "body": json.dumps({
                "message": "Exception",
            }),
        }
    return err_response, re_connect


def lambda_handler(event, context):
    """Sample pure Lambda function

    Parameters
    ----------
    event: dict, required
        API Gateway Lambda Proxy Input Format

        Event doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format

    context: object, required
        Lambda Context runtime methods and attributes

        Context doc: https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html

    Returns
    ------
    API Gateway Lambda Proxy Output Format: dict

        Return doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html
    """
    print("lambda start")

    connector, cursor = get_connect()

    exec_query(connector, cursor, check_version_query)
    result = cursor.fetchone()
    print(result[0] + "に接続しています。")

    err_response, re_connect = exec_query(connector, cursor, create_query)
    if re_connect:
        connector, cursor = get_connect()
    if err_response is not None:
        return err_response

    err_response, re_connect = exec_query(connector, cursor, insert_query)
    if re_connect:
        connector, cursor = get_connect()
    if err_response is not None:
        return err_response

    err_response, re_connect = exec_query(connector, cursor, select_query)
    if re_connect:
        connector, cursor = get_connect()
    if err_response is not None:
        return err_response

    rows = cursor.fetchall()
    print(rows)

    connector.commit()
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "hello world",
            "row": rows,
        }),
    }
