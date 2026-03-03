# spec-weaver-fingerprint: da191d2e4724ecd8ae92af47b1508866117b34863797bc3f9789eef8992ef1fc
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

  Scenario: 指定ファイルが .feature でない場合にエラーになる
    Given ".txt" ファイルが存在する
    When `spec-weaver review not_feature.txt` を実行する
    Then 終了コードが1である
    And エラーメッセージが表示される
