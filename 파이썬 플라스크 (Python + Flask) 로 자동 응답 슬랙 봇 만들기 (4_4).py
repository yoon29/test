'''
파이썬 플라스크 (Python + Flask) 로 자동 응답 슬랙 봇 만들기 (4_4)
https://kitle.xyz/post/151/

4/4)번째 마지막 강좌입니다. 지난 강좌에서는 slack을 이용하여 @botname 메세지를 입력하면 똑같이 대답해주는 앵무새 봇을 만들었습니다.

슬랙과 여러분이 만든 서버가 메세지를 주고 받고 할 수 있게 된 것이죠.

마지막 시간은 여러분이 원하는 응답을 사전식으로 만들어 놓고 이를 대답할 수 있게 만들어 보겠습니다. 물론 더 좋은 방법과 지능적인 방법이 있겠지만 여기서는 여러가지 답변들을 미리 등록해 놓고 대답하는 FAQ같은 기능이라고 보면 되겠습니다.

그리고 사용자들이 어떤 검색어를 입력했는지 로그를 남기고, 이를 토대로 봇을 발전시켜 나갈수도 있겠죠?

그러면 마지막 강좌를 시작하겠습니다.

앵무새 답변이 아닌 키워드 식으로 답변하기
예를들어 'hello' 라고 입력하면 'hi there' 이라고 답변하게 만들어주고 싶습니다.

python에서는 dict 자료구조를 활용하여 쉽게 만들 수 있죠. 수정할 부분은 지난번 앵무새 봇에서 만들어 두었던

def get_answer(user_query): 부분을 수정하겠습니다.

def get_answer(user_query):
    raw_user_query = user_query
    user_query = raw_user_query.replace(" ", "")

    answer_dict = {
        'hello': 'hi there',
    }

사용자 입력은 띄어쓰기를 하는 사람도 있고 아닌 사람도 있고 천차 만별일 겁니다. 여기서는 모든 띄어쓰기를 없에는 방식으로 구현해보겠습니다. 사용자 입력은 모두 공백을 제거하도록 하겠습니다.
답변 딕셔너리에 key-value 방식으로 만들었습니다.

그리고 몇가지 예외처리를 해줘야겠습니다. 봇을 호출했지만 아무말도 안쓴 경우도 있을 겁니다. 그런 경우는 예외처리를 해줍니다.

def get_answer(user_query):
    raw_user_query = user_query
    user_query = raw_user_query.replace(" ", "")

    answer_dict = {
        'hello': 'hi there',
    }

    if user_query == '' or None:
        return "앗.. 아무것도 안쓰셨거나.. 혹은 아직 해석 불가 글자에요. 아직 그정도로 똑똑하진 않아요."
    elif user_query in answer_dict.keys():  # 결과 있으면 리턴
        return answer_dict[user_query]
    else:
        return user_query+"은(는) 없는 질문입니다."

자 이제 봇에게 명령을 날려보죠.


3가지 모드가 구현되었습니다.
딕셔너리에 없으면 없는 질문으로 처리되었습니다.
hello는 키에 매핑되기 때문에 답변되었습니다.
그리고 :) 등의 이모티콘만 날리면 사용자 메세지는 없는 것으로 되더라구요. 그래서 이부분은 없는 것으로 보고 예외처리를 하였습니다. 센스있게 답변 메세지는 언제든지 바꿀 수있어요.

키워드 답변에 날짜/요일 알려주기
팀원분들께 테스트를 해보니 '오늘이 무슨 요일이니?' 등의 고급 질의를 ㅠ.ㅠ 하시더라구요. 그래서 이부분을 완벽히 처리할 수는 없지만 요일을 입력하면 간단히 처리할 수 있게 키워드를 등록해 보겠습니다. 현재 날짜 시간등 정보를 얻어오기위해 파이썬 pytz 를 사용하겠습니다.

터미널로 이동하여 설치하여주세요.

(venv) $ pip install pytz
설치가 완료되었으면 import 해줍니다.

from datetime import datetime
import time
import pytz


def get_datetime(weekday=None):
    asia_seoul = datetime.fromtimestamp(time.time(), pytz.timezone('Asia/Seoul'))
    t = ['월요일', '화요일', '수요일', '목요일', '금요일', '토요일', '일요일']

    if weekday is None:
        fmt = "%Y-%m-%d %H:%M:%S"
        s = asia_seoul.strftime(fmt)
        return s
    else:
        return t[asia_seoul.today().weekday()]

def get_answer(user_query):
    raw_user_query = user_query
    user_query = raw_user_query.replace(" ", "")

    answer_dict = {
        'hello': 'hi there',
        '요일': 'Asia/Seoul 현재 ' + str(get_datetime()) + '입니다. 오늘은 ' + str(get_datetime('weekday')) + '입니다.',

    }
    # 뒷부분 생략..


현재의 날짜와 요일을 계산하는 get_datetime() 함수를 만들고 답변 딕셔너리에는 '요일'을 입력하면 해당 날짜와 요일을 알려주는 부분을 넣었습니다. 돌려보죠

생각보다 잘 돌아가는군요. 아주 좋습니다.
이번엔 회사 전화번호를 알려주는 부분을 넣어 보겠습니다.
답변 딕셔너리를 다음과 같이 수정하겠습니다.

   answer_dict = {
        'hello': 'hi there',
        '요일': 'Asia/Seoul 현재 ' + str(get_datetime()) + '입니다. 오늘은 ' + str(get_datetime('weekday')) + '입니다.',
        '전화번호': '\n회사 번호 :  02-000-000. \n 고객 콜센터: 080-1544-0000',
    }
'전화번호' 라는 키워드로 답변이 되지만 '번호' 나 '콜센터'를 검색하는 경우는 없는 단어로 나올 겁니다.
이 부분은 어떻게 처리하면 좋을까요? 키워드나 내용에 해당 단어가 있으면 완벽한 매칭(hit)는 아니더라도, 추천 답변으로 처리할 수 있을 겁니다. 다음을 보시죠.

get_answer 의 조건문을 조금 조정해보겠습니다.

 if user_query == '' or None:
        return "앗.. 아무것도 안쓰셨거나.. 혹은 아직 해석 불가 글자에요. 아직 그정도로 똑똑하진 않아요."
    elif user_query in answer_dict.keys():  # 결과 있으면 리턴
        return answer_dict[user_query]
    else:

        for now_key in answer_dict.keys():  # 키에서 먼저 찾고
            if now_key.find(user_query) != -1:
                return "연관 단어인 '"+now_key+"'에 대한 답변입니다.\n"+now_key+' : '+answer_dict[now_key]

        for now_key in answer_dict.keys():  # 키가 없으면 본문에 검색
            if answer_dict[now_key].find(raw_user_query[1:]) != -1:
                return "관련이 있나 모르겠지만 답변 내용에"+answer_dict[now_key]+'가 있네요.\n'+now_key+'에 대한 답변이에요.'

    return user_query+"은(는) 없는 질문입니다."

위와 같이 처리하면 부분 매칭이 되도 검색 결과를 보여줄 것입니다. 다만 부정확한 결과가 될 수 있어 고도화가 필요합니다.
결과를 한번 보시죠.

첫번째는 딕셔너리 키에 매핑되는 경우, 두번째는 딕셔너리 키에 없고 키에 부분매칭 되는 경우, 세번째는 키에 매칭이 없고 내용에서 찾은 경우입니다. 다만 단어에따라 엉뚱한 답변이 올 수 있으므로 이 부분은 사용자들이 어떤 단어를 검색하는지 기록하고 이를 통해 고도화 할 필요가 있겠습니다.

사용자 검색어를 로그로 저장하기
마지막으로 사용자 검색어를 로그로 저장해 분석해보도록 하겠습니다. 간단하게 검색어를 파일로 해당 시간에 저장하면 끝입니다. 최종 코드까지 한번에 확인하시죠.

일단 디버그용 코드이니 적절히 수정하셔서 사용하시면 될것 같습니다.
그러면 로그가 잘 남았나 마지막으로 확인하고 마치겠습니다.
소스 수정 후 누군가 봇에게 메세지를 남기면 searchlog.log 파일로 남게 됩니다. 확장자는 편하게 .csv 등으로 변경해도 문제가 없겠네요.

봇 다이렉트 응답 만들기
매번 @ 로 봇을 불러서 하기도 귀찮을 수 있습니다. 봇과 1:1로 직접 대화하는 것도 좋겠죠. 채널에 불필요한 알람도 줄이구요.
이부분은 위 소스 코드에 다이렉트 호출 부분에 적용되어 있습니다.

Apps -> 해당 봇에 바로 말을 걸면 멘션을 쓰지 않아도 훨 편리하게 됩니다. 봇과의 비밀스런(이라고 쓰고 로그 남음) 대화도 가능하겠네요.

이제 사용자 입력을 통해 키워드와 답변을 고도화 하면 될것 같습니다. 이상 마치겠습니다.

'''

from slacker import Slacker
import json
from flask import Flask, request, make_response
from datetime import datetime
import time
import pytz

token = "YOUR_TOKEN" #이부분 api.slack.com에서 발급받은 부분 넣으세요
slack = Slacker(token)

app = Flask(__name__)


def get_datetime(weekday=None):
    asia_seoul = datetime.fromtimestamp(time.time(), pytz.timezone('Asia/Seoul'))
    t = ['월요일', '화요일', '수요일', '목요일', '금요일', '토요일', '일요일']

    if weekday is None:
        fmt = "%Y-%m-%d %H:%M:%S"
        s = asia_seoul.strftime(fmt)
        return s
    else:
        return t[asia_seoul.today().weekday()]


def get_answer(user_query):
    with open('searchlog.log', 'a') as f:  # 유저 검색어는 로그로 저장, 시간 / 검색어만 저장
        f.write(str(get_datetime())+','+user_query+'\n')

    raw_user_query = user_query
    user_query = raw_user_query.replace(" ", "")

    answer_dict = {
        'hello': 'hi there',
        '요일': 'Asia/Seoul 현재 ' + str(get_datetime()) + '입니다. 오늘은 ' + str(get_datetime('weekday')) + '입니다.',
        '전화번호': '\n회사 번호 :  02-000-000. \n 고객 콜센터: 080-1544-0000',
    }

    if user_query == '' or None:
        return "앗.. 아무것도 안쓰셨거나.. 혹은 아직 해석 불가 글자에요. 아직 그정도로 똑똑하진 않아요."
    elif user_query in answer_dict.keys():  # 결과 있으면 리턴
        return answer_dict[user_query]
    else:

        for now_key in answer_dict.keys():  # 키에서 먼저 찾고
            if now_key.find(user_query) != -1:
                return "연관 단어인 '" + now_key + "'에 대한 답변입니다.\n" + now_key + ' : ' + answer_dict[now_key]

        for now_key in answer_dict.keys():  # 키가 없으면 본문에 검색
            if answer_dict[now_key].find(raw_user_query[1:]) != -1:
                return "관련이 있나 모르겠지만 답변 내용에" + answer_dict[now_key] + '가 있네요.\n' + now_key + '에 대한 답변이에요.'

    return user_query + "은(는) 없는 질문입니다."


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
    elif string_slack_event.find("'channel_type': 'im'") != -1:  # 다이렉트로 호출
        try:
            if slack_event['event']['client_msg_id']:
                user_query = slack_event['event']['text']
                answer = get_answer(user_query)
                slack.chat.post_message(channel, answer)
                return make_response("ok", 200, )
        except IndexError:
            pass
        except KeyError:
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

