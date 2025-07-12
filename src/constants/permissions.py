from enum import Enum
from typing import Dict, List, Optional

class BasePermissionEnum(str, Enum):

    def __new__(cls, value, description):
        obj = str.__new__(cls, value)
        obj._value_ = value
        obj.description = description
        return obj

    @classmethod
    def keys(cls):
        return list(cls.__members__.keys())

    @classmethod
    def values(cls):
        return [member.value for member in cls]

    @classmethod
    def descriptions(cls):
        return [member.description for member in cls]
    
    @classmethod
    def values_and_descriptions(cls):
        return [{"name": member.value, "description": member.description} for member in cls]
    
    @classmethod
    def list_only_values(cls, only: Optional[List[str]] = None):
        if only:
            return [
                member.value
                for name, member in cls.__members__.items()
                if any(filter_value.upper() in name for filter_value in only)
            ]
        return cls.values()
    
    @classmethod
    def list_except_values(cls, except_: Optional[List[str]] = None):
        if except_:
            return [
                member.value
                for name, member in cls.__members__.items()
                if all(filter_value.upper() not in name for filter_value in except_)
            ]
        return cls.values()
    
    @classmethod
    def permission_and_description_as_dict(cls) -> Dict[str, str]:
        return {member.value: member.description for member in cls}

    def __str__(self):
        return self.value

    def __repr__(self):
        return str(self)


class CategoryPermissions(BasePermissionEnum):
    CAN_CREATE_CATEGORY = ("can_create_category", "Permission to create a category")
    CAN_VIEW_CATEGORIES = ("can_view_categories", "Permission to view all categories")
    CAN_UPDATE_CATEGORY = ("can_update_category", "Permission to update a category")
    CAN_DELETE_CATEGORY = ("can_delete_category", "Permission to delete a category")


class ProductPermissions(BasePermissionEnum):
    CAN_CREATE_PRODUCT = ("can_create_product", "Permission to create a product")
    CAN_VIEW_PRODUCTS = ("can_view_products", "Permission to view all products")
    CAN_UPDATE_PRODUCT = ("can_update_product", "Permission to update a product")
    CAN_DELETE_PRODUCT = ("can_delete_product", "Permission to delete a product")


class OrderItemPermissions(BasePermissionEnum):
    CAN_CREATE_ORDER_ITEM = ("can_create_order_item", "Permission to create an order item")
    CAN_VIEW_ORDER_ITEMS = ("can_view_order_items", "Permission to view all order items")
    CAN_UPDATE_ORDER_ITEM = ("can_update_order_item", "Permission to update an order item")
    CAN_DELETE_ORDER_ITEM = ("can_delete_order_item", "Permission to delete an order item")


class OrderPermissions(BasePermissionEnum):
    CAN_CREATE_ORDER = ("can_create_order", "Permission to create an order")
    CAN_LIST_PRODUCTS_BY_ORDER_STATUS = ("can_list_products_by_order_status", "Permission to list products by order status")
    CAN_VIEW_ORDER = ("can_view_order", "Permission to view an order")
    CAN_ADD_ITEM = ("can_add_item", "Permission to add an item to an order")
    CAN_REMOVE_ITEM = ("can_remove_item", "Permission to remove an item from an order")
    CAN_CHANGE_ITEM_QUANTITY = ("can_change_item_quantity", "Permission to change the quantity of an item in an order")
    CAN_CHANGE_ITEM_OBSERVATION = ("can_change_item_observation", "Permission to change the observation of an item in an order")
    CAN_CLEAR_ORDER = ("can_clear_order", "Permission to clear an order")
    CAN_LIST_ORDER_ITEMS = ("can_list_order_items", "Permission to list all items in an order")
    CAN_CANCEL_ORDER = ("can_cancel_order", "Permission to cancel an order")
    CAN_NEXT_STEP = ("can_next_step", "Permission to go to the next step in an order")
    CAN_GO_BACK = ("can_go_back", "Permission to go back in an order")
    CAN_LIST_ORDERS = ("can_list_orders", "Permission to list all orders")


class OrderStatusPermissions(BasePermissionEnum):
    CAN_CREATE_ORDER_STATUS = ("can_create_order_status", "Permission to create an order status")
    CAN_VIEW_ORDER_STATUSES = ("can_view_order_statuses", "Permission to view all order statuses")
    CAN_UPDATE_ORDER_STATUS = ("can_update_order_status", "Permission to update an order status")
    CAN_DELETE_ORDER_STATUS = ("can_delete_order_status", "Permission to delete an order status")

class OrderPaymentPermissions(BasePermissionEnum):
    CAN_CREATE_ORDER_PAYMENT = ("can_create_order_payment", "Permission to create an order payment")
    CAN_VIEW_ORDER_PAYMENTS = ("can_view_order_payments", "Permission to view all order payments")
    CAN_UPDATE_ORDER_PAYMENT = ("can_update_order_payment", "Permission to update an order payment")
    CAN_DELETE_ORDER_PAYMENT = ("can_delete_order_payment", "Permission to delete an order payment")


