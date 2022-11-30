---
name: Refactoring
about: Refactoring
title: リファクタリング：
labels: fix
assignees: ''

---

作業ブランチ名：fix/
作業ファイル名：aurl/environment/controller/

突貫で実装したものを丁寧に作り直してください。
元のソースコードは[ここ](https://github.com/2022-IS-team/2022-is-experiments2-team-3/tree/main/src/aurl/environment/controller)から見れます。

## 実施手順
1. developブランチを同期する
```
git checkout develop
git pull origin develop
```
2. 作業ブランチを作成し、そこへ移動する
```
git checkout -b <<作業ブランチ名>>
```
3. <<作業ファイル名>>を開き、要件の通りの関数となるよう実装を行う

その関数に求められる機能は関数内のコメントに記載してあるので参照する。
ファイルの中身は以下のようになる。
```python
from ～～ import ～～
...
def  <<関数名>>(<<引数>>) -> <<返り値の型>>:
    ```<<関数名>>
    
    要件・実装指示

    引数・返り値についての説明

    ```
```
4. テストの実行
```
make
```
上記のコマンドを実行すると、しばらくログが流れた後、「ファイルの監視を開始しました。ファイルを保存するとテストが実行され結果が表示されます。」と表示される。
この状態で、作業ファイルを保存すると、作業対象の関数についてテストが実行され、求められる機能が満たせているか確かめることができる。
エラーがあれば赤字で指摘されるので、よく読んで修正する。
「～ passed in ～s」と緑字で表示されたら完了。
5. 作業の保存・アップロード
```
git add src/aurl/environment/controller/<<作業ファイル名>>
git commit -m "<<作業内容が分かるコメント>>"
git push origin <<作業ブランチ名>>
```
6. プルリクエストの作成
Githubページ上で操作
  a. 「Pull requests」を押す
  ![image](https://user-images.githubusercontent.com/64251336/204714120-711b1096-5eac-4619-978f-0f9648b4ae1b.png)
  b.  「New pull request」
  ![image](https://user-images.githubusercontent.com/64251336/204714405-41b907a6-5fd3-4c89-9f0c-bf8ad274106f.png)
  c.  「base」は"develop"のまま、「compare」は"<<作業ブランチ名>>"にする。
  ![image](https://user-images.githubusercontent.com/64251336/204716237-66ae2687-9681-41d0-aeb4-2e0b6f25ef0f.png)
  d. 「Create pull request」
  ![image](https://user-images.githubusercontent.com/64251336/204716393-d67131bb-453c-4599-9e97-02ba75e0ba43.png)
  e. 「Create pull request」
  ![image](https://user-images.githubusercontent.com/64251336/204716504-7a79cfb9-f650-4b75-8d0e-2a9352722c26.png)
7. ここまでできたらdiscordで川田に連絡
