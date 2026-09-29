from db import get_connection


class QueueStorage:

    def save(self, item):
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO queue_items (item)
                    VALUES (%s)
                    """,
                    (str(item),),
                )

    def load_all(self):
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT item
                    FROM queue_items
                    ORDER BY id ASC
                    """
                )

                items = []

                for row in cursor.fetchall():
                    value = row[0]

                    try:
                        value = int(value)
                    except (ValueError, TypeError):
                        pass

                    items.append(value)

                return items

    def remove(self, item):
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    DELETE FROM queue_items
                    WHERE id = (
                        SELECT id
                        FROM queue_items
                        WHERE item = %s
                        ORDER BY id ASC
                        LIMIT 1
                    )
                    """,
                    (str(item),),
                )

    def clear(self):
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "TRUNCATE TABLE queue_items RESTART IDENTITY"
                )