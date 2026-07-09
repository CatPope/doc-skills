# doc-skills

문서 작업을 위한 이식성 높은 [Agent Skills](https://skills.sh) 모음입니다. 각 스킬은
**자기완결형**입니다 — 레포를 clone하고 스킬의 `setup` 스크립트만 실행하면 바로
동작하며, 다른 스킬·플러그인·프레임워크가 없어도 됩니다.

## 스킬 목록

| 스킬 | 설명 |
|------|------|
| [`hwpx-table-kit`](skills/hwpx-table-kit) | 기존 한글 `.hwpx` 문서를 손상시키지 않고 편집 가능한 OWPML 표를 삽입합니다. 재사용 엔진. |
| [`hwpx-image-table-to-table`](skills/hwpx-image-table-to-table) | 레시피: `.hwpx` 안에 **이미지로 들어간 표**를 실제 편집 가능한 표로 변환합니다(필요 시 `.xlsx`에서 데이터 추출). `hwpx-table-kit`을 사용합니다. |

## 빠른 시작 (어떤 에이전트든, 사전 설정 불필요)

```bash
git clone https://github.com/CatPope/doc-skills.git
cd doc-skills/skills/hwpx-table-kit
bash setup.sh          # 또는(Windows): pwsh setup.ps1

# 생성
python scripts/inject_tables.py --base IN.hwpx --tables tables.json --out OUT.hwpx
# 검증(선택, Node 필요)
node scripts/verify_hwpx.mjs OUT.hwpx
```

자세한 사용법은 각 스킬의 `SKILL.md`를 참고하세요.

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

- **Python 3.9+** — 표 생성(Pillow + openpyxl, `setup`이 설치).
- **Node 18+** — 선택. [`kordoc`](https://www.npmjs.com/package/kordoc)을 이용한 roundtrip 검증에만 사용.

## 범위와 한계

이 스킬들은 HWPX XML을 직접 생성·재압축합니다. 한글(한컴오피스) 애플리케이션을
필요로 하거나 자동화하지 **않습니다**. 그래서 생성된 `.hwpx`는 항상 사람이 한 번
열어 시각적 결과를 확인해야 합니다. 병합 셀(colspan/rowspan) 생성은 범위 밖입니다.

## 라이선스

MIT
