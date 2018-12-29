from django.contrib import admin

from book.models import Book
from book.models import BookReading
from book.models import Category
from book.models import Genre


class BookAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'owner', 'publisher', 'publishing_year', 'pages', 'amazon_link')
    search_fields = ('name', 'author', 'owner', )


admin.site.register(Book, BookAdmin)


class BookReadingAdmin(admin.ModelAdmin):
    list_display = ('book', 'user', 'status', 'date_start', 'date_end')


admin.site.register(BookReading, BookReadingAdmin)


class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', )


admin.site.register(Genre, GenreAdmin)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', )


admin.site.register(Category, CategoryAdmin)
