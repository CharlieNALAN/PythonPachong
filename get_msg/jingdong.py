import os
import requests
import xlwt
from lxml import etree
from bs4 import BeautifulSoup
import redis

pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)#连接redis池
r = redis.Redis(host='localhost', port=6379, decode_responses=True)

keyword = '数据结构'
workbook = xlwt.Workbook(encoding='utf-8')
worksheet_np = workbook.add_sheet('alli')
url = f'https://search.jd.com/Search?keyword={keyword}'#地址
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,' \
                  'like Gecko) Chrome/81.0.4044.138 Safari/537.36 Edg/81.0.416.77'
}
root = os.getcwd()
os.chdir("jingdong")
response = requests.get(url=url, headers=headers)#发送请求
tree = etree.HTML(response.text)
li_list = tree.xpath('//div[@id="J_goodsList"]/ul/li')#获取列表
index = 1
soup = BeautifulSoup(response.text, 'html.parser')
for li in li_list:
    try:
        name = ''.join(li.xpath('./div/div[3]//em//text()'))

        price = li.xpath('.//div[@class="p-price"]//i/text()')[0]

        src = li.xpath('.//a/img/@data-lazy-img')[0]


    except:
        name = ''.join(li.xpath('.//div[@class="p-name p-name-type-2"]/a/em//text()'))

        price = li.xpath('.//div[@class="p-price"]//i/text()')[0]

        link = li.xpath('.// div / div[1] / a / img/@source-data-lazy-img src')[0]

    dic = {
        'name': name.strip(),
        'price': price.strip(),
        'tupian': src.strip(),
        'from': '京东'
    }
    r.hmset(f'{index}', dic)#存入redis数据库
    print(r.hgetall(f'{index}'))
    resp = requests.get('http:' + src, headers=headers)
    try:
        with open(f"{name}.jpg", "wb") as f:
            f.write(resp.content)
    except:
        print('')
    worksheet_np.write(index, 0, dic['name'])#保存到excel
    worksheet_np.write(index, 1, dic['price'])
    worksheet_np.write(index, 2, dic['from'])
    max_price = 0
    index = index + 1
print("Redis数据存储完毕，经计算后，最高价格为：")
for i in range(1, index):
    max_price = max(float(r.hget(f'{i}', 'price')), max_price)
print("最高价格为：", max_price)
worksheet_np.write(0, 0, "名称")
worksheet_np.write(0, 1, "价格")
worksheet_np.write(0, 2, "来源")
workbook.save('数据结构京东.xls')
response.close()
