from django.contrib import admin

from laporanhasil.models import Lhp, LhpMedia

# Register your models here.


class LhpMediaAdmin(admin.StackedInline):
    model = LhpMedia


@admin.register(Lhp)
class PostAdmin(admin.ModelAdmin):
    inlines = [LhpMediaAdmin]

    class Meta:
        model = Lhp


@admin.register(LhpMedia)
class PostImageAdmin(admin.ModelAdmin):
    pass
