## 概要
メンションを飛ばすと天気予報を返してくれるslack bot.
slack上で`天気　地名`とメンションを飛ばすと、三日分の天気を返してくれる。
サポートしている地名一覧は`地名一覧`で確認することができる。
Slack Event Api+Api Gateway+lambdaで構成されている。ボットへのメンションをトリガーにしており、
livedoor天気予報から情報を取ってくる。
イメージは以下の画像を参照。


## 使い方
### GitHubからクローンしてくる。
```
git clone git@github.com:odrum428/slack_tenki_bot.git
```

### プロジェクトファイル内だけをzip化してまとめる
lambdaに挙げるために プロジェクトファイルの中身だけをzipファイルにする
 - city_list.py
 - lambda_function.py
 - livedoor_tenki.py
 - primary_area.xml


### IAMロールを作成する
AWSに登録するところは割愛。
lambda関数にアクセス許可を与えるためにロールを作成する。
`IAMロール`に移動して、`ロールを作成する`から新しいロールを作る。
与える権限は`AWSLambdaBasicExecutionRole`で十分。名前は好きにつけてください。
  
### AWS lambdaで関数を作成する
lambdaに移動し、関数を作成する。
`関数の作成`を選択し、`一から関数を作成`を選ぶ。
ランタイムは`Python 3.6`.ロールは先ほど作成したロールを割り当てる。
例によって関数名は好きにつけてください。

ページが遷移したら、`関数コード`にある`コードエントリタイプ`の中から`.zipファイルをアップロード`を選択。
先ほど作成したzipファイルを選択し、アップロードする。

### API Gatewayの作成
Slackとlambda関数をつなげる役割。
`API Gateway`に移動し、`APIの作成`をクリック。
名前をつけて、APIを作る。名前は...以下略.

作成完了後は、`アクション`から`メソッドの作成`をクリックし、POSTメソッドを選択。
設定はデフォルトで`Lambda関数`の部分を先ほど作成したlambda関数名を入力。

### API Gatewayのデプロイ
APIにアクセスできるようにするためにデプロイを行う。
`アクション`から`APIのデプロイ`を選択。
`デプロイされるステージ`は`新しいステージ`を選択し、適当な名前を付ける。

デプロイしたら、URLが表示されるので、コピーしておく。

### Slack Botの作成
以下のURLにアクセスする。
https://api.slack.com/apps/

ここで`Create New App`か`Building start`をクリックする。
あらかじめワークスペースを持ってないとダメなのでない人はつくってください。
botの名前はお好きにどうぞ。

アプリを作成したら、ページが遷移するはず。
サイドメニューにある`Bot User`から`Add Bot User`をクリックし、Botを作成する。

### Eventの設定
サイドメニューにある`Event Subscriptions`をクリック。
`Enable Events`をオンにし、`Request URL`に先ほどコピーしたAPI GatewayのURLを貼り付ける。

`Subscribe to Bot Events`以下の`Add Bot User Event`をクリックし、ボットへのメンションを意味する`app_mention`を選択し、
`Save Changes`をクリックして、保存する。

### ボットをワークスペースにインストール
ボットをワークスペースに追加する。
`OAuth & Permissions`に移動し、`Install App`をクリックし、アプリをインストールする。


### 環境変数を設定する
lambda関数にslackのアクセストークンを渡すための設定をする。
lambdaにはweb上で環境変数を設定できる仕組みがあるので、これを利用する。

`環境変数`で以下のように設定する。
- SLACK_APP_AUTH_TOKEN : Slack OAuth & PermissionsにあるOAuth Access Tokenをコピペ
- SLACK_BOT_USER_ACCESS_TOKEN : Slack OAuth & PermissionsにあるBot User OAuth Access Tokenをコピペ
    
### 実際に使ってみる
これで設定が完了したので、さっそく使ってみよう。
`@ボットの名前　天気　地名`で天気を確認できる。
サポートしている地名一覧は`@ボットの名前　地名一覧`で確認できる。
いっぱい使ってくれたらうれしいよ！！！

### エラーがでたら
つまることもあるでしょう。しょうがない。
そんなときはAWS CloudWatchを確認してみよう。
ここにログが吐かれているはずなので、これを追ってみると原因がわかるかも。
がんばれ。






