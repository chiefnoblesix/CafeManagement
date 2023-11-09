from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from B import *
from CafeDB import *


from flask import render_template, request

def create_app():
    app = Flask(__name__, static_url_path='/static')
    app.config['SECRET_KEY'] = 'caipng'
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///database.db"
    db.init_app(app)


    with app.app_context():
        db.drop_all()
        db.create_all()
        app.add_url_rule('/', 'login',view_func=LogInBoundary.render_login_page, methods=["GET","POST"])
        app.add_url_rule('/login',view_func=SubmitLoginB.SubmitLogin, methods=["POST", "GET"])
        app.add_url_rule('/logout', 'logout', view_func=LogoutB.logout)

        app.add_url_rule('/StaffHome','StaffHome', view_func=StaffHomeViewB.render_staffhome)
        app.add_url_rule('/StaffHome/delete/<int:id>','delete_bid', view_func=DeleteBidB.delete_bid)
        app.add_url_rule('/CreateBid/<string:user_id>', 'create_bid', view_func=CreateBidB.render_create)
        app.add_url_rule('/Bid/<int:slot_id>', 'bid', view_func=BidB.place_bid)
        app.add_url_rule('/StaffHome/render_update/<int:update_id>', 'render_update_bid', view_func=UpdateBidB.render_update_bid)
        app.add_url_rule('/UpdateBid/<int:id>', 'update_bid', view_func=UpdateBidB.update_bid, methods=['POST'])

        app.add_url_rule('/owner_home','owner_home', view_func=WorkSlotBoundary.render_available_work_slots)
        app.add_url_rule('/render_create_ws','render_create_ws', view_func=CreateWSBoundary.render_create_ws)
        app.add_url_rule('/render_create_ws/create_ws','create_ws', view_func=CreateWSBoundary.create_workslot, methods=['POST'])
        app.add_url_rule('/owner_home/delete/<int:id>','delete_work_slot', view_func=DeleteWorkslotBoundary.delete_workslot)

        app.add_url_rule('/SysAdminHome', 'SysAdminHome', view_func=SysAdminViewB.render_sys_admin)
        app.add_url_rule('/render_createAcc', 'render_createAcc', view_func=CreateAccountB.render_create_account)
        app.add_url_rule('/render_createAcc/create_new', 'create_new', view_func=CreateAccountB.create_acc, methods=['POST'])
        app.add_url_rule('/render_editAcc/<string:id>', 'render_editAcc', view_func=EditAccountB.render_editAcc)
        app.add_url_rule('/render_editAcc/editAcc/<string:id>', 'editAcc', view_func=EditAccountB.edit_accB, methods=["GET","POST"])
        app.add_url_rule('/SysAdminHome/Delete/<string:delete_id>', 'delete_acc', view_func=DeleteAccB.delete_acc)
        app.add_url_rule('/SysAdminHome/Search', 'search_results', view_func=AdminSearchB.search)
        new_workslot = WorkSlot(
            id = 1,
            shiftType = 'AFTERNOON',
            date = '01-01-2000',
            status = 'Available',

        )
        new_workslot1 = WorkSlot(
            id = 2,
            shiftType = 'AFTERNOON',
            date = '02-01-2000',
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

        new_admin = Staff(
            username = "M",
            password = "M",
            job = "Admin",
            avail = "FT",
            userRole = new_role4.role,
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
        db.session.add(new_workslot1)
        db.session.add(new_role)
        db.session.add(new_role2)
        db.session.add(new_role3)
        db.session.add(new_role4)
        db.session.add(new_user)
        db.session.add(new_user2)
        #db.session.add(new_bid)
        db.session.add(new_admin)
        
        db.session.commit()
    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
















