# i18n 監査レポート

> 生成日: 2026-06-24 ／ 対象: `i18n/{en,ja,zh,ko}.json`、`i18n/phonemes/{en,ja,zh,ko}.json`、`index.html`

翻訳の良し悪しは判断していません。キー所在とハードコードの可視化のみ。

---

## 1. UI 文言キー × 言語

| キー | en | ja | zh | ko | 画面 |
|------|----|----|----|----|------|
| `back_top` | Menu | TOPへ | 首页 | 처음 | 共通 |
| `brand.name` | IPA Dictation · Decoder / Encoder | IPA音写 · Decoder / Encoder | IPA听写 · Decoder / Encoder | IPA 받아쓰기 · Decoder / Encoder | 共通（トップバー） |
| `brand.sub` | CEFR A1–A2 · General American | CEFR A1–A2 · General American | CEFR A1–A2 · 美式英语 | CEFR A1–A2 · 미국 영어 | 共通（トップバー） |
| `build_ph` | Tap the IPA keys below to build the pronunciation | 下のIPAキーをタップして発音を組み立てる | 点击下方IPA键拼出发音 | 아래 IPA 키를 눌러 발음을 만드세요 | encode |
| `check` | Check | 答え合わせ | 核对 | 채점 | decode/encode |
| `clear` | Clear | クリア | 清除 | 지우기 | encode |
| `dir.decode_d` | Read the IPA and spell the word | 発音記号を読んで綴りを当てる | 读IPA并拼写单词 | IPA를 읽고 철자를 맞추기 | setup |
| `dir.decode_t` | Decode · IPA &rarr; word | 読む · IPA &rarr; 単語 | 解码 · IPA &rarr; 单词 | 읽기 · IPA &rarr; 단어 | setup |
| `dir.encode_d` | Build the pronunciation with the IPA keyboard | IPAキーボードで発音を組み立てる | 用IPA键盘拼出发音 | IPA 키보드로 발음 조립하기 | setup |
| `dir.encode_t` | Encode · word &rarr; IPA | 書く · 単語 &rarr; IPA | 编码 · 单词 &rarr; IPA | 쓰기 · 단어 &rarr; IPA | setup |
| `dir.label` | Direction | 方向 | 方向 | 방향 | setup |
| `grp.all` | All | すべて | 全部 | 전체 | setup |
| `grp.label` | Spelling pattern group | 綴り規則グループ | 拼写规则组 | 철자 규칙 그룹 | setup |
| `grp.long` | Long vowels · silent e | 長母音・マジックe | 长元音·不发音e | 장모음·묵음 e | setup |
| `grp.r` | R-colored vowels | r音色 | r化元音 | r색 모음 | setup |
| `grp.short` | Short vowels | 短母音 | 短元音 | 단모음 | setup |
| `grp.team` | Vowel teams | 母音チーム | 元音组合 | 모음 팀 | setup |
| `hint.first` | First letter | 最初の文字 | 首字母 | 첫 글자 | （未使用・hidden） |
| `hint.pos` | Part of speech | 品詞 | 词性 | 품사 | （未使用・hidden） |
| `hint.syl` | Syllables | 音節数 | 音节数 | 음절 수 | （未使用・hidden） |
| `info.mouth` | Mouth | 口の形 | 口型 | 입 모양 | decode/encode/reveal（音素パネル） |
| `info.watch` | Watch out | 注意 | 注意 | 주의 | decode/encode/reveal（音素パネル） |
| `input_ph` | Type the word | 単語を入力 | 输入单词 | 단어 입력 | decode |
| `kbd.consonants` | Consonants | 子音 | 辅音 | 자음 | encode |
| `kbd.diphthongs` | Diphthongs | 二重母音 | 双元音 | 이중 모음 | encode |
| `kbd.r_vowels` | R-colored | r母音 | r化元音 | r색 모음 | encode |
| `kbd.stress` | Stress | 強勢 | 重音 | 강세 | encode |
| `kbd.vowels` | Vowels | 母音 | 元音 | 모음 | encode |
| `lang_opts.en` | English | English | English | English | settings |
| `lang_opts.ja` | 日本語 | 日本語 | 日本語 | 日本語 | settings |
| `lang_opts.ko` | 한국어 | 한국어 | 한국어 | 한국어 | settings |
| `lang_opts.zh` | 中文 | 中文 | 中文 | 中文 | settings |
| `lead_html` | Retrain <b>pronunciation only</b> for words you already k... | 既知の単語の<b>発音だけ</b>を鍛え直すツール。&ldquo;発音できない音は聞き取れない&rdquo; のギ... | 专为<b>已学单词</b>重练<b>发音</b>。弥合&ldquo;不会发的音就听不出来&rdquo;的缺口。通过... | 이미 아는 단어의 <b>발음만</b> 다시 훈련합니다. &ldquo;낼 수 없는 소리는 들리지 않는다&... | setup |
| `listen` | Listen | 音を聞く | 播放发音 | 듣기 | decode/encode/reveal |
| `load_fail` | Load failed | 読み込み失敗 | 加载失败 | 불러오기 실패 | setup |
| `loading` | Loading… | 読み込み中… | 加载中… | 불러오는 중… | setup |
| `lvl.all` | A1+A2 | A1+A2 | A1+A2 | A1+A2 | setup |
| `lvl.b1` | B1 | B1 | B1 | B1 | setup |
| `lvl.b2` | B2 | B2 | B2 | B2 | setup |
| `lvl.c1` | C1 | C1 | C1 | C1 | setup |
| `lvl.label` | Level | レベル | 级别 | 레벨 | setup |
| `lvl.pool` | Pool: {n} words | 対象 {n} 語 | 词库 {n} 词 | 대상 {n}개 단어 | setup |
| `meter_done` | done | 完了 | 完成 | 완료 | summary |
| `next` | Next | 次へ | 下一题 | 다음 | reveal |
| `note.pattern` | Spelling pattern: {p} | 綴り規則: {p} | 拼写规则: {p} | 철자 규칙: {p} | reveal |
| `note.schwa` | Schwa (ə/ɚ): stay weak and vague, not led by spelling | 弱化母音(ə/ɚ): 綴りに引っ張られず曖昧に | 弱读元音(ə/ɚ): 勿被拼写牵引，要含糊轻读 | 약화 모음(ə/ɚ): 철자에 끌리지 말고 약하고 모호하게 | reveal |
| `note.stress` | Stress syllable {n} ({sy} syllables) | 第{n}音節を強く（{sy}音節） | 重读第{n}音节（共{sy}音节） | 제{n}음절 강세 ({sy}음절) | reveal |
| `note.tricky` | Tricky sounds: {s} | 要注意音: {s} | 需注意音: {s} | 주의할 소리: {s} | reveal |
| `patterns.magic_e` | silent e | マジックe | 不发音e | 묵음 e | reveal（pattern置換） |
| `pos.be動詞` | be verb | be動詞 | be动词 | be동사 | （未使用・posLabel定義のみ） |
| `pos.代名詞` | pronoun | 代名詞 | 代词 | 대명사 | （未使用・posLabel定義のみ） |
| `pos.前置詞` | preposition | 前置詞 | 介词 | 전치사 | （未使用・posLabel定義のみ） |
| `pos.副詞` | adverb | 副詞 | 副词 | 부사 | （未使用・posLabel定義のみ） |
| `pos.副詞 / 前置詞` | adverb / preposition | 副詞 / 前置詞 | 副词 / 介词 | 부사 / 전치사 | （未使用・posLabel定義のみ） |
| `pos.助動詞` | modal verb | 助動詞 | 情态动词 | 조동사 | （未使用・posLabel定義のみ） |
| `pos.動詞` | verb | 動詞 | 动词 | 동사 | （未使用・posLabel定義のみ） |
| `pos.名詞` | noun | 名詞 | 名词 | 명사 | （未使用・posLabel定義のみ） |
| `pos.形容詞` | adjective | 形容詞 | 形容词 | 형용사 | （未使用・posLabel定義のみ） |
| `pos.形容詞 / 副詞` | adjective / adverb | 形容詞 / 副詞 | 形容词 / 副词 | 형용사 / 부사 | （未使用・posLabel定義のみ） |
| `pos.接続詞` | conjunction | 接続詞 | 连词 | 접속사 | （未使用・posLabel定義のみ） |
| `pos.間投詞` | interjection | 間投詞 | 感叹词 | 감탄사 | （未使用・posLabel定義のみ） |
| `pos.限定詞` | determiner | 限定詞 | 限定词 | 한정사 | （未使用・posLabel定義のみ） |
| `see_answer` | See the answer | 答えを確認 | 查看答案 | 정답 확인 | reveal |
| `set.daily_d` | Common words (including irregular spellings) | よく使う語（不規則綴りを含む） | 常用词（含不规则拼写） | 자주 쓰는 단어(불규칙 철자 포함) | setup |
| `set.daily_t` | Daily words · CEFR A1–A2 | 日常語 · CEFR A1–A2 | 日常词 · CEFR A1–A2 | 일상 어휘 · CEFR A1–A2 | setup |
| `set.label` | Question set | 出題セット | 题库 | 문제 세트 | setup |
| `set.phonics_d` | Words with regular spelling&ndash;sound correspondences | 綴りと発音が規則的に対応する語 | 拼写与读音规则对应的词 | 철자와 소리가 규칙적으로 대응하는 단어 | setup |
| `set.phonics_t` | Phonics patterns · spelling &harr; sound | 規則パターン · 綴り &harr; 音 | 拼读规则 · 拼写 &harr; 音 | 규칙 패턴 · 철자 &harr; 소리 | setup |
| `settings_btn` | Settings | 設定 | 设置 | 설정 | settings |
| `settings_close` | Close | 閉じる | 关闭 | 닫기 | settings |
| `settings_lang` | Language | 言語 | 语言 | 언어 | settings |
| `start` | Start | はじめる | 开始 | 시작 | setup |
| `summary.again` | Play again | もう一周 | 再来一轮 | 다시 하기 | summary |
| `summary.line` | {c} / {t} correct · {m} to review | {c} / {t} 正解 · 復習 {m} 語 | {c} / {t} 正确 · 复习 {m} 词 | {c} / {t} 정답 · 복습 {m}개 | summary |
| `summary.review` | Review list: {list} | 復習リスト: {list} | 复习列表: {list} | 복습 목록: {list} | summary |
| `summary.weak_btn` | Review misses only | 苦手だけ復習 | 只复习错题 | 틀린 것만 복습 | summary |
| `summary.weak_head` | Sounds to practice next | 次に練習すべき音 | 建议练习的音 | 다음에 연습할 소리 | summary |
| `summary.weak_none_d` | No missed sounds. Try a higher level. | ミスした音はありません。レベルを上げてもOK。 | 没有错过的音。可尝试更高难度。 | 틀린 소리가 없습니다. 레벨을 올려 보세요. | summary |
| `summary.weak_none_t` | No weak sounds detected | 苦手音は検出されませんでした | 未检测到薄弱音 | 약한 소리가 감지되지 않았습니다 | summary |
| `syl` | {n} syllable | {n}音節 | {n}个音节 | {n}음절 | reveal（未使用？） |
| `syl_pl` | {n} syllables | {n}音節 | {n}个音节 | {n}음절 | reveal（未使用？） |
| `tips_head` | Pronunciation tips | 発音ポイント | 发音要点 | 발음 포인트 | reveal |
| `wordlist_fail` | Failed to load word list | 単語リストの読み込みに失敗しました | 词表加载失败 | 단어 목록을 불러오지 못했습니다 | setup |
| `you` | You: {a} | あなた: {a} | 你的答案: {a} | 당신: {a} | reveal |

