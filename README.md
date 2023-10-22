# Python-MicrosoftGraphAPI
This is a basic module I have built out for python to interact with Microsoft's Graph API.

You will need to have the correct permissions added to your token in Azure to have functionality of everything in this api.

## Azure Auth Token Getter

A simple Python utility for obtaining Azure Graph API tokens.

## Description

This script provides a class, AzureAuthToken, that allows users to obtain an access token for the Graph API. This is useful for applications that need to communicate with Microsoft Azure services and require authentication.

### How to use
Initialization:

```auth_token_getter = AzureAuthToken(tenant_id, client_id, client_secret)```

Parameters:
  - tenant_id: The ID of your Azure Active Directory tenant.
  - client_id: The ID of your Azure AD app registration (application).
  - client_secret: The secret key associated with the client_id.

### Obtaining the Access Token:

After initializing the object, you can obtain the access token using:

```
token = auth_token_getter.get_access_token()
```

If the token is successfully obtained, it will be returned as a string. Otherwise, the function will print an error message and return None.
Important Notes

  - Ensure that your client_id and client_secret have the necessary permissions to obtain tokens.
  - This script assumes the default Graph API scope. If you need a different scope, you'll need to modify the data dictionary in the get_access_token method.

### Error Handling

The script prints the error status code and response text if the token retrieval process fails.


## GraphAPI: AzureAD Class for Microsoft Graph API

This class provides functionalities to interact with Microsoft's Graph API, specifically tailored to user data.

The GraphAPI class includes a schema user_schema that details the expected structure and required fields of user data in AzureAD.
Initialization

```
graph_api_instance = GraphAPI(access_token)
```

Parameters:

- access_token: The access token obtained using the AzureAuthToken class.

### Methods

#### Fetch User by ID

To get information about a user by their userID, use the fetch_user_by_id method:

```
user_data = graph_api_instance.fetch_user_by_id(user_id)
```
- user_id: The ID of the user you want to retrieve.
- Returns the user data in JSON format if successful, otherwise prints an error message and returns None.


This class provides basic error handling by printing the status code and response text if a Graph API request fails.

#### Fetch User by Email

To retrieve user details based on their email address:

```
user_data = graph_api_instance.fetch_user_by_email(email)
```
- email: Email address of the user you're looking for.
- Returns user details if found; if not, indicates no user was found with the given email.

#### Fetch User Sign-in Activity

To fetch a user's sign-in activities:

```
signin_data = graph_api_instance.fetch_user_signin_activity(user_id)
```
- user_id: The ID of the user whose sign-in activities you want to retrieve.
- Returns a list of sign-in activities for the specified user.

#### Fetch All Users

To retrieve details of all users in Office 365:

```
all_users = graph_api_instance.fetch_users_all()
```
- Returns a list containing details of all users.

#### Fetch User Licenses

To retrieve the licenses of a specific user:
```
licenses = graph_api_instance.fetch_user_licenses(user_id)
```
- user_id: The ID of the user whose licenses you want to retrieve.
- Returns the licenses associated with the specified user.

#### Fetch User Groups

To fetch all group memberships of a user:

```
user_groups = graph_api_instance.fetch_user_groups(user_id)
```
- user_id: The ID of the user whose group memberships you want to retrieve.
- Returns a list of groups the specified user is a member of.

#### Fetch All Groups

To retrieve all groups in Office 365:

```
all_groups = graph_api_instance.fetch_groups_all()
```
- Returns a list containing details of all groups.

#### Fetch Group by Name

To search and retrieve group(s) based on their display name:

```
groups = graph_api_instance.fetch_group_by_name(group_name)
```
- group_name: The display name (or part of it) of the group you're searching for.
- Returns a list of groups that match the specified name.

#### Fetch Group by Email

To retrieve a group based on its email address:

```
group_data = graph_api_instance.fetch_group_by_email(email)
```
- email: Email address of the group you're searching for.
- Returns group details if found; if not, indicates no group was found with the given email.

#### Fetch Group Membership

To fetch members of a specific group:

```
group_members = graph_api_instance.fetch_group_membership(group_id)
```
- group_id: The ID of the group whose members you want to retrieve.
- Returns a list of members associated with the specified group.

#### Fetch Available Licenses

To list all available licenses for your organization:

```
available_licenses = graph_api_instance.fetch_available_licenses()
```
- Returns a list containing details of all available licenses.

#### Create User

To create a new user in the organization:

```
new_user = graph_api_instance.user_create(user_data)
```
- user_data: A dictionary containing user details conforming to the defined user schema.
- Returns the created user's details if successful.

#### Disable User

To disable an existing user:

```
disable_status = graph_api_instance.user_disable(user_id)
```
- user_id: The ID of the user you wish to disable.
- Returns True if the user was successfully disabled, otherwise False.

#### Enable User

To enable a previously disabled user:

```
enable_status = graph_api_instance.user_enable(user_id)
```
- user_id: The ID of the user you wish to enable.
- Returns True if the user was successfully enabled, otherwise False.
16. Delete User

To delete a user from the organization:

```
delete_status = graph_api_instance.user_delete(user_id)
```
- user_id: The ID of the user you wish to delete.
- Returns True if the user was successfully deleted, otherwise False.

#### Add User to Group

To add a user to a specific group:

```
add_status = graph_api_instance.user_add_to_group(user_id, group_id)
```
- user_id: The ID of the user you wish to add to a group.
- group_id: The ID of the group you wish to add the user to.
- Returns True if the user was successfully added to the group, otherwise False.

#### Assign License to User

To assign a license to a user:

```
assign_status = graph_api_instance.user_assign_license(user_id, sku_id)
```
- user_id: The ID of the user you wish to assign the license to.
- sku_id: The SKU ID of the license.
- Returns True if the license was successfully assigned to the user, otherwise False.

#### Remove All Licenses from User

To remove all licenses from a user:

```
remove_status = graph_api_instance.user_remove_licenses(user_id)
```

- user_id: The ID of the user from whom you want to remove all licenses.
- Returns True if all licenses were successfully removed, otherwise False.

#### Set User's Usage Location

To set the usage location for a user:

```
location_status = graph_api_instance.user_set_usage_location(user_id, country_code)
```
- user_id: The ID of the user for whom you want to set the usage location.
- country_code: The country code for the user's usage location (e.g., "CA" for Canada).
- Returns True if the usage location was successfully set, otherwise False.

#### Remove User from Group

To remove a user from a specific group:

```
remove_status = graph_api_instance.user_remove_from_group(user_id, group_id)
```
- user_id: The ID of the user you wish to remove from a group.
- group_id: The ID of the group you wish to remove the user from.
- Returns True if the user was successfully removed from the group, otherwise False.
