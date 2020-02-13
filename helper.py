import psycopg2
import pprint


CONNECTION_STRING = (
    "postgresql://postgres:postgres@localhost/todo"  # update this path accordingly
)

NOTSTARTED = "Not Started"
INPROGRESS = "In Progress"
COMPLETED = "Completed"


def run_query(query, args=[]):
    conn = psycopg2.connect(CONNECTION_STRING)
    c = conn.cursor()
    c.execute(query, args)
    conn.commit()
    try:
        rows = c.fetchall()
    except Exception as e:
        rows = None
        print("Error: ", e)
    conn.close()
    return rows


def add_to_list(item):
    try:

        # keep the initial status as Not Started
        run_query("insert into items(item, status) values(%s,%s)", (item, NOTSTARTED))

        return {"item": item, "status": NOTSTARTED}
    except Exception as e:
        print("Error: ", e)
        return None


def get_all_items():
    # returns number of items and names of items returned by query
    try:

        rows = run_query(
            "select * from items"
        )  # returns all records; use c.fetchone() for a single item
        return {"count": len(rows), "items": rows}
    except Exception as e:
        print("Error: ", e)
        return None


def get_item(item):
    try:
        rows = run_query("select status from items where item=%s", [item])
        pprint.pprint(rows)
        status = rows[0][0]
        return status
    except Exception as e:
        print("Error: ", e)
        return None


def update_status(item, status):
    # check if the passed status is a valid value
    clean_status = status.lower().strip()
    if clean_status == "not started":
        status = NOTSTARTED
    elif clean_status == "in progress":
        status = INPROGRESS
    elif clean_status == "completed":
        status = COMPLETED
    else:
        print("Invalid Status: '%s'" % status)
        return None

    try:
        run_query("update items set status=%s where item=%s", (status, item))
        return {item: status}
    except Exception as e:
        print("Error: ", e)
        return None


def delete_item(item):
    try:
        run_query("delete from items where item=%s", (item,))
        return {"item": item}
    except Exception as e:
        print("Error: ", e)
        return None
