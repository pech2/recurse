import json
from time import sleep
from datetime import datetime
import zulip


def check_group_membership(client, target_group_name, target_emails, notify_email):
    users_result = client.get_users()
    if users_result["result"] != "success":
        print(f"Error fetching users: {users_result.get('msg')}")
        return

    email_to_id = {user["email"]: user["user_id"] for user in users_result["members"]}

    groups_result = client.get_user_groups()
    if groups_result["result"] != "success":
        print(f"Error fetching groups: {groups_result.get('msg')}")
        return

    target_group = None
    for group in groups_result["user_groups"]:
        if group["name"] == "Currently at the hub":
            target_group = group
            break

    if not target_group:
        print("Group 'Currently at the hub' not found.")
        return

    group_members = set(target_group["members"])

    found_users = []
    for email in target_emails:
        user_id = email_to_id.get(email)
        if user_id and user_id in group_members:
            found_users.append(email)

    if found_users:
        content = f"**Group Check Alert:**\nThe following users in **{target_group_name}** group are at the hub:\n"
        content += "\n".join([f"- {email}" for email in found_users])

        request = {"type": "private", "to": [notify_email], "content": content}

        response = client.send_message(request)
        if response["result"] == "success":
            print(f"DM sent successfully for '{target_group_name}'.")
        else:
            print(f"Failed to send DM: {response.get('msg')}")
    else:
        print(f"None of the specified users in '{target_group_name}' are at the hub.")


if __name__ == "__main__":
    try:
        with open("config.json", "r") as config_file:
            config = json.load(config_file)
    except FileNotFoundError:
        print("Error: config.json file not found.")
        exit(1)
    except json.JSONDecodeError:
        print("Error: config.json is not a valid JSON file.")
        exit(1)

    client = zulip.Client(config_file="zuliprc")

    notify_email = config.get("notify_email")
    groups = config.get("groups_to_check", {})

    now = datetime.now()
    now_formatted = now.strftime("%Y-%m-%d %I:%M %p")
    
    print(f"{now_formatted}: Starting script")
    for group_name, users_to_find in groups.items():
        print(f"Checking group: {group_name}...")
        check_group_membership(client, group_name, users_to_find, notify_email)

