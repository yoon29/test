'''
파이썬 플라스크 (Python + Flask) 로 자동 응답 슬랙 봇 만들기 (2_4)
https://kitle.xyz/post/62/

두번째 시간입니다.

Python + Flask 로 간단한 응답 서버 만들기
파이썬 개발환경은 구축되어 있으시죠? 없다면 PC에 pycharm 을 검색해 설치하시고 프로젝트를 하나 만들어주세요.

그다음 필요한 패키지를 설치해 보겠습니다. 파이썬 및 가상환경이 설치되어 있다는 가정하에 설명 드리겠습니다. 가상환경 만드는 법은 저의 python + flask 호스팅 게시글을 참고해주세요.

파이참 콘솔창을 실행합니다.
여기서 사용할 서버 프레임 워크는 flask로 정했습니다.
다음과 같이 설치해주세요.
pip install flask

그다음 slack 연결을 도와줄 slacker 패키지를 설치합니다.
pip install slacker

준비가 되었다면 이제 flask로 간단한 서버를 만들어 보겠습니다.
프로젝트에 새로운 파일을 만듭니다. flask_server.py 파일로 만듭니다.

다음을 복붙합니다.
크게 어려울 것 없이 서버의 / 로 이동하면 헬로월드를 리턴해주라는 간단한 함수를 만들었습니다.

바로 실행해보죠. 파이참의 터미널을 켭니다.
flask_server.py 가 있는 곳에서 다음과 같이 실행합니다.
터미널에서,
export FLASK_APP=flask_server.py
flask run

Serving Flask app "flask_server.py" (lazy loading)
 * Environment: development
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)

다음과 같은 실행화면을 볼 수 있을 겁니다.
웹브라우저에서 http://127.0.0.1:5000/ 을 접속해봅시다.
Hello,world! 가 출력되는 것을 알 수 있을 겁니다.

자 이제 슬랙 앱(봇)과 통신할 수 있는 서버를 만들었습니다.
Python + Flask 로컬 주소를 외부에서 접속 가능하게 끔 ngrok 를 사용하여 도메인 연결하기

하지만 내 PC는 외부에서 접속가능한 상용 서버가 아닙니다. 말그대로 로컬 서버라는 것이죠.
원래는 정식적으로 도메인을 구입하고 서버를 호스팅 받아 연결해야 합니다.
그러기엔 시간도 걸리고 비용도 발생하므로 우선은 임시 서비스로 해보겠습니다.
여기서는 ngrok 이라는 서비스를 이용해 해보겠습니다. 무료로는 임시로 8시간정도 제공됩니다.
재 발급시 url 주소가 바뀝니다.
추후에 직접 도메인 / 호스팅을 구매하시거나 무료 호스팅을 찾아보세요(쉽지는 않습니다).

개인적으로 유료 구매를 권장합니다.
혹시 사내 서비스로 이용하실 것이면 서버 관리자나 담당자에게 문의하여 발급 받도록 합니다.

자 그럼 다시 돌아와서 내 로컬 서버를 외부에서 접속하게 해주는 ngrok 을 설치해 보겠습니다.
이것은 파이썬 패키지로 설치하는 것이 아니라 내 PC에 설치하는 것입니다.

맥북의 경우 다음과 같이 설치합니다.
맥 터미널(콘솔) 창을 엽니다.

brew cask install ngrok
으로 설치합니다.

flask 로컬 서버를 먼저 실행하고 그다음 ngrok http 5000 명령어를 날립니다.
아까  http://127.0.0.1:5000/  이 플라스크를 이용한 서버였으니, http 5000 포트를 ngrok을 이용해 외부에서 접속할 수 있게 만들어줘 라고하는 요청입니다.

정상적으로 실행이 되면 Forwarding http https 두가지가 생깁니다. 여기서는 http:// 로 연결해보겠습니다.
http://127.0.0.1:5000/ 의 경우는 외부로 연결이 되지 않아 다른 PC에서는 확인이 불가합니다.

하지만 연결된 링크로는 정상적으로 웹사이트에서 보일 것입니다.
자 이제 외부에서도 접속 할 수 있게 되었으므로, Slack과 해당 주소를 연결 해 보겠습니다.

http://api.slack.com 으로 돌아가서 Your Apps > 만들어둔 봇 선택 >  Basic information > add features and functionality 메뉴로 진입합니다.
Event Subscriptions 메뉴로 진입합니다.

OFF -> ON 으로 켜주시고 Request URL에 ngrok 으로 발급받은 주소를 넣어봅니다.
Your URL didn't respond with the value of the challengeparameter. 에러가 나올 것입니다.
당신의 주소에 필수적으로 challenge value에 대한 것들과 응답을 맞춰 넣으라고 합니다. 안전을 위해 자체적으로 송수신 통신 약속을 만드는 것이죠.
플라스크 서버 파일에 challenge value와 통신 프로토콜을 정의 해 보도록 하겠습니다.
우선 인증을 위한 token 을 업데이트 해보겠습니다.
api.slack.com 의 OAuth & Permissions 메뉴로 진입하면 Bot User OAuth Access TokenOAuth & Permissions
부분에 있습니다.
이부분을 복사하여  flask_server.py 부분에 업데이트 합니다. token = "xoxb-YOURTOKEN" 부분을 본인의 앱 토큰으로 변경 해주세요. 그리고 다음과 같이 수정해봅시다.

# -*- coding: utf-8 -*-
import json
from flask import Flask, request, make_response
from slacker import Slacker

token = "xoxb-YOURTOKEN" #여기를 변경 해주세요
slack = Slacker(token)

app = Flask(__name__)

@app.route('/', methods=['POST'])
def hello_there():
    slack_event = json.loads(request.data)
    if "challenge" in slack_event:
        return make_response(slack_event["challenge"], 200, {"content_type": "application/json"})
    return make_response("There are no slack request events", 404, {"X-Slack-No-Retry": 1})

if __name__ == '__main__':
    app.run(debug=True)

자 이제 모든 연결이 끝났습니다.

자 다시 http://api.slack.com 으로 돌아가서 Basic information > add features and functionality 메뉴로 진입합니다.
Event Subscriptions 메뉴로 진입합니다.
OFF -> ON 으로 켜주시고 Request URL에 ngrok 으로 발급받은 주소를 넣어봅니다.
Your URL didn't respond with the value of the challengeparameter. 에러가 나오지 않고 Verified 가 나와야 합니다.
드디어 연결 성공입니다.
만약 성공하지 못한다면 flask가 실행중인지, ngrok 을 맞게 연결했는지, ngrok이 시간 초과되지 않았는지(무료계정은 8시간 및 재발급시 만료됩니다).
천천히 검토해보시기 바랍니다.

다음시간은 봇이 응답을 듣고 답변하도록 만들어 보도록 하겠습니다.

'''

import json
from flask import Flask, request, make_response
from slacker import Slacker

token = "xoxb-YOURTOKEN"
slack = Slacker(token)

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'


# @app.route('/', methods=['POST'])
# def hello_there():
#     slack_event = json.loads(request.data)
#     if "challenge" in slack_event:
#         return make_response(slack_event["challenge"], 200, {"content_type": "application/json"})
#     return make_response("There are no slack request events", 404, {"X-Slack-No-Retry": 1})
#
# if __name__ == '__main__':
#     app.run(debug=True)
