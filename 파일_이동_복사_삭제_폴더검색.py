'''
파이썬(Python) - 파일_이동_복사_삭제_폴더검색
https://angel-breath.tistory.com/12

# 참고 사이트
# http://flowerykeyboard.tistory.com/6
# https://code.i-harness.com/ko-kr/q/3c7f09
# 파이썬 조각 코드 모음집 : https://wikidocs.net/book/536</code>
'''
import os
# 셸 유틸리티는 파일 및 디렉터리 작업을 수행하는 데 사용할 모듈의 이름
import shutil
# BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# 다운로드 받은 동영상 파일이 있는 최상위 폴더
inputdirpath = "D:\\movie"

# 한군데 폴더로 옮기고 싶은 위치
savedir = inputdirpath + '\\' + "mp4"
# 혹여나, 파일을 옮기고 싶지 않은 폴더가 있다면 정의
exceptfolder1 = 'D:\\movie\\mp4'
exceptfolder2 = 'D:\\movie\\keep'
exceptfolder3 = 'D:\\movie\\temp'

# 폴더가 없다면 만들어서 사용하기
def makedir(dirname):
    if not os.path.exists(dirname):
        os.makedirs(dirname)
        print('made sub-dir')

# 폴더를 계속 검색하면서 반복하게 된다.
def searchdir(dirname):
    try:
        # 전체 폴더 목록을 가져온다.
        filenames = os.listdir(dirname)

        # 폴더 목록에서 한개씩 폴더 경로를 가져온다.
        for filename in filenames:
            # 전체 경로를 가져온다.
            full_filename = os.path.join(dirname, filename)

            # if dirname == savedir and dirname == exceptfolder1 and dirname == exceptfolder2:
            #     continue

            # 폴더가 맞는지 확인
            if os.path.isdir(full_filename):
                # 폴더 안에 또 폴더가 있다면 다시 검색 함수 호출
                searchdir(full_filename)

                # 삭제 제외 목록이 아니면 폴더 삭제
                if full_filename != savedir and full_filename != exceptfolder1 and full_filename != exceptfolder2 and full_filename != exceptfolder3:
                    shutil.rmtree(full_filename)   # 폴더 삭제
                    print("Delete folder", full_filename)
            # else:
            # 폴더가 제외할 목록이 아니면 파일 이동 / 삭제 / 확인을 수행
            elif dirname != savedir and dirname != exceptfolder1 and dirname != exceptfolder2 and full_filename != exceptfolder3:
                # 파일 이름과 확장자를 분리해서 확인
                ext = os.path.splitext(full_filename)[-1]
                name = os.path.basename(full_filename)
                # print(full_filename)
                # 동영상용 파일 이라면...
                if ext == '.mp4' or ext == '.mkv' or ext == '.avi' or ext == '.wmv':
                    print('find >> ' + full_filename)
                    # 화질이 좋은 동영상을 분류하기 위해...
                    # 만일 파일 사이즈가 저용량 이라면 삭제 / 폴더도 삭제
                    if os.path.getsize(full_filename) < (1024*1024*300):
                        # 저용량 파일 삭제
                        if os.path.isfile(full_filename):
                            os.remove(full_filename)    # 파일 삭제
                            print("delete >>", full_filename)
                            # shutil.rmtree(dirname)   # 폴더 삭제
                            # print("Delete folder", dirname)
                    else:
                        # 파일 사이즈가 고용량이면 지정 폴더로 이동
                        shutil.move(full_filename, savedir + '\\' + name)
                        print('move << ' + savedir + '\\' + name)
                else:
                    os.remove(full_filename)
    except PermissionError:
        pass

# 프로그램 완료
def finish():
    print('complete')

# 순차적으로 프로그램 수행
if __name__ == "__main__":
    print('main program')
    makedir(savedir)
    searchdir(inputdirpath)
    finish()