class PermissionPermissions(BasePermissionEnum):
    CAN_CREATE_PERMISSION = ("can_create_permission", "Permission to create a permission")
    CAN_VIEW_PERMISSIONS = ("can_view_permissions", "Permission to view all permissions")
    CAN_UPDATE_PERMISSION = ("can_update_permission", "Permission to update a permission")
    CAN_DELETE_PERMISSION = ("can_delete_permission", "Permission to delete a permission")


class ProfilePermissions(BasePermissionEnum):
    CAN_CREATE_PROFILE = ("can_create_profile", "Permission to create a profile")
    CAN_VIEW_PROFILES = ("can_view_profiles", "Permission to view all profiles")
    CAN_UPDATE_PROFILE = ("can_update_profile", "Permission to update a profile")
    CAN_DELETE_PROFILE = ("can_delete_profile", "Permission to delete a profile")


class ProfilePermissionPermissions(BasePermissionEnum):
    CAN_CREATE_PROFILE_PERMISSION = ("can_create_profile_permission", "Permission to create a profile permission")
    CAN_VIEW_PROFILE_PERMISSIONS = ("can_view_profile_permissions", "Permission to view all profile permissions")
    CAN_UPDATE_PROFILE_PERMISSION = ("can_update_profile_permission", "Permission to update a profile permission")
    CAN_DELETE_PROFILE_PERMISSION = ("can_delete_profile_permission", "Permission to delete a profile permission")


class PaymentMethodPermissions(BasePermissionEnum):
    CAN_CREATE_PAYMENT_METHOD = ("can_create_payment_method", "Permission to create a payment method")
    CAN_VIEW_PAYMENT_METHODS = ("can_view_payment_methods", "Permission to view all payment methods")
    CAN_UPDATE_PAYMENT_METHOD = ("can_update_payment_method", "Permission to update a payment method")
    CAN_DELETE_PAYMENT_METHOD = ("can_delete_payment_method", "Permission to delete a payment method")


class PaymentPermissions(BasePermissionEnum):
    CAN_CREATE_PAYMENT = ("can_create_payment", "Permission to create a payment")
    CAN_VIEW_PAYMENTS = ("can_view_payments", "Permission to view all payments")
    CAN_UPDATE_PAYMENT = ("can_update_payment", "Permission to update a payment")
    CAN_DELETE_PAYMENT = ("can_delete_payment", "Permission to delete a payment")


class PaymentStatusPermissions(BasePermissionEnum):
    CAN_CREATE_PAYMENT_STATUS = ("can_create_payment_status", "Permission to create a payment status")
    CAN_VIEW_PAYMENT_STATUSES = ("can_view_payment_statuses", "Permission to view all payment statuses")
    CAN_UPDATE_PAYMENT_STATUS = ("can_update_payment_status", "Permission to update a payment status")
    CAN_DELETE_PAYMENT_STATUS = ("can_delete_payment_status", "Permission to delete a payment status")


class RolePermissions(BasePermissionEnum):
    CAN_CREATE_ROLE = ("can_create_role", "Permission to create a role")
    CAN_VIEW_ROLES = ("can_view_roles", "Permission to view all roles")
    CAN_UPDATE_ROLE = ("can_update_role", "Permission to update a role")
    CAN_DELETE_ROLE = ("can_delete_role", "Permission to delete a role")


class UserPermissions(BasePermissionEnum):
    CAN_CREATE_USER = ("can_create_user", "Permission to create a user")
    CAN_VIEW_USERS = ("can_view_users", "Permission to view all users")
    CAN_UPDATE_USER = ("can_update_user", "Permission to update a user")
    CAN_DELETE_USER = ("can_delete_user", "Permission to delete a user")


class UserProfilePermissions(BasePermissionEnum):
    CAN_CREATE_USER_PROFILE = ("can_create_user_profile", "Permission to create a user profile")
    CAN_VIEW_USER_PROFILES = ("can_view_user_profiles", "Permission to view all user profiles")
    CAN_UPDATE_USER_PROFILE = ("can_update_user_profile", "Permission to update a user profile")
    CAN_DELETE_USER_PROFILE = ("can_delete_user_profile", "Permission to delete a user profile")


class EmployeePermissions(BasePermissionEnum):
    CAN_CREATE_EMPLOYEE = ("can_create_employee", "Permission to create an employee")
    CAN_VIEW_EMPLOYEES = ("can_view_employees", "Permission to view all employees")
    CAN_UPDATE_EMPLOYEE = ("can_update_employee", "Permission to update an employee")
    CAN_DELETE_EMPLOYEE = ("can_delete_employee", "Permission to delete an employee")

class CustomerPermissions(BasePermissionEnum):
    CAN_CREATE_CUSTOMER = ("can_create_customer", "Permission to create a customer")
    CAN_VIEW_CUSTOMERS = ("can_view_customers", "Permission to view all customers")
    CAN_UPDATE_CUSTOMER = ("can_update_customer", "Permission to update a customer")
    CAN_DELETE_CUSTOMER = ("can_delete_customer", "Permission to delete a customer")

class PersonPermissions(BasePermissionEnum):
    CAN_CREATE_PERSON = ("can_create_person", "Permission to create a person")
    CAN_VIEW_PERSONS = ("can_view_persons", "Permission to view all persons")
    CAN_UPDATE_PERSON = ("can_update_person", "Permission to update a person")
    CAN_DELETE_PERSON = ("can_delete_person", "Permission to delete a person")