---

## 2. 画面別分類

### decode

- `input_ph`

### decode/encode

- `check`

### decode/encode/reveal

- `listen`

### decode/encode/reveal（音素パネル）

- `info.mouth`
- `info.watch`

### encode

- `build_ph`
- `clear`
- `kbd.consonants`
- `kbd.diphthongs`
- `kbd.r_vowels`
- `kbd.stress`
- `kbd.vowels`

### reveal

- `next`
- `note.pattern`
- `note.schwa`
- `note.stress`
- `note.tricky`
- `see_answer`
- `tips_head`
- `you`

### reveal（pattern置換）

- `patterns.magic_e`

### reveal（未使用？）

- `syl`
- `syl_pl`

### settings

- `lang_opts.en`
- `lang_opts.ja`
- `lang_opts.ko`
- `lang_opts.zh`
- `settings_btn`
- `settings_close`
- `settings_lang`

### setup

- `dir.decode_d`
- `dir.decode_t`
- `dir.encode_d`
- `dir.encode_t`
- `dir.label`
- `grp.all`
- `grp.label`
- `grp.long`
- `grp.r`
- `grp.short`
- `grp.team`
- `lead_html`
- `load_fail`
- `loading`
- `lvl.all`
- `lvl.b1`
- `lvl.b2`
- `lvl.c1`
- `lvl.label`
- `lvl.pool`
- `set.daily_d`
- `set.daily_t`
- `set.label`
- `set.phonics_d`
- `set.phonics_t`
- `start`
- `wordlist_fail`

