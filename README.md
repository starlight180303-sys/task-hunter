# Task Hunter ⚔️

締切、作業時間、難易度、進捗率から課題の危険度を計算し、ゲームのボス風に表示するWebアプリです。生成AIを利用した授業課題として作成しました。

## 入力・処理・出力
- 入力: 課題名、科目名、締切、予想作業時間、難易度、進捗率
- 処理: 締切までの時間、残作業時間、難易度、進捗率から危険度を算出
- 出力: 0〜100の危険度、ボスランク、残り時間、行動アドバイス

## 主な機能
- 課題の登録とSQLiteへの永続保存
- 危険度順の表示、ボスランク判定
- 討伐完了と削除
- レスポンシブUI、Dockerヘルスチェック

## 使用技術
Python 3.12 / Flask / SQLite / HTML / CSS / JavaScript / Gunicorn / Docker Compose

## 起動方法
```bash
git clone https://github.com/starlight180303-sys/task-hunter.git
cd task-hunter
docker compose up --build
```
ブラウザで http://localhost:5000 を開きます。

## 停止方法
```bash
docker compose down
```
データも消す場合は `docker compose down -v` を実行します。

## 使い方
1. フォームに課題情報を入力します。
2. 「危険度を診断する」を押します。
3. 危険度が高い課題から取り組みます。
4. 完了したら「討伐完了」を押します。

## 動作画面
画面を撮影して `screenshots/main.png` を追加し、ここに掲載してください。

## 生成AIの利用
企画、技術選定、Flaskアプリ、危険度計算、Docker関連ファイル、UI、README、テストの作成に生成AIを利用しました。

## 注意
診断結果は学習計画を立てるための目安です。実際の提出条件と締切は授業案内を確認してください。
