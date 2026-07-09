from app.extensions import ma
from app.models import Customer


class CustomerSchema(ma.SQLAlchemyAutoSchema):
    # load_only=True means password can be sent IN, but is never
    # included when we jsonify a customer back out.
    password = ma.String(load_only=True)

    class Meta:
        model = Customer
        load_instance = True


class LoginSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Customer
        fields = ('email', 'password')  # only these two fields for login


customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many=True)
login_schema = LoginSchema()