### summary

- `meter_done`
- `summary.again`
- `summary.line`
- `summary.review`
- `summary.weak_btn`
- `summary.weak_head`
- `summary.weak_none_d`
- `summary.weak_none_t`

### 共通

- `back_top`

### 共通（トップバー）

- `brand.name`
- `brand.sub`

### （未使用・hidden）

- `hint.first`
- `hint.pos`
- `hint.syl`

### （未使用・posLabel定義のみ）

- `pos.be動詞`
- `pos.代名詞`
- `pos.前置詞`
- `pos.副詞`
- `pos.副詞 / 前置詞`
- `pos.助動詞`
- `pos.動詞`
- `pos.名詞`
- `pos.形容詞`
- `pos.形容詞 / 副詞`
- `pos.接続詞`
- `pos.間投詞`
- `pos.限定詞`

---

## 3. 音素解説（`i18n/phonemes/*.json`）

- 音素記号数: en=43, ja=43, zh=43, ko=43
- 4言語間で音素キー集合は一致

各記号のフィールド: `lab`, `ex`, `mouth`, `trap`, `t`（要注意フラグ）

| 記号 | 画面 | フィールド |
|------|------|-----------|
| `aɪ` | decode/encode/reveal（音素パネル） | lab, ex, mouth, trap, t |
| `aʊ` | decode/encode/reveal（音素パネル） | lab, ex, mouth, trap, t |
| `b` | decode/encode/reveal（音素パネル） | lab, ex, mouth, trap, t |
| `d` | decode/encode/reveal（音素パネル） | lab, ex, mouth, trap, t |
| `dʒ` | decode/encode/reveal（音素パネル） | lab, ex, mouth, trap, t |
| … | （全記号同様） | |

