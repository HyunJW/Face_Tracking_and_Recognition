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

    def monday_start(self, obj): return obj.mon_start.strftime("%H:%M")
    def monday_end(self, obj): return obj.mon_end.strftime("%H:%M")
    def tuesday_start(self, obj): return obj.tue_start.strftime("%H:%M")
    def tuesday_end(self, obj): return obj.tue_end.strftime("%H:%M")
    def wednesday_start(self, obj): return obj.wed_start.strftime("%H:%M")
    def wednesday_end(self, obj): return obj.wed_end.strftime("%H:%M")
    def thursday_start(self, obj): return obj.thu_start.strftime("%H:%M")
    def thursday_end(self, obj): return obj.thu_end.strftime("%H:%M")
    def friday_start(self, obj): return obj.fri_start.strftime("%H:%M")
    def friday_end(self, obj): return obj.fri_end.strftime("%H:%M")
    def saturday_start(self, obj): return obj.sat_start.strftime("%H:%M")
    def saturday_end(self, obj): return obj.sat_end.strftime("%H:%M")
    def sunday_start(self, obj): return obj.sun_start.strftime("%H:%M")
    def sunday_end(self, obj): return obj.sun_end.strftime("%H:%M")

    monday_start.short_description = '월요일 시작시간'
    tuesday_start.short_description = '화요일 시작시간'
    wednesday_start.short_description = '수요일 시작시간'
    thursday_start.short_description = '목요일 시작시간'
    friday_start.short_description = '금요일 시작시간'
    saturday_start.short_description = '토요일 시작시간'
    sunday_start.short_description = '일요일 시작시간'
    monday_end.short_description = '월요일 종료시간'
    tuesday_end.short_description = '화요일 종료시간'
    wednesday_end.short_description = '수월요일 종료시간'
    thursday_end.short_description = '목요일 종료시간'
    friday_end.short_description = '금요일 종료시간'
    saturday_end.short_description = '토요일 종료시간'
    sunday_end.short_description = '일요일 종료시간'


@admin.register(UserList)
class UserListAdmin(admin.ModelAdmin):
    list_display = ('student', 'class_id', 'is_teacher')
