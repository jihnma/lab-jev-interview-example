# バックエンドエンジニア（Java / Rust）採用要項 — 株式会社ツキウサギペイ
# Backend Engineer (Java / Rust) — Tsukiusagi Pay, Inc.

> 株式会社ツキウサギペイは実在しない架空の会社です。この文書は面接システムの実験のために書かれました。
> Tsukiusagi Pay, Inc. is a fictional company. This document was written for an experiment on an interview system.

---

## 日本語

### 会社概要
株式会社ツキウサギペイは東京に本社を置く、従業員約300名の金融テクノロジー企業です。個人向けのスマートフォン決済アプリ、送金、後払い、少額投資を提供しています。登録ユーザーは約900万人、1日あたりの決済件数は最大約400万件です。資金移動業者としての登録があり、残高は預かり資産として扱われます。

### プロダクトと開発環境
- iOS / Android アプリ（Swift、Kotlin）と、加盟店向けの Web 管理画面
- バックエンドは Java 21 と Spring Boot によるマイクロサービス群（約60サービス）。Kafka によるイベント連携、PostgreSQL、Redis、Kubernetes 上で稼働
- 台帳（残高・取引履歴）、決済オーソリ、精算、不正検知、通知の各ドメインにチームが分かれています
- モバイルエンジニアとバックエンドエンジニアを継続的に採用しています

### 現在の Java アーキテクチャ
台帳サービスは複式簿記の仕訳を PostgreSQL に書き込み、Kafka で下流（精算、通知、分析）へイベントを流します。決済リクエストは冪等キーで重複を排除し、オーソリと確定は別トランザクションです。加盟店への精算は毎朝バッチで確定し、確定後の修正は新しい仕訳として記録します（上書きは禁止）。JVM のGCチューニング、コネクションプール、トランザクション境界の設計が日常的な仕事です。

### Rust への方向性
決済オーソリと不正検知のホットパスで、レイテンシとメモリ使用量の予測可能性を高めるため、Rust の採用を段階的に進めています。すでに2つのサービス（トークン化、レート制限）が Rust で本番稼働しています。今後2年で台帳の書き込み経路の一部を Rust に移す計画です。全面的な書き直しはしません。境界を決め、計測し、Java と共存させながら移します。Rust の経験は必須ではありませんが、実務経験があるか、現実的に習得できる見込みがあることを重視します。

### 募集ポジション：バックエンドエンジニア（台帳・決済）
#### 主な業務
- 台帳・決済ドメインの Java サービスの設計、実装、運用
- Rust への移行対象の選定、境界設計、段階的な移行の実装
- 冪等性、整合性、精算突合のような「お金が合う」仕組みの維持と改善
- オンコール当番（チーム全員が輪番で担当します）
- 障害の振り返り（ポストモーテム）の作成と再発防止

#### 必須スキル
- Java での本番バックエンド開発経験 3年以上（Spring または同等のフレームワーク）
- リレーショナルデータベースのトランザクション設計と、障害時の整合性回復の経験
- 分散システムでの冪等性、リトライ、重複配信への対処の実務経験
- 自分が運用したシステムの障害について、原因と対処を具体的に説明できること

#### 歓迎スキル
- Rust の実務経験、または個人プロジェクトで所有権・ライフタイム・非同期ランタイムを扱った経験
- Kafka などのイベント基盤の運用経験
- 決済、銀行、証券など、お金を扱うシステムの経験
- Java から別言語への移行や、サービス境界の切り出しを主導した経験

### エンジニアリングに求めること
- 台帳が真実です。数字が合わないときは機能より数字の整合を優先します
- 小さく出し、計測し、戻せる状態を保ちます
- 自分が出したものは自分たちで運用します。オンコールは全員の仕事です
- 分からないことは早く言います。抱え込んで朝の障害にしないでください
- 変更は必ずレビューとデプロイ手順を通します。緊急時でも手順を省略せず、省略が必要なら宣言して記録します

### 行動原則（Working Principles）
1. **証拠で議論し、決めたら従う。** 反対意見は歓迎します。ただし決定後に独断で覆さないでください
2. **隠さない。** 障害、ミス、遅れは起きた時点で共有します。責めません。隠すことだけを問題にします
3. **お金は試験環境ではない。** 本番の残高で実験しない。確認できない変更は出さない
4. **運用とサポートは対等な仕事。** オンコール、問い合わせ対応、ジュニアの育成を「本業ではない」と扱いません
5. **境界を決めてから書き直す。** 技術的な好みで全面書き換えを始めない。移行は計測と合意の上で行います

### 面接での評価基準
面接では次の観点を評価します。各観点について、具体的な経験に基づく回答を求めます。
1. **Java バックエンドの実務力** — 本番で動いた設計と、その運用の実際
2. **Rust への準備度** — 実務経験、または所有権モデルや移行境界について現実的に考えられること
3. **お金の正しさと運用判断** — 冪等性、突合のずれ、障害時の対応を自分の経験として語れること
4. **働き方の一致** — 上記の行動原則に沿った行動を実際にしてきたこと

### 評価を下げる条件
- 「チームでやりました」と言うが、自分が何をしたか説明できない
- フレームワークや技術の名前は多く出るが、設計の理由や失敗の話が出ない
- 質問に対して一般論や教科書的な説明だけで、自分の経験が伴わない
- 話は流暢だが、具体的な数字、期間、失敗、判断の根拠が出てこない
- 質問と関係のない経歴の話を長く続ける

