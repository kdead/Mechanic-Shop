from app.extensions import ma
from app.models import Customer


class CustomerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Customer
        load_instance = True  # allows .load() to return a real Customer object


customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many=True)
