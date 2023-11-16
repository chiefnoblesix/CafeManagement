from flask import render_template, request, flash, session, redirect, url_for
from CafeDB import *
from sqlalchemy import or_
from datetime import datetime

class WorkSlotEntity:
    
    def get_available_work_slots():
        return WorkSlot.query.all()
    
    def create_workslot(id, shift_type, date, status):
        workslots = WorkSlotEntity.search_workslots(shift_type, status, date)
        work_slot = WorkSlot(id=id,shiftType=shift_type, date=date, status=status)
        for w in workslots:
            if w.shiftType == work_slot.shiftType and w.date == work_slot.date:
                return False
            
        db.session.add(work_slot)
        db.session.commit()
        return True
            
    def update_ws(id, shift_type, shift_date):
        ws = WorkSlot.query.get(id)
        if ws:
            ws.shiftType = shift_type
            ws.date = shift_date
            db.session.commit()
            return True
        else:
            return False 
        
    def get_a_ws(id):
        return WorkSlot.query.filter_by(id =id).all() 

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
    
    def get_all_ws():
        return WorkSlot.query.all()
    
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
    
    def update_approve_bid(id):
        # Assuming day and shiftType are the values you want to filter on
        workslot_to_update = WorkSlot.query.filter_by(id=id).first()

        # Update the status to 'Complete (A)' if the workslot is found
        if workslot_to_update:
            workslot_to_update.status = 'Complete (A)'
            db.session.commit()
            return True  # Indicate success
        else:
            return False  # Indicate that the workslot was not found
        
    def update_reject_bid(id):
        # Assuming day and shiftType are the values you want to filter on
        workslot_to_update = WorkSlot.query.filter_by(id=id).first()

        # Update the status to 'Complete (A)' if the workslot is found
        if workslot_to_update:
            workslot_to_update.status = 'Incomplete'
            db.session.commit()
            return True  # Indicate success
        else:
            return False  # Indicate that the workslot was not found

    def search(query):
        # Query workslots based on the given parameters
        work_slots_query = WorkSlot.query.filter(
            (WorkSlot.date.ilike(f'%{query}%')) |
            (WorkSlot.shiftType.ilike(f'%{query}%'))
        )
        if work_slots_query is not None:
            return work_slots_query
        else:
            return None
    
    def compare_id(workslot_ids_with_bids):
        return WorkSlot.id.in_(workslot_ids_with_bids)



class BidsEntity:
   
    def get_all_bids(user_id):
        return Bids.query.filter_by(staff_user = user_id).all()
    
    def get_all_bids_ws():
        return Bids.query.all()
    
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
        new_bid = Bids(id=bid_id, shift_id=shift_id, shift_type=shift_type, shift_date=shift_date, staff_user=staff_user)
        db.session.add(new_bid)
        db.session.commit()
        return True


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
        
    def update_approve_bid(id, staff):
        # Assuming day, shiftType, and staff are the values you want to filter on
        bids_to_update = Bids.query.filter_by(shift_id=id, staff_user=staff).all()

        # Update the approval to True for each matched record
        for bid in bids_to_update:
            bid.approval = True

        # Commit the changes to the database
        db.session.commit()

    def update_reject_bid(id, staff):
        # Assuming day, shiftType, and staff are the values you want to filter on
        bids_to_update = Bids.query.filter_by(shift_id=id, staff_user=staff).all()

        # Update the approval to True for each matched record
        for bid in bids_to_update:
            bid.approval = False

        # Commit the changes to the database
        db.session.commit()

    def search(query):
        bids_query = Bids.query.filter(
            (Bids.shift_date.ilike(f'%{query}%')) |
            (Bids.shift_type.ilike(f'%{query}%')) |
            (Bids.staff_user.ilike(f'%{query}%'))
        )
        return bids_query


        


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

    def create_newProfile(username, password, userRole, job, avail):
        new_Profile = Staff(username=username, password=password, job=job, avail=avail, userRole=userRole)
        db.session.add(new_Profile)
        db.session.commit()
        return True
        
    def search_acc_exist(username):
        return Staff.query.filter_by(username=username).first() is not None

    def search_profile_exist(username):
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

    def edit_profile(olduser, username, password, userRole, job, avail):
        profile = Staff.query.get(olduser)
        if profile:
            profile.username = username
            profile.password = password
            profile.userRole = userRole
            profile.job = job
            profile.avail = avail
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

    def delete_profile(delete_id):
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
