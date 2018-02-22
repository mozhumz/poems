import htmlUtil
from docx import Document
import docxUtil

#获取目标URL
def get_target_url(url,str1):
    target_url=''
    url_=str(url)
    url_s=url_.split('/')
    str2=str1.split('/')[1]
    for i in range(len(url_s)):
        if url_s[i]==str2:
            target_url=url_[0:url_.index(str2)-1]+str1
    return target_url

#循环获取目标诗歌标题列表
def get_poemTitle_list(pre,suf,pages,url_pre):
    poems=[]
    totalPage=pages
    page=1
    url=''
    a_list=[]
    while(page<=totalPage):
        url=url_pre+pre+'_'+str(page)+suf
        # print(url)
        soup=htmlUtil.getSoup(url)
        div=soup.find('div',class_='shicilist')
        if div:
            ul_list=div.find_all('ul')
            for ul in ul_list:
                a=ul.find('a')
                a_list.append(a)
                # print(a)
        # print(a_list)
        page+=1
    for a in a_list:
        target_url=get_target_url(url_pre,str(a.attrs.get('href')))
        # print(target_url)
        title=str(a.text)
        a_dict={'href':target_url,'title':title}
        poems.append(a_dict)
    return poems

#诗歌内容列表写入word
def write_poems_docx(poems,writer):
    content_list=[]
    document = Document()
    i=0
    for poem in poems:
        url=poem['href']
        # html = htmlUtil.getReq(url=url)
        title=poem['title']
        # print(url,title)
        soup=htmlUtil.getSoup(url)
        middle_div=soup.find(id='middlediv')
        div=middle_div.find('div',class_='zhuti yuanjiao')
        # h2=div.find('h2')
        content=div.find(id='shicineirong')
        sx=soup.find('div',class_='shangxi yuanjiao')
        h3_text=str(sx.find('h3').text)
        print(h3_text)
        #诗歌内容
        text=str(content.text).replace('<br/>','\n').replace('<br>','\n')
        #赏析
        sx_str=''
        if sx and h3_text!=writer+'简介':
            sx_str=str(sx.text).replace('<br/>','\n').replace('<br>','\n')

        #写入word
        i+=1
        document=docxUtil.write_docx(document,title,text,sx_str,i)


        # print(title,text,sx_str)
        # with open('h:/test/'+title+'.doc','w+') as f:
        #     f.write(title+'\n')
        #     f.write(text+'\n')
        #     f.write(sx_str)

    document.save('H:/test/'+writer+'诗歌.docx')


def get_poems(writer):

    # writer='李白'
    writer_e=htmlUtil.encodeurl(writer)
    url='http://www.shicimingju.com/chaxun/all/'+writer_e
    html=htmlUtil.getReq(url)
    # print(html)
    soup=htmlUtil.parseHtml(html)
    #获取a标签
    a=soup.find(id='alllist').find('a')
    # print(a)
    a_href=str(a.attrs.get('href'))
    a_text=str(a.text)
    # print(a_href,a_text)
    #总页数
    total=int(a_text[a_text.index('(')+1:a_text.index(')')])
    # print(totalPage)
    #获取目标URL,前后缀
    target_url=get_target_url(url,a_href)
    # print(target_url)
    target_url_=target_url.split('/')
    suffix=target_url_[len(target_url_)-1]
    # print(suffix)
    prefix=target_url[0:target_url.rindex('/')+1]
    # print(target_url,prefix)
    #前缀
    pre=suffix[0:1]
    #后缀
    suf='.'+suffix.split('.')[1]
    # print(suf)
    totalPage=int(total/40)+1
    poems=get_poemTitle_list(pre,suf,totalPage,prefix)
    write_poems_docx(poems,writer)

if __name__=="__main__":
    print("start...\n")
    writer='李白'
    get_poems(writer)
    print("\n"+"end")