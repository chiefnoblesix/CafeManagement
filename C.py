from flask import render_template, request, flash, session, redirect, url_for, session
from CafeDB import *
from E import *

bidID = 1
wsID = 1
#Controller Classes

class LogInController:
    def get_login_from_entity(username, password, role):
        if StaffEntity.get_login(username, password, role):
            return True
        else:
            return False

class WorkSlotController:
    
    def get_from_entity():
        return WorkSlotEntity.get_available_work_slots()


class ViewC:
    
    def get_from_entity_bids(user_id):
        return BidsEntity.get_all_bids(user_id)
    
class CreateWorkslotC:
    def create_workslot(shift_type, date, status):
        global wsID
        id = wsID
        
        if WorkSlotEntity.create_workslot(id, shift_type, date, status):
            wsID+=1
            return True
        else: 
            return False
    
class UpdateWSC:
    def get_ws_updated(id):
        ws = WorkSlotEntity.get_a_ws(id)
        return ws
    
    def update_ws(id, shiftType, date):
        return WorkSlotEntity.update_ws(id, shiftType, date)
    
class DeleteWorkslotC:
    def delete_workslot(id):
        
        return WorkSlotEntity.delete_workslot(id)
        
class OwnerSearchC:
    def search(query, status, date):
        return WorkSlotEntity.search_workslots(query, status, date)

class SysAdminViewC:
    def view_all_staff():
        return StaffEntity.view_all_staff() #List
    
class CreateAccountC:
    def create_newAcc(username, password, userRole, job, avail):
        if job is None:
            job = 'Non-Staff'
        if StaffEntity.search_acc_exist(username):
            return False
        
        return StaffEntity.create_newAcc(username, password, userRole, job, avail)
    
class EditAccountC:
    
    def edit_accC(olduser, username, password, userRole, job, avail):
        if job is None:
            job = 'Non-Staff'
        if StaffEntity.search_acc_exist(olduser):
            return StaffEntity.edit_acc(olduser, username, password, userRole, job, avail)
        else:
            return redirect(url_for('SysAdminHome'))
        
class DeleteAccC:
    def delete_acc(delete_id):
        return StaffEntity.delete_acc(delete_id)
    
class AdminSearchC:
    def search(query):
        return StaffEntity.search(query)
    

            


class DeleteBidC:
    def delete_bid(id):
        if BidsEntity.search_bid(id) is not None:

            return BidsEntity.delete_bid(id)
        
class CreateBidC:
    def get_from_entity(user_id):
        workslots = WorkSlotEntity.get_available_work_slots()
        bids = BidsEntity.get_all_bids(user_id)
        for workslot in workslots:
            for bid in bids:
                if workslot.id == bid.shift_id:
                    workslots.remove(workslot)

        return workslots
    
    def place_the_bid(slot_id):
        global bidID
        workslot = WorkSlotEntity.get_workslot(slot_id)
        if workslot:
            bid_id = bidID
            shift_id = workslot.id
            shift_type = workslot.shiftType
            shift_date = workslot.date
            staff_user = session.get('user_id')
            
            bidID += 1
            return BidsEntity.create_bid(bid_id,shift_id, shift_type, shift_date, staff_user )
        else:
            return redirect(url_for('create_bid'))
        
        
class UpdateBidC:
    def get_bid_updated(id):
        bid = BidsEntity.get_a_bid(id)
        return bid
    
    def update_bid(id, shift_type, shift_date):
        return BidsEntity.update_bid(id, shift_type, shift_date)
    
class StaffSearchC:
    def search(query, status, date):
        return WorkSlotEntity.search_workslots(query, status, date)
            
        

class StaffProfileC:
    def view_profile(username):
        return StaffEntity.view_staff(username)


    def update(username, new_job, new_avail):
        if StaffEntity.update(username, new_job, new_avail):
            return True
        else:
            return False
