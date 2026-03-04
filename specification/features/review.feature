# spec-weaver-fingerprint: 8558674633eb8fa7d81a20573dc103f24fb474919b6f6c0d926937136ca17e0b
# spec-weaver-fingerprint-QA-004: zJZ8rKdo5j3CC50cStOQT-dYQz3fw8w45YpbYNLYs6o=
@QA-004
Feature: review コマンド — .feature ファイルへのフィンガープリント書き込み
  指定した .feature ファイルの構造コンテンツ（Feature / Background / Scenario）の
  SHA-256 ハッシュを計算し、ファイル先頭にコメントとして書き込む。
  これにより、ファイルが最後にレビューされた時点の状態を自身が記録する。

  Scenario: .feature ファイルを指定してフィンガープリントが書き込まれる
    Given ".feature" ファイルが存在する
    When `spec-weaver review specification/features/audit.feature` を実行する
    Then review 終了コードが0である
    And ファイル先頭に "# spec-weaver-fingerprint:" コメントが追加される

  Scenario: 既存のフィンガープリントコメントが新しいハッシュで上書きされる
    Given ".feature" ファイルの先頭に古いフィンガープリントコメントが存在する
    When `spec-weaver review specification/features/audit.feature` を実行する
    Then review 終了コードが0である
    And ファイル先頭のコメントが新しいハッシュ値で上書きされる

  Scenario: 存在しないファイルを指定するとエラーになる
    When `spec-weaver review nonexistent.feature` を実行する
    Then review 終了コードが1である
    And review エラーメッセージが表示される

  Scenario: 指定ファイルが .feature でない場合にエラーになる
    Given ".txt" ファイルが存在する
    When `spec-weaver review not_feature.txt` を実行する
    Then review 終了コードが1である
    And review エラーメッセージが表示される

  Scenario: --all で全 .feature ファイルと全 Doorstop アイテムを一括レビューできる
    Given feature_dir に複数の ".feature" ファイルが存在する
    And 複数のアクティブな Doorstop アイテムが存在する
    When `spec-weaver review --all --feature-dir ./specification/features` を実行する
    Then review 終了コードが0である
    And 全 ".feature" ファイルにフィンガープリントが書き込まれる
    And アクティブな全 Doorstop アイテムがレビュー済みになる

  Scenario: --all と対象パスを同時に指定するとエラーになる
    When `spec-weaver review --all specification/features/audit.feature` を実行する
    Then review 終了コードが1である
    And review エラーメッセージが表示される

  Scenario: 引数も --all も指定しないとエラーになる
    When `spec-weaver review` を引数なしで実行する
    Then review 終了コードが1である
    And review エラーメッセージが表示される
