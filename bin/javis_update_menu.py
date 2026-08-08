#!/usr/bin/env python3
"""cys-update — cys pack-plan/pack-merge 위에 얹는 번호선택형 업데이트 메뉴.

새 파일(비임베드) — pack-guard 정책상 벤더 팩 업데이트가 이 파일을 절대 건드리지 않는다
(hooks/pack-guard.sh:51 "자작 기능은 새 파일로(비임베드=업데이트 불가침)").

동작:
  1) `cys pack-plan` 실행 결과를 그대로 보여주고, 개별 파일 항목을 번호 매겨 나열한다.
  2) "⏸ 보존+병합 대기" 항목은 사용자 설정과 충돌(breaking)로 표시한다.
  3) 번호를 선택하면 그 항목만 바로 처리한다:
     - breaking 항목 → `cys pack-merge --file <path> --ai` (AI가 내 수정 의도를 신버전에 재적용,
       덮어쓰지 않음)
     - 충돌 없는 항목 → 개별 파일 단위 반영 CLI가 없어(cys pack-update는 전체 단위), 확인 후
       `cys pack-update` 전체 반영을 선택적으로 실행한다.
"""
import subprocess
import sys
import re
import shutil

CYS = shutil.which("cys") or "cys"

# pack-plan이 출력하는 섹션 중 "사용자 설정과 충돌"을 뜻하는 기호.
BREAKING_SYMBOLS = ("⏸",)

SECTION_RE = re.compile(r"^([^\sA-Za-z0-9가-힣])\s*(.+?)\s*\((\d+)건\)\s*(?:—\s*(.*))?$")


def run_plan():
    r = subprocess.run([CYS, "pack-plan"], capture_output=True, text=True)
    if r.returncode != 0:
        sys.stderr.write(r.stdout + r.stderr)
        sys.exit(r.returncode)
    return r.stdout


def parse_plan(text):
    sections = []
    cur = None
    for raw in text.splitlines():
        line = raw.rstrip("\n")
        stripped = line.strip()
        if not stripped:
            continue
        m = SECTION_RE.match(stripped)
        if m:
            symbol, label, count, note = m.groups()
            cur = {"symbol": symbol, "label": label, "count": int(count), "note": note or "", "files": []}
            sections.append(cur)
            continue
        if stripped.startswith("=") or stripped.startswith("※"):
            cur = None  # 요약/각주 줄 — 개별 항목 없음
            continue
        if cur is not None and line.startswith("  "):
            cur["files"].append(stripped)
    return sections


def flatten(sections):
    items = []
    for s in sections:
        breaking = s["symbol"] in BREAKING_SYMBOLS
        for f in s["files"]:
            items.append({"file": f, "label": s["label"], "breaking": breaking})
    return items


def main():
    text = run_plan()
    print(text)

    items = flatten(parse_plan(text))
    if not items:
        print("[cys-update] 선택 가능한 개별 항목이 없습니다(모두 최신이거나 벤더 자동 반영 대상).")
        return

    print("부모 저장소 업데이트 항목:")
    for i, it in enumerate(items, 1):
        flag = " ⚠ 내 설정과 충돌(병합 대기)" if it["breaking"] else ""
        print(f"  {i}) {it['file']}{flag}")

    try:
        choice = input("\n번호 선택 (Enter=취소) > ").strip()
    except EOFError:
        return
    if not choice:
        print("취소했습니다.")
        return
    if not choice.isdigit() or not (1 <= int(choice) <= len(items)):
        sys.stderr.write(f"[cys-update] 잘못된 번호: {choice}\n")
        sys.exit(1)

    target = items[int(choice) - 1]
    path = target["file"]

    if target["breaking"]:
        print(f"\n→ AI가 내 수정({path})을 지키며 신버전에 재적용 중...")
        r = subprocess.run([CYS, "pack-merge", "--file", path, "--ai"])
        sys.exit(r.returncode)

    print(f"\n→ '{path}'은(는) 충돌 없는 벤더 항목입니다.")
    print("  cys pack-update는 파일 단위가 아니라 팩 전체 단위로만 반영됩니다.")
    try:
        yn = input("  지금 전체 pack-update를 실행할까요? [y/N] > ").strip().lower()
    except EOFError:
        yn = ""
    if yn == "y":
        r = subprocess.run([CYS, "pack-update"])
        sys.exit(r.returncode)
    print("취소했습니다.")


if __name__ == "__main__":
    main()
