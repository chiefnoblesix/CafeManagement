from flask import render_template, request, flash, session, redirect, url_for
from CafeDB import *

class LogInBoundary:
    @staticmethod
    def render_login_page():
        return render_template('login.html')
        
            
class SubmitLoginB:
    def SubmitLogin():
        # return redirect(url_for('StaffBids'))
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            role = request.form['role']

            user = LogInController.get_login_from_entity(username, password, role)

            if user:
                # session['user_id'] = user.username  
                if role == 'CafeOwner':
                    return redirect(url_for('owner_home'))
                if role == 'CafeStaff':
                    return redirect(url_for('StaffBids'))  
            else:
                flash('Invalid username or password', 'error')
                return render_template('login.html')

        return render_template('login.html')
        

        

class WorkSlotBoundary:
    @staticmethod
    def render_available_work_slots():
        work_slots = WorkSlotController.get_from_entity()
        return render_template('owner_home.html', work_slots=work_slots)

    # Add methods to handle other views and user interactions

class BidsBoundary:
    @staticmethod
    def render_all_bids():
        all_bids = BidsController.get_from_entity_bids()
        return render_template('staff_bids.html', bids=all_bids)
    
class LogInController:
    def get_login_from_entity(username, password, role):
        if Login.get_login(username, password, role):
            return True
        else:
            return False
    


class WorkSlotController:
    @staticmethod
    def get_from_entity():
        return WorkSlotEntity.get_available_work_slots()

    # Add methods to create, update, and delete work slots

class BidsController:
    @staticmethod
    def get_from_entity_bids():
        return BidsEntity.get_all_bids()
    
class WorkSlotEntity:
    @staticmethod
    def get_available_work_slots():
        return WorkSlot.query.filter_by(status='Available').all()
    
    def create_workslot(shift_type, date, status):
        work_slot = WorkSlot(shiftType=shift_type, date=date, status=status)
        db.session.add(work_slot)
        db.session.commit()

    def delete_workslot(id):

        work_slot = WorkSlot.query.get(id)

        if work_slot:
            # Delete the work slot from the database
            db.session.delete(work_slot)
            db.session.commit()
            return True
        else:
            return False

        

    # Add methods to create, update, and delete work slots 

class BidsEntity:
    @staticmethod
    def get_all_bids():
        return Bids.query.filter_by(staff_user = 'John').all()
    
class Login:
    def get_login(username, password, role):
        user = Staff.query.filter_by(username=username, password=password, userRole=role).first()
        return user
    

class CreateWSBoundary:
    @staticmethod
    def render_create_ws():
        return render_template('owner_create_workslot.html')
    
class CreateRoomModalController:
    @staticmethod
    def insert_create_room():
        # Handle the creation of a room. You can access form data using request.form.
        # Use CreateRoomEntity to perform database operations.
        # You can use this method to handle form submissions and insert room data.
        pass

class CreateWorkslotBoundary:
    def create_workslot():
        shift_type = request.form.get('shift_type')
        date = request.form.get('date')
        status = 'Available'
        return CreateWorkslotC.create_workslot(shift_type, date, status)
    
class CreateWorkslotC:
    def create_workslot(shift_type, date, status):

        return WorkSlotEntity.create_workslot(shift_type, date, status)
    
class DeleteWorkslotBoundary:
    def delete_workslot(id):
        if DeleteWorkslotC.delete_workslot(id) == True:
            flash('Work Slot deleted successfully', 'success')
        else:
            flash('Work Slot not found', 'error')
        return redirect(url_for('owner_home'))
    
class DeleteWorkslotC:
    def delete_workslot(id):
        
        return WorkSlotEntity.delete_workslot(id)
        

