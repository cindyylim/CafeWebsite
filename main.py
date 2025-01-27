from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean
import random
from functools import reduce
import os

app = Flask(__name__)


# CREATE DB
class Base(DeclarativeBase):
    pass


# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DB_URI", "sqlite:///cafes.db")
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# Cafe TABLE Configuration
class Cafe(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    map_url: Mapped[str] = mapped_column(String(500), nullable=False)
    img_url: Mapped[str] = mapped_column(String(500), nullable=False)
    location: Mapped[str] = mapped_column(String(250), nullable=False)
    seats: Mapped[str] = mapped_column(String(250), nullable=False)
    has_toilet: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_wifi: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_sockets: Mapped[bool] = mapped_column(Boolean, nullable=False)
    can_take_calls: Mapped[bool] = mapped_column(Boolean, nullable=False)
    coffee_price: Mapped[str] = mapped_column(String(250), nullable=True)

    def to_dict(self):
        dictionary = {column.name: getattr(self, column.name) for column in self.__table__.columns}
        return dictionary


with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/cities")
def cities():
    return render_template("cities.html")


# HTTP GET - Read Record
@app.route("/random")
def get_random_cafe():
    all_cafes = db.session.execute(db.select(Cafe)).scalars().all()
    random_cafe = random.choice(all_cafes)
    return jsonify(cafe=random_cafe.to_dict())


@app.route("/all")
def get_all_cafes():
    all_cafes = db.session.execute(db.select(Cafe).order_by(Cafe.name)).scalars().all()
    all_cafes = [cafe.to_dict() for cafe in all_cafes]
    return jsonify(cafes=all_cafes)


@app.route("/search")
def get_cafe_at_location():
    query_location = request.args.get("loc").capitalize()
    if request.args.get("has_toilet", False):
        toilet_checked = True
    else:
        toilet_checked = False
    if request.args.get("has_sockets", False):
        sockets_checked = True
    else:
        sockets_checked = False
    if request.args.get("has_wifi", False):
        wifi_checked = True
    else:
        wifi_checked = False
    if request.args.get("can_take_calls", False):
        can_take_calls_checked = True
    else:
        can_take_calls_checked = False
    result = Cafe.query.filter(Cafe.location == query_location).all()
    if toilet_checked:
        result1 = Cafe.query.filter(Cafe.has_toilet == True).all()
    else:
        result1 = result
    if sockets_checked:
        result2 = Cafe.query.filter(Cafe.has_sockets == True).all()
    else:
        result2 = result
    if wifi_checked:
        result3 = Cafe.query.filter(Cafe.has_wifi == True).all()
    else:
        result3 = result
    if can_take_calls_checked:
        result4 = Cafe.query.filter(Cafe.can_take_calls == True).all()
    else:
        result4 = result
    result5 = Cafe.query.filter(Cafe.location == query_location).all()
    all_cafes = intersect_multiple_arrays(result1, result2, result3, result4, result5)
    if all_cafes:
        all_cafes = [cafe.to_dict() for cafe in all_cafes]
        return render_template("cafe.html", location=query_location, cafes=all_cafes,
                               toilet_checked=toilet_checked, sockets_checked=sockets_checked,
                               wifi_checked=wifi_checked, can_take_calls_checked=can_take_calls_checked)
    return render_template("cafe.html", location=query_location, cafes=[],
                           toilet_checked=toilet_checked, sockets_checked=sockets_checked,
                           wifi_checked=wifi_checked, can_take_calls_checked=can_take_calls_checked)


def intersect_multiple_arrays(*arrays):
    # Use reduce to apply set intersection across all arrays
    return list(reduce(lambda x, y: set(x) & set(y), arrays))


@app.route("/suggest")
def suggest_new_place():
    return render_template("add_cafe.html")


# HTTP POST - Create Record
@app.route("/add", methods=["POST"])
def add_cafe():
    name = request.form.get("name")
    if name.strip() == "":
        return render_template("add_cafe.html",
                               error_msg="ERROR: Name is not filled out.")
    map_url = request.form.get("map_url")
    if map_url.strip() == "":
        return render_template("add_cafe.html",
                               error_msg="ERROR: Google Maps Url is not filled out.")
    img_url = request.form.get("img_url")
    if img_url.strip() == "":
        return render_template("add_cafe.html",
                               error_msg="ERROR: Image Url is not filled out.")
    location = request.form.get("loc").capitalize()
    if location.strip() == "":
        return render_template("add_cafe.html",
                               error_msg="ERROR: City is not filled out.")
    seats = request.form["seats"]
    has_toilet, has_wifi, has_sockets, can_take_calls = False, False, False, False
    if request.form.get("toilet"):
        has_toilet = True
    if request.form.get("wifi"):
        has_wifi = True
    if request.form.get("sockets"):
        has_sockets = True
    if request.form.get("calls"):
        can_take_calls = True
    coffee_price = request.form["coffee_price"]
    new_cafe = Cafe(name=name, map_url=map_url, img_url=img_url, location=location, seats=seats,
                    has_toilet=has_toilet, has_wifi=has_wifi, has_sockets=has_sockets,
                    can_take_calls=can_take_calls, coffee_price=coffee_price)
    try:
        db.session.add(new_cafe)
        db.session.commit()
    except IntegrityError:
        return render_template("add_cafe.html",
                               error_msg="ERROR: A cafe with that name already exists. Please try another cafe.")
    return jsonify(response={"success": "Successfully added the new cafe."})


# HTTP PUT/PATCH - Update Record
@app.route("/update-price/<int:cafe_id>", methods=["PATCH"])
def update_price(cafe_id):
    new_price = request.args.get("new_price")
    cafe = db.get_or_404(Cafe, cafe_id)
    if cafe:
        cafe.coffee_price = new_price
        db.session.commit()
        return jsonify(response={"success": "Successfully updated the price."}), 200
    return jsonify(error={"Not Found": "Sorry a cafe with that id was not found in the database."}), 404


# HTTP DELETE - Delete Record
@app.route("/report-closed", methods=["POST"])
def delete_cafe():
    cafe_name = request.form.get("cname")
    cafes = Cafe.query.filter(Cafe.name == cafe_name).all()
    if cafes:
        db.session.delete(cafes[0])
        db.session.commit()
        return jsonify(response={"success": "Successfully deleted the cafe."}), 200
    return jsonify(error={"Not Found": "Sorry a cafe with that id was not found in the database."}), 404


if __name__ == '__main__':
    app.run(debug=True)
