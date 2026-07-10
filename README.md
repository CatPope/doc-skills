# doc-skills

문서 편집 작업을 위한 이식성 높은 [Agent Skills](https://skills.sh) 모음입니다.
한글 `.hwpx`부터 시작해 **다양한 종류의 문서 편집 스킬**이 계속 추가됩니다.
여러 문서·스킬에 공통으로 쓰이는 로직은 `shared/` **공용 레이어**로 추상화하고,
각 스킬은 그 위에서 자기 역할만 담당합니다. 자기완결·자기부트스트랩의 단위는
개별 폴더가 아니라 **레포 전체**이며, 다른 플러그인·프레임워크 없이 clone만 하면
동작합니다.

## 구조

```
doc-skills/
  skills/     # 개별 문서 작업 스킬 (SKILL.md + 스킬 고유 로직)
  shared/     # 여러 스킬이 공유하는 공용 모듈 (포맷 무관 유틸)
```

스킬은 하드코딩 경로 없이 레포 루트를 탐색해 `shared/`를 참조합니다(자세한 규칙은
[`portable-skill-authoring`](skills/portable-skill-authoring) 참고). 스킬 문서는
영어로 작성합니다.

## 스킬 목록

### 문서용 스킬

실제 문서 파일을 만들거나 편집하는 스킬입니다.

| 스킬 | 문서 | 설명 |
|------|------|------|
| [`hwpx-table-kit`](skills/hwpx-table-kit) | `.hwpx` | 기존 한글 `.hwpx` 문서를 손상시키지 않고 편집 가능한 OWPML 표를 삽입합니다. 재사용 엔진. |
| [`hwpx-image-table-to-table`](skills/hwpx-image-table-to-table) | `.hwpx` (+`.xlsx`) | 레시피: `.hwpx` 안에 **이미지로 들어간 표**를 실제 편집 가능한 표로 변환합니다(필요 시 `.xlsx`에서 데이터 추출). `hwpx-table-kit`을 사용합니다. |

### 그 외 용도 스킬

문서를 직접 다루지 않고, 이 레포의 스킬을 만들고 유지하는 데 쓰는 도구입니다.

| 스킬 | 용도 | 설명 |
|------|------|------|
| [`portable-skill-authoring`](skills/portable-skill-authoring) | 스킬 작성(메타) | 노 베이스 에이전트가 clone만으로 쓸 수 있는 **이식성 높은 스킬을 작성**하는 규칙 + 표준 라이브러리 전용 검증기(`check_skill.py`) + 템플릿. |
| [`skill-repair`](skills/skill-repair) | 스킬 문제 해결(메타) | 기존 스킬대로 했는데 **문제가 생겼을 때**(단계 실패, 결과물 손상·오류) 진단·보완·수정하고, 그 수정을 스킬에 되먹여 PR로 반영하는 절차 + OPC/ZIP 문서 진단기(`opc_doctor.py`). |

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

스킬이 `shared/` 공용 레이어에 의존할 수 있으므로, **개별 스킬 폴더만 복사하지
말고 레포 전체**를 두고 에이전트가 그 경로를 바라보게 하세요. 스킬 디렉터리에
설치할 때도 레포째로 두는 방식을 권장합니다:

```bash
# 레포 전체를 스킬 경로 아래에 클론 (shared/까지 함께 유지)
git clone https://github.com/CatPope/doc-skills.git ~/.claude/skills/doc-skills
# 또는 프로젝트 레벨
git clone https://github.com/CatPope/doc-skills.git .claude/skills/doc-skills
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

## 원격 반영 범위 (엄격)

원격(`https://github.com/CatPope/doc-skills.git`)에는 **다음 두 가지만** 반영합니다.

1. **스킬** — `skills/` 아래의 스킬과 공용 레이어 `shared/`, 그리고 이들이 동작하는 데
   필요한 스크립트·템플릿·설정 파일(`.gitattributes`, `.gitignore` 등).
2. **레포 내부 문서** — 이 레포 자체를 설명하는 문서(`README.md`, `LICENSE`,
   각 스킬의 `SKILL.md`, `shared/README.md` 등).

그 외에는 **일체 반영을 금지**합니다. 특히 다음은 절대 커밋/푸시하지 않습니다:

- 스킬이 **처리 대상으로 삼는 문서**나 그 **결과물**(예: `.hwpx`, `.xlsx`,
  이미지, `*_변환.hwpx`) — 이는 사용자 데이터이지 레포 자산이 아닙니다.
- 사용자·업무 데이터, 비밀값·자격증명, 로컬 경로, 임시/스크래치 파일, 빌드 산출물.

이 경계는 `.gitignore`로도 강제하며, 새 파일을 올리기 전 "이게 스킬인가, 레포
문서인가?"를 확인합니다. 둘 다 아니면 올리지 않습니다.

## 기여 / 새 스킬 추가

새 문서 편집 스킬을 추가할 때는 [`portable-skill-authoring`](skills/portable-skill-authoring)의
규칙을 따르세요. 요약:

- **스킬은 영어로 작성**합니다(사용자 트리거 용어는 원어 병기 가능).
- 공통 로직은 스킬마다 복제하지 말고 `shared/`로 **추상화**합니다.
- 커밋 전에 이식성 검증기를 통과시킵니다:

  ```bash
  python skills/portable-skill-authoring/scripts/check_skill.py skills/
  ```

- 원격 반영은 `main` 직접 푸시가 아니라 **PR**로 올립니다(스킬 + 문서 갱신 한 커밋).

## 라이선스

MIT
