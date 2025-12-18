from django.contrib import admin, messages
from django.urls import path
from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.core.management import call_command

# Store original get_urls to avoid recursion
_orig_get_urls = admin.site.get_urls

@staff_member_required
def delete_all_view(request):
    # Restrict to superuser only
    if not request.user.is_superuser:
        messages.error(request, "Only superusers may perform this action.")
        return redirect('admin:index')

    if request.method == 'POST':
        if request.POST.get('confirm', '').strip().lower() == 'yes':
            try:
                # Flush removes all data while keeping the schema
                call_command('flush', '--no-input')
                messages.success(request, "All data deleted (database flushed).")
            except Exception as e:
                messages.error(request, f"Error flushing database: {e}")
            return redirect('admin:index')

    return render(request, 'admin/delete_all_confirm.html', context={})


def get_urls():
    custom_urls = [
        path('delete_all/', admin.site.admin_view(delete_all_view), name='delete_all'),
    ]
    return custom_urls + _orig_get_urls()

# Monkey patch admin site to add our URL
admin.site.get_urls = get_urls
