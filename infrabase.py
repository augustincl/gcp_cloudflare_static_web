import pulumi
from pulumi_gcp import storage
import pulumi_cloudflare as cloudflare

#
#SOME KNOWN VAR (You might implement a yml reader to keep this!)
#
#COMMON
DOMAIN_NAME="[USE-YOUR-DOMAIN-NAME]"

#GCP
TARGET_PROJECT="[YOUR-PROVISION-PROJECT]"
BUCKET_TARGET_URL="c.storage.googleapis.com"
MAIN_SUFFIX="index.html"
ERR_SUFFIX="404.html"

#Cloudflare
ZONE_ID="[YOUR-ZONE-ID]"
RULE_TARGET="[YOUR-ROOT-URL] e.g. yourdomain.org/*"
#MUST END WITH "/$1"
FORWARD_TARGET="[YOUR-SERVING-URL] e.g. www.yourdomain.org/$1"


#step 1. create the website bucket
web_bucket=storage.Bucket("official-web"
    ,name=DOMAIN_NAME #this variable MUST be set as your domain name
    ,website=storage.BucketWebsiteArgs(main_page_suffix=MAIN_SUFFIX,not_found_page=ERR_SUFFIX)
    ,location="us-central1"
    ,project=TARGET_PROJECT
    ,storage_class="REGIONAL")

access_ctl=storage.DefaultObjectAccessControl("official-web-read"
    ,bucket=web_bucket.name
    ,role="READER"
    ,entity="allUsers")

#step 2. add RECORD to DNS
www=cloudflare.Record("www-sub"
    ,zone_id=ZONE_ID
    ,name="www"
    ,value="c.storage.googleapis.com"
    ,type="CNAME"
    ,proxied=1
    ,ttl=1)
root=cloudflare.Record("root"
    ,zone_id=ZONE_ID
    ,name="cpht.pro"
    ,value="c.storage.googleapis.com"
    ,type="CNAME"
    ,proxied=True
    ,ttl=1)

#step 3. add a page rule
always_root_rule=cloudflare.PageRule("www2root"
    ,zone_id=ZONE_ID
    ,target=RULE_TARGET
    ,priority=1
    ,actions=cloudflare.PageRuleActionsArgs(
        forwarding_url=cloudflare.PageRuleActionsForwardingUrlArgs(status_code=301
            ,url=FORWARD_TARGET
        )
))