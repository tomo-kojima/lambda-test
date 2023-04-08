# API Gateway + Lambda + RDS

## インストール
* aws sam cli

    https://docs.aws.amazon.com/ja_jp/serverless-application-model/latest/developerguide/install-sam-cli.html

* aws cli 

    https://docs.aws.amazon.com/ja_jp/cli/latest/userguide/getting-started-install.html

## 準備
* IAMユーザ作成

    |  ポリシー(ざっくり)  |
    | ---- |
    |  AmazonAPIGatewayAdministrator  |
    |  AmazonAPIGatewayInvokeFullAccess  |
    |  AmazonRDSFullAccess  |
    |  AmazonS3FullAccess  |
    |  AWSCloudFormationFullAccess  |
    |  AWSLambda_FullAccess  |
    |  IAMFullAccess  |
    |  AmazonEC2FullAccess  |
* IAM > ユーザー >　{ユーザー名} > セキュリティ人称情報からアクセスキーを作成
* `aws configure`コマンドで、アクセスキーとシークレットキー、リージョンを設定

## Lambda＋API Gateway構築
* `sam init`コマンド実行
```
\git\lambda>sam init

You can preselect a particular runtime or package type when using the `sam init` experience.
Call `sam init --help` to learn more.

Which template source would you like to use?
        1 - AWS Quick Start Templates
        2 - Custom Template Location
Choice: 1

Choose an AWS Quick Start application template
        1 - Hello World Example
        2 - Multi-step workflow
        3 - Serverless API
        4 - Scheduled task
        5 - Standalone function
        6 - Data processing
        7 - Hello World Example With Powertools
        8 - Infrastructure event management
        9 - Serverless Connector Hello World Example
        10 - Multi-step workflow with Connectors
        11 - Lambda EFS example
        12 - DynamoDB Example
        13 - Machine Learning
Template: 1

Use the most popular runtime and package type? (Python and zip) [y/N]: y

Would you like to enable X-Ray tracing on the function(s) in your application?  [y/N]: N

Would you like to enable monitoring using CloudWatch Application Insights?
For more info, please view https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/cloudwatch-application-insights.html [y/N]: N

Project name [sam-app]: lambda-test

    -----------------------
    Generating application:
    -----------------------
    Name: lambda-test
    Runtime: python3.9
    Architectures: x86_64
    Dependency Manager: pip
    Application Template: hello-world
    Output Directory: .
    Configuration file: lambda-test\samconfig.toml

    Next steps can be found in the README file at lambda-test\README.md


Commands you can use next
=========================
[*] Create pipeline: cd lambda-test && sam pipeline init --bootstrap
[*] Validate SAM template: cd lambda-test && sam validate
[*] Test Function in the Cloud: cd lambda-test && sam sync --stack-name {stack-name} --watch
```

* 作成されたlambda-testフォルダ内のtemplate.yamlを修正
    * Resourcesに下記を追加
    ```
    Resources:
      SecurityGroup: # 追加
        Type: AWS::EC2::SecurityGroup # 追加
        Properties: # 追加
          VpcId: {デフォルトのVPCID} # 追加
          GroupDescription: db connect function. # 追加
    ```

