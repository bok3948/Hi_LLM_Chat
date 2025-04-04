# date_callback.py
import datetime
import time
import os

# --- 설정 ---
# 목표 날짜 범위 (시작일 ~ 종료일)
start_year, start_month, start_day = 2024, 3, 1
end_year, end_month, end_day = 2024, 12, 31
# 각 커밋 사이에 증가시킬 시간 (초 단위). 예: 3600*6 = 6시간
time_increment_seconds = 3600 * 6
# --- 설정 끝 ---

# 타임존 문제 및 계산 편의를 위해 UTC 사용
try:
    start_date = datetime.datetime(start_year, start_month, start_day, 0, 0, 0, tzinfo=datetime.timezone.utc)
    end_date = datetime.datetime(end_year, end_month, end_day, 23, 59, 59, tzinfo=datetime.timezone.utc)
    start_ts = int(start_date.timestamp())
    end_ts = int(end_date.timestamp())
except ValueError as e:
    print(f"오류: 날짜 설정이 잘못되었습니다 - {e}")
    exit(1)

# filter-repo 콜백 간 상태 유지를 위한 전역 유사 변수
# 스크립트가 처음 로드될 때 초기화
if 'counter_state_date_change' not in globals():
    globals()['counter_state_date_change'] = {'current_ts': start_ts}

def modify_commit_date_sequential(commit, metadata):
    """각 커밋의 Author Date와 Committer Date를 순차적으로 변경하는 콜백 함수"""
    state = globals()['counter_state_date_change']
    current_ts = state['current_ts']

    # 종료 날짜를 넘지 않도록 현재 할당할 타임스탬프 결정
    if current_ts > end_ts:
        assign_ts = end_ts
    else:
        assign_ts = current_ts
        # 다음 커밋에 할당할 시간 증가 (종료 날짜 초과 방지 로직은 위에서 처리)
        state['current_ts'] += time_increment_seconds

    # 원본 커밋의 타임존 오프셋 유지 시도
    original_offset = '+0000' # 기본값 UTC
    try:
        # author_date, committer_date는 bytes 타입 (예: b'1712280536 +0900')
        original_date_str = commit.author_date.decode('utf-8', errors='ignore')
        parts = original_date_str.split()
        if len(parts) > 1 and len(parts[1]) == 5 and parts[1][0] in '+-':
            original_offset = parts[1]
    except Exception:
        pass # 에러 발생 시 기본 오프셋 사용

    # 새로운 날짜 문자열 생성 ('타임스탬프 오프셋' 형식)
    new_author_date_str = f"{assign_ts} {original_offset}"
    new_committer_date_str = f"{assign_ts} {original_offset}" # 커미터 날짜도 동일하게 변경

    # 바이트로 인코딩하여 커밋 객체에 할당
    commit.author_date = new_author_date_str.encode('utf-8')
    commit.committer_date = new_committer_date_str.encode('utf-8')

# filter-repo가 사용할 콜백 함수 지정
#commit_callback = modify_commit_date_sequential