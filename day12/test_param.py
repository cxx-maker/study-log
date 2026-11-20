import pytest #做测试的库导入
import requests  #发送http请求的库导入
import yaml  #yaml文件解析的库导入
from pathlib import Path #拼路径，摆脱系统差异的库导入

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0",
    "Referer": "https://www.bilibili.com",
}#请求头的伪装成浏览器
#读yaml 返回python列表，每个元素是一条用例数据
def load_cases(path):
    with open(path,"r",encoding="utf-8") as f:#with出块自动关文件
        cases = yaml.safe_load(f)   #直接返回list[dict]不用自己解析
    return cases #文件一关，数据以在内存里
BASE_DIR = Path(__file__).parent #本.py文件所在目录
cases = load_cases(BASE_DIR/"cases.yaml") #模块及执行，pytest收集阶段就读好数据

@pytest.mark.parametrize("case",cases)#五条数据展开成五条测试，参数名必须跟下面一致
def test_bili_api(case):#case=列表里的某一条dict
    resp = requests.get(case["url"],headers=HEADERS,timeout=5)#url来自数据，代码不知道具体接口
    body = resp.json()#响应字符串变成字典
    assert body["code"] == case["expect_code"]#业务码对比