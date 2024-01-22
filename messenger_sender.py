from pywinauto import findwindows, win32_element_info
from pywinauto import application
import time

app = application.Application(backend='uia')
base_path = "C:/Program Files (x86)/Hiworks/Messenger/HiworksMessenger.exe"
# data = app.start("C:/Program Files (x86)/Hiworks/Messenger/HiworksMessenger.exe") #이것만 하면 안된다 왜냐하면 뒤에 나오는 코드들이 해당 앱이 실행되기전에 찾지못하니까.


def sendToMe(name, Text) :
    count = 0
    while True :
        lst = []
        error = False
        if count >= 5 :
            break
        
        try :
            data = app.start(base_path)
            data = app.connect(title="하이웍스 메신저")
            
            if "하이웍스 메신저" in [w.window_text() for w in app.windows()] :                    
                dlg = app.window(title="하이웍스 메신저")
                # app['하이웍스 메신저'].print_control_identifiers()
                dlg.restore().set_focus()
                my_tree_item = dlg.child_window(title=name, control_type ="Text", auto_id="Name", top_level_only=True)
                # a = dlg['임재성Static0']
                
                my_tree_item.right_click_input()                

                dlg.child_window(title="채팅하기", control_type ="MenuItem")
                dlg['채팅하기MenuItem'].click_input()                

                chat = app.window(title='{}(나와의 채팅방)'.format(name))
                chat.restore().set_focus()        
                # chat.print_control_identifiers()
                
                input = chat.child_window( auto_id="SendRichTextBox", control_type="Document")
                input.click_input()        
                
                input.type_keys(Text)
                
                send_btn = chat.child_window(auto_id="Send_Btn", control_type="Custom")
                send_btn.click_input()
                break
            
        except Exception as e :
            error = True
            print(e)
        finally :
            if error :
                print("not running")
                time.sleep(1)
                count = count + 1
            else :
                print("end")
                break