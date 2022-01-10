""" import requests
from bs4 import BeautifulSoup

problem_num = 1021

headers = {
    # 'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'}        
    'User-Agent':'python-requests/2.24.0'}
# URL = 'http://www.useragentstring.com/'
URL = f'https://www.acmicpc.net/problem/{problem_num}'

# html = requests.get(URL, headers=headers)
# html = requests.get(URL).text
html = requests.get(URL,headers=headers)
# print(html)
soup = BeautifulSoup(html.content, 'html.parser')
print(soup.select('#problem_title'))
"""

from markdownify import markdownify as md
import requests
from bs4 import BeautifulSoup
import os

path= os.path.dirname(os.path.abspath(__file__))

problem_num = 1021
# problem_num = 11052

class autoBaekjoon:

    def __init__(self) -> None:
        headers = {            
            'User-Agent':'python-requests/2.24.0'}
        URL = f'https://www.acmicpc.net/problem/{problem_num}'
        html = requests.get(URL, headers=headers)
        self.soup = BeautifulSoup(html.content, 'html.parser')

    def parsing(self,id):
        datas = self.soup.select(f'{id}')
        # return [i.text for i in datas]
        return datas
    
    
    def mkreadme(self,title,description,ex_input,ex_output,sample_data):
        # with open("MKDIRTEST.md", "w", encoding="utf-8") as f:
        with open(f"{path}\{problem_num}\TEST_README.md", "w", encoding="utf-8") as f:
            f.write("# ")
            for i in title:
                f.write(i)

            f.write("\n\n## 문제\n")
            for i in description:
                f.write(i)

            f.write("\n\n## 입력\n\n")
            for i in ex_input:
                f.write(i)

            f.write("\n\n## 출력\n\n")
            for i in ex_output:
                f.write(i)
            
            f.write("\n")
            cnt = 1
            for i in range(len(sample_data)):
                
                if i % 2 == 0:
                    f.write(f"\n### 예제 입력{cnt}\n\n")
                    f.write("```\n")
                    f.write(sample_data[i])
                    f.write("```\n")
                else :
                    f.write(f"\n### 예제 출력{cnt}\n\n")
                    f.write("```\n")
                    f.write(sample_data[i])
                    f.write("```\n")
                    cnt += 1
                
            f.write(f"""\n### 링크\n<a href="https://www.acmicpc.net/problem/{problem_num}" target="_blank">{problem_num}</a>""")

    """ def mkdir(self,problem_num):
        os.makedirs(f"{path}\{problem_num}") """
        

    """ try:
            print(path,problem_num)
            if not os.path.exists(f"{path}\{problem_num}"):
                os.makedirs(f"{path}\{problem_num}")            
        except OSError:
            print ('Error: already directory exist.' + problem_num) """

        


if __name__ == '__main__':
    auto = autoBaekjoon()

    title = auto.parsing("#problem_title") # 제목
    title = md(str(title[0])).strip('\n')        
    try:
        os.makedirs(f"{path}\{problem_num}") # 디렉터리 생성
        description = auto.parsing("#problem_description") # 문제설명
        description = md(str(description[0])).strip('\n')
        
        ex_input = auto.parsing("#problem_input > p") # 입력        
        ex_input = md(str(ex_input[0])).strip('\n')    

        ex_output = auto.parsing("#problem_output") # 출력
        ex_output = md(str(ex_output[0])).strip('\n')    

        sample_data = [i.text for i in auto.parsing(".sampledata")] # 예제 입,출력
        auto.mkreadme(title,description,ex_input,ex_output,sample_data) # readme 파일 생성    
    except FileExistsError:
        print (f'Error: already directory exist:\n {path}\{problem_num}')



