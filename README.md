# Delete Backups

These python scripts delete unnecessary backup vaults from AWS.

# Setup

- Install `python`
- Install `pip`
- Install `maws-aws-cli` (via `pip`)
- Install `boto3` (via `pip`)
- Run `$(maws)` before executing these scripts

The `$(maws)` command sets these ENVIRONMENT VARIABLES that will be used when you run the scripts:

```
AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY
AWS_SESSION_TOKEN
MAWS_PROMPT
AWS_SESSION_EXPIRATION
```

You can inspect their values by running `env | grep AWS` in your shell. If you're curious about what other environment variables are set, you can run `env` to see all of them.

# Files

example_filter_vaults.py
example_list_stacks.py
example_list_stack_owned_vaults.py
example_list_vaults.py
json_utils.py

| File                                 | What is it                                                                                                                                                                                 |
| ------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `README.md`                          | Documentation                                                                                                                                                                              |
| `example_list_vaults.py`             | Request a list of backup vaults from AWS. Save the output to a `json` file.                                                                                                                |
| `example_list_stacks.py`             | Request a list of stacks from AWS. Filter those without parents (non-nested stacks), and save those to a `json` file.                                                                      |
| `example_list_stack_owned_vaults.py` | Load a json file of stacks. Find the BackupVaultName from its resource list.                                                                                                               |
| `example_filter_vaults.py`           | Filter the list of backup vaults to delete. Do not delete vaults associated with active stacks.                                                                                            |
| `json_utils.py`                      | Provides `read_json_file` and `write_json_file`, which do what they sound like. Also resolves a problem with serializing and deserializing ISO timestamps, which we receive from AWS APIs. |
