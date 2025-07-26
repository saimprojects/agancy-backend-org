from rest_framework import serializers
from django.contrib.auth import get_user_model
from core.models import (
    Service, Industry, Project, ProjectImage, ProjectTag,
    Testimonial, BlogCategory, BlogTag, BlogPost, Package, Lead, TeamMember,
    Job, JobApplication, FAQ, Invoice, SiteSettings
)

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role', 'phone', 'company', 'avatar', 'is_verified', 'created_at']
        read_only_fields = ['id', 'created_at']

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']

class IndustrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Industry
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']

class ProjectImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectImage
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']

class ProjectTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectTag
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']

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
    
    class Meta:
        model = Testimonial
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']

class BlogCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogCategory
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']

class BlogTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogTag
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']

class BlogPostSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.get_full_name', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    tags_list = BlogTagSerializer(source='tags', many=True, read_only=True)
    
    class Meta:
        model = BlogPost
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at', 'views_count']

class BlogPostListSerializer(serializers.ModelSerializer):
    """Simplified serializer for blog post lists"""
    author_name = serializers.CharField(source='author.get_full_name', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    
    class Meta:
        model = BlogPost
        fields = ['id', 'title', 'slug', 'excerpt', 'featured_image', 'author_name', 'category_name', 'published_at', 'views_count']

class PackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Package
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']

class LeadSerializer(serializers.ModelSerializer):
    interested_service_name = serializers.CharField(source='interested_service.title', read_only=True)
    assigned_to_name = serializers.CharField(source='assigned_to.get_full_name', read_only=True)
    
    class Meta:
        model = Lead
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']

class LeadCreateSerializer(serializers.ModelSerializer):
    """Simplified serializer for creating leads from contact form"""
    class Meta:
        model = Lead
        fields = ['name', 'email', 'phone', 'company', 'message', 'interested_service', 'budget_range']

class TeamMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamMember
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']

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
    """Simplified serializer for job listings"""
    class Meta:
        model = Job
        fields = ['id', 'title', 'slug', 'job_type', 'location', 'salary_range', 'status', 'created_at']

class JobApplicationSerializer(serializers.ModelSerializer):
    job_title = serializers.CharField(source='job.title', read_only=True)
    
    class Meta:
        model = JobApplication
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']

class JobApplicationCreateSerializer(serializers.ModelSerializer):
    """Simplified serializer for creating job applications"""
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
    class Meta:
        model = SiteSettings
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']
