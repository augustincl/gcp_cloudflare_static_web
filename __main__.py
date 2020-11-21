"""A Google Cloud Python Pulumi program"""

import pulumi
import infrabase


# Export the DNS name of the bucket
pulumi.export('bucket_name', infrabase.web_bucket.url)
