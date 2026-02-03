from sqladmin import ModelView
from app.db.models.user import User
from app.db.models.role import Role
from app.db.models.request_log import RequestLog
from app.db.models.refresh_token import RefreshToken

class UserAdmin(ModelView, model=User):
    # Removed User.is_superuser
    column_list = [User.id, User.email, User.username, User.is_active, User.role_id, User.created_at]
    column_searchable_list = [User.email, User.username]
    column_sortable_list = [User.id, User.created_at]
    icon = "fa-solid fa-user"

class RoleAdmin(ModelView, model=Role):
    column_list = [Role.id, Role.name, Role.description]
    icon = "fa-solid fa-user-tag"

class RequestLogAdmin(ModelView, model=RequestLog):
    column_list = [RequestLog.id, RequestLog.method, RequestLog.path, RequestLog.status_code, RequestLog.timestamp]
    column_sortable_list = [RequestLog.timestamp, RequestLog.status_code]
    column_default_sort = ("timestamp", True)
    icon = "fa-solid fa-list"
    can_create = False
    can_edit = False
    can_delete = True

class TokenAdmin(ModelView, model=RefreshToken):
    column_list = [RefreshToken.id, RefreshToken.user_id, RefreshToken.expires_at, RefreshToken.is_revoked] # Changed from revoked
    icon = "fa-solid fa-key"