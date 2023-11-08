from flask import render_template, request, flash, session, redirect, url_for
from CafeDB import *

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


class BidsEntity:
    @staticmethod
    def get_all_bids():
        return Bids.query.filter_by(staff_user = 'John').all()


class StaffEntity:
    
    def view_all_staff():
        return Staff.query.all()
    
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