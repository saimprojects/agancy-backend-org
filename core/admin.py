from django.contrib import admin
from .models import (
    Service, Industry, Project, ProjectImage, ProjectTag,
    Testimonial, BlogCategory, BlogTag, BlogPost, Package, Lead, TeamMember,
    Job, JobApplication, FAQ, Invoice, SiteSettings
)

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'price_starting_from', 'is_featured', 'is_active', 'order', 'created_at')
    list_filter = ('is_featured', 'is_active', 'created_at')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}
    ordering = ('order', 'title')

@admin.register(Industry)
class IndustryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'created_at')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}

class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'client_name', 'industry', 'is_featured', 'is_published', 'created_at')
    list_filter = ('industry', 'is_featured', 'is_published', 'created_at')
    search_fields = ('title', 'client_name', 'description')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ProjectImageInline]
    filter_horizontal = ('tags',)
    ordering = ('-created_at',)

@admin.register(ProjectTag)
class ProjectTagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'created_at')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('name', 'company', 'rating', 'is_featured', 'is_published', 'created_at')
    list_filter = ('rating', 'is_featured', 'is_published', 'created_at')
    search_fields = ('name', 'company', 'testimonial_text')
    ordering = ('-created_at',)

@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'created_at')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(BlogTag)
class BlogTagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'created_at')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'is_published', 'is_featured', 'published_at', 'views_count')
    list_filter = ('category', 'tags', 'is_published', 'is_featured', 'published_at', 'created_at')
    search_fields = ('title', 'content', 'excerpt')
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('tags',)
    ordering = ('-published_at', '-created_at')

@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = ('name', 'package_type', 'price', 'billing_period', 'is_popular', 'is_active', 'order')
    list_filter = ('package_type', 'billing_period', 'is_popular', 'is_active')
    search_fields = ('name', 'description')
    ordering = ('order', 'price')

@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'company', 'status', 'source', 'assigned_to', 'created_at')
    list_filter = ('status', 'source', 'interested_service', 'assigned_to', 'created_at')
    search_fields = ('name', 'email', 'company', 'message')
    ordering = ('-created_at',)

@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'email', 'order', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'role', 'bio')
    ordering = ('order', 'name')

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'job_type', 'location', 'status', 'posted_by', 'created_at')
    list_filter = ('job_type', 'status', 'location', 'created_at')
    search_fields = ('title', 'description', 'requirements')
    prepopulated_fields = {'slug': ('title',)}
    ordering = ('-created_at',)

@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ('name', 'job', 'email', 'status', 'created_at')
    list_filter = ('status', 'job', 'created_at')
    search_fields = ('name', 'email', 'job__title')
    ordering = ('-created_at',)

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'category', 'order', 'is_active', 'created_at')
    list_filter = ('category', 'is_active', 'created_at')
    search_fields = ('question', 'answer')
    ordering = ('order', 'question')

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('invoice_number', 'client', 'total_amount', 'status', 'due_date', 'created_at')
    list_filter = ('status', 'due_date', 'created_at')
    search_fields = ('invoice_number', 'client__email', 'description')
    ordering = ('-created_at',)

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'company_email', 'updated_at')
    
    def has_add_permission(self, request):
        # Only allow one instance of SiteSettings
        return not SiteSettings.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        # Don't allow deletion of SiteSettings
        return False
