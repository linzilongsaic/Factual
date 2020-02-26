import re
import time
import datetime
from tqdm import tqdm


# 进度信息可视化(进度条)
def sleepBar(seconds):
    for _ in tqdm(range(seconds)):
        time.sleep(1)


# 命名方法
def prettyOutputName(query, filetype='html'):
    _query = re.sub('\s|\"|\/|\:|\.','_', query.rstrip())
    prettyname = _query
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y_%H-%M-%S-%f')
    if filetype != 'html':
        prettyname += "_" + st + "." + filetype
    else:
        prettyname += "_" + st + "." + filetype
    return prettyname
