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


stacks_without_parents = filter(lambda stack: stack.get("ParentId") == None, stacks)
write_json_file("data/stacks.json", list(stacks_without_parents))
