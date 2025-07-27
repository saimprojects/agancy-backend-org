from rest_framework import serializers
from django.conf import settings
from django.contrib.auth import get_user_model
from core.models import (
    Service, Industry, Project, ProjectImage, ProjectTag,
    Testimonial, BlogCategory, BlogTag, BlogPost, Package, Lead, TeamMember,
    Job, JobApplication, FAQ, Invoice, SiteSettings
)

User = get_user_model()

# Helper function to build full Cloudinary URL
def get_cloudinary_url(path):
    if path and not str(path).startswith('http'):
        return f"https://res.cloudinary.com/{settings.CLOUDINARY_CLOUD_NAME}/{path}"
    return path

class UserSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role', 'phone', 'company', 'avatar', 'is_verified', 'created_at']
        read_only_fields = ['id', 'created_at']

    def get_avatar(self, obj):
        return get_cloudinary_url(obj.avatar)

class ServiceSerializer(serializers.ModelSerializer):
    icon = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

    class Meta:
        model = Service
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_icon(self, obj):
        return get_cloudinary_url(obj.icon)

    def get_image(self, obj):
        return get_cloudinary_url(obj.image)

class IndustrySerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Industry
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_image(self, obj):
        return get_cloudinary_url(obj.image)

class ProjectImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = ProjectImage
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_image(self, obj):
        return get_cloudinary_url(obj.image)

class ProjectTagSerializer(serializers.ModelSerializer):
    icon = serializers.SerializerMethodField()

    class Meta:
        model = ProjectTag
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_icon(self, obj):
        return get_cloudinary_url(obj.icon)

class ProjectSerializer(serializers.ModelSerializer):
    industry_name = serializers.CharField(source='industry.name', read_only=True)
    client_email = serializers.CharField(source='client.email', read_only=True)
    tags = ProjectTagSerializer(many=True, read_only=True)
    images = ProjectImageSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']

class TestimonialSerializer(serializers.ModelSerializer):
    project_title = serializers.CharField(source='project.title', read_only=True)
    image = serializers.SerializerMethodField()

    class Meta:
        model = Testimonial
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_image(self, obj):
        return get_cloudinary_url(obj.image)

class BlogCategorySerializer(serializers.ModelSerializer):
    icon = serializers.SerializerMethodField()

    class Meta:
        model = BlogCategory
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_icon(self, obj):
        return get_cloudinary_url(obj.icon)

class BlogTagSerializer(serializers.ModelSerializer):
    icon = serializers.SerializerMethodField()

    class Meta:
        model = BlogTag
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_icon(self, obj):
        return get_cloudinary_url(obj.icon)

class BlogPostSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.get_full_name', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    tags_list = BlogTagSerializer(source='tags', many=True, read_only=True)
    featured_image = serializers.SerializerMethodField()

    class Meta:
        model = BlogPost
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at', 'views_count']

    def get_featured_image(self, obj):
        return get_cloudinary_url(obj.featured_image)

class BlogPostListSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.get_full_name', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    featured_image = serializers.SerializerMethodField()
    featured_image_thumbnail = serializers.SerializerMethodField()

    class Meta:
        model = BlogPost
        fields = [
            'id', 'title', 'slug', 'excerpt', 'featured_image', 
            'featured_image_thumbnail', 'author_name', 'category_name', 
            'published_at', 'views_count'
        ]

    def get_featured_image(self, obj):
        return get_cloudinary_url(obj.featured_image)

    def get_featured_image_thumbnail(self, obj):
        if obj.featured_image:
            return obj.featured_image.build_url(width=400, height=250, crop='fill', gravity='auto')
        return None

class PackageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Package
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_image(self, obj):
        return get_cloudinary_url(obj.image)

class LeadSerializer(serializers.ModelSerializer):
    interested_service_name = serializers.CharField(source='interested_service.title', read_only=True)
    assigned_to_name = serializers.CharField(source='assigned_to.get_full_name', read_only=True)

    class Meta:
        model = Lead
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']

class LeadCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lead
        fields = ['name', 'email', 'phone', 'company', 'message', 'interested_service', 'budget_range']

class TeamMemberSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = TeamMember
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_image(self, obj):
        return get_cloudinary_url(obj.image)

class JobSerializer(serializers.ModelSerializer):
    posted_by_name = serializers.CharField(source='posted_by.get_full_name', read_only=True)
    applications_count = serializers.SerializerMethodField()

    class Meta:
        model = Job
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_applications_count(self, obj):
        return obj.applications.count()

class JobListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = ['id', 'title', 'slug', 'job_type', 'location', 'salary_range', 'status', 'created_at']

class JobApplicationSerializer(serializers.ModelSerializer):
    job_title = serializers.CharField(source='job.title', read_only=True)
    resume = serializers.SerializerMethodField()

    class Meta:
        model = JobApplication
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_resume(self, obj):
        return get_cloudinary_url(obj.resume)

class JobApplicationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobApplication
        fields = ['job', 'name', 'email', 'phone', 'resume', 'cover_letter', 'portfolio_url']

class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']

class InvoiceSerializer(serializers.ModelSerializer):
    client_name = serializers.CharField(source='client.get_full_name', read_only=True)
    client_email = serializers.CharField(source='client.email', read_only=True)
    project_title = serializers.CharField(source='project.title', read_only=True)

    class Meta:
        model = Invoice
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']

class SiteSettingsSerializer(serializers.ModelSerializer):
    logo = serializers.SerializerMethodField()
    favicon = serializers.SerializerMethodField()

    class Meta:
        model = SiteSettings
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_logo(self, obj):
        return get_cloudinary_url(obj.logo)

    def get_favicon(self, obj):
        return get_cloudinary_url(obj.favicon)
