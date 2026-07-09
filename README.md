# doc-skills

문서 편집 작업을 위한 이식성 높은 [Agent Skills](https://skills.sh) 모음입니다.
한글 `.hwpx`부터 시작해 **다양한 종류의 문서 편집 스킬**이 계속 추가됩니다. 각 스킬은
**자기완결형**이라 다른 스킬·플러그인·프레임워크가 없어도 동작합니다.

## 스킬 목록

| 스킬 | 문서 | 설명 |
|------|------|------|
| [`hwpx-table-kit`](skills/hwpx-table-kit) | `.hwpx` | 기존 한글 `.hwpx` 문서를 손상시키지 않고 편집 가능한 OWPML 표를 삽입합니다. 재사용 엔진. |
| [`hwpx-image-table-to-table`](skills/hwpx-image-table-to-table) | `.hwpx` (+`.xlsx`) | 레시피: `.hwpx` 안에 **이미지로 들어간 표**를 실제 편집 가능한 표로 변환합니다(필요 시 `.xlsx`에서 데이터 추출). `hwpx-table-kit`을 사용합니다. |
| [`portable-skill-authoring`](skills/portable-skill-authoring) | — (메타) | 노 베이스 에이전트가 clone만으로 쓸 수 있는 **이식성 높은 스킬을 작성**하는 규칙 + 표준 라이브러리 전용 검증기(`check_skill.py`) + 템플릿. |

## 빠른 시작 — clone만 하면 됩니다

사람이 할 일은 레포를 clone하는 것 하나뿐입니다. 나머지(환경 부트스트랩, 명령 실행,
검증)는 **에이전트(LLM)가 각 스킬의 `SKILL.md`를 읽고 알아서** 처리합니다.

```bash
git clone https://github.com/CatPope/doc-skills.git
```

그 다음 에이전트에게 원하는 작업을 시키면 됩니다. 예:

> "doc-skills 레포를 참고해서 이 `.hwpx`의 이미지 표를 편집 가능한 표로 바꿔줘."

에이전트는 알맞은 스킬을 골라 `setup` 스크립트로 환경을 구축하고, 스킬에 적힌 절차대로
작업한 뒤 결과를 검증합니다.

## Claude Code / Claude 에이전트에서 사용하기

에이전트가 스킬 폴더를 바라보게 하거나, 스킬 디렉터리에 설치하세요:

```bash
# 사용자 레벨(모든 프로젝트)
cp -r skills/* ~/.claude/skills/
# 또는 프로젝트 레벨
cp -r skills/* .claude/skills/
```

배포 등록 후에는 Skills CLI로도 설치할 수 있습니다:
`npx skills add CatPope/doc-skills@hwpx-table-kit`

## 요구 사항

스킬마다 다르며 각 스킬의 `setup` 스크립트가 자동으로 설치합니다. 공통 베이스:

- **Python 3.9+** — 대부분의 스킬이 사용하는 런타임.
- **Node 18+** — 선택. 일부 스킬의 검증(예: `kordoc` roundtrip)에만 사용.

## 범위와 한계

- 스킬들은 문서 파일 포맷을 **직접 다룹니다**(예: HWPX/OWPML XML을 생성·재압축).
  한컴오피스·MS Office 같은 **애플리케이션을 필요로 하거나 자동화하지 않습니다.**
- 따라서 애플리케이션이 하던 렌더링·검증은 대신하지 않습니다. 문서를 생성·수정하는
  스킬의 결과물은 **사람이 한 번 열어 시각적으로 확인**하는 단계를 권장합니다.
- 각 스킬의 세부 범위와 미지원 항목(예: 병합 셀 생성)은 해당 `SKILL.md`에 명시합니다.

## 기여 / 새 스킬 추가

새 문서 편집 스킬을 추가할 때는 [`portable-skill-authoring`](skills/portable-skill-authoring)의
규칙을 따르고, 커밋 전에 이식성 검증기를 통과시키세요:

```bash
python skills/portable-skill-authoring/scripts/check_skill.py skills/
```

## 라이선스

MIT
