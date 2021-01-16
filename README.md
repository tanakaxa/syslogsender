# syslogsender
json形式に記載したsyslogをリモートサーバに送りつけるためのpythonスクリプト

# 説明
json形式で記載したsyslogプロトコルのメッセージを読み込み、リモートのSyslogサーバにSyslog(RFC5424)転送するスクリプト

# 動作要件
- Python3.x
    - WSLのUbuntu20.04上の3.8.5で動作確認済み

# 使い方
```
$ python3 syslogsender.py sample.json
```

## jsonサンプル
`sample.json`は3つのSyslogを定義したサンプルファイルである。

サンプルのように複数のオブジェクトを定義することで複数のログを順次送付することが可能。
なお、オブジェクト名はプログラム内では参照しない。

### サンプル実行例
```
$ python3 syslogsender.py sample.json
Send To 10.0.0.1(TCP) MSG:<137>1 2003-10-11T22:14:15.003000+09:00 mymachine.example.com evntslog 123 ID47 [exampleSDID@32473 iut="3" eventSource="Application" eventID="1011"] LOCAL1 EMERGENCY MESSAGE
Send To 10.0.0.2 MSG:<170>1 2021-01-16T22:27:22.003496+09:00 - - - - CRITICAL MESSAGE
Send To 10.0.0.2 MSG:<134>1 2021-01-16T22:27:22.003652+09:00 - - - - INFO MESSAGE
```

### サンプル受信サーバ出力例
実際の出力は受信したSyslogサーバの設定に依存よって異なる。
```
Oct 11 22:14:15 mymachine.example.com evntslog[123] LOCAL1 EMERGENCY MESSAGE
Jan 16 22:27:22 - - CRITICAL MESSAGE
Jan 16 22:27:22 - - INFO MESSAGE
```

## jsonパラメータ
1オブジェクトにつき下記パラメータを指定可能。

| パラメータ | 型 | 必須 | デフォルト | コメント |
| :--- | :--- | :--- | :--- | :--- |
| logserver_ip | string | Yes | n/a | 送信先syslogサーバのIPアドレス。 例)`10.0.0.1` |
| logserver_port | int | | 514 | 送信先syslogサーバのポート番号。 例)`514` |
| tcp | bookean | | false | ログ送信時にTCPを使用する場合は`true`。UDPを使用する場合は未指定または`false`。 |
| facility | int | | 16 | SyslogのFacility値。デフォルトでは`16`(LOCAL0)。 | 
| severity | int | | 6 | SyslogのSeverity値。デフォルトでは`6`(INFO)。|
| timestamp | string | | 実行時のJST時刻 | Syslogヘッダ内のTIMESTAMP。RFC3339に準拠した値を指定する。例)`2021-01-16T21:46:17.548485+09:00` |
| hostname | string | | - | Syslogヘッダ内のHOSTNAME。ログを生成したホストのFQDN/hostname/IPアドレスなどを記載する。例)`testmachine.example.com` |
| appname | string | | - | Syslogヘッダ内のAPP-NAME。ログを生成したアプリケーションの名前を記載する。 |
| procid | string | | - | Syslogヘッダ内のPROCID。プロセス名またはプロセスIDを記載する。 |
| msgid | string | | - | Syslogヘッダ内のMSGID。 |
| msg | string | Yes | n/a | Syslogのメッセージを記載する。また、必要に応じてSTRUCTURED-DATAも合わせて記載することで、STRUCTURED-DATA付きのSyslogメッセージを送付することが可能。 |

各パラメータの詳細はRFC5424で確認可能。


# 既知の問題
- 同一のメッセージを繰り返し送信しているが、サーバ側で出力がされない
    - syslogサーバ側で、バッファの使用率やログサイズの削減のため同じメッセージの出力を抑止している可能性あり。メッセージの一部を変えて再送することで再度出力される。