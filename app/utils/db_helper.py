"""
DB Helper module
"""


def get_row_by_value(db_cursor, table, field_name, field_value):
    """
    get_row_by_value
    """
    db_cursor.execute(f"""
        SELECT *
        FROM {table}
        WHERE {field_name} = %s
    """, (field_value,))
    result = db_cursor.fetchall()
    return result