* 作成されたlambda-testフォルダ内で、`sam deploy --guided`
```

\git\lambda\lambda-test>sam deploy --guided

Configuring SAM deploy
======================

        Looking for config file [samconfig.toml] :  Found
        Reading default arguments  :  Success

        Setting default arguments for 'sam deploy'
        =========================================
        Stack Name [lambda-test]:
        AWS Region [ap-northeast-1]:
        #Shows you resources changes to be deployed and require a 'Y' to initiate deploy
        Confirm changes before deploy [Y/n]: Y
        #SAM needs permission to be able to create roles to connect to the resources in your template
        Allow SAM CLI IAM role creation [Y/n]: Y
        #Preserves the state of previously provisioned resources when an operation fails
        Disable rollback [y/N]: y
        HelloWorldFunction may not have authorization defined, Is this okay? [y/N]: y
        Save arguments to configuration file [Y/n]: y
        SAM configuration file [samconfig.toml]:
        SAM configuration environment [default]:

        Looking for resources needed for deployment:

        Managed S3 bucket: aws-sam-cli-managed-default-samclisourcebucket-19epka0e1rvxk
        A different default S3 bucket can be set in samconfig.toml and auto resolution of buckets turned off by setting resolve_s3=False

        Parameter "stack_name=lambda-test" in [default.deploy.parameters] is defined as a global parameter [default.global.parameters].
        This parameter will be only saved under [default.global.parameters] in \git\lambda\lambda-test\samconfig.toml.

        Saved arguments to config file
        Running 'sam deploy' for future deployments will use the parameters saved above.
        The above parameters can be changed by modifying samconfig.toml
        Learn more about samconfig.toml syntax at
        https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-config.html

        Uploading to lambda-test/1657479c89d91742e08d668fed4143d2  857 / 857  (100.00%)

        Deploying with following values
        ===============================
        Stack name                   : lambda-test
        Region                       : ap-northeast-1
        Confirm changeset            : True
        Disable rollback             : True
        Deployment s3 bucket         : aws-sam-cli-managed-default-samclisourcebucket-19epka0e1rvxk
        Capabilities                 : ["CAPABILITY_IAM"]
        Parameter overrides          : {}
        Signing Profiles             : {}

Initiating deployment
=====================

        Uploading to lambda-test/006b8fe86fa0fc4730246bc2bc26b2fe.template  1257 / 1257  (100.00%)


Waiting for changeset to be created..

CloudFormation stack changeset
---------------------------------------------------------------------------------------------------------------------
Operation                     LogicalResourceId             ResourceType                  Replacement
---------------------------------------------------------------------------------------------------------------------
+ Add                         HelloWorldFunctionHelloWorl   AWS::Lambda::Permission       N/A
                              dPermissionProd
+ Add                         HelloWorldFunctionRole        AWS::IAM::Role                N/A
+ Add                         HelloWorldFunction            AWS::Lambda::Function         N/A
+ Add                         ServerlessRestApiDeployment   AWS::ApiGateway::Deployment   N/A
                              47fc2d5f9d
+ Add                         ServerlessRestApiProdStage    AWS::ApiGateway::Stage        N/A
+ Add                         ServerlessRestApi             AWS::ApiGateway::RestApi      N/A
---------------------------------------------------------------------------------------------------------------------


Changeset created successfully. arn:aws:cloudformation:ap-northeast-1:xxxxxxxxxxxx:changeSet/samcli-deploy1680931684/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx


Previewing CloudFormation changeset before deployment
======================================================
Deploy this changeset? [y/N]: y

2023-04-08 14:28:14 - Waiting for stack create/update to complete

CloudFormation events from stack operations (refresh every 5.0 seconds)
---------------------------------------------------------------------------------------------------------------------
ResourceStatus                ResourceType                  LogicalResourceId             ResourceStatusReason
---------------------------------------------------------------------------------------------------------------------
REVIEW_IN_PROGRESS            AWS::CloudFormation::Stack    lambda-test                   User Initiated
CREATE_IN_PROGRESS            AWS::CloudFormation::Stack    lambda-test                   User Initiated
CREATE_IN_PROGRESS            AWS::IAM::Role                HelloWorldFunctionRole        -
CREATE_IN_PROGRESS            AWS::IAM::Role                HelloWorldFunctionRole        Resource creation Initiated
CREATE_COMPLETE               AWS::IAM::Role                HelloWorldFunctionRole        -
CREATE_IN_PROGRESS            AWS::Lambda::Function         HelloWorldFunction            -
CREATE_IN_PROGRESS            AWS::Lambda::Function         HelloWorldFunction            Resource creation Initiated
CREATE_COMPLETE               AWS::Lambda::Function         HelloWorldFunction            -
CREATE_IN_PROGRESS            AWS::ApiGateway::RestApi      ServerlessRestApi             -
CREATE_IN_PROGRESS            AWS::ApiGateway::RestApi      ServerlessRestApi             Resource creation Initiated
CREATE_COMPLETE               AWS::ApiGateway::RestApi      ServerlessRestApi             -
CREATE_IN_PROGRESS            AWS::Lambda::Permission       HelloWorldFunctionHelloWorl   -
                                                            dPermissionProd
CREATE_IN_PROGRESS            AWS::ApiGateway::Deployment   ServerlessRestApiDeployment   -
                                                            47fc2d5f9d
CREATE_IN_PROGRESS            AWS::Lambda::Permission       HelloWorldFunctionHelloWorl   Resource creation Initiated
                                                            dPermissionProd
CREATE_IN_PROGRESS            AWS::ApiGateway::Deployment   ServerlessRestApiDeployment   Resource creation Initiated
                                                            47fc2d5f9d
CREATE_COMPLETE               AWS::ApiGateway::Deployment   ServerlessRestApiDeployment   -
                                                            47fc2d5f9d
CREATE_IN_PROGRESS            AWS::ApiGateway::Stage        ServerlessRestApiProdStage    -
CREATE_IN_PROGRESS            AWS::ApiGateway::Stage        ServerlessRestApiProdStage    Resource creation Initiated
CREATE_COMPLETE               AWS::ApiGateway::Stage        ServerlessRestApiProdStage    -
CREATE_COMPLETE               AWS::Lambda::Permission       HelloWorldFunctionHelloWorl   -
                                                            dPermissionProd
CREATE_COMPLETE               AWS::CloudFormation::Stack    lambda-test                   -
---------------------------------------------------------------------------------------------------------------------

CloudFormation outputs from deployed stack
---------------------------------------------------------------------------------------------------------------------
Outputs
---------------------------------------------------------------------------------------------------------------------
Key                 HelloWorldFunctionIamRole
Description         Implicit IAM Role created for Hello World function
Value               xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

Key                 HelloWorldApi
Description         API Gateway endpoint URL for Prod stage for Hello World function
Value               xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

Key                 HelloWorldFunction
Description         Hello World Lambda Function ARN
Value               xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
---------------------------------------------------------------------------------------------------------------------


Successfully created/updated stack - lambda-test in ap-northeast-1
```
上記後、AWS マネジメントコンソールから見ると、LambdaとApiGateway、セキュリティグループが作成されている。

