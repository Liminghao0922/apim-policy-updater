import os
from jinja2 import Template
from apim_client import APIMClient
from dotenv import load_dotenv

load_dotenv()

DIST_PATH = os.path.join(os.path.dirname(__file__), '..', 'dist')
TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), 'policy_template.xml')
OUTPUT_PATH = os.path.join(DIST_PATH, 'policy.xml')

def main():
    os.makedirs(DIST_PATH, exist_ok=True)
    apim = APIMClient()
    product_id = os.environ.get("APIM_PRODUCT_ID")  # 需在 secrets 或 env 里配置

    # 1. 列出所有 subscriptions
    subscriptions = apim.list_product_subscriptions(product_id)
    # print("Subscriptions:", subscriptions)
    # for sub in subscriptions:
    #     print(f"Subscription name: {getattr(sub, 'name', None)}, id: {getattr(sub, 'id', None)}")
    #     try:
    #         key = apim.get_subscription_key(sub.name)
    #         print(f"Primary key: {key}")
    #     except Exception as e:
    #         print(f"Error getting key for {getattr(sub, 'name', None)}: {e}")

    # 2. 获取所有 subscription key
    keys = [apim.get_subscription_key(sub.name) for sub in subscriptions]

    # 3. 生成 XML
    values_xml = "\n".join([f'      <value>Bearer {k}</value>' for k in keys])

    with open(TEMPLATE_PATH, encoding='utf-8') as f:
        template_content = f.read()

    policy_xml = template_content.replace('{{values}}', values_xml)
    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        f.write(policy_xml)
    print(f"Policy XML generated at {OUTPUT_PATH}")

if __name__ == "__main__":
    main()
