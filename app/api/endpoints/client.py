"""
Client endpoints module
"""
from typing import List
import snowflake.connector as snowflake_connector
from app.model.models import ClientBase, ClientUpdate, ClientResponse
from app.core.database import setup_snowflake_connection
from app.utils.db_helper import *
from fastapi import APIRouter, HTTPException


client_router = APIRouter(prefix="/clients", tags=["Clients"])


@client_router.post("", status_code=201, response_model=ClientResponse)
async def create_new_client(client: ClientBase):
    """
    Create a Client (POST /clients)
    """
    with setup_snowflake_connection() as db_connection:
        cursor = db_connection.cursor()
        try:
            # Check email is unique
            result = get_row_by_value(cursor, "clients", "email", client.email)
            if result:
                raise HTTPException(status_code=400, detail="Email already exists")

            # Insert client
            cursor.execute("""
                INSERT INTO clients (name, email)
                VALUES (%s, %s)
            """, (client.name, client.email))

            # Get client
            cursor.execute("""
                SELECT id, name, email, created_at
                FROM clients 
                WHERE email = %s
            """, (client.email,))

            result = cursor.fetchone()
            return ClientResponse(
                id=result[0],
                name=result[1],
                email=result[2],
                created_at=result[3]
            )
        except snowflake_connector.errors.ProgrammingError as e:
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            cursor.close()


@client_router.get("", response_model=List[ClientResponse])
async def get_all_clients():
    """
    Get All Clients (GET /clients)
    """
    with setup_snowflake_connection() as db_connection:
        cursor = db_connection.cursor()
        cursor.execute("""
            SELECT id, name, email, created_at
            FROM clients
            ORDER BY id;
        """)

        clients = []
        for row in cursor:
            clients.append(ClientResponse(
                id=row[0],
                name=row[1],
                email=row[2],
                created_at=row[3]
            ))
        cursor.close()
        return clients


@client_router.get("/{client_id}", response_model=ClientResponse)
async def get_client_by_id(client_id: int):
    """
    Get a Client by ID (GET /clients/{id})
    """
    with setup_snowflake_connection() as db_connection:
        cursor = db_connection.cursor()
        cursor.execute("""
            SELECT id, name, email, created_at
            FROM clients
            WHERE id = %s
        """, (client_id,))

        result = cursor.fetchone()
        cursor.close()

        if not result:
            raise HTTPException(status_code=404, detail="Client not found")

        return ClientResponse(
            id=result[0],
            name=result[1],
            email=result[2],
            created_at=result[3]
        )


@client_router.put("/{client_id}", response_model=ClientResponse)
async def update_client_by_id(client_id: int, client: ClientUpdate):
    """
    Update a Client (PUT /clients/{id})
    """
    with setup_snowflake_connection() as db_connection:
        cursor = db_connection.cursor()
        try:
            # Check client exists
            result = get_row_by_value(cursor, "clients", "id", client_id)
            if not result:
                raise HTTPException(status_code=404, detail="Invalid id!")

            # Validate body
            client_data = client.dict(exclude_unset=True)
            for field in client_data:
                if field.lower() == "email":
                    result = get_row_by_value(cursor, "clients", "email", client.email)
                    if result and result[0][0] != client_id:
                        raise HTTPException(status_code=400, detail="Email is taken!")

            # Update client
            update_str = ", ".join([f"{key} = '{value}'" for key, value in client.dict(exclude_unset=True).items()])
            cursor.execute(f"""
                UPDATE clients
                SET {update_str}
                WHERE id = %s
            """, (client_id,))

            # Get client
            cursor.execute("""
                SELECT id, name, email, created_at
                FROM clients
                WHERE id = %s
            """, (client_id,))

            result = cursor.fetchone()
            cursor.close()

            return ClientResponse(
                id=result[0],
                name=result[1],
                email=result[2],
                created_at=result[3]
            )
        except snowflake_connector.errors.ProgrammingError as e:
            raise HTTPException(status_code=500, detail=str(e))


@client_router.delete("/{client_id}", status_code=204)
async def delete_client_by_id(client_id: int):
    """
    Delete a Client (DELETE /clients/{id})
    """
    with setup_snowflake_connection() as db_connection:
        cursor = db_connection.cursor()

        # Check if client exists
        cursor.execute("SELECT id FROM clients WHERE id = %s", (client_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Client not found")

        # Delete client
        cursor.execute("DELETE FROM clients WHERE id = %s", (client_id,))
        cursor.close()
