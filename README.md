# Python-MicrosoftGraphAPI
This is a basic module I have built out for python to interact with Microsoft's Graph API.

You will need to have the correct permissions added to your token in Azure to have functionality of everything in this api.

## Azure Auth Token Getter

A simple Python utility for obtaining Azure Graph API tokens.

## Description

This script provides a class, AzureAuthToken, that allows users to obtain an access token for the Graph API. This is useful for applications that need to communicate with Microsoft Azure services and require authentication.
Dependencies

    json
    requests
    jsonschema

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

### Future Improvements

  - Implement more comprehensive error handling.
  - Allow custom scopes to be passed as arguments.




# License
GPL
