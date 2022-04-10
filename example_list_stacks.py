#!/usr/bin/env python3

from boto3 import client
from json_utils import write_json_file

stacks = (
    client("cloudformation")
    .list_stacks(
        StackStatusFilter=[
            "CREATE_COMPLETE",
        ]
    )
    .get("StackSummaries")
)


def hasNoParent(stack):
    return stack.get("ParentId") == None


root_stacks = filter(hasNoParent, stacks)
write_json_file("data/stacks.json", list(root_stacks))
print("Wrote ./data/stacks.json")
