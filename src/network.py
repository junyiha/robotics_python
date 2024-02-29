'''

'''

from base import *

headers = {'Content-Type' : 'application/json'}

# 3kg
addr = "http://192.169.7.32:9999"

# 10kg
# addr = "http://192.169.0.125:9999"

def SendRequest(url, body = ''):
    '''
        输入请求地址和请求数据，返回响应数据
    '''
    try:
        if body:
            print("请求方法: POST\n")
            response = requests.post(url, data=body, headers=headers)
        else:
            print("请求方法: GET\n")
            response = requests.get(url)
    except requests.exceptions.RequestException as e:
        print(f"请求发生异常: {e}")
        sys.exit(-1)
        
    return response