import sys
import json
import base64
import time

from pyaudio_record import record_audio
from jason_parse import read_result

from urllib.request import urlopen
from urllib.request import Request
from urllib.error import URLError
from urllib.parse import urlencode

#
# timer = time.perf_counter()

#
# API_KEY = 'Sy1nNGgsCo7YG8eXWKUjE8Xj'
# SECRET_KEY = '1bBkBkK3404NNPttOOQycDh8mxGg8Zhp'

AUDIO_FILE = './audio/record.wav'
FORMAT = AUDIO_FILE[-3:]

CUID = '123456PYTHON'
RATE = 16000

DEV_PID = 1537
ASR_URL = 'http://vop.baidu.com/server_api'
SCOPE = 'audio_voice_assistant_get'


def get_key(path = "KEY.txt"):
    with open(path, "r", encoding="utf-8") as f:
        API_KEY = f.readline().strip()
        SECRET_KEY = f.readline().strip()
        return API_KEY, SECRET_KEY

def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()

class DemoError(Exception):
    pass


""" TOKEN start """

TOKEN_URL = 'http://openapi.baidu.com/oauth/2.0/token'

def fetch_token():
    API_KEY,SECRET_KEY = get_key()
    params = {'grant_type': 'client_credentials',
              'client_id': API_KEY,
              'client_secret': SECRET_KEY}
    # print(params)
    post_data = urlencode(params)
    # IF PYTHON3
    # if IS_PY3:
    post_data = post_data.encode('utf-8')
    req = Request(TOKEN_URL, post_data)
    try:
        f = urlopen(req)
        result_str = f.read()
    except URLError as err:
        print('token http response http code : ' + str(err.code))
        result_str = err.read()
    # IF PYTHON3
    # if IS_PY3:
    result_str = result_str.decode()

    # print(result_str)
    result = json.loads(result_str)
    # print(result)
    if ('access_token' in result.keys() and 'scope' in result.keys()):
        # print(SCOPE)
        if SCOPE and (not SCOPE in result['scope'].split(' ')):  # SCOPE = False 忽略检查
            raise DemoError('scope is not correct')
        # print('SUCCESS WITH TOKEN: %s  EXPIRES IN SECONDS: %s' % (result['access_token'], result['expires_in']))
        return result['access_token']
    else:
        raise DemoError('MAYBE API_KEY or SECRET_KEY not correct: access_token or scope not found in token response')

""" TOKEN end   """


def asr_json():
    speech_data = []
    with open(AUDIO_FILE, 'rb') as speech_file:
        speech_data = speech_file.read()

    length = len(speech_data)
    if length == 0:
        raise DemoError('file %s length read 0 bytes' % AUDIO_FILE)
    speech = base64.b64encode(speech_data)
    # IF PYTHON3
    # if IS_PY3:
    speech = str(speech, 'utf-8')
    params = {'dev_pid': DEV_PID,
              # "lm_id" : LM_ID,    #测试自训练平台开启此项
              'format': FORMAT,
              'rate': RATE,
              'token': token,
              'cuid': CUID,
              'channel': 1,
              'speech': speech,
              'len': length
              }
    post_data = json.dumps(params, sort_keys=False)
    # print post_data
    req = Request(ASR_URL, post_data.encode('utf-8'))
    req.add_header('Content-Type', 'application/json')
    try:
        begin = timer()
        f = urlopen(req)
        result_str = f.read()
        # print ("Request time cost %f" % (timer() - begin))
    except URLError as err:
        # print('asr http response http code : ' + str(err.code))
        result_str = err.read()

    # if (IS_PY3):
    # if IS_PY3:
    result_str = str(result_str, 'utf-8')
    # print(result_str)
    with open("./result/result.txt","w") as of:
        of.write(result_str)

if __name__ == '__main__':
    timer = time.perf_counter

    record_audio("./audio/record.wav", record_second=5)

    token = fetch_token()

    asr_json()

    dict = json.loads(read_result())
    print('当前识别的内容为：' + dict['result'][0])
