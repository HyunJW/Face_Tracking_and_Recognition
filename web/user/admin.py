from django.contrib import admin
from user.models import User
from attendance.models import Attendance, AcademyInfo, ClassInfo, ClassTime, UserList


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'name', 'birthdate', 'gender', 'phone_number', 'address', 'profile_picture',
                    'joined_at', 'last_login_at', 'is_superuser', 'is_active')
    list_display_links = ('id', 'email')
    exclude = ('password',)

    def joined_at(self, obj):
        return obj.date_joined.strftime("%Y-%m-%d")

    def last_login_at(self, obj):
        if not obj.last_login:
            return ''
        return obj.last_login.strftime("%Y-%m-%d %H:%M")

    joined_at.admin_order_field = '-date_joined'  # 가장 최근에 가입한 사람부터 리스팅
    joined_at.short_description = '가입일'
    last_login_at.admin_order_field = 'last_login_at'
    last_login_at.short_description = '최근로그인'


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('index', 'user', 'date', 'timestamp', 'is_entering', 'remark')
    list_display_links = ('index',)


@admin.register(AcademyInfo)
class AcademyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'address', 'tel')
    list_display_links = ('id', 'name')


@admin.register(ClassInfo)
class ClassInfoAdmin(admin.ModelAdmin):
    list_display = ('id', 'academy', 'name', 'start_date', 'end_date')
    list_display_links = ('id', 'name')


@admin.register(ClassTime)
class ClassTimeAdmin(admin.ModelAdmin):
    list_display = ('class_id', 'mon_start', 'mon_end', 'tue_start', 'tue_end', 'wed_start', 'wed_end',
                    'thu_start', 'thu_end', 'fri_start', 'fri_end', 'sat_start', 'sat_end', 'sun_start', 'sun_end')
    list_display_links = ('class_id',)


@admin.register(UserList)
class UserListAdmin(admin.ModelAdmin):
    list_display = ('student', 'class_id', 'is_teacher')
