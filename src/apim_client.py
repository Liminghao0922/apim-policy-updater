import os
from azure.identity import ClientSecretCredential
from azure.mgmt.apimanagement import ApiManagementClient

class APIMClient:
    def __init__(self):
        self.subscription_id = os.environ["AZURE_SUBSCRIPTION_ID"]
        self.resource_group = os.environ["AZURE_RESOURCE_GROUP"]
        self.service_name = os.environ["AZURE_APIM_NAME"]
        self.credential = ClientSecretCredential(
            tenant_id=os.environ["AZURE_TENANT_ID"],
            client_id=os.environ["AZURE_CLIENT_ID"],
            client_secret=os.environ["AZURE_CLIENT_SECRET"]
        )
        self.client = ApiManagementClient(self.credential, self.subscription_id)

    def list_product_subscriptions(self, product_id):
        return list(self.client.product_subscriptions.list(
            self.resource_group, self.service_name, product_id
        ))

    def get_subscription_key(self, sid):
        secrets = self.client.subscription.list_secrets(
            self.resource_group, self.service_name, sid
        )
        return secrets.primary_key
