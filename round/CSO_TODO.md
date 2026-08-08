<!-- javis:todo v1 owner=cso scope=pack lane=restore-2026-08-03 status=active since=2026-08-03 -->
# CSO_TODO — 영속 todo (절대지침 7)

> 세부 완료마다 갱신·디스크 영속. 세션 clear/재시작 후 이 파일부터 읽고 복원한다.

## 2026-08-03 재등록 후 각성

- [x] 역할 재등록: `cys claim-role cso` → surface:12 (오너 확인 후 집행, 이전 세션은 역할주소 상실 상태였음)
- [x] 현황 파악 ①`cys list`: 5노드 전부 live(exited=false) — reviewer-claude-2(surface:9)·worker(surface:10)·
      reviewer-claude-1(surface:11)·cso(surface:12, 본인)·master(surface:13). exited surface 없음 → reap 대상 없음.
- [x] 현황 파악 ②`cys ps`: ledger empty — scoped 프로세스 없음, 원장 이상 없음.
- [x] 현황 파악 ③`cys feed list`: pending 1건 — req-6832-1785717230-0 [bootstrap-fail / 자원 soft_warn / decision=-]
- [x] pending feed 항목(req-6832-1785717230-0) 처리 완료: feed.jsonl 원장 직접 조회(publisher_pid=10800,
      publisher_surface=4)→둘 다 현재 미생존 확인(고아 항목)→`cys feed reply ... deny --reason ...`로 정리.
      잔여 pending 0건 확인(cys feed list 재조회).
- [x] master에 상태 1줄 요약 + pending 처리결과 + 부가발견(master surface:13 승인프롬프트 3연속
      stale-clear 이력) 보고 완료
- [x] `cys events --category watchdog --category health --category queue --reconnect` 상시 구독 시작(백그라운드, task id=bviavi700)
