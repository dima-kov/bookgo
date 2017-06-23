from django.contrib import admin

from book.models import Book
from book.models import BookReading


class BookAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'owner', )
    search_fields = ('name', 'author', 'owner', )


admin.site.register(Book, BookAdmin)


class BookReadingAdmin(admin.ModelAdmin):
    list_display = ('book', 'user', 'date_start', 'date_end')


admin.site.register(BookReading, BookReadingAdmin)
