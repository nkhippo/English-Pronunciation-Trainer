# `docs/cursor/` — Cursor / Claude タスク履歴

AI エージェント向けの**作業指示・実装レポート・設計相談**を格納。アプリ runtime からは参照されない。

| Subfolder | Contents |
|-----------|----------|
| [`instructions/`](instructions/) | タスク指示書（`cursor-instructions-*.md`） |
| [`reports/`](reports/) | 実装レポート（`cursor-implementation-report-*.md`）— Claude への作業報告用 |
| [`briefs/`](briefs/) | 設計相談・機能ブリーフ（実装前の議論資料） |

**注意:** 古いレポート内のパスは 2026-07-09 リポジトリ再編以前の記述を含む場合がある。現行パスは [`../REPOSITORY-STRUCTURE.md`](../REPOSITORY-STRUCTURE.md) を正とする。

## 直近の主要タスク（2026-07-10）

| テーマ | 指示書 | レポート |
|--------|--------|----------|
| Phase 2 M2 完了（B2 +569） | `instructions/cursor-instructions-phase2-m2*.md` | `reports/cursor-implementation-report-phase2-m2*.md` |
| 進捗チェック UI | `instructions/cursor-instructions-progress-checks.md` | `reports/cursor-implementation-report-progress-checks.md` |
| Phrases CEFR バッジ | `instructions/cursor-instructions-connected-weak-cefr-badges.md` | `reports/cursor-implementation-report-connected-weak-cefr-badges.md` |
| dignify RP ホットフィックス | `instructions/cursor-instructions-dignify-hotfix.md` | `reports/cursor-implementation-report-dignify-hotfix.md` |
