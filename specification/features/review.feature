# spec-weaver-fingerprint: 6b53cf78ccd167d8a82ddbd5b5f2e7a694ad6ba14dbe956b7fc1209dc02ad749
# spec-weaver-fingerprint-QA-004: zJZ8rKdo5j3CC50cStOQT-dYQz3fw8w45YpbYNLYs6o=
@QA-004
Feature: review コマンド — .feature ファイルへのフィンガープリント書き込み
  指定した .feature ファイルの構造コンテンツ（Feature / Background / Scenario）の
  SHA-256 ハッシュを計算し、ファイル先頭にコメントとして書き込む。
  これにより、ファイルが最後にレビューされた時点の状態を自身が記録する。

  Scenario: .feature ファイルを指定してフィンガープリントが書き込まれる
    Given ".feature" ファイルが存在する
    When `spec-weaver review specification/features/audit.feature` を実行する
    Then 終了コードが0である
    And ファイル先頭に "# spec-weaver-fingerprint:" コメントが追加される

  Scenario: 既存のフィンガープリントコメントが新しいハッシュで上書きされる
    Given ".feature" ファイルの先頭に古いフィンガープリントコメントが存在する
    When `spec-weaver review specification/features/audit.feature` を実行する
    Then 終了コードが0である
    And ファイル先頭のコメントが新しいハッシュ値で上書きされる

  Scenario: 存在しないファイルを指定するとエラーになる
    When `spec-weaver review nonexistent.feature` を実行する
    Then 終了コードが1である
    And エラーメッセージが表示される
