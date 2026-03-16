import os
from azure.identity import ClientSecretCredential
from azure.mgmt.apimanagement import ApiManagementClient
from dotenv import load_dotenv

load_dotenv()

# 环境变量配置
SUBSCRIPTION_ID = os.environ["AZURE_SUBSCRIPTION_ID"]
RESOURCE_GROUP = os.environ["AZURE_RESOURCE_GROUP"]
SERVICE_NAME = os.environ["AZURE_APIM_NAME"]
PRODUCT_ID = os.environ["APIM_PRODUCT_ID"]  # 需在.env或环境变量中配置

credential = ClientSecretCredential(
    tenant_id=os.environ["AZURE_TENANT_ID"],
    client_id=os.environ["AZURE_CLIENT_ID"],
    client_secret=os.environ["AZURE_CLIENT_SECRET"]
)

client = ApiManagementClient(credential, SUBSCRIPTION_ID)

# 强制使用user_id为'1'
USER_ID = "1"

# 批量创建参数
COUNT = int(os.environ.get("BATCH_SUBSCRIPTION_COUNT", 5000))
NAME_PREFIX = os.environ.get("BATCH_SUBSCRIPTION_PREFIX", "AutoSub-")



for i in range(COUNT):
    display_name = f"{NAME_PREFIX}{i+1}"
    subscription_id = f"{NAME_PREFIX.lower()}{i+1}"
    print(f"Creating subscription: {display_name} (id: {subscription_id})")
    result = client.subscription.create_or_update(
        resource_group_name=RESOURCE_GROUP,
        service_name=SERVICE_NAME,
        sid=subscription_id,
        parameters={
            "display_name": display_name,
            "scope": f"/products/{PRODUCT_ID}",
            "user_id": f"/users/{USER_ID}",
            "state": "active"
        }
    )
    print(f"Created: {result.name}")

print("Batch creation completed.")
