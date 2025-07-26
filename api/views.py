from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter, BaseFilterBackend
from django.contrib.auth import get_user_model
from django.db.models import Q, F
from core.models import (
    Service, Industry, Project, ProjectTag, Testimonial, BlogCategory, 
    BlogTag, BlogPost, Package, Lead, TeamMember, Job, JobApplication, 
    FAQ, Invoice, SiteSettings
)
from .serializers import (
    UserSerializer, ServiceSerializer, IndustrySerializer, ProjectSerializer,
    ProjectTagSerializer, TestimonialSerializer, BlogCategorySerializer,
    BlogTagSerializer, BlogPostSerializer, BlogPostListSerializer, PackageSerializer,
    LeadSerializer, LeadCreateSerializer, TeamMemberSerializer, JobSerializer,
    JobListSerializer, JobApplicationSerializer, JobApplicationCreateSerializer,
    FAQSerializer, InvoiceSerializer, SiteSettingsSerializer
)

User = get_user_model()

class AdminOnlyPermission(permissions.BasePermission):
    """Allow access only to admin users"""
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == 'admin'


class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.filter(is_active=True)
    serializer_class = ServiceSerializer
    # Use IsAuthenticatedOrReadOnly for public read and restricted write.
    # If only admins should edit, use [AdminOnlyPermission].
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['is_featured']
    search_fields = ['title', 'description']
    ordering_fields = ['order', 'title', 'created_at']
    ordering = ['order', 'title']
    lookup_field = 'slug'


class IndustryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Industry.objects.all()
    serializer_class = IndustrySerializer
    permission_classes = [permissions.AllowAny]

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.filter(is_published=True)
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['industry', 'is_featured']
    search_fields = ['title', 'description', 'client_name']
    ordering_fields = ['created_at', 'title']
    ordering = ['-created_at']
    lookup_field = 'slug'

class ProjectTagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ProjectTag.objects.all()
    serializer_class = ProjectTagSerializer
    permission_classes = [permissions.AllowAny]

class TestimonialViewSet(viewsets.ModelViewSet):
    queryset = Testimonial.objects.filter(is_published=True)
    serializer_class = TestimonialSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['is_featured', 'rating']
    ordering_fields = ['created_at', 'rating']
    ordering = ['-created_at']

class BlogCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = BlogCategory.objects.all()
    serializer_class = BlogCategorySerializer
    permission_classes = [permissions.AllowAny]

class BlogTagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = BlogTag.objects.all()
    serializer_class = BlogTagSerializer
    permission_classes = [permissions.AllowAny]

class BlogPostViewSet(viewsets.ModelViewSet):
    queryset = BlogPost.objects.filter(is_published=True)
    serializer_class = BlogPostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['category', 'tags', 'is_featured']
    search_fields = ['title', 'content', 'excerpt']
    ordering_fields = ['published_at', 'views_count']
    ordering = ['-published_at']
    lookup_field = 'slug'
    
    def get_serializer_class(self):
        if self.action == 'list':
            return BlogPostListSerializer
        return BlogPostSerializer
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        # Increment view count atomically to prevent race conditions
        instance.views_count = F('views_count') + 1
        instance.save(update_fields=['views_count'])
        # Refresh the instance from the DB to get the updated value for serialization
        instance.refresh_from_db()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

class PackageViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Package.objects.filter(is_active=True)
    serializer_class = PackageSerializer
    permission_classes = [permissions.AllowAny]
    ordering = ['order', 'price']

class LeadViewSet(viewsets.ModelViewSet):
    queryset = Lead.objects.all()
    serializer_class = LeadSerializer
    permission_classes = [AdminOnlyPermission]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'source', 'interested_service']
    search_fields = ['name', 'email', 'company']
    ordering_fields = ['created_at', 'status']
    ordering = ['-created_at']

class ContactFormView(APIView):
    """Public endpoint for contact form submissions"""
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = LeadCreateSerializer(data=request.data)
        if serializer.is_valid():
            lead = serializer.save()
            # TODO: Send email notification
            return Response({
                'message': 'Thank you for your inquiry. We will get back to you soon!',
                'lead_id': lead.id
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TeamMemberViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TeamMember.objects.filter(is_active=True)
    serializer_class = TeamMemberSerializer
    permission_classes = [permissions.AllowAny]
    ordering = ['order', 'name']

class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.filter(status='open')
    serializer_class = JobSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['job_type', 'location', 'status']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'title']
    ordering = ['-created_at']
    lookup_field = 'slug'
    
    def get_serializer_class(self):
        if self.action == 'list':
            return JobListSerializer
        return JobSerializer

class JobApplicationViewSet(viewsets.ModelViewSet):
    queryset = JobApplication.objects.all()
    serializer_class = JobApplicationSerializer
    permission_classes = [AdminOnlyPermission]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'job']
    search_fields = ['name', 'email']
    ordering_fields = ['created_at', 'status']
    ordering = ['-created_at']

class JobApplicationCreateView(APIView):
    """Public endpoint for job applications"""
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = JobApplicationCreateSerializer(data=request.data)
        if serializer.is_valid():
            application = serializer.save()
            # TODO: Send email notification
            return Response({
                'message': 'Your application has been submitted successfully!',
                'application_id': application.id
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FAQViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = FAQ.objects.filter(is_active=True)
    serializer_class = FAQSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['category']
    ordering = ['order', 'question']

class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    permission_classes = [AdminOnlyPermission]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'client']
    search_fields = ['invoice_number', 'client__email']
    ordering_fields = ['created_at', 'due_date']
    ordering = ['-created_at']

class SiteSettingsView(APIView):
    """Get site settings"""
    permission_classes = [permissions.AllowAny]
    
    def get(self, request):
        # Use get_or_create for a cleaner and more atomic operation for this singleton model
        settings, created = SiteSettings.objects.get_or_create(pk=1)
        serializer = SiteSettingsSerializer(settings)
        return Response(serializer.data)

class DashboardStatsView(APIView):
    """Dashboard statistics for admin"""
    permission_classes = [AdminOnlyPermission]
    
    def get(self, request):
        stats = {
            'total_projects': Project.objects.count(),
            'active_projects': Project.objects.filter(is_published=True).count(),
            'total_leads': Lead.objects.count(),
            'new_leads': Lead.objects.filter(status='new').count(),
            'total_blog_posts': BlogPost.objects.count(),
            'published_blog_posts': BlogPost.objects.filter(is_published=True).count(),
            'total_testimonials': Testimonial.objects.count(),
            'featured_testimonials': Testimonial.objects.filter(is_featured=True).count(),
            'total_services': Service.objects.count(),
            'active_services': Service.objects.filter(is_active=True).count(),
            'total_team_members': TeamMember.objects.count(),
            'active_team_members': TeamMember.objects.filter(is_active=True).count(),
            'total_jobs': Job.objects.count(),
            'open_jobs': Job.objects.filter(status='open').count(),
            'total_applications': JobApplication.objects.count(),
            'pending_applications': JobApplication.objects.filter(status='submitted').count(),
        }
        return Response(stats)