## RDS作成
* セキュリティグループ作成（RDSに付与するセキュリティグループ。PostgreSQLを許容するようにする）
  * EC2 > セキュリティグループ > セキュリティグループを作成
    * セキュリティグループ名：rds-security-group（任意）
    * 説明：rds secrity group（任意）
    * VPC：デフォルト
    * インバウンドルールの追加
      * タイプ：PostgresSQL
      * ソース: lambda-test-SecurityGroup-XXXXXXXXXX（上記sam deployで出来たセキュリティグループ）
　　　 * 他はデフォルト

* プライベートサブネット作成
  * VPC > サブネット > サブネットを作成
    * VPCIDはデフォルトを選択
    * サブネット1つ目
      * サブネット名：rds-private-subnet-1（任意）
      * アベイラビリティゾーン: ap-northeast-1a（aじゃなくてもOK）
      * IPv4 CIDR ブロック：172.31.120.0/20（使われてない適当な値）
    * サブネット2つ目
       * サブネット名：rds-private-subnet-2（任意）
      * アベイラビリティゾーン: ap-northeast-1a（bじゃなくてもOK。1と違う場所にする。未指定なら適当に作ってくれると思う）
      * IPv4 CIDR ブロック：172.31.140.0/20（使われてない適当な値）
* サブネットグループ作成
  * RDS > サブネットグループ > DB サブネットグループを作成
    * 名前：rds-subnet-group（任意）
    * 説明：rds-subnet-group（任意）
    * VPC：デフォルトVPC
    * サブネットを追加：上記で作ったサブネットID
* RDS > データベースの作成
  * 標準作成
  * エンジンのオプション：PostgresSQL
  * テンプレート：無料枠
  * 設定
    * DBインスタンス識別子：postgres-db（任意）
    * マスターユーザー名:postgres（任意）
    * マスターパスワード:任意
  * インスタンスの設定:デフォルト
  * ストレージ:デフォルト
  * 接続
    * コンピューティングリソース:EC2コンピューティングリソースに接続しない
    * ネットワークタイプ:IPv4
    * VPC:デフォルトVPC
    * パブリックアクセス:無し 
    * VPC接続グループ(ファイアウォール):既存の選択
    * 既存のＶＰＣセキュリティグループ:rds-security-group（上記で作成したセキュリティグループ）
    * アベイラビリティゾーン:指定無し
    * RDS Proxy:デフォルト
    * 認証機関:デフォルト
    * データベース認証:パスワード認証（デフォルト）
  * モニタリング:チェック外す
  * 追加設定
    * 最初のデータベース名:test（任意）
    * DB パラメータグループ情報:デフォルト
    * その他はそのまま

* LambdaのVPC設定
  * template.yamlに`追加`の部分を追記
    * SubnetIdsはRDSに設定したものを指定（RDS > データベース > postgres-db > 接続とセキュリティ）
  ```
      HelloWorld:
        Type: Api # More info about API Event Source: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#api
        Properties:
          Path: /hello
          Method: get
     VpcConfig: # 追加
       SecurityGroupIds: # 追加
       - Ref: SecurityGroup # 追加
       SubnetIds: # 追加
       - subnet-xxxxxxxxxxxxxxxxx # 追加
       - subnet-xxxxxxxxxxxxxxxxx # 追加
  ```
* hello_world/app.pyを書き換えてpostgresに接続する処理を追加。
* hello_world/requirements.txtに`aws-psycopg2`を追加
* lambda-testフォルダで、`sam build`, `sam deploy`
* EC2繋ぎたい場合は、RDSのセキュリティグループのインバウントルール追加。（上記作成したルールとほぼ一緒。ソースにEC2セキュリティグループを指定する） 
