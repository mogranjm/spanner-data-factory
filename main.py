import random

from google.cloud import spanner
from randomuser import RandomUser

from config import SPANNER_INSTANCE, SPANNER_DATABASE


def get_random_user() -> dict:
    user = RandomUser()

    return {
        'fname': user.get_first_name(),
        'lname': user.get_last_name(),
        'username': user.get_username(),
        'phone': user.get_phone(),
        'email': user.get_email(),
        'addr_street': user.get_street(),
        'addr_city': user.get_city(),
        'addr_state': user.get_state(),
        'addr_country': user.get_country(),
        'addr_pc': user.get_postcode(),
        'registered': user.get_registered(),
        'subscribed': random.choice([True, False])
    }


def insert_random_user(event, context):
    user = get_random_user()
    user_data = f"{hash(user['fname'] + user['lname'])}, " \
                f"'{user['fname']}', '{user['lname']}', '{user['username']}', '{user['phone']}', '{user['email']}', " \
                f"'{user['addr_street']}', '{user['addr_city']}', '{user['addr_state']}', '{user['addr_country']}', '{user['addr_pc']}', " \
                f"DATE('{user['registered']}'), {user['subscribed']}"

    wrench = spanner.Client()
    instance = wrench.instance(SPANNER_INSTANCE)
    database = instance.database(SPANNER_DATABASE)

    def insert(transaction):
        row_ct = transaction.execute_update(
            "INSERT Customers ("
            "CustomerID,"
            "fname, lname, username, phone, email, "
            "addr_street, addr_city, addr_state, addr_country, addr_pc,"
            "registered, subscribed"
            f") VALUES ({user_data});"
        )
        print(f"{row_ct} record(s) inserted.")

    database.run_in_transaction(insert)
