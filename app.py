from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from BCE import *
from CafeDB import *


from flask import render_template, request

def create_app():
    app = Flask(__name__, static_url_path='/static')
    app.config['SECRET_KEY'] = 'caipng'
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///database.db"
    db.init_app(app)

    app.add_url_rule('/', 'login',view_func=LogInBoundary.render_login_page, methods=["GET","POST"])
    app.add_url_rule('/login',view_func=SubmitLoginB.SubmitLogin, methods=["POST", "GET"])
    app.add_url_rule('/StaffBids','StaffBids', view_func=BidsBoundary.render_all_bids)
    app.add_url_rule('/owner_home','owner_home', view_func=WorkSlotBoundary.render_available_work_slots)
    app.add_url_rule('/render_create_ws','render_create_ws', view_func=CreateWSBoundary.render_create_ws)
    app.add_url_rule('/render_create_ws/create_ws','create_ws', view_func=CreateWorkslotBoundary.create_workslot, methods=['POST'])
    app.add_url_rule('/owner_home/delete/<int:id>','delete_work_slot', view_func=DeleteWorkslotBoundary.delete_workslot)

    with app.app_context():
        db.drop_all()
        db.create_all()
        new_workslot = WorkSlot(
            id = 1,
            shiftType = 'AFTERNOON',
            date = '01-01-2000',
            status = 'Available',

        )

        new_role = UserRole(
            role = "CafeStaff",
        )
        new_role2 = UserRole(
            role = "CafeOwner",
        )
        new_role3 = UserRole(
            role = "CafeManager",
        )
        new_role4 = UserRole(
            role = "SystemAdmin",
        )

        new_user = Staff(
            username = "John",
            password = "John2",
            job = "Waiter",
            avail = "FT",
            userRole = new_role.role,
        )

        new_user2 = Staff(
            username = "Cena",
            password = "Cena",
            job = "Owner",
            avail = "FT",
            userRole = new_role2.role,
        )

        new_bid = Bids(
            id = 1,
            shift_id = new_workslot.id,
            shift_type = new_workslot.shiftType,
            shift_date = new_workslot.date,
            staff_user = new_user.username,
            approval = True,

        )
        
        db.session.add(new_workslot)
        db.session.add(new_role)
        db.session.add(new_role2)
        db.session.add(new_role3)
        db.session.add(new_role4)
        db.session.add(new_user)
        db.session.add(new_user2)
        db.session.add(new_bid)
        
        db.session.commit()
    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
















