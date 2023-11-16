from flask import render_template, request, flash, session, redirect, url_for, session
from CafeDB import *
from E import *
from datetime import datetime

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

class CreateProfileC:
    def create_newProfile(username, password, userRole, job, avail):
        if job is None:
            job = 'Non-Staff'
        if StaffEntity.search_profile_exist(username):
            return False
        
        return StaffEntity.create_newProfile(username, password, userRole, job, avail)
    
class EditAccountC:
    
    def edit_accC(olduser, username, password, userRole, job, avail):
        if job is None:
            job = 'Non-Staff'
        if StaffEntity.search_acc_exist(olduser):
            return StaffEntity.edit_acc(olduser, username, password, userRole, job, avail)
        else:
            return redirect(url_for('SysAdminHome'))

class EditProfileC:
    
    def edit_profileC(olduser, username, password, userRole, job, avail):
        if job is None:
            job = 'Non-Staff'
        if StaffEntity.search_profile_exist(olduser):
            return StaffEntity.edit_profile(olduser, username, password, userRole, job, avail)
        else:
            return redirect(url_for('SysAdminHome'))
        
class DeleteAccC:
    def delete_acc(delete_id):
        return StaffEntity.delete_acc(delete_id)

class DeleteProfileC:
    def delete_profile(delete_id):
        return StaffEntity.delete_profile(delete_id)
    
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


class ManagerViewC:
    
    
    def get_all_ws():
        workslots = {}
        all_workslots = WorkSlotEntity.get_all_ws()
        all_bids = BidsEntity.get_all_bids_ws()

        for workslot in all_workslots:
            status = workslot.status
            bid_count = 0  # Counter to keep track of the number of bids for the current workslot

            for bids in all_bids:
                if bids.shift_id == workslot.id:
                    bid_status = 'Awaiting Approval'

                    if bids.approval != True and bids.approval != False:
                        bid_status = 'Awaiting Approval'
                    elif bids.approval == False:
                        bid_status = 'Incomplete (R)'
                        status = 'Incomplete'
                    else:
                        bid_status = 'Complete (A)'
                        status = 'Complete (A)'

                    staff = bids.staff_user
                    shiftdate = workslot.date
                    day = datetime.strptime(shiftdate, "%Y-%m-%d").strftime('%A')  # Get the full day
                    shift_data = {
                        'shift_id': workslot.id,
                        'shift-type': workslot.shiftType,
                        'status': bid_status,
                        'name': staff,
                        'alert': workslot.status == 'Complete (A)' or workslot.status == 'Awaiting Approval',  # Alert is True when status is 'Available'
                    }

                    if day not in workslots:
                        workslots[day] = {'date': workslot.date, 'shifts': []}

                    workslots[day]['shifts'].append(shift_data)

                    # Increment the bid count
                    bid_count += 1

                    # Break out of the loop if the bid count reaches 5
            if bid_count <= 5:
                status = 'Incomplete'
            
                

            shiftdate = workslot.date
            day = datetime.strptime(shiftdate, "%Y-%m-%d").strftime('%A')  # Get the full day
            shift_data = {
                'shift_id': workslot.id,
                'shift-type': workslot.shiftType,
                'status': status,
                'name': '',
                'alert': workslot.status == 'Complete (A)' or workslot.status == 'Awaiting Approval',  # Alert is True when status is 'Available'
            }

            if day not in workslots:
                workslots[day] = {'date': workslot.date, 'shifts': []}

            workslots[day]['shifts'].append(shift_data)

        return workslots

    
    
class ManagerApproveC:
    def update_approve(id , staff):
        
        BidsEntity.update_approve_bid(id, staff)
        return WorkSlotEntity.update_approve_bid(id)
    
class ManagerRejectC:
    def reject_approve(id, staff):
        
        BidsEntity.update_reject_bid(id, staff)
        return WorkSlotEntity.update_reject_bid(id)
        
