'''
파이썬 플라스크 (Python + Flask) 로 자동 응답 슬랙 봇 만들기 (3_4)
https://kitle.xyz/post/67/

지난시간 내용들 빠르게 정리하여 드리겠습니다.
1교시 Slack 가입 및 Workspace 생성 > Slack API 사이트에서 APP(BOT)만들기
Bot 권한주기 설치하기 > Workspace에서 Bot 불러오기
2교시 Python + Flask로 서버 만들기
외부에서 접속 가능하게 끔 ngrok 을 이용하여 도메인 만들기
만든 주소를 SLACK API App(Bot)에 Event 연결하기 - 연결 시 통신 check 를 위해 challenge value 설정하기
이렇게 진행되었고요.


이제야 직접 봇에게 말을 듣고 하게 할 수 있습니다.
로봇 만들기 만만치 않죠?
1, 2 교시에서 어지간한 설정은 했지만
오늘은 추가적인 설정을 마무리하고 실제 로봇과의 대화에 들어가겠습니다.

첫번째로 할 일은 @ 태그로 봇에게 요청했을때 답변하게 하도록 해 보겠습니다.
첫번째로는 권한을 주어야겠죠?

앱설정 > Event Subscriptions > subscribe to bot event 메뉴로 갑니다.
Event Name - app_mention  해당 권한을 추가합니다.


앱을 멘션하면 이 이벤트를 감지하겠다는 겁니다.

로봇도 생명체와 같이
서버를 실행해 생명을 불어 넣고,
누가 널 부르면 반응해줘 - 라는 교육을 시키듯이 해당 이벤트를 추가합니다.
그런데 뭐라고 대답할지는 가르쳐 주지 않았습니다.
가르쳐야죠. (으휴 이 깡통..)

flask_server.py 를 수정해보겠습니다.
다음과 같이 수정했습니다.

hello_there 함수 부터 보시죠.
기존에 challenge 부분은 slack 과 통신이 잘 되는지 체크하는 부분이고,

만약 슬랙에서 event가 들어왔다면 이벤트를 처리해 줄 수 있는 event_handler 에게 넘겨주는 역할이 추가되었습니다.

그다음은 event_handler 가 처리합니다.
봇은 이 부분에서 다양한 이벤트 중에 어떤 이벤트를 어떻게 처리할지를 정하게 되는데요.

실제 어떤 내용이 전달되는지는
이벤트 핸들러 안에서, print(slack_event)를 호출해 보시면 아 이런식으로 메세지가 오는구나 알 수 있습니다.
그러나 포멧이 항상 동일하지는 않습니다. 사람이 보낸 경우, 봇이 응답한 경우, DM인경우, 채널에 보낸 경우 데이터와 양이 모두 다른데요. 여기서는 우선 간단하게 좀 지저분한 방법으로 메세를 전부 스트링으로 바꾸어 내가 원하는 메세지가 어떤정보를 포함하는지에 따라 처리하도록 하겠습니다.
  string_slack_event.find("{'type': 'user', 'user_id': ") != -1:  부분입니다. (좋은 처리 방법은 아닙니다)
파이썬의 문자열 찾기 기능을 활용해보니 타입이 유저이고 유저 아이디 필드가 있다면 사람이 직접 메세지를 보낸 것이라고 가정할 수 있습니다. 로봇이 보낸 응답을 로봇이 또 응답하면 무한루픙에 빠지기 때문에 이런 처리가 필요하죠. 사실 멘션으로 호출하지 않았을 수도 있지만, 어차피 우리가 모니터링 하는 권한은 현재 멘션밖에 없기때문에 쓸 수 있습니다. 멘션/멘션아닌 경우를 분리하는 것은 뒤에 넣도록 하죠.
  user_query = slack_event['event']['blocks'][0]['elements'][0]['elements'][1]['text']
 윗 부분은 얻어온 값중 실제 메세지 부분만 뽑아 낸 것입니다.

이제 봇에 걸맞게 답변을 해주는 함수를 만들기 전에...
모든것은 단계가 있죠. 우선 앵무새 봇을 만들어 볼게요. 내가 말한 것을 똑바로 알아듣고 똑같이 대답할 수 있다면 모든 통신이 완벽하게 되었음을 의미하기 때문입니다.

 answer = get_answer(user_query) #사용자 질의에 맞는 답변을 구하여
 slack.chat.post_message(channel, answer) #해당하는 슬랙 채널에 메세지를 보내거라

함수부는 이렇게 됩니다.
def get_answer(user_query):
    return user_query
받은대로 돌려준다. 참 똑똑하죠? -.-

실제 돌려보겠습니다. 잘 되죠?

공개된 채널에서 @으로 봇을 호출했을때와 그냥 대화할때랑 차이가 있을 겁니다.
이제 4교시에서는 원하는 질문에 맞게 대답하도록 Bot에게 지능을 주어보겠습니다.

4교시 이동 : http://kitle.xyz/post/151
내용 참고한곳 : https://ndb796.tistory.com/201

'''

# -*- coding: utf-8 -*-
import json
from flask import Flask, request, make_response
from slacker import Slacker

token = "YOUR_BOT_TOKEN" #Bot
slack = Slacker(token)

app = Flask(__name__)



def get_answer(user_query):
    return user_query

def event_handler(event_type, slack_event):
    channel = slack_event["event"]["channel"]
    string_slack_event = str(slack_event)
    if string_slack_event.find("{'type': 'user', 'user_id': ") != -1:  # 멘션으로 호출
        try:
            user_query = slack_event['event']['blocks'][0]['elements'][0]['elements'][1]['text']
            answer = get_answer(user_query)
            slack.chat.post_message(channel, answer)
            return make_response("ok", 200, )
        except IndexError:
            pass

    message = "[%s] cannot find event handler" % event_type
    return make_response(message, 200, {"X-Slack-No-Retry": 1})



@app.route('/', methods=['POST'])
def hello_there():
    slack_event = json.loads(request.data)
    if "challenge" in slack_event:
        return make_response(slack_event["challenge"], 200, {"content_type": "application/json"})
    if "event" in slack_event:
        event_type = slack_event["event"]["type"]
        return event_handler(event_type, slack_event)
    return make_response("There are no slack request events", 404, {"X-Slack-No-Retry": 1})



if __name__ == '__main__':
    app.run(debug=True)

