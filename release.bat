@REM pyinstaller -F -w mk_readme_gui.py
pyinstaller -F -w mk_readme_gui.spec
rmdir /s /q .\__pycache__\
rmdir /s /q .\build\
@REM del /q .\baekjoon_parsing.spec
move D:\code\github\baekjoon_readme\dist\mk_readme_gui.exe D:\code\github\baekjoon_readme
rmdir /s /q .\dist\