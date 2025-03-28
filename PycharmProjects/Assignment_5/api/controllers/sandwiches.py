from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response, Depends
from ..models import models, schemas


def create(db: Session, sandwich):
    # Create a new instance of the Sandwich model with the provided data
    db_sandwiches = models.Sandwich(
        sandwich_name=sandwich.sandwich_name,
        price=sandwich.price,
    )
    # Add the newly created Sandwich object to the database session
    db.add(db_sandwiches)
    # Commit the changes to the database
    db.commit()
    # Refresh the Sandwich object to ensure it reflects the current state in the database
    db.refresh(db_sandwiches)
    # Return the newly created Sandwich object
    return db_sandwiches


def read_all(db: Session):
    return db.query(models.Sandwich).all()


def read_one(db: Session, sandwich_id):
    return db.query(models.Sandwich).filter(models.Sandwich.id == sandwich_id).first()


def update(db: Session, sandwich_id, sandwich):
    # Query the database for the specific order to update
    db_sandwiches = db.query(models.Sandwich).filter(models.Sandwich.id == sandwich_id)
    # Extract the update data from the provided 'Sandwich' object
    update_data = sandwich.model_dump(exclude_unset=True)
    # Update the database record with the new data, without synchronizing the session
    db_sandwiches.update(update_data, synchronize_session=False)
    # Commit the changes to the database
    db.commit()
    # Return the updated Sandwich record
    return db_sandwiches.first()


def delete(db: Session, sandwich_id):
    # Query the database for the specific Sandwich to delete
    db_sandwiches = db.query(models.Sandwich).filter(models.Sandwich.id == sandwich_id)
    # Delete the database record without synchronizing the session
    db_sandwiches.delete(synchronize_session=False)
    # Commit the changes to the database
    db.commit()
    # Return a response with a status code indicating success (204 No Content)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

