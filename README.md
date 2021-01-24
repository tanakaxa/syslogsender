# syslogsender
json形式に記載したsyslogをリモートサーバに送りつけるためのpythonスクリプト

# 説明
json形式で記載したsyslogプロトコルのメッセージを読み込み、リモートのSyslogサーバにSyslog転送するスクリプト

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
Send To 10.0.0.1:514 MSG:<137>Jan 24 11:50:38 testhost This message is rfc3164 format Alert Message
Send To 10.0.0.2:514 MSG:<134>Jan 24 12:06:45 - This message is Info Message
```

### サンプル受信サーバ出力例
実際の出力は受信したSyslogサーバの設定に依存よって異なる。
```
Jan 24 11:50:38 testhost This message is rfc3164
```

## jsonパラメータ
1オブジェクトにつき下記パラメータを指定可能。

| パラメータ | 型 | 必須 | デフォルト | コメント |
| :--- | :--- | :--- | :--- | :--- |
| logserver_ip | string | Yes | n/a | 送信先syslogサーバのIPアドレス。 例)`10.0.0.1` |
| logserver_port | int | | 514 | 送信先syslogサーバのポート番号。 例)`514` |
| tcp | boolean | | false | ログ送信時にTCPを使用する場合は`true`。UDPを使用する場合は未指定または`false`。 |
| facility | int | | 16 | SyslogのFacility値。デフォルトでは`16`(LOCAL0)。 | 
| severity | int | | 6 | SyslogのSeverity値。デフォルトでは`6`(INFO)。|
| timestamp | string | | 実行時のデバイス時刻 | Syslogヘッダ内のTIMESTAMP。例)`Jan 24 11:50:38` |
| hostname | string | | - | Syslogヘッダ内のHOSTNAME。ログを生成したホストのFQDN/hostname/IPアドレスなどを記載する。例)`testmachine.example.com` |
| msg | string | Yes | n/a | Syslogのメッセージを記載する。 |

各パラメータの詳細はRFC3164で確認可能。


# (Option)RFC5424方式のメッセージ
## 追加jsonパラメータ
| パラメータ | 型 | 必須 | デフォルト | コメント |
| :--- | :--- | :--- | :--- | :--- |
| rfc5424 | boolean | | false | ログメッセージにRFC5424形式を使用する場合は`true`。RFC3164形式を使用する場合は未指定または`false`。 |
| timestamp | string | | 実行時のJST時刻 | 【RFCによる変更】Syslogヘッダ内のTIMESTAMP。RFC3339に準拠した値を指定する。例)`2021-01-16T21:46:17.548485+09:00` |
| appname | string | | - | Syslogヘッダ内のAPP-NAME。ログを生成したアプリケーションの名前を記載する。 |
| procid | string | | - | Syslogヘッダ内のPROCID。プロセス名またはプロセスIDを記載する。 |
| msgid | string | | - | Syslogヘッダ内のMSGID。 |
| msg | string | Yes | n/a | 【RFCによる変更】Syslogのメッセージを記載する。また、必要に応じてSTRUCTURED-DATAも合わせて記載することで、STRUCTURED-DATA付きのSyslogメッセージを送付することが可能。 |

各パラメータの詳細はRFC5424で確認可能。


# (Option)送信元IPの詐称
`ext-syslogsender.py`は送信元IPを詐称できる拡張スクリプトである。

## 追加動作要件
- Scapy
```
$ sudo pip3 install scapy
```
- WSLなどNAPT環境では利用不可

## 使い方
管理者権限が必要
```
$ sudo python3 ext-syslogsender.py sample.json
```

## 追加jsonパラメータ
| パラメータ | 型 | 必須 | デフォルト | コメント |
| :--- | :--- | :--- | :--- | :--- |
| custom_srcip | string |  | n/a | 送信元IPアドレス。`TCP`パラメータとの両立不可(`custom_srcip`を優先)。 例)`10.0.0.2` |

# 既知の問題
- 同一のメッセージを繰り返し送信しているが、サーバ側で出力がされない
    - syslogサーバ側で、バッファの使用率やログサイズの削減のため同じメッセージの出力を抑止している可能性がある
        - rsyslogの場合、`$RepeatedMsgReduction`が有効な場合に発生
    - confを書き換えるか、集約条件に含まれるいずれかのプロパティを変更し再送することで回避可能
