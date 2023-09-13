from the_project import app, db
result = db.engine.execute("SELECT 1")
print(result)