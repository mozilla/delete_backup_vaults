# Delete Backups

These python scripts delete unnecessary backup vaults from AWS.

# Setup

- Install `python`
- Install `pip`
- Install `maws-aws-cli` (via `pip`)
- Install `boto3` (via `pip`)
- Install `termcolor` (via `pip`)
- Run `$(maws)` before executing these scripts
- Set your AWS region (Probably `us-east-1`).

## The `maws` command

The `$(maws)` command sets these ENVIRONMENT VARIABLES that will be used when you run the scripts:

```
AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY
AWS_SESSION_TOKEN
MAWS_PROMPT
AWS_SESSION_EXPIRATION
```

You can inspect their values by running `env | grep AWS` in your shell. If you're curious about what other environment variables are set, you can run `env` to see all of them.

## Configuring your default region

The `maws` command configures your environment variables with most everything you need. The last thing you need to do for these scripts is to specify a region. You can either run `export AWS_DEFAULT_REGION=us-east-1` for each terminal session, or save an AWS config file at `$HOME/.aws/config`:

```
[default]
region = us-east-1
```

# Files

|                                 File | What is it                                                                                                                                                                                 |
| -----------------------------------: | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
|                          `README.md` | Documentation                                                                                                                                                                              |
|             `example_list_vaults.py` | Request a list of backup vaults from AWS. Save the output to a `json` file.                                                                                                                |
|             `example_list_stacks.py` | Request a list of stacks from AWS. Filter those without parents (non-nested stacks), and save those to a `json` file.                                                                      |
| `example_list_stack_owned_vaults.py` | Load a json file of stacks. Find the BackupVaultName from its resource list.                                                                                                               |
|           `example_filter_vaults.py` | Filter the list of backup vaults to delete. Do not delete vaults associated with active stacks.                                                                                            |
|                      `json_utils.py` | Provides `read_json_file` and `write_json_file`, which do what they sound like. Also resolves a problem with serializing and deserializing ISO timestamps, which we receive from AWS APIs. |

# Running the examples

- Follow the setup steps above.
- Run `example_list_vaults.py`. If successful, you should see "Found N vaults." This verifies that your setup is working.
- Read `example_list_stacks.py`. Inspect the output file.
- Read `example_list_stack_owned_vaults.py`. Inspect the output file.
- Read `example_filter_vaults.py`. Inspect the output.

# What's next?

These scripts should get you started towards a solution of deleting unnecessary stacks. Before AWS lets you delete stacks, they require you to empty them. You can read the boto3 documentation to find the functions you will need to invoke.

I also encourage you to familiarize yourself with the following python topics / functions, as they are useful in a wide variety of situations, including this one:

- Python [`Dictionaries`](https://docs.python.org/3/tutorial/datastructures.html#dictionaries)
- Higher-order functions like [`map`](https://docs.python.org/3/library/functions.html#map), [`filter`](https://docs.python.org/3/library/functions.html#filter), and [`reduce`](https://docs.python.org/3/library/functools.html#functools.reduce). Each take a function and an iterable (e.g. a list) and will perform an action for each item in the list. (Note that sometimes I have to wrap these in a call to `list` so that it actually performs the action, instead of just "getting ready to perform the action".)
- The `lambda` keyword, which lets you write inline-functions.
