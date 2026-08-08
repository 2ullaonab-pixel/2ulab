# SILENT_FAILURE_CATALOG — 무음실패 카탈로그 (OpenMontage D5)

<!-- 생성됨: `javis_orchestra.py silent-failure-catalog` 가 SILENT_FAILURES에서 결정론 파생.
     손편집 금지 — 재생성: `javis_orchestra.py silent-failure-catalog`. 드리프트는 preflight C38(WARN)·`--check`가 탐지. -->

> cys엔 guard.sh가 없다 — denylist는 CLAUDE.md §6 산문이다. 이 표는 그 산문을 각 항목의 **탐지절(위반 증명 아티팩트)**로 큐레이션한 것이다. 무점수(수치 등급 없음). source-of-record=javis_orchestra.py 내부 `SILENT_FAILURES`.

| id | source (CLAUDE.md §ref) | constraint | DETECTION CLAUSE | kind |
|---|---|---|---|---|
| SF-CONSENSUS-AVERAGE | §6 eval-driven·verdict 계약(독립 재유도) | 리뷰어(agy·codex) 불일치는 다수결·평균 금지 — master 독립 재유도로만 해소 | agy.verdict≠codex.verdict인데 최종 확정 전 master 독립 재유도 레코드(별도 타임스탬프·증거)가 없으면 consensus-collapse | deterministic |
| SF-CROSSVERIFY-GATE-SWALLOWED | §8 품질 절대우선·§5② 교차검증 게이트 | 교차검증 게이트 실패 시 후속 ③공통분모·④대립비교·⑤결론 전면 중단+보고 — 통과로 흘리기 금지 | cross_verification_passed 플래그가 명시 True가 아닌데(누락 포함) ③④⑤ 산출물이 존재하면 swallowed-gate | deterministic |
| SF-DENY-CHARTER-EDIT | §6 denylist② charter 편집 | soul.md·CLAUDE.md·*_DIRECTIVE.md·헌법 편집은 자율 금지 — 오너(owner) 토큰 승인 필수 | git diff 경로가 soul.md/CLAUDE.md/*_DIRECTIVE.md/directives/ 에 매칭되는데 owner 승인 토큰 레코드가 없으면 위반 | deterministic |
| SF-DENY-EXTERNAL-PUBLISH | §6 denylist③ 외부발행 | 외부발행/발송(git push·gh release·전송·공개)은 비가역 — 자율 금지·멈춰 승인(로컬커밋만 가역=허용) | 실행 명령이 git push/gh release/gh pr create/merge/publish/deploy/외부 전송 패턴에 매칭되는데 승인 없이 실행 로그에 있으면 경계 침범(R1·R2 preflight) | deterministic |
| SF-DENY-IRREVERSIBLE-DELETE | §6 denylist④ 비가역 삭제 | 비가역 삭제/이동(rm·mv·chmod·git clean·truncate) 자율 금지 — 매 action 효과기반 preflight | action 명령이 rm/mv/chmod/git clean/truncate 패턴에 매칭되는데 승인 없이 실행됐거나 preflight 로그가 비면 침범 | deterministic |
| SF-DIRECTIVE-NOT-INJECTED | §3 워커 즉시 지침 주입 | 워커/리뷰어 생성 직후, 작업 티켓보다 선행해 DIRECTIVE 주입(각성) — 미주입 위임 금지(단일 sub-agent 수렴 치명에러) | launch-agent 후 첫 task-prompt timestamp가 directive-ack push timestamp보다 앞서면 inject-skip 위반 | deterministic |
| SF-ESCALATION-MISSING | §6 라운드 루프 8(10R escalation) | 10R 도달인데 잠근 합격 기준에 미달이면 무한루프 금지 + 주인님께 격차 보고·판단 요청 필수 | 기록 라운드>=10 AND 수렴 미달인데 SESSION_STATE에 ESCALATION 레코드+master→owner push가 없으면 위반 | deterministic |
| SF-GATE-SCORE-FIELD | §6 리뷰어 verdict 타입 계약 | verdict는 enum(ACCEPT/REVISE/BLOCK/ESCALATE)+evidence:file:line만 — 수치 score 금지(다수결·reward-hack 차단) | verdict/round-log 레코드에 score 키 또는 0-100·0-1 수치 등급 값이 있으면 위반 — javis_verdict.py 스키마 게이트가 차단 | deterministic |
| SF-GATE-SKIPPED-AS-FALSE | §6 라운드 게이트·D5 3-state | 의도적 SKIP은 None(미기록)·False(미승인)과 구분돼 명시 기록 — PASS-by-absence 위장 금지 | gate_verdicts가 'SKIPPED:' verdict를 Skip 인스턴스로 가로채는지(isinstance v,Skip) — False/None로 삼켜지면 위반; honest-skip만 남으면 gate-status exit 2 | deterministic |
| SF-HALLUCINATION-NO-SOURCE | §8 환각방지·§5② 검색 선행 | 출처·근거 없는 단정 금지 — 모든 사실 주장은 인용/출처(URL·file:line) 동반(garbage-in 차단) | 사실 주장 문장에 출처 마커가 0이면 환각 의심 — 완결된 산문은 결정론 분리가 어려워 샘플 팩트체크 병행(heuristic) | heuristic |
| SF-KILLSWITCH-IGNORED | §6 자율주행 메타안전(kill-switch) | 오너 아무 입력=즉시 일시정지(kill-switch) · CSO 2-phase handshake 부재 시 self-clear 금지 | owner 입력 이벤트 timestamp 이후 autopilot 새 action 실행이 있으면 위반; self-clear에 대응 CSO handshake ack 레코드 없으면 unsafe-clear | deterministic |
| SF-PLAN-DOWNGRADE | 라우팅(tier 격하 금지) | 라우터 판정 tier(slow>deliberate>fast)는 격상만 허용·격하 금지(과소발화가 안전) | tier 격하를 증명할 필드-diff 아티팩트가 없어 결정론 탐지 불가 — 라우터 로그 대 실제 처리 모드 수기 대조(heuristic only) | heuristic |
| SF-PRODUCER-EQ-EVALUATOR | §6 eval-driven(producer≠evaluator) | 측정 자기채점 금지 — 산출 노드(producer)와 채점 노드(evaluator) 분리, 채점=master LOCKED ref launcher·암호학적 핀 | eval 레코드의 producer_node_id==evaluator_node_id 이거나 LOCKED ref 핀(해시) 누락·불일치면 measurement 무효 | deterministic |
| SF-RENDER-RUNTIME-SWAP | 영상 v2 §3 — OM CRITICAL 거버넌스(매니페스트 locked runtime ≠ 실제 렌더 = 위반) | edit가 고정한 render_runtime을 compose가 무음으로 교체 금지 — render_report.render_runtime이 edit_decisions의 고정값과 일치해야 한다(불일치·누락=무음 품질/포맷 강등) | 아키타입 매니페스트(D4) edit/compose phase의 field_present:render_runtime 게이트가 필드 부재를 1차 차단(check-criteria) + render_report.render_runtime != edit_decisions.render_runtime 값 대조는 video-verify 독립 노드(D1 verdict) | deterministic |
| SF-RETENTION-DELETE | §6 eval-driven(retention gate) | 점수 올리려 콘텐츠·테스트 삭제하는 reward-hack 차단 — 이전 산출물·테스트 보존 강제 | 라운드 N 항목집합이 N-1 집합을 포함하지 않으면(명시 deprecation 사유 없이) retention 위반·측정 무효 | deterministic |
| SF-SUMMARY-COMPRESSION | §8 최종 산출물(요약금지) | 최종 산출물 요약·압축 금지 — 분석·수치·표·단서 보존, 길이 원문 수준(쉬운 말 풀이 허용·항목 삭제 금지) | 최종본 길이·표·수치 개수가 직전 검증본 대비 현저히 감소하면 content-loss 의심 — 항목 삭제 여부는 수기 대조(heuristic) | heuristic |

총 16개 항목 — deterministic 13 · heuristic 3.
