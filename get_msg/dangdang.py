import os
import requests
import xlwt
from lxml import etree
from bs4 import BeautifulSoup
import redis

pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)#连接redis池
r = redis.Redis(host='localhost', port=6379, decode_responses=True)
keyword='数据结构'
workbook = xlwt.Workbook(encoding='utf-8')
worksheet_np = workbook.add_sheet('all')
url = f'http://search.dangdang.com/?key={keyword}'#地址
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML'\
    ', like Gecko) Chrome/95.0.4638.69 Safari/537.36'
}
root = os.getcwd()

os.chdir("dangdang")
response = requests.get(url=url, headers=headers)#发送请求
tree = etree.HTML(response.text)
print(tree)
li_list = tree.xpath('//div[@id="search_nature_rg"][@dd_name="普通商品区域"]/ul/li')#获取列表
index = 1
soup = BeautifulSoup(response.text,'html.parser')
print(soup.select('img'))
for li in li_list:
    try:
        name = li.xpath('.//p[@class="name"]/a/@title')[0]
        print(name)
        price = li.xpath('.//span[@class="search_now_price"]/text()')[0].replace('¥', '')
        print(price)
        src = li.xpath('.//a/img[@alt]/@data-original')[0]
        print(src)
    except:
        name = li.xpath('.//p[@class="name"]/a/@title')[0]
        print(name)
        price = li.xpath('.//span[@class="search_now_price"]/text()')[0].replace('¥', '')
        print(price)
        src = li.xpath('.//a/img[@alt]/@src')[0]
        print(src)
    dic = {#存入字典
            'name': name.strip(),
            'price': price.strip(),
            'lian': src.strip(),
            'from': '当当网'
    }
    r.hmset(f'{index}', dic)#存入redis数据库
    print(r.hgetall(f'{index}'))
    resp = requests.get('http:' + src, headers=headers)
    try:
        with open(f"{name}.jpg", "wb") as f:#下载图片
            f.write(resp.content)
            print(f"{name} {src} 保存成功")
    except:
        print('')
    print(dic)
    worksheet_np.write(index, 0, dic['name'])#保存到excel
    worksheet_np.write(index, 1, dic['price'])
    worksheet_np.write(index, 2, dic['from'])
    index = index+1
max_price = 0
print("Redis数据存储完毕，经计算后，最高价格为：")
for i in range(1, index):
    max_price = max(float(r.hget(f'{i}', 'price')), max_price)
print("最高价格为：", max_price)
worksheet_np.write(0, 0, "名称")
worksheet_np.write(0, 1, "价格")
worksheet_np.write(0, 2, "来源")
workbook.save('数据结构当当.xls')
response.close()