---

## 4. ハードコード文字列（ユーザー可視・i18n未経由または初期HTMLのみ）

| ファイル:行 | 文字列 | 推定画面 | 備考 |
|------------|--------|----------|------|
| `index.html:6` | IPA Dictation | 共通 |  |
| `index.html:185` | IPA Dictation | 共通 | **常に英語のまま**（`brand.*` キーは存在するが未配線） |
| `index.html:185` | A1–A2 · GA | 共通 | **常に英語のまま**（`brand.*` キーは存在するが未配線） |
| `index.html:188` | Settings | 共通/各画面 | 起動後 `applyI18n()` で置換される |
| `index.html:196` | (英語リード文・HTML初期値) | setup | 起動後 `applyI18n()` で置換される |
| `index.html:237` | Loading… | setup | 起動後 `applyI18n()` で置換される |
| `index.html:244` | Listen | 共通/各画面 | 起動後 `applyI18n()` で置換される |
| `index.html:248` | Type the word | decode | 起動後 `applyI18n()` で置換される |
| `index.html:257` | Listen | 共通/各画面 | 起動後 `applyI18n()` で置換される |
| `index.html:274` | Listen | 共通/各画面 | 起動後 `applyI18n()` で置換される |
| `index.html:296` | Close | 共通/各画面 | 起動後 `applyI18n()` で置換される |
| `index.html:300` | English | settings | 起動後 `applyI18n()` で置換される |
| `index.html:301` | 日本語 | settings | 起動後 `applyI18n()` で置換される |
| `index.html:302` | 中文 | settings | 起動後 `applyI18n()` で置換される |
| `index.html:303` | 한국어 | settings | 起動後 `applyI18n()` で置換される |
| `index.html:359` | マジックe（正規表現リテラル） | reveal |  |
| `index.html:642` | `{n} / {total}` 形式（スラッシュ区切り） | decode/encode |  |
| `index.html:705` | ⌫ | encode |  |
