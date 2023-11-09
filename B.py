from flask import render_template, request, flash, session, redirect, url_for, session
from CafeDB import *
from C import *


#Boundary Classes
class LogInBoundary:
    @staticmethod
    def render_login_page():
        return render_template('login.html')
    
class LogoutB:
    def logout():
        return redirect('/')


class SubmitLoginB:
    def SubmitLogin():
        # return redirect(url_for('StaffBids'))
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            role = request.form['role']
            
            user = LogInController.get_login_from_entity(username, password, role)

            if user:
                session['user_id'] = username 
                if role == 'CafeOwner':
                    return redirect(url_for('owner_home'))
                if role == 'CafeStaff':
                    return redirect(url_for('StaffHome'))  
                if role == 'SystemAdmin':
                    return redirect(url_for('SysAdminHome'))
            else:
                flash('Invalid username or password', 'error')
                return render_template('login.html')

        return render_template('login.html')

class WorkSlotBoundary:
    @staticmethod
    def render_available_work_slots():
        work_slots = WorkSlotController.get_from_entity()
        return render_template('owner_home.html', work_slots=work_slots)




class CreateWSBoundary:
    @staticmethod
    def render_create_ws():
        return render_template('owner_create_workslot.html')
    
    def create_workslot():
        shift_type = request.form.get('shift_type')
        date = request.form.get('date')
        status = 'Available'
        return CreateWorkslotC.create_workslot(shift_type, date, status)

         
class DeleteWorkslotBoundary:
    def delete_workslot(id):
        if DeleteWorkslotC.delete_workslot(id) == True:
            flash('Work Slot deleted successfully', 'success')
        else:
            flash('Work Slot not found', 'error')
        return redirect(url_for('owner_home'))
        
class SysAdminViewB:
    def render_sys_admin():
        all_staff = SysAdminViewC.view_all_staff()
        return render_template('SysADmin_home.html',all_staff=all_staff)
    
class AdminSearchB:
    def search():
        query = request.args.get('query')
        results = AdminSearchC.search(query)
        if results is not None:
            return render_template('search_results.html', query=query, results=results)
        else:
            return redirect(url_for('SysAdminHome'))
    

class CreateAccountB:
    def render_create_account():
        return render_template('newAccnt.html')
    def create_acc():
        render_template('newAccnt.html')
        username = request.form.get('username')
        password = request.form.get('password')
        userRole = request.form.get('userRole')
        job = request.form.get('job')
        avail = request.form.get('avail')
        if CreateAccountC.create_newAcc(username, password, userRole, job, avail):
            return redirect(url_for('SysAdminHome'))
        
class DeleteAccB:
    def delete_acc(delete_id):
        if DeleteAccC.delete_acc(delete_id):
            return redirect(url_for('SysAdminHome'))
        else:
            return redirect(url_for('SysAdminHome'))
        
class EditAccountB:
    
    def render_editAcc(id):
        return render_template('editAccnt.html', id=id)
        
    def edit_accB(id):
        olduser = id
       
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            userRole = request.form.get('userRole')
            job = request.form.get('job')
            avail = request.form.get('avail')
            EditAccountC.edit_accC(olduser, username, password, userRole, job, avail)
            return redirect(url_for('SysAdminHome'))
        
        else:
            return render_template('editAccnt.html', id=id)
    
class StaffHomeViewB:
    def render_staffhome():
        user_id = session.get('user_id')
        if user_id is not None:

            all_bids = ViewC.get_from_entity_bids(user_id)
            return render_template('staff_home.html', bids=all_bids)
        else:
            return redirect(url_for('/'))

class DeleteBidB:
    def delete_bid(id):
        if DeleteBidC.delete_bid(id) == True:
            flash('Bid deleted successfully', 'success')
        else:
            flash('Bid not found', 'error')
        return redirect(url_for('StaffHome'))
    
class CreateBidB:
    def render_create(user_id):
        work_slots = CreateBidC.get_from_entity(user_id)
        return render_template('staff_create_bids.html', work_slots=work_slots)
    
class BidB:
    def place_bid(slot_id):
        if BidC.place_the_bid(slot_id):
            return redirect(url_for('StaffHome'))
        else:
            return redirect(url_for('create_bid'))
        
class UpdateBidB:
    def render_update_bid(update_id):
        bid = UpdateBidC.get_bid_updated(update_id)
        return render_template('staff_update_bid.html', bid=bid)
    
    def update_bid(id):
        
        if request.method == 'POST':
            # Handle form submission, update the bid, and save it to the database
            shift_type = request.form['shift_type']
            shift_date = request.form['shift_date']
            if UpdateBidC.update_bid(id, shift_type, shift_date):
                return redirect(url_for('StaffHome'))
            else:
                return redirect(url_for('UpdateBid'))

            


        
    
        

            


    





    