### 技術力が高くても不採用になる条件
- レビューやデプロイ手順を、緊急でもないのに意図的に省略した経験を肯定的に語る
- 障害やミスを報告しなかった、または報告を遅らせたことを問題と考えていない
- オンコール、サポート対応、ジュニアの育成を自分の仕事ではないと明言する
- チームの決定を無視して独断で実装や書き換えを進めたことを誇る
- 本番のデータや残高を検証のために使ったことを問題視しない

---

## English

### Company overview
Tsukiusagi Pay, Inc. is a Tokyo-based financial technology company with about 300 employees. We offer a consumer smartphone payment app, peer-to-peer transfers, buy-now-pay-later, and small-amount investing. About 9 million registered users make up to about 4 million payments per day. We are registered as a funds transfer service provider, and user balances are held as customer assets.

### Product and engineering environment
- iOS and Android apps (Swift, Kotlin) and a web console for merchants
- Backend: about 60 microservices in Java 21 with Spring Boot. Kafka for events, PostgreSQL, Redis, running on Kubernetes
- Teams own the ledger (balances and history), payment authorization, settlement, fraud detection, and notifications
- We hire mobile engineers and backend engineers continuously

### Current Java architecture
The ledger service writes double-entry journal lines to PostgreSQL and publishes events to Kafka for downstream settlement, notifications, and analytics. Payment requests are de-duplicated by idempotency key; authorization and capture are separate transactions. Merchant settlement is finalized by a batch every morning. A correction after finalization is a new journal entry, never an edit. JVM garbage-collection tuning, connection pools, and transaction boundaries are everyday work.

### Direction for Rust
We are adopting Rust step by step on hot paths in payment authorization and fraud detection, where predictable latency and memory use matter. Two services (tokenization, rate limiting) already run in Rust in production. Over the next two years we plan to move part of the ledger write path to Rust. We will not rewrite everything. We choose a boundary, measure, and migrate while Java and Rust coexist. Rust experience is not required. We value real experience with it, or a realistic ability to learn it.

### Open position: Backend Engineer (Ledger and Payments)
#### Responsibilities
- Design, build, and operate Java services in the ledger and payments domain
- Select migration targets for Rust, design the boundaries, and implement the migration step by step
- Maintain and improve the mechanisms that keep money correct: idempotency, consistency, settlement reconciliation
- Take part in the on-call rotation (every engineer on the team does)
- Write blameless postmortems and prevent repeat incidents

#### Required skills
- 3 or more years of production backend development in Java (Spring or an equivalent framework)
- Experience with transaction design in a relational database and with restoring consistency after a failure
- Hands-on experience with idempotency, retries, and duplicate delivery in a distributed system
- Ability to explain, concretely, the cause of and the response to an incident on a system you operated

#### Preferred skills
- Production Rust experience, or personal projects that dealt with ownership, lifetimes, and async runtimes
- Experience operating an event platform such as Kafka
- Experience with systems that handle money: payments, banking, securities
- Experience leading a migration from Java to another language, or carving out a service boundary

### Engineering expectations
- The ledger is the truth. When the numbers disagree, correct numbers come before features
- Ship small, measure, and keep every change reversible
- We operate what we ship. On-call is everyone's job
- Say early what you do not know. Do not carry it alone until it becomes a morning incident
- Every change goes through review and the deployment procedure. In an emergency you may need to skip a step; if so, you announce it and record it

### Working principles
1. **Argue with evidence, then follow the decision.** Disagreement is welcome. Do not overturn a decision alone after it is made
2. **Do not hide.** Incidents, mistakes, and delays are shared when they happen. We do not blame. We only treat hiding as a problem
3. **Money is not a test environment.** Do not experiment with production balances. Do not ship a change you cannot verify
4. **Operations and support are equal work.** On-call, customer inquiries, and mentoring juniors are not "someone else's job"
5. **Decide the boundary before you rewrite.** Do not start a full rewrite out of technical preference. Migration follows measurement and agreement

### Interview evaluation criteria
The interview assesses the following. For each, we expect answers based on specific experience.
1. **Java backend practice** — designs that ran in production, and what operating them was actually like
2. **Rust readiness** — real experience, or a realistic way of thinking about the ownership model and migration boundaries
3. **Money correctness and operational judgment** — idempotency, reconciliation mismatches, and incident response told as the candidate's own experience
4. **Alignment with how we work** — actual past behavior that matches the working principles above

### Conditions that lead to a low evaluation
- Says "we did it as a team" but cannot explain their own part
- Names many frameworks and technologies but gives no design reasons and no failures
- Answers with general or textbook explanations that carry no experience of their own
- Speaks fluently but gives no concrete numbers, durations, failures, or reasons for decisions
- Spends the answer on unrelated career history

### Conditions that lead to rejection even when technical ability is strong
- Describes deliberately skipping review or the deployment procedure, without an emergency, as a good thing
- Does not consider it a problem that they did not report, or delayed reporting, an incident or a mistake
- States that on-call, support work, or mentoring juniors is not their job
- Is proud of implementing or rewriting something alone, against a team decision
- Sees no problem in using production data or balances for verification
