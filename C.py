from flask import render_template, request, flash, session, redirect, url_for
from CafeDB import *
from E import *


#Controller Classes

class LogInController:
    def get_login_from_entity(username, password, role):
        if StaffEntity.get_login(username, password, role):
            return True
        else:
            return False

class WorkSlotController:
    @staticmethod
    def get_from_entity():
        return WorkSlotEntity.get_available_work_slots()


class BidsController:
    @staticmethod
    def get_from_entity_bids():
        return BidsEntity.get_all_bids()
    
class CreateWorkslotC:
    def create_workslot(shift_type, date, status):

        return WorkSlotEntity.create_workslot(shift_type, date, status)
    

    
class DeleteWorkslotC:
    def delete_workslot(id):
        
        return WorkSlotEntity.delete_workslot(id)
        


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