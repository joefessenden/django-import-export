from django.contrib import admin

from import_export.admin import ExportActionModelAdmin, ImportExportMixin, ImportMixin, ImportExportModelAdmin
from import_export.resources import ModelResource

from .forms import CustomConfirmImportForm, CustomImportForm
from .models import Author, Book, Category, Child, EBook, Reader


class ChildAdmin(ImportMixin, admin.ModelAdmin):
    pass


class BookResource(ModelResource):

    class Meta:
        model = Book

    def for_delete(self, row, instance):
        return self.fields['name'].clean(row) == ''


class BookAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ('name', 'author', 'added')
    list_filter = ['categories', 'author']
    resource_class = BookResource


class CategoryAdmin(ExportActionModelAdmin):
    pass


class AuthorAdmin(ImportMixin, admin.ModelAdmin):
    pass


class CustomBookAdmin(BookAdmin):
    """BookAdmin with custom import forms"""

    def get_import_form(self):
        return CustomImportForm

    def get_confirm_import_form(self):
        return CustomConfirmImportForm

    def get_form_kwargs(self, form, *args, **kwargs):
        # update kwargs with authors (from CustomImportForm.cleaned_data)
        if isinstance(form, CustomImportForm):
            if form.is_valid():
                author = form.cleaned_data['author']
                kwargs.update({'author': author.id})
        return kwargs


admin.site.register(Book, BookAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Child, ChildAdmin)
admin.site.register(EBook, CustomBookAdmin)

class ReaderResource(ModelResource):
    class Meta:
        model = Reader
        exclude = ('id',)
        import_id_fields = ['reader']
        fields = (
            'reader',
            'reader_name',
        )

# Decorator Approach
#class ReaderImportExport(ImportExportModelAdmin):
#    resource_class: ReaderResource
#
#@admin.register(Reader)
#class ReservationAdmin(ReaderImportExport):
#    fields = ["reader","reader_name",]
#    #def sales_rep_full_name(self, obj):
#    #    return obj.sales_rep.get_full_name()

# Mixin Approach
class ReaderAdmin(ImportExportMixin, admin.ModelAdmin):
    resource_class = ReaderResource

admin.site.register(Reader, ReaderAdmin)