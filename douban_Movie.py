#coding=utf-8
#导入第三方库
#requests获取网页的方法
import requests
#lxml.html支持用xpath从网页数据过滤所需网页内容
import lxml.html
#将获取的内容以csv的格式保存到本地
import csv

#目标网页的url是"https://movie.douban.com/top250?start=0&filter=", 每页的差别只是start=25/50/75...,规律是(i-1)*25,用start={}替换即可
douban_url = "https://movie.douban.com/top250?start={}&filter="

#定义一个函数，获取目标网页内容
def getSource(url):
    response = requests.get(url)
    #将获取内容转成utf-8编码格式
    response.encoding = "utf-8"
    #将网页内容返回
    return response.content
#定义一个函数，从网页所有内容里，分析并且获取到每一条电影内容
def getEveryItem(source):
    #通过lxml.html.document_fromstring方法将网页内容转换
    selector =lxml.html.document_fromstring(source)
    #通过xpath过滤出每条电影，xpath格式'//div[@class="info"]/a/span[@class="title"]/text()'
    movieItemList = selector.xpath('//div[@class="info"]')
    #定义一个列表，用来存放所有电影信息
    movieList = []

    for eachMovie in movieItemList:
        #定义一个字典，用来存放每条电影的标题、评分、名句、url
        movieDict ={}
        #通过xpath定位电影标题
        title = eachMovie.xpath('div[@class="hd"]/a/span[@class="title"]/text()')
        #通过xpath定位电影英文标题
        otherTitle = eachMovie.xpath('div[@class="hd"]/a/span[@class="other"]/text()')
        #通过xpath定位url
        link = eachMovie.xpath('div[@class="hd"]/a/@href')[0]
        #通过xpath定位评分
        star = eachMovie.xpath('div[@class="bd"]/div[@class="star"]/span[@class="rating_num"]/text()')
        #通过xpath定位名句
        quote = eachMovie.xpath('div[@class="bd"]/p[@class="quote"]/span[@class="inq"]/text()')
        #将电影标题、url、评分、名句存放到字典里
        movieDict['title'] = ''.join(title+otherTitle)
        movieDict['url'] = link
        movieDict['star'] = star
        movieDict['quote'] = quote
        #将每条电影信息打印出来
        #print(movieDict)
        #将每条电信信息以字典的形式添加到电影列表里
        movieList.append(movieDict)
    #将所有电影信息返回
    return movieList
#定义一个函数，将返回的电影内容保存到本地
def writeData(movieList):
    #创建一个以utf-8格式的空的csv文件，用于存放电影信息
    with open('./DouBanMovie.csv','w',encoding='utf-8') as f:
        #创建文件第一行以title/star/quote/url
        writer = csv.DictWriter(f,fieldnames=['title','star','quote','url'])
        #把文件头写好
        writer.writeheader()
        #把每一条电影信息写到csv的每一行
        for each in movieList:
            writer.writerow(each)

if __name__ == '__main__':
    for i in range(10):
        movieList = []
        pageLink = douban_url.format(i*25)
        print(pageLink)
        source = getSource(pageLink)
        movieList +=getEveryItem(source)

    print(movieList[:10])
    writeData(movieList)




