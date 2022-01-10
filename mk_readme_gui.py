import sys
from PyQt5.QtWidgets import QApplication, QGridLayout, QHBoxLayout, QWidget, QLabel, QLineEdit, QDesktopWidget, QPushButton
from PyQt5.QtGui import QIcon, QIntValidator, QPalette, QColor
from markdownify import markdownify as md
import requests
from bs4 import BeautifulSoup
import os

path= os.path.dirname(os.path.abspath(__file__))

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
                    f.write(sample_data[i])
                    f.write("```\n")
                else :
                    f.write(f"\n### 예제 출력{cnt}\n\n")
                    f.write("```\n")
                    f.write(sample_data[i])
                    f.write("```\n")
                    cnt += 1
                
            f.write(f"""\n### 링크\n<a href="https://www.acmicpc.net/problem/{problem_num}" target="_blank">{problem_num}</a>""")

class mkReadmeGUI(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()
                        
    def initUI(self):
        self.setWindowTitle('입력창')        
        self.setWindowIcon(QIcon('keyboard.png'))
        self.setFixedSize(260,70)
        pal = QPalette()
        pal.setColor(QPalette.Background,QColor(255,255,255))
        self.setAutoFillBackground(True)
        self.setPalette(pal)
        self.center()
        
        self.button = QPushButton('&입력',self)
        self.button.clicked.connect(self.takeTextFunction)
                
        self.label = QLabel(self)
        
        self.line_edit = QLineEdit(self)        
        self.line_edit.setValidator(QIntValidator(1000,40000,self))        
        self.line_edit.returnPressed.connect(self.takeTextFunction)
        
        # layout = QHBoxLayout() # 수평 박스 레이아웃 사용
        layout = QGridLayout() # 격자 레이아웃 사용
        layout.addWidget(self.line_edit,0,0)
        layout.addWidget(self.button,0,1)
        layout.addWidget(self.label,1,0)

        self.setLayout(layout)

        self.show()    
      
    def takeTextFunction(self): #Lineedit에 있는 글자를 가져오는 메서드        
        try:
            if self.line_edit.text() == '':
                raise ValueError
            else:
                global problem_num
                problem_num = int(self.line_edit.text())
                print(f'문제번호 : {problem_num}')                
                self.label.setHidden(True) # 성공일시 ValueError 메세지를 숨김.
                self.baekjoonParsing(problem_num)
        except ValueError:
            self.label.setHidden(False)
            self.label.setText("입력값이 잘못되었습니다")
            self.label.setStyleSheet("color: red")
            self.label.adjustSize()
    
    def baekjoonParsing(self, problem_num):
        auto = autoBaekjoon()
        title = auto.parsing("#problem_title") # 제목
        try:
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
                self.label.setHidden(False)
                self.label.setText("폴더가 이미존재합니다")
                self.label.setStyleSheet("color: red")
                self.label.adjustSize()
        except IndexError:
            self.label.setHidden(False)
            self.label.setText("없는 문제입니다.")
            self.label.setStyleSheet("color: red")
            self.label.adjustSize()            

    def center(self): # 화면 중앙에 위치시켜주는 메서드
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()        
        qr.moveCenter(cp)
        self.move(qr.topLeft())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = mkReadmeGUI()
    
    sys.exit(app.exec_())
