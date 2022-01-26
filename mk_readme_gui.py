import sys
from PyQt5.QtWidgets import QApplication, QGridLayout, QWidget, QLabel, QLineEdit, QDesktopWidget, QPushButton
from PyQt5.QtGui import QIcon, QIntValidator, QPalette, QColor
from markdownify import markdownify as md
import requests
from bs4 import BeautifulSoup
import os
import argparse

class autoBaekjoon:

    def __init__(self) -> None:
        headers = {            
            'User-Agent':'python-requests/2.24.0'}
        URL = f'https://www.acmicpc.net/problem/{problem_num}'
        html = requests.get(URL, headers=headers)
        self.soup = BeautifulSoup(html.content, 'html.parser')

    def parsing(self,id):
        datas = self.soup.select(f'{id}')        
        return datas
    
    
    def mkreadme(self,title,description,ex_input,ex_output,sample_data):        
        with open(f"{path}\{problem_num}\README.md", "w", encoding="utf-8") as f:
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
                    f.write(sample_data[i].rstrip())
                    f.write("\n```\n")
                else :
                    f.write(f"\n### 예제 출력{cnt}\n\n")
                    f.write("```\n")
                    f.write(sample_data[i].rstrip())                    
                    f.write("\n```\n")
                    cnt += 1
                
            f.write(f"""\n### 링크\n<a href="https://www.acmicpc.net/problem/{problem_num}" target="_blank">{problem_num}</a>""")

class mkReadmeGUI(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()
                        
    def initUI(self):
        self.setWindowTitle('입력창')        
        self.setWindowIcon(QIcon('.\\img\\keyboard.png'))
        # self.setFixedSize(260,100)
        self.setFixedSize(260,80)
        pal = QPalette()
        pal.setColor(QPalette.Background,QColor(255,255,255))
        self.setAutoFillBackground(True)
        self.setPalette(pal)
        self.center()
        
        self.button = QPushButton('&입력',self)
        self.button.clicked.connect(self.takeTextFunction)
                
        self.label = QLabel(self)                                
        # self.label.resize(260,300)        

        # self.label2 = QLabel(self)
        # self.label2.setText(f"경로:{path}")
        
        self.line_edit = QLineEdit(self)        
        self.line_edit.setValidator(QIntValidator(1000,40000,self))        
        self.line_edit.returnPressed.connect(self.takeTextFunction)
        
        # layout = QHBoxLayout() # 수평 박스 레이아웃 사용
        layout = QGridLayout() # 격자 레이아웃 사용        
        layout.addWidget(self.line_edit,0,0)
        layout.addWidget(self.button,0,1)
        layout.addWidget(self.label,1,0,1,0)
        # layout.addWidget(self.label2,1,0)

        self.setLayout(layout)

        self.show()    
      
    def takeTextFunction(self): #Lineedit에 있는 글자를 가져오는 메서드        
        try:
            if self.line_edit.text() == '':
                raise ValueError
            else:
                global problem_num
                problem_num = int(self.line_edit.text())                
                self.baekjoonParsing(problem_num)
        except ValueError:
            self.showLabel("입력값이 잘못되었습니다.")                        

    def showLabel(self,string, level=-1):
        # default 는 성공/실패 에따른 텍스트 색상 -1 : red 이외 black
        self.label.setHidden(False)
        if string.__len__() > 23:
            self.label.setText(string[:24]+'\n'+string[24:]) # 32
        else:
            self.label.setText(string)
        
        if level == -1:        
            self.label.setStyleSheet("color: red")
        else:
            self.label.setStyleSheet("color: green")
    
    def baekjoonParsing(self, problem_num):
        auto = autoBaekjoon()
        title = auto.parsing("#problem_title") # 제목
        try:
            title = md(str(title[0])).strip('\n')                    
            try:
                os.makedirs(f"{path}\{problem_num}") # 디렉터리 생성
                description = auto.parsing("#problem_description") # 문제설명
                description = md(str(description[0])).strip('\n')
                print(description.find('![](/'))
                if description.find('![](/') > -1:
                    description = description.replace('![](/','![](https://www.acmicpc.net/')

                ex_input = auto.parsing("#problem_input > p") # 입력        
                ex_input = md(str(ex_input[0])).strip('\n')    

                ex_output = auto.parsing("#problem_output") # 출력
                ex_output = md(str(ex_output[0])).strip('\n')    

                sample_data = [i.text for i in auto.parsing(".sampledata")] # 예제 입,출력
                auto.mkreadme(title,description,ex_input,ex_output,sample_data) # readme 파일 생성                
                self.showLabel(f"readme를 작성했습니다 경로:{path}\\{problem_num}",0)
            except FileExistsError:
                self.showLabel(f"폴더가 이미존재합니다.{path}\\{problem_num}")
                
        except IndexError:
            self.showLabel("없는 문제입니다.")

    def center(self): # 화면 중앙에 위치시켜주는 메서드
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()        
        qr.moveCenter(cp)
        self.move(qr.topLeft())

def get_arguments():
    parser = argparse.ArgumentParser(description="README.md 자동작성 프로그램")    
    parser.add_argument("-v", "--version", action="store_true", help="show version")
    parser.add_argument('-p', '--path', help="Input directory path.")
        
    args = parser.parse_args()

    if args.version:        
        print("version: v1.0.1")
        sys.exit(0)
    return args.path

if __name__ == '__main__':        
    try: # pyinstaller -F(exe파일 1개로만 생성) 옵션을 사용해 appdata 밑의 img\\keyboard.png 이미를 찾기위해 사용
        os.chdir(sys._MEIPASS)
        print(sys._MEIPASS)
    except:
        os.chdir(os.getcwd())

    path = get_arguments()    
    if not path :
        if getattr(sys, "frozen", False):            
            path = os.path.dirname(sys.executable)
        else:            
            path = os.path.dirname(os.path.abspath(__file__))
    
    app = QApplication(sys.argv)
    ex = mkReadmeGUI()
    
    sys.exit(app.exec_())