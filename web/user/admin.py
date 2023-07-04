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

    joined_at.admin_order_field = '-date_joined'
    joined_at.short_description = '가입일'
    last_login_at.admin_order_field = 'last_login_at'
    last_login_at.short_description = '최근로그인'


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('index', 'user', 'attending_date', 'attending_time', 'is_entering', 'remark')
    list_display_links = ('index',)
    
    def attending_date(self, obj):
        return obj.date.strftime("%Y-%m-%d")
    
    def attending_time(self, obj):
        return obj.timestamp.strftime("%H:%M")
    
    attending_date.admin_order_field = '-date'
    attending_date.short_description = '날짜'
    attending_time.admin_order_field = '-timestamp'
    attending_time.short_description = '시간'


@admin.register(AcademyInfo)
class AcademyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'address', 'tel')
    list_display_links = ('id', 'name')


@admin.register(ClassInfo)
class ClassInfoAdmin(admin.ModelAdmin):
    list_display = ('id', 'academy', 'name', 'starting_date', 'ending_date')
    list_display_links = ('id', 'name')

    def starting_date(self, obj):
        return obj.start_date.strftime("%Y-%m-%d")

    def ending_date(self, obj):
        if obj.end_date is None:
            return ''
        return obj.end_date.strftime("%Y-%m-%d")

    starting_date.admin_order_field = '-start_date'
    starting_date.short_description = '시작일자'
    ending_date.admin_order_field = '-end_date'
    ending_date.short_description = '종료일자'


@admin.register(ClassTime)
class ClassTimeAdmin(admin.ModelAdmin):
    list_display = ('class_id', 'monday_start', 'monday_end', 'tuesday_start', 'tuesday_end', 'wednesday_start',
                    'wednesday_end', 'thursday_start', 'thursday_end', 'friday_start', 'friday_end', 'saturday_end',
                    'saturday_end', 'sunday_start', 'sunday_end')
    list_display_links = ('class_id',)
    day_list = [['monday', 'mon', '월요일'], ['tuesday', 'tue', '화요일'], ['wednesday', 'wed', '수요일'], ['thursday', 'thu', '목요일'],
                ['friday', 'fri', '금요일'], ['saturday', 'sat', '토요일'], ['sunday', 'sun', '일요일']]
    for days in day_list:
        day = days[0]
        abb = days[1]
        word = days[2]
        day_start = f'{day}_start'
        day_end = f'{day}_end'
        abb_start = f'{abb}_start'
        abb_end = f'{abb}_end'

        def day_start(self, obj):
            if obj.abb_start is None:
                return ''
            return obj.abb_start.strftime("%H:%M")

        def day_end(self, obj):
            if obj.abb_end is None:
                return ''
            return obj.abb_end.strftime("%H:%M")

        day_start.short_description = f'{word} 시작시간'
        day_end.short_description = f'{word} 종료시간'


@admin.register(UserList)
class UserListAdmin(admin.ModelAdmin):
    list_display = ('student', 'class_id', 'is_teacher')
