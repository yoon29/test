'''
Python에서 Signal 처리
http://blog.kichul.co.kr/2018/01/12/python%EC%97%90%EC%84%9C-signal-%EC%B2%98%EB%A6%AC/

Python 스크립트가 예기치 않게 종료했을 때, 어떤 signal에 의해 종료되었는지를 확인이 필요한 경우가 있다.  다음 코드를 변형해서 프로그램에 맞게, 적절히 적용할 수 있다.
'''

############################################################################
import signal

# 각각의 signal에 대한 핸들러
def sighandler(signum, frame):
    ''' 시그널 처리 '''
    raise Exception("Signal. %i" % signum)

# signal 수신 함수
def register_all_signal():
    ''' 모든 시그널 등록 '''
    for x in dir(signal):
        if not x.startswith("SIG"):
            continue

        try:
            signum = getattr(signal, x)
            signal.signal(signum, sighandler)
        except:
            # signal 등록에 실패하는 경우 표시
            print('Skipping the signal : %s' % x)
            continue

# signal을 수신하는 function 실행
register_all_signal()

############################################################################
'''
이 외에도 종료되는 시점에 무엇인가 실행할 필요가 있을 때는 atexit를 사용 할 수 있다.
'''
import atexit

def at_exit_func():
    print
    "exited."

atexit.register(at_exit_func)

############################################################################

