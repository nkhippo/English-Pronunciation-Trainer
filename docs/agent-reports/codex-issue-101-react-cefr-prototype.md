---
id: pj-2026-07-20-4b71
aliases:
- pj-2026-07-20-4b71
title: 'Track B React + Vite Phase 1 prototype (#101) — 実装レポート'
created: '2026-07-20'
---

# Track B React + Vite Phase 1 prototype (#101) — 実装レポート

## 関連 Issue / PR

- Issue: #101
- PR: draft PR（作成予定）
- Agent: codex

## Issue 背景（Issue 本文から要約）

本番の単一 HTML を維持しながら React 移行の実現性と意思決定材料を得るため、Track B の独立プロトタイプを構築する。L3 × [C4, C3, C2] として、新しいフレームワーク、ディレクトリ、npm build tooling を本番 Runtime から隔離し、最小の CEFR フィルターだけを移植する。

## 実装内容

- Pre-Issue Recon として、既存 Setup と Vocab の CEFR 複数選択、正本仕様、Runtime 保護対象を確認した
- `experimental/react-prototype/` に Vite + React + TypeScript の独立環境を追加した
- A1–C2 の 6 レベルを `Set` で複数選択する `CEFRFilter` を実装した
- 選択状態を CEFR 順の配列で親へ通知し、App で JSON 表示した
- 局所 `.gitignore` で `node_modules/` と `dist/` を除外した
- README に判断根拠と Phase 2 以降の課題を記録した
- `npm install` で lockfile を生成し、依存解決を再現可能にした

## 変更ファイル

```
- experimental/react-prototype/.gitignore (A)
- experimental/react-prototype/README.md (A)
- experimental/react-prototype/index.html (A)
- experimental/react-prototype/package-lock.json (A)
- experimental/react-prototype/package.json (A)
- experimental/react-prototype/tsconfig.json (A)
- experimental/react-prototype/vite.config.ts (A)
- experimental/react-prototype/src/App.tsx (A)
- experimental/react-prototype/src/components/CEFRFilter.tsx (A)
- experimental/react-prototype/src/main.tsx (A)
- experimental/react-prototype/src/styles.css (A)
- experimental/react-prototype/src/vite-env.d.ts (A)
- docs/agent-reports/codex-issue-101-react-cefr-prototype.md (A)
```

プロトタイプ成果物はすべて `experimental/react-prototype/` 配下。最後の 1 ファイルは Issue 本文と `AGENTS.md` が要求する実装レポートであり、既存 docs の編集はしていない。

## デグレ防止検証

- Phase 0: `origin/main` から隔離した worktree で全既存ファイルの md5 を記録
- Phase 1: `experimental/react-prototype/` へ新規ファイルのみ追加
- Phase 2: 全既存ファイルの md5 が Phase 0 と一致することを再検証
- Phase 3: `git check-ignore` で `node_modules/` と `dist/` の除外を確認
- Phase 4: production build とブラウザ操作を確認
- 実装中の自己判断による追加変更: なし
- 実装中に発覚した懸念: 初回ブラウザ確認で state updater 内から親を更新する React 警告を検出。イベントハンドラー内で次状態を確定してから親へ通知する構造に修正し、再確認で警告ゼロ

## 動作確認

- `npm install`: 成功、脆弱性 0 件
- `npm run build`: 成功（TypeScript 型チェック + Vite production build）
- `npm run dev -- --host 127.0.0.1`: localhost 起動成功
- ブラウザで A1–C2 の 6 ボタン表示: OK
- 初期状態 A1/A2 選択: OK
- C2 クリック後の `aria-pressed="true"`: OK
- App の JSON が `["A1", "A2", "C2"]` に更新: OK
- 修正後のブラウザ console error: 0 件
- `node_modules/` / `dist/` の git 除外: OK
- 既存ファイルの md5: 全件一致
- 既存機能への影響: なし
- データ整合性: Runtime data contract を変更していない

## 実装過程での気づき

- Vite は組み込み変換で TSX を扱えるため、Phase 1 では React plugin を追加せず、直接依存を React / ReactDOM / TypeScript / Vite と型定義だけに限定できた。
- TypeScript 7 では CSS の side-effect import に宣言が必要だったため、標準の `vite/client` 型参照を追加した。
- ローカルブラウザ検証が、ビルドだけでは見つからない React の親更新タイミング警告の発見と修正につながった。
- `.gitignore` はプロトタイプ直下に置くことで、本番や将来の別 Track B 実験への暗黙の影響を避けた。

## 後続への影響

- CEFR 値と親子コンポーネント境界の最小 TypeScript モデルを Phase 2 の検討材料にできる。
- i18n、TTS、Runtime data fetch、Vercel 出力統合、永続状態、テスト戦略は README の課題リストから個別に設計できる。

## 残課題・申し送り

- C1/C2 は UI 骨格のみで、本番データの CEFR 対応や既存フィルター parity は未実装。
- React plugin、lint、テスト、状態管理ライブラリ、本番 build 統合は意図的に Phase 2 以降へ保留。

## Complexity Retrospective (完了時点検)

### 事前分類 vs 実際

- 事前 Complexity Level: L3
- 実装後の妥当性判定: 妥当
- 判定根拠: 本番から隔離された小規模実装でも、React + TypeScript への stack 転換、独立ディレクトリ、npm build tooling と lockfile の初導入を同時に検証したため L3 の管理が適切だった。

### 事前 Change Pattern vs 実際

- 事前 Pattern: C4, C3, C2
- 実装中に追加が必要になった Pattern: なし

### 構造・契約への影響点検

- [x] Runtime data contract 8 パスへの影響なし
- [x] i18n schema への影響なし
- [x] URL 構造への影響なし
- [ ] ビルドシステムへの影響なし（本番 build は不変だが、experimental 配下に独立 build を意図的に追加）
- [x] AI 参照ドキュメント Category A への影響なし
- [x] 既存ファイルパスへの依存関係が壊れていない

### Phase 分割の妥当性

- 想定 Phase 数: 1
- 実際の Phase 数: 1
- 相互依存の発生有無: なし。本番 SPA との統合を Phase 2 以降へ分離できた

### 総合判定

- [x] 事前分類妥当、PR 作成可
- [ ] Level 昇格提案、Issue Comment で報告して中断
- [ ] Pattern 追加提案、Issue Comment で報告して中断

### 昇格・追加提案がある場合の詳細

なし
