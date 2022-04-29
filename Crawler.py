import requests
import re
import os

headers={
     'User-Agent':'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
}
r=requests.get('http://jhsjk.people.cn/',headers=headers).text
    
pattern1=re.compile(r'<li><a href="article/(.*?)\?isindex=1" target="_blank"><span>.*?</span><i>.*?</i></a></li>')
ids=re.findall(pattern1,r)
#print(ids)
pattern2=re.compile('<li><a href="article/.*?\?isindex=1" target="_blank"><span>(.*?)</span><i>.*?</i></a></li>')
titles=re.findall(pattern2,r)
#print(titles)

flag=False
with open('info.txt','r',encoding='utf-8') as f:
    title=f.readline().strip()
    print(title)
    print(titles[0])
    if(title!=titles[0]):
        #更新
        flag=True
        
def Get_article(article_id):
    r=requests.get('http://jhsjk.people.cn/article/'+article_id,headers=headers).text
    title=re.findall('<h1>(.*?)</h1>',r)[0]
    infos=re.findall('<div class="d2txt_1 clearfix">(.*?)&nbsp;&nbsp;(.*?)</div>',r)
    paras=re.findall(r'\n<p style="text-indent: 2em;">(.*?)</p>',r,re.DOTALL)
    if(len(paras)==0):
        paras=re.findall(r'\n<p>(.*?)</p>',r,re.DOTALL)
    #print(r)
    #print(paras)
    with open('article.txt','w',encoding='utf-8') as f:
        f.write(title)
        f.write('\n')
        f.write('\n')
        f.write(infos[0][0])
        f.write(infos[0][1])
        f.write('\n')
        for para in paras:
            f.write(para)
            f.write('\n')
   
#print(flag)
if(flag):
    with open('info.txt','w',encoding='utf-8') as f:
        f.write(titles[0])
        f.write('\n')
        f.write(ids[0])
    Get_article(ids[0])

env_file = os.getenv('GITHUB_ENV')
with open(env_file, "a") as myfile:
    myfile.write("CHANGED="+str(flag))
