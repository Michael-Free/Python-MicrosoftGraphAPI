"""
Library for interacting with Microsoft Azure Graph API
"""
import json
import requests
from jsonschema import validate, ValidationError


class AzureAuthToken:
    """
    Obtaining an Graph API token
    """

    def __init__(self, tenant_id, client_id, client_secret):
        self.tenant_id = tenant_id
        self.client_id = client_id
        self.client_secret = client_secret
        self.token_url = (
            f"https://login.microsoftonline.com/{self.tenant_id}/oauth2/v2.0/token"
        )

    def get_access_token(self):
        """
        Get an API access token
        """
        data = {
            "client_id": self.client_id,
            "scope": "https://graph.microsoft.com/.default",
            "client_secret": self.client_secret,
            "grant_type": "client_credentials",
        }
        response = requests.post(self.token_url, data=data, timeout=60)
        if response.status_code == 200:
            access_token_status = json.loads(response.text)["access_token"]
        else:
            print("Error:", response.status_code, response.text)
            access_token_status = None
        return access_token_status


class GraphAPI:
    """AzureAD Class for Microsoft Graph API"""

    user_schema = {
        "type": "object",
        "properties": {
            "accountEnabled": {"type": "boolean"},
            "displayName": {"type": "string"},
            "givenName": {"type": "string"},
            "surname": {"type": "string"},
            "mailNickname": {"type": "string"},
            "userPrincipalName": {
                "type": "string",
            },
            "passwordProfile": {
                "type": "object",
                "properties": {
                    "forceChangePasswordNextSignIn": {"type": "boolean"},
                    "password": {
                        "type": "string",
                        "minLength": 8,  # Ensure password has a minimum length
                    },
                },
                "required": ["forceChangePasswordNextSignIn", "password"],
            },
        },
        "required": [
            "accountEnabled",
            "displayName",
            "givenName",
            "surname",
            "mailNickname",
            "userPrincipalName",
            "passwordProfile",
        ],
    }

    def __init__(self, access_token):
        """
        Initialize the class
        """
        # self._validate(user_schema)
        self.access_token = access_token
        self.base_api_url = "https://graph.microsoft.com/v1.0/"
        self.user_api_url = f"{self.base_api_url}users"
        self.audit_api_url = f"{self.base_api_url}auditLogs"
        self.groups_api_url = f"{self.base_api_url}/groups"
        self.directoryobjects_api_url = f"{self.base_api_url}/directoryObjects"
        self.headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
        }

    def _validate(self, data):
        """
        method to validate user json schema
        """
        try:
            validate(instance=data, schema=self.user_schema)
            return True
        except ValidationError as err_msg:
            print(f"Invalid data provided: {err_msg.message}")
            return False

    def fetch_user_by_id(self, user_id):
        """
        Fetch user information by providing userID
        """
        license_url = f"{self.user_api_url}/{user_id}"
        response = requests.get(license_url, headers=self.headers, timeout=60)
        if response.status_code == 200:
            fetch_user_status = response.json()
        else:
            print(f"Error {response.status_code}: {response.text}")
            fetch_user_status = None
        return fetch_user_status

    def fetch_user_by_email(self, email):
        """
        Fetch a user ID by providing their email address
        """
        users_url = f"{self.user_api_url}?$filter=mail eq '{email}'"
        response = requests.get(users_url, headers=self.headers, timeout=60)
        if response.status_code == 200:
            users = response.json().get("value", [])
            if users:
                fetch_email_status = users[0]
            else:
                print(f"No user found with email: {email}")
                fetch_email_status = None
        else:
            print(f"Error {response.status_code}: {response.text}")
            fetch_email_status = False
        return fetch_email_status

    def fetch_user_signin_activity(self, user_id):
        """
        Fetch a users sign-in activity by providing their user ID
        """
        activity_url = f"{self.audit_api_url}/signIns?$filter=userId eq '{user_id}'"
        response = requests.get(activity_url, headers=self.headers, timeout=60)
        if response.status_code == 200:
            activity = response.json().get("value", [])
            fetch_signin_status = activity
        else:
            print(f"Error {response.status_code}: {response.text}")
            fetch_signin_status = None
        return fetch_signin_status

    def fetch_users_all(self):
        """
        Fetch all users in o365
        """
        users_json = []
        users_url = self.user_api_url
        while users_url:
            response = requests.get(users_url, headers=self.headers, timeout=60)
            if response.status_code == 200:
                data = response.json()
                users_from_response = data.get("value", [])
                users_json.extend(users_from_response)
                users_url = data.get("@odata.nextLink", None)
            else:
                print(f"Error {response.status_code}: {response.text}")
                break
        return users_json

    def fetch_user_licenses(self, user_id):
        """
        Fetch all users o365 licenses by providing a user ID
        """
        license_url = f"{self.user_api_url}/{user_id}/licenseDetails"
        response = requests.get(license_url, headers=self.headers, timeout=60)
        if response.status_code == 200:
            fetch_user_license_status = response.json()
        else:
            print(f"Error {response.status_code}: {response.text}")
            fetch_user_license_status = None
        return fetch_user_license_status

    def fetch_user_groups(self, user_id):
        """
        Fetch all group memberships by providing a user ID
        """
        groups_url = f"{self.user_api_url}/{user_id}/memberOf"
        response = requests.get(groups_url, headers=self.headers, timeout=60)
        if response.status_code == 200:
            fetch_user_groups_status = response.json().get("value", [])
        else:
            print(f"Error {response.status_code}: {response.text}")
            fetch_user_groups_status = None
        return fetch_user_groups_status

    def fetch_groups_all(self):
        """
        Fetch all groups in o365
        """
        groups_url = f"{self.groups_api_url}"
        response = requests.get(groups_url, headers=self.headers, timeout=60)
        if response.status_code == 200:
            groups = response.json().get("value", [])
            fetch_all_groups_status = groups
        else:
            print(f"Error {response.status_code}: {response.text}")
            fetch_all_groups_status = None
        return fetch_all_groups_status

    def fetch_group_by_name(self, group_name):
        """
        Fetch groups in o365 by their display name
        """
        groups_url = (
            f"{self.groups_api_url}?$filter=startswith(displayName, '{group_name}')"
        )
        response = requests.get(groups_url, headers=self.headers, timeout=60)
        if response.status_code == 200:
            groups = response.json().get("value", [])
            fetch_group_name_status = groups
        else:
            print(f"Error {response.status_code}: {response.text}")
            fetch_group_name_status = None
        return fetch_group_name_status

    def fetch_group_by_email(self, email):
        """
        fetch a user's groups by email
        """
        groups_url = f"{self.groups_api_url}?$filter=mail eq '{email}'"
        response = requests.get(groups_url, headers=self.headers, timeout=60)
        if response.status_code == 200:
            groups = response.json().get("value", [])
            if groups:
                fetch_group_email_status = groups[
                    0
                ]  # Return the first group matching the email (should be unique)
            else:
                print(f"No group found with email: {email}")
                fetch_group_email_status = None
        else:
            print(f"Error {response.status_code}: {response.text}")
            fetch_group_email_status = False
        return fetch_group_email_status

    def fetch_group_membership(self, group_id):
        """
        fetch a user's group membership by user ID
        """
        membership_url = f"{self.groups_api_url}/{group_id}/members"
        response = requests.get(membership_url, headers=self.headers, timeout=60)
        if response.status_code == 200:
            members = response.json().get("value", [])
            fetch_group_status = members
        else:
            print(f"Error {response.status_code}: {response.text}")
            fetch_group_status = None
        return fetch_group_status

    def fetch_available_licenses(self):
        """
        Lists all available licenses (subscribed SKUs) for the organization.
        """
        license_url = f"{self.base_api_url}/subscribedSkus"
        response = requests.get(license_url, headers=self.headers, timeout=60)
        if response.status_code == 200:
            fetch_license_status = response.json().get("value", [])
        else:
            print(f"Error {response.status_code}: {response.text}")
            fetch_license_status = None
        return fetch_license_status

    def user_create(self, user_data):
        """
        create a user by passing relevant json data
        """
        is_valid_schema = self._validate(user_data)
        if not is_valid_schema:
            print("Invalid user data provided.")
            create_status = False
        else:
            users_url = f"{self.user_api_url}"
            response = requests.post(
                users_url, headers=self.headers, data=json.dumps(user_data), timeout=60
            )
            if response.status_code == 201:  # HTTP 201 means Created
                user = response.json()
                create_status = user
            else:
                print(f"Error {response.status_code}: {response.text}")
                create_status = False
        return create_status

    def user_disable(self, user_id):
        """
        Disable a user in o365 by providing their user_id
        """
        user_url = f"{self.user_api_url}/{user_id}"
        payload = {"accountEnabled": False}
        response = requests.patch(
            user_url, headers=self.headers, data=json.dumps(payload), timeout=60
        )

        if response.status_code == 204:
            disable_status = True
        else:
            print(f"Error {response.status_code}: {response.text}")
            disable_status = False
        return disable_status

    def user_enable(self, user_id):
        """
        Disable a user by providing the user_ID
        """
        user_url = f"{self.user_api_url}/{user_id}"
        payload = {"accountEnabled": True}
        response = requests.patch(
            user_url, headers=self.headers, data=json.dumps(payload), timeout=60
        )

        if response.status_code == 204:
            enable_status = True
        else:
            print(f"Error {response.status_code}: {response.text}")
            enable_status = False
        return enable_status

    def user_delete(self, user_id):
        """
        Delete a user by providing their user_id
        """
        user_url = f"{self.user_api_url}/{user_id}"
        response = requests.delete(user_url, headers=self.headers, timeout=60)

        if response.status_code == 204:
            delete_status = True
        else:
            print(f"Error {response.status_code}: {response.text}")
            delete_status = False
        return delete_status

    def user_add_to_group(self, user_id, group_id):
        """
        Add a user to a group by providing their user_id and group_id
        """
        add_member_url = f"{self.groups_api_url}/{group_id}/members/$ref"
        payload = {"@odata.id": f"{self.directoryobjects_api_url}/{user_id}"}
        response = requests.post(
            add_member_url, headers=self.headers, data=json.dumps(payload), timeout=60
        )
        if response.status_code == 204:
            user_add_status = True
        else:
            print(f"Error {response.status_code}: {response.text}")
            user_add_status = False
        return user_add_status

    def user_assign_license(self, user_id, sku_id):
        """
        Assigns a license (sku_id) to a user (user_id).
        """
        user_url = f"{self.user_api_url}/{user_id}/assignLicense"
        license_payload = {
            "addLicenses": [{"disabledPlans": [], "skuId": sku_id}],
            "removeLicenses": [],
        }
        response = requests.post(
            user_url, headers=self.headers, data=json.dumps(license_payload), timeout=60
        )
        if response.status_code == 200:
            assign_status = True
        else:
            print(f"Error assigning license {response.status_code}: {response.text}")
            assign_status = False
        return assign_status

    def user_remove_licenses(self, user_id):
        """
        Removes all licenses from a user (identified by user_id).
        """
        user_url = f"{self.user_api_url}/{user_id}/assignLicense"
        current_licenses = self.fetch_user_licenses(user_id)
        if not current_licenses["value"]:
            print("No licenses assigned to the user.")
            user_remove_status = True
        license_skus = []
        for user_license in current_licenses["value"]:
            license_skus.append(user_license["skuId"])
        removed_skus = []
        for sku in license_skus:
            license_payload = {"addLicenses": [], "removeLicenses": [sku]}
            response = requests.post(
                user_url,
                headers=self.headers,
                data=json.dumps(license_payload),
                timeout=60,
            )
            if response.status_code == 200:
                removed_skus.append(sku)
            else:
                print(
                    f"Error removing licenses {response.status_code}: {response.text}"
                )
        if not removed_skus:
            user_remove_status = False
        else:
            user_remove_status = True
        return user_remove_status

    def user_set_usage_location(self, user_id, country_code):
        """
        Sets the usage location for a user. (CA for Canada)
        """
        user_url = f"{self.user_api_url}/{user_id}"
        location_payload = {"usageLocation": country_code}
        response = requests.patch(
            user_url,
            headers=self.headers,
            data=json.dumps(location_payload),
            timeout=60,
        )
        if response.status_code == 204:
            location_status = True
        else:
            print(
                f"Error setting usage location {response.status_code}: {response.text}"
            )
            location_status = False
        return location_status

    def user_remove_from_group(self, user_id, group_id):
        """
        Removes a user from a specified group.
        """
        group_members_url = f"{self.groups_api_url}/{group_id}/members/{user_id}/$ref"
        response = requests.delete(group_members_url, headers=self.headers, timeout=60)
        if response.status_code == 204:
            remove_status = True
        else:
            print(
                f"Error removing user from group {response.status_code}: {response.text}"
            )
            remove_status = False
        return remove_status


def pretty_print(json_input):
    """print json output nicely"""
    print(json.dumps(json_input, indent=4))


def main():
    """Main test area"""
    user_data = {
        "accountEnabled": True,
        "displayName": "John Doe",
        "mailNickname": "John",
        "userPrincipalName": "john.doe@example.com",
        "passwordProfile": {
            "forceChangePasswordNextSignIn": True,
            "password": "StrongPassword123!",
        },
    }


if __name__ == "__main__":
    main()
