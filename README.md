# Leverage Cloudflare and GCP to construct the cheapest infra for Static Web 

This project will use google bucket as the web backend to serving a website.
As for DNS and CDN, we will leverage Cloudflare as the solution to serve the request

:triangular_flag_on_post: TLS with auto-updates by default!
:bulb: This implementation will leverage two different kinds of the cloud providers to serve the web.
The purpose here is to lower down the initial cost for the static web. At the very begining and the general purpose, we do need a robust, but a cheap solution for your own web. However, if you have any concerns, please feel free to take them into considerations and just modify them as you expect. 

## Prerequisite

* This project leverages GCP. Please setup your [gcloud SDK](https://cloud.google.com/sdk/docs/install#deb)
* You should leverage gcloud command to setup your application token
* Python **3.7+**. :warning: DO NOT USE VERSION 2.x
* [Pulumi](https://www.pulumi.com/docs/get-started/install/)
* Please prepare your [Cloudflare](https://www.cloudflare.com/) account and generate an API token for the operation.
* Change your domain name server with the ones provided by cloudflare. [more](https://support.cloudflare.com/hc/en-us/articles/205195708-Changing-your-domain-nameservers-to-Cloudflare)
* In your moved website from Cloudflare, set your SSL/TLS encryption mode as **FULL**

:mega: 
1. All the commands are based on **LINUX**
2. If you are a Windows user, please note that you might need to adjust some instructions!
3. Please refer to the official site for gcloud and pulumi for more details about the installation
4. Please leverage Anaconda to setup your python environment.

## Running the App

1. Download and initialize your environment

    :warning: 
    For Windows users, please leverage Anaconda to create your virtual environment. Then, use command to install requirements.txt

    ```
    $ python3 -m venv venv
    $ source venv/bin/activate
    $ pip3 install -r requirements.txt
    ```
    
2.  Create a new stack:

    ```
    $ pulumi stack init dev
    ```

3.  Configure the project:

    ```
    $ pulumi config set gcp:project YOURGOOGLECLOUDPROJECT
    $ pulumi set cloudflare:email mail@yours
    $ pulumi set cloudflare:apiKey  I_AM_A_KEY_FOR_CLOUDFLARE --secret
    ```

4.  Edit the following variable in infrabase.py based on your domain

    ```
    DOMAIN_NAME="[USE-YOUR-DOMAIN-NAME]" 
    TARGET_PROJECT="[YOUR-PROVISION-PROJECT]"
    ZONE_ID="[YOUR-ZONE-ID]"
    RULE_TARGET="[YOUR-ROOT-URL] e.g. yourdomain.org/*"
    FORWARD_TARGET="[YOUR-SERVING-URL] e.g. www.yourdomain.org/$1" DO NOT FORGET $1
    ```

5.  Run `pulumi up -y` to preview and deploy changes:

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

6.  Upload your index.html and 404.html
    
    a. Go to [Google Console](https://console.cloud.google.com/) and open the created bucket, named with "[USE-YOUR-DOMAIN-NAME]".<br/>
    b. upload your html files into it.

7. Now, you could find your web from [USE-YOUR-DOMAIN-NAME]!

8. Don't forget to clean up the infrastructure, if you just give it a try.

    ```
    $ pulumi destroy
    $ pulumi stack rm
    ```
