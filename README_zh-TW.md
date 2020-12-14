# 使用 Cloudflare 與 GCP 打造零元的靜態網站基礎設施 

將採用 Google Bucket 來存放靜態網頁，並且提供給使用者瀏覽。DNS 與 CDN 則採用 Cloudflare 的解決方案，一方面為網站提供穩妥的導流，另一方面也去除了自架的 CDN 與負載均衡器的費用。

:triangular_flag_on_post: 預設使用 Cloudflare 的憑證服務，來自動提供 TLS 保護!<br/><br/>

:bulb: 專案採用了兩個不同的雲端解決方案供應商，來組合整個基礎設施，主要目的是在不減低網站的穩定性下，又能進一步降低維護靜態網站基礎設施的費用。如果你有任何其他考量，完全可以將其加入實作中，當然有什麼建議也可以透過 github 的 issue 交流。

## Prerequisite

* 此專案是基於 Google 的雲端服務，為了完成整個佈署，請安裝 [gcloud SDK](https://cloud.google.com/sdk/docs/install#deb)
* Python 3.7+ :warning: 請勿安裝2.x的版本
* [Pulumi](https://www.pulumi.com/docs/get-started/install/)
* 備妥 [Cloudflare](https://www.cloudflare.com/) 帳號，並且產生用於驗證 API 呼叫的權柄(token)
* 將你的 DNS 主機改成使用 Cloudflare.[more](https://support.cloudflare.com/hc/en-us/articles/205195708-Changing-your-domain-nameservers-to-Cloudflare)
* 在 Cloudflare 所託管的目標網站中，將 SSL/TLS 加密模式設置為 **完整**

:mega: 
1. 本專案所有操作都是基於 **LINUX**。
2. 如果是 Windows 的使用者，一些操作指令可能不適用! 請稍加調適。
3. gcloud與pulumi的設置請參考官網，而Python則請用anaconda建立執行環境


## Running the App

1. 下載並且初始你的環境

    :warning:
    Windows 使用者請利用 Anaconda 建立虛擬環境，再利用指令安裝 requirements.txt 即可!

    ```
    $ python3 -m venv venv
    $ source venv/bin/activate
    $ pip3 install -r requirements.txt
    ```
    
2.  建立一個新的堆疊:

    ```
    $ pulumi stack init dev
    ```

3.  設定專案組態屬性:

    ```
    $ pulumi config set gcp:project YOURGOOGLECLOUDPROJECT
    $ pulumi set cloudflare:email mail@yours
    $ pulumi set cloudflare:apiKey  I_AM_A_KEY_FOR_CLOUDFLARE --secret
    ```

4.  打開 infrabase.py 檔案，並且將已申請好的域名指派給如下的域名變數

    ```
    DOMAIN_NAME="[USE-YOUR-DOMAIN-NAME]" 
    TARGET_PROJECT="[YOUR-PROVISION-PROJECT]"
    ZONE_ID="[YOUR-ZONE-ID]"
    RULE_TARGET="[YOUR-ROOT-URL] e.g. yourdomain.org/*"
    FORWARD_TARGET="[YOUR-SERVING-URL] e.g. www.yourdomain.org/$1" DO NOT FORGET $1
    ```

5.  執行 `pulumi up -y` 來預覽整個基礎設施的配置，並且進行佈署:

    ``` 
    Previewing update (dev)

    View Live: https://app.pulumi.com/augustincl/gcp_cloudflare_static_web/dev/previews/647e7c7c-28f8-4a35-b7ad-7d45996becc8

     Type                                       Name                           Plan       
     +   pulumi:pulumi:Stack                        gcp_cloudflare_static_web-dev  create     
     +   ├─ cloudflare:index:Record                 root                           create     
     +   ├─ cloudflare:index:PageRule               www2root                       create     
     +   ├─ gcp:storage:Bucket                      official-web                   create     
     +   ├─ cloudflare:index:Record                 www-sub                        create     
     +   └─ gcp:storage:DefaultObjectAccessControl  official-web-read              create     
 
    Resources:
        + 6 to create

    Updating (dev)

    View Live: https://app.pulumi.com/augustincl/gcp_cloudflare_static_web/dev/updates/4

     Type                                       Name                           Status      
     +   pulumi:pulumi:Stack                        gcp_cloudflare_static_web-dev  created     
     +   ├─ gcp:storage:Bucket                      official-web                   created     
     +   ├─ cloudflare:index:Record                 root                           created     
     +   ├─ cloudflare:index:Record                 www-sub                        created     
     +   ├─ cloudflare:index:PageRule               www2root                       created     
     +   └─ gcp:storage:DefaultObjectAccessControl  official-web-read              created     
 
    Outputs:
        bucket_name: "gs://[USE-YOUR-DOMAIN-NAME]"

    Resources:
        + 6 created

    Duration: 8s
    ```

6.  上傳你的預設首頁(index.html)與錯誤頁(404.html)!
    
    a. 前往 [Google Console](https://console.cloud.google.com/)，並且打開命名為 "[USE-YOUR-DOMAIN-NAME]" 的 bucket。<br/>
    b. 上傳 index.html 與 404.html.

7. 現在你可以透過 [USE-YOUR-DOMAIN-NAME] 來瀏覽你的網站!

8. 如果你只是進行測試，別忘記在測試完畢後，將所有資源刪除!

    ```
    $ pulumi destroy
    $ pulumi stack rm
    ```
