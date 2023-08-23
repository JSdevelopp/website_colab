from the_project import app, db
from the_project.models import Pages_info

with app.app_context():
    # Reflect the database tables
    db.reflect()

    # Choose the 'books' table to get column information for
    table = db.metadata.tables['books']

    # Iterate through the columns and print their names and data types
    for column in table.columns:
        column_name = column.name
        data_type = column.type
        print(f"Column: {column_name}, Data Type: {data_type}")

# No need to close the connection, SQLAlchemy manages connections

