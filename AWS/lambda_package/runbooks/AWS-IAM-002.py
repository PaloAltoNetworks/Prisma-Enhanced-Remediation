"""
AWS:IAM-002 Password Policy

For a pass alert, the account need to have at least the following password policy:
- MinimumPasswordLength: 14 or more
- RequireLowercaseCharacters: True
- RequireUppercaseCharacters: True
- RequireNumbers: True
- RequireNumbers: True
- MaxPasswordAge: 90 or less
- AllowUsersToChangePassword: True
- PasswordReusePrevention: 1 or more

If there's an existing password policy, the remediation script will:
- take the higher number for MinimumPasswordLength and PasswordReusePrevention
- take the lower number for MaxPasswordAge

Required permissions / Sample IAM Policy:
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "Stmt1507759700000",
      "Effect": "Allow",
      "Action": [
        "iam:UpdateAccountPasswordPolicy"
      ],
      "Resource": [
        "*"
      ]
    }
  ]
}

"""

# If set to True, no change will be made to password policy.
# If set to False, password policy will be changed
dry_run = True

def remediate(session, alert, lambda_context):
    enforced_policy = {
        'MinimumPasswordLength': 14,
        'MaxPasswordAge': 90,
        'RequireLowercaseCharacters': True,
        'RequireUppercaseCharacters': True,
        'RequireNumbers': True,
        'RequireSymbols': True,
        'AllowUsersToChangePassword': True,
        'PasswordReusePrevention': 1
    }

    # If there is an existing policy, grab the more restrictive MinimumPasswordLength, PasswordReusePrevention, and MaxPasswordAge
    if 'passwordPolicy' in alert['metadata']:
        print("current password policy", alert['metadata']['passwordPolicy'])
        current_policy = {k.lower(): v for k, v in alert['metadata']['passwordPolicy'].items()}

        for key in ['MinimumPasswordLength','PasswordReusePrevention']:
            if key.lower() in current_policy and current_policy[key.lower()] is not None:
                enforced_policy[key] = max(current_policy[key.lower()],enforced_policy[key])
        
        for key in ['MaxPasswordAge']:
            if key.lower() in current_policy and current_policy[key.lower()] is not None:
                enforced_policy[key] = min(current_policy[key.lower()],enforced_policy[key])
    else:
        current_policy = {}


    iam_client = session.client('iam')
    try:
        print("current password policy: ", current_policy)
        print('Updating account password policy with: ', enforced_policy)

        if dry_run:
            print('Dry run mode. No changes made')
            return
        else:
            resp = iam_client.update_account_password_policy(**enforced_policy)

    except Exception as e:
        raise e
    
    print('Password policy updated')
    return 
