from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import (
    ServiceViewSet, IndustryViewSet, ProjectViewSet, ProjectTagViewSet,
    TestimonialViewSet, BlogCategoryViewSet, BlogTagViewSet, BlogPostViewSet,
    PackageViewSet, LeadViewSet, ContactFormView, TeamMemberViewSet,
    JobViewSet, JobApplicationViewSet, JobApplicationCreateView,
    FAQViewSet, InvoiceViewSet, SiteSettingsView, DashboardStatsView
)

router = DefaultRouter()
router.register(r'services', ServiceViewSet)
router.register(r'industries', IndustryViewSet)
router.register(r'projects', ProjectViewSet)
router.register(r'project-tags', ProjectTagViewSet)
router.register(r'testimonials', TestimonialViewSet)
router.register(r'blog-categories', BlogCategoryViewSet)
router.register(r'blog-tags', BlogTagViewSet)
router.register(r'blog-posts', BlogPostViewSet)
router.register(r'packages', PackageViewSet)
router.register(r'leads', LeadViewSet)
router.register(r'team-members', TeamMemberViewSet)
router.register(r'jobs', JobViewSet)
router.register(r'job-applications', JobApplicationViewSet)
router.register(r'faqs', FAQViewSet)
router.register(r'invoices', InvoiceViewSet)

urlpatterns = [
    # Authentication
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Public endpoints
    path('contact/', ContactFormView.as_view(), name='contact_form'),
    path('apply/', JobApplicationCreateView.as_view(), name='job_application_create'),
    path('settings/', SiteSettingsView.as_view(), name='site_settings'),
    
    # Admin endpoints
    path('dashboard/stats/', DashboardStatsView.as_view(), name='dashboard_stats'),
    
    # Router URLs
    path('', include(router.urls)),
]

