from flask import render_template, request, flash, session, redirect, url_for
from CafeDB import *
from sqlalchemy import or_
from datetime import datetime

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
        
    def get_workslot(id):
        return WorkSlot.query.get(id)
    
    def search_workslots(query, status=None, date=None):
        workslots = WorkSlot.query

        if query:
            # Define your search criteria and apply case-insensitive search
            criteria = [WorkSlot.shiftType.ilike(f'%{query}%')]
            
            if status:
                criteria.append(WorkSlot.status == status)
            
            if date:
                date_obj = datetime.strptime(date, '%Y-%m-%d')
                criteria.append(WorkSlot.date == date_obj)

            # Combine criteria using OR logic
            workslots = workslots.filter(or_(*criteria))

        return workslots.all()



class BidsEntity:
    @staticmethod
    def get_all_bids(user_id):
        return Bids.query.filter_by(staff_user = user_id).all()
    
    def search_bid(bid_id):
        return Bids.query.filter_by(id=bid_id).all()
    
    def delete_bid(id):
        bid =Bids.query.get(id)
        if bid:
            db.session.delete(bid)
            db.session.commit()
            return True
        else:
            return False
        
    def create_bid(bid_id,shift_id, shift_type, shift_date, staff_user):
        
        try:
            
            # Attempt to create and commit the new bid
            new_bid = Bids(id=bid_id, shift_id=shift_id, shift_type=shift_type, shift_date=shift_date, staff_user=staff_user)
            db.session.add(new_bid)
            db.session.commit()
            return True
        except Exception as e:
            # Log the exception or print it for debugging
            
            return render_template('error.html', e=e)


    def get_a_bid(id):
        return Bids.query.filter_by(id =id).all()
    
    def update_bid(id, shift_type, shift_date):
        bid = Bids.query.get(id)
        if bid:
            bid.shift_type = shift_type
            bid.shift_date = shift_date
            db.session.commit()
            return True
        else:
            return False
        


class StaffEntity:
    
    def view_all_staff():
        return Staff.query.all()
    
    def view_staff(username):
        return Staff.query.filter_by(username=username).first()
    
    def get_login(username, password, role):
        user = Staff.query.filter_by(username=username, password=password, userRole=role).first()
        return user
    
    def create_newAcc(username, password, userRole, job, avail):
        new_Acc = Staff(username=username, password=password, job=job, avail=avail, userRole=userRole)
        db.session.add(new_Acc)
        db.session.commit()
        return True
        
    def search_acc_exist(username):
        return Staff.query.filter_by(username=username).first() is not None
        
    def edit_acc(olduser, username, password, userRole, job, avail):
        acc = Staff.query.get(olduser)
        if acc:
            acc.username = username
            acc.password = password
            acc.userRole = userRole
            acc.job = job
            acc.avail = avail
            db.session.commit()
            return True
        else:
            return False
        
    def delete_acc(delete_id):
        staff = Staff.query.get(delete_id)
        if staff:
            db.session.delete(staff)
            db.session.commit()
            return True
        else:
            return False
        
    def search(query):
        staff = Staff.query.filter(
            (Staff.username.ilike(f'%{query}%')) |  # Case-insensitive search by username
            (Staff.job.ilike(f'%{query}%')) |      # Case-insensitive search by job
            (Staff.userRole.ilike(f'%{query}%'))   # Case-insensitive search by userRole
        ).all()
        return staff
    
    def update(username, new_job, new_avail):
        staff = Staff.query.get(username)
        if staff:
            staff.job = new_job
            staff.avail = new_avail

            db.session.commit()
            return True
        else:
            return False
