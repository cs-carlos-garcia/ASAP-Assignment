from flask import Flask, render_template, request
from flask_restful import Api, Resource
from uuid import uuid4
from http import HTTPStatus
from marshmallow import (Schema, fields, validate, ValidationError)

app = Flask(__name__)
api = Api(app)


generated_ids = set()
members = dict()

class Member(Schema):
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    dob = fields.Str(required=True)
    country = fields.Str(required=True, validate=[validate.Length(equal=2)])

member_schema = Member()

class JsonEndpoint(Resource):
    def post(self):
        json_data = request.get_json()
        try:
            data = member_schema.load(json_data)
        except ValidationError as err:
            return{"messages":err.messages, "valid": err.valid_data}, HTTPStatus.BAD_REQUEST
        member_id = str(uuid4())
        generated_ids.add(member_id)
        members[member_id] = data
        print(generated_ids)
        return member_schema.dump(members[member_id]), HTTPStatus.CREATED

@app.route("/member_id/validate", methods=["GET", "POST"])
def hello_world():
    if request.method == "POST":
        if request.form["my_id"] in members:
            SUCCESS = "Received valid member id"
        else:
            SUCCESS = "Invalid member id receiveda"
        return render_template('my_form.html', my_success=SUCCESS)
    return render_template('my_form.html')

api.add_resource(JsonEndpoint, "/member_id")
api.add_resource(HtmlEndpoint, "/member_id/validate")

if __name__ == '__main__':
    app.run(debug=True)

