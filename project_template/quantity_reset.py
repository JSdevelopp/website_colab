from the_project import app, db
from the_project.models import Pages_info

with app.app_context():
    # Assuming you have a model named Pages_info and a column named quantity_count
    # Update rows where quantity_count is currently NULL
    db.session.query(Pages_info).filter(Pages_info.quantity_count.is_(None)).update({Pages_info.quantity_count: 10})

    # Commit the changes
    db.session.commit()


    
