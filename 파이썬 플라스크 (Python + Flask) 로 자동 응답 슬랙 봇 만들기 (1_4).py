'''
파이썬 플라스크 (Python + Flask) 로 자동 응답 슬랙 봇 만들기 (1_4)
https://kitle.xyz/post/60/

이제 즉문 즉답의 시대.. 데이터를 모아서 Bot이 한번에 처리할 수 있는 봇을 만들어 보겠습니다. 선수지식은 python 기초 프로그래밍 지식이 필요합니다.

생성 순서는 다음과 같습니다. 막상보면 어려울것 같지만 천천히 따라오시면 누구나 가능합니다.

[슬랙 봇 - Python + Flask 로 자동 답변 봇 만들기 (1)]
Slack 가입을 위한 이메일 확보
Slack 워크 스페이스 생성 및 가입
Slack API 메뉴에서 App 생성
App(Bot)에게 설정 및 권한주기
App(Bot)을 컨트롤 하기 위한 정보 체크
App(Bot)을 인스톨 하여 Bot 사용 가능하게 만들기
App(Bot)을 @ 태그하여 채널에 추가하기

[슬랙 봇 - Python + Flask 로 자동 답변 봇 만들기 (2)]
Python + Flask 로 간단한 응답 서버 만들기
Python + Flask 로컬 주소를 외부에서 접속 가능하게 끔 ngrok 를 사용하여 도메인 연결하기
Python + Flask 에서 채팅 메세지를 Bot으로 보내는 이벤트 핸들러 만들기

[슬랙 봇 - Python + Flask 로 자동 답변 봇 만들기 (3~4)]
Python + Flask 에서 채팅 메세지에 따라 다르게 답변하도록 만들기
Python + Flask 각종 예외 처리와 팁


최대한 쉽게 설명할테니 잘 따라와 주세요.

1. 테스트용 이메일 계정 확보하기
연습용 이메일 계정이 하나 필요합니다. 이미 계정이 있다면 계정 로그인 잘되나 우선 체크해보시고 따로 만들고 싶다면 하나 만듭니다. 여기서는 무난한 gmail.com에 접속하여 하나 가입했습니다.

2. 테스트용 무료 슬랙 공간 만들기
www.slack.com 에 접속합니다.slack은 제한적이지만 무료로도 이용할 수 있습니다. 슬랙에서는 이런 공간 개념으로 이야기하는데 이제부터는 workspace 라고 합니다.
slack.com > TRY SLACK FOR FREE 메뉴를 클릭 해 workspace을 만들 수 있습니다. 그다음 Create a Slack Workspace 를 누릅니다.그러면 e-mail 입력창이 발생합니다. 위 1에서 생성 또는 가지고 계신 이메일을 입력해 인증을 받습니다.그리고 workspace이름등을 이미 만들어진 이름이 아니게 잘 선정하면 생성 및 로그인이 완료 될 것입니다.
3. App(Bot) 만들기
슬랙에서는 다양한 App을 만들 수 있으며 그 하위기능으로 Bot기능이 존재합니다. 따라서 App만들기를 하시고 그안에 Bot 설정을 할 수 있습니다.
웹 slack에 로그인 되어 있는 상태에서, https://api.slack.com 으로 이동합니다. 우상단 Your apps 버튼을 클릭합니다. 아니면 https://api.slack.com/apps 로 이동해도 무방합니다.
Your Apps 화면에서 Create New App 버튼을 클릭합니다.App 이름을 입력합니다. 나중에 변경도 가능하다니 아무거나 일단 만드세요. Development Slack Workspace 선택 화면이 있습니다. 드롭다운 메뉴를 눌러보시면 하나 또는 여러개의 워크스페이스가 보이실 겁니다. 테스트용으로 2에서 만들었던 워크스페이스를 선택해 줍니다.
4. App(Bot) 설정하기
App이 만들어지면 자동으로 Setting > Basic Information 화면으로 이동합니다. 다음과 같은 화면이 보이시나요?

App이 생성만 된 상태이고 아직 할 수 있는 건 크게 없습니다. Bot으로 동작할 수 있게, 만든 슬랙의 메세지를 읽고 쓸 수 있게 권한을 주어야 합니다. 아무 봇이나 접근하면 안되잖아요?
1) 권한 추가하기
Basic Information > Add features and functionality > OAuth & Permissions 메뉴로 우선 이동합니다. 스크롤을 내려 하단 Scopes 메뉴에 다음의 권한을 추가하겠습니다. Add an OAuth Scope 버튼을 클릭합니다. 다음의 권한을 추가합니다.app_mentions:read 대화에서 봇이 @ 로 멘션 언급을 읽을 수 있는 권한을 갖습니다.chat:write 대화에서 봇이 글을 작성할 수 있는 권한을 갖습니다.im:write 사람들과 다이렉트 메세지를 나눌 수 있게 해줍니다.

Settings > Basic Information 화면으로 이동하면 Bots / Permissions 에 체크 활성화가 되어 보여질 것입니다. 권한을 주어 체크되었으니 이 권한을 해제하면 올바르게 동작을 하지못합니다.

5. App(Bot) 인스톨 하기
작성한 Bot을 사용하기 위해서는 workspace에 해당 봇을 설치 하여야 합니다.아래 메뉴에서 가능해요.Settings > Basic Information > Install Your app to your workspace 메뉴에서 Install 버튼을 누르고 확인 창에서 Allow 허용 해줍니다.

인스톨 후 메뉴에 확인하면 인스톨까지 완료 된 것을 볼 수 있을 겁니다.
6. Slack Workspace에 초대할 채널 만들기
workspace는 channel 로 나뉩니다. 쉽게 대화방이라고 생각하세요.해당 Bot은 구현하기 나름이겠지만 여기서는 channel 에 봇을 초대하겠습니다.우선 왼쪽 + 버튼을 눌러 채널을 만듭니다.처음엔 채널에 아무도 없어 대화할 사람을 초대하라고 나옵니다.

이 대화창에서는 Bot을 추가하려고 해도 검색이 되지 않습니다.여기선 Done을 눌러주세요.
그다음 대화창에서 @ 는 멘션(호출)기능을 활용하여 만든 봇을 불러봅니다.그러면 해당봇은 대화에 참여중이 아니니 초대할까요? 물어봅니다. Yes로 진행하시면 이제 정상적으로 초대가 됩니다.

드디어 기본 설정이 완료 되었습니다.

몸은 다 만들었지만, 아직 봇이 어떻게 동작시킬지 머리를 만들지 않았습니다.
다음게시글에서 이어서 진행하도록 하겠습니다.

'''