class ManagerSearchC:
    def search(query):
        workslots = {}
        all_workslots = WorkSlotEntity.get_all_ws()
        all_bids = BidsEntity.get_all_bids_ws()
        
        

        for workslot in all_workslots:
            status = workslot.status
            for bids in all_bids:
                bid_status = 'Awaiting Approval'
                if bids.shift_id == workslot.id:
                    if  bids.approval != True and bids.approval != False :
                        bid_status = 'Awaiting Approval'
                    elif bids.approval == False:
                        bid_status = 'Incomplete (R)'
                    else:
                        bid_status = 'Complete (A)'
                     
                        
                    staff = bids.staff_user
                    shiftdate = workslot.date
                    day = datetime.strptime(shiftdate, "%Y-%m-%d").strftime('%A')  # Get the full day
                    shift_data = {
                        'shift_id': workslot.id,
                        'shift-type': workslot.shiftType,
                        'status' : bid_status,
                        'name': staff,  
                        'alert': workslot.status == 'Complete (A)' or workslot.status == 'Awaiting Approval',  # Alert is True when status is 'Available'
                    }

                    if day not in workslots:
                        workslots[day] = {'date': workslot.date, 'shifts': []}

                    workslots[day]['shifts'].append(shift_data)

            shiftdate = workslot.date
            day = datetime.strptime(shiftdate, "%Y-%m-%d").strftime('%A')  # Get the full day
            shift_data = {
                'shift_id': workslot.id,
                'shift-type': workslot.shiftType,
                'status': workslot.status,
                'name': '',  
                'alert': workslot.status == 'Complete (A)' or workslot.status == 'Awaiting Approval',  # Alert is True when status is 'Available'
            }

            if day not in workslots:
                workslots[day] = {'date': workslot.date, 'shifts': []}

            workslots[day]['shifts'].append(shift_data)
                    
        search_query = request.form.get('search_query', '').strip().capitalize()
        filtered_workslots = {} 

        if search_query:
            for day, data in workslots.items():
                # Check if search_query matches day
                if (
                    search_query.lower() in day.lower() or
                    search_query in data['date']
                ):
                    filtered_workslots[day] = data
                    continue

                # Check if search_query matches any name, status, or permission in shifts
                filtered_shifts = []
                for shift in data['shifts']:
                    if (
                        search_query in shift['name'].capitalize() or
                        search_query.lower() in shift['status'].lower() or
                        search_query in shift.get('permission', '').lower() or
                        search_query in shift['shift-type'].lower()
                    ):
                        filtered_shifts.append(shift)
                        
                    elif search_query == 'Complete (A)' and shift['status'].lower() == 'Complete (A)':
                        filtered_shifts.append(shift)

                # If any shifts match the search_query, add them to the filtered_workslots
                if filtered_shifts:
                    filtered_workslots[day] = {'date': data['date'], 'shifts': filtered_shifts}

        return filtered_workslots






        # workslot_query = WorkSlotEntity.search(query)
        # bids_query = BidsEntity.search(query)
        # bids_staff_query = BidsEntity.get_all_bids(query)
        # # workslot_ids_with_bids = [bid.shift_id for bid in bids_query]
        # # compare_bids_in_ws = WorkSlotEntity.compare_id(workslot_ids_with_bids)
        # # work_slots_ = workslot_query.filter(compare_bids_in_ws).all()

        
        # if workslot_query is None:

        #     for bids in bids_staff_query:
        #         status = 'Available'
        #         if  bids.approval != True and bids.approval != False :
        #             status = 'Awaiting Approval'
        #         elif bids.approval == False:
        #             status = 'Complete (R)'
        #         else:
        #             status = 'Complete (A)'
                
                    
        #         staff = bids.staff_user
        #         shiftdate = bids.shift_date
        #         day = datetime.strptime(shiftdate, "%Y-%m-%d").strftime('%A')  # Get the full day
        #         shift_data = {
        #             'shift_id': bids.shift_id,
        #             'shift-type': bids.shift_type,
        #             'status' : status,
        #             'name': staff,  
        #             'alert': status == 'Available',  # Alert is True when status is 'Available'
        #         }

        #         if day not in workslots:
        #             workslots[day] = {'date': bids.shift_date, 'shifts': []}

        #         workslots[day]['shifts'].append(shift_data)
                    

        # else:
        #     for workslot in workslot_query:
        #         status = workslot.status
        #         for bids in bids_query:
        #             if bids.shift_id == workslot.id:
        #                 if  bids.approval != True and bids.approval != False :
        #                     status = 'Awaiting Approval'
        #                 elif bids.approval == False:
        #                     status = 'Complete (R)'
        #                 else:
        #                     status = 'Complete (A)'
                        
                            
        #                 staff = bids.staff_user
        #                 shiftdate = workslot.date
        #                 day = datetime.strptime(shiftdate, "%Y-%m-%d").strftime('%A')  # Get the full day
        #                 shift_data = {
        #                     'shift_id': workslot.id,
        #                     'shift-type': workslot.shiftType,
        #                     'status' : status,
        #                     'name': staff,  
        #                     'alert': workslot.status == 'Available',  # Alert is True when status is 'Available'
        #                 }

        #                 if day not in workslots:
        #                     workslots[day] = {'date': workslot.date, 'shifts': []}

        #                 workslots[day]['shifts'].append(shift_data)

        #             else:
        #                 shiftdate = workslot.date
        #                 day = datetime.strptime(shiftdate, "%Y-%m-%d").strftime('%A')  # Get the full day
        #                 shift_data = {
        #                     'shift_id': workslot.id,
        #                     'shift-type': workslot.shiftType,
        #                     'status': workslot.status,
        #                     'name': '',  
        #                     'alert': workslot.status == 'Available',  # Alert is True when status is 'Available'
        #                 }

        #                 if day not in workslots:
        #                     workslots[day] = {'date': workslot.date, 'shifts': []}

        #                 workslots[day]['shifts'].append(shift_data)
        # return workslots

