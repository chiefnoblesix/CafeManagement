from flask import render_template, request, flash, session, redirect, url_for
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
                # session['user_id'] = user.username  
                if role == 'CafeOwner':
                    return redirect(url_for('owner_home'))
                if role == 'CafeStaff':
                    return redirect(url_for('StaffBids'))  
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

class BidsBoundary:
    @staticmethod
    def render_all_bids():
        all_bids = BidsController.get_from_entity_bids()
        return render_template('staff_bids.html', bids=all_bids)


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
    


            


    





    
