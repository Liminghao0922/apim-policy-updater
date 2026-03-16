# APIM Policy Updater

This project automates the process of updating Azure API Management (APIM) policies using a GitHub Actions pipeline and Python scripts.

## Features

- List all subscriptions under a Product
- Fetch subscription keys
- Generate APIM policy XML from a template
- Automatically update APIM policy via GitHub Actions

---

## Prerequisites

- Azure Subscription
- Azure API Management instance
- Python 3.8+
- Azure AD (Entra ID) App Registration

---

## 1. Create an Entra ID (Azure AD) App Registration

1. Go to [Azure Portal > Microsoft Entra ID > App registrations](https://portal.azure.com/#view/Microsoft_AAD_RegisteredApps/ApplicationsListBlade).
2. Click **New registration**.
3. Enter a name (e.g., `apim-policy-updater`).
4. Set **Supported account types** as needed (usually "Single tenant").
5. Click **Register**.
6. After registration, note the **Application (client) ID** and **Directory (tenant) ID**.
7. Go to **Certificates & secrets** > **New client secret**. Add a description and expiration, then click **Add**. Copy the value immediately.

### Assign Role to the App

1. Go to your APIM resource in Azure Portal.
2. Click **Access control (IAM)** > **Add role assignment**.
3. Assign the role **API Management Service Contributor** (or least privilege required) to your App Registration (Service Principal).

---

## 2. GitHub Secrets Setup

In your GitHub repository, go to **Settings > Secrets and variables > Actions > New repository secret** and add the following:

- `AZURE_SUBSCRIPTION_ID`: Your Azure Subscription ID
- `AZURE_RESOURCE_GROUP`: Resource group name of your APIM
- `AZURE_APIM_NAME`: APIM instance name
- `AZURE_CLIENT_ID`: Application (client) ID from Entra ID
- `AZURE_CLIENT_SECRET`: Client secret value
- `AZURE_TENANT_ID`: Directory (tenant) ID from Entra ID
- `AZURE_APIM_API_ID`: The API ID in APIM you want to update
- `APIM_PRODUCT_ID`: The Product ID in APIM whose subscriptions you want to enumerate

---

## 3. Local Development

1. Copy `.env.example` to `.env` and fill in all required values.
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Run the policy generator:
   ```sh
   python src/generate_policy.py
   ```

---

## 4. GitHub Actions Pipeline

The workflow is defined in `.github/workflows/update-policy.yml`. On every push to `main`, it will:

- Generate the policy XML
- Update the APIM policy using the official Azure action

---

## References

- [Azure API Management documentation](https://learn.microsoft.com/en-us/azure/api-management/)
- [Azure/apim-policy-update GitHub Action](https://github.com/Azure/apim-policy-update)
- [Microsoft Entra ID documentation](https://learn.microsoft.com/en-us/azure/active-directory/)
