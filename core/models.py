from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.core.validators import MinValueValidator, MaxValueValidator
from django_ckeditor_5.fields import CKEditor5Field
from cloudinary_storage.storage import RawMediaCloudinaryStorage
from cloudinary.models import CloudinaryField  # ✅ import Cloudinary

User = get_user_model()

class TimeStampedModel(models.Model):
    """Abstract base model with timestamp fields"""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True

        
class Service(TimeStampedModel):
    """Service model for agency services"""
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = CKEditor5Field('Text', config_name='default')
    short_description = models.CharField(max_length=300)
    icon = CloudinaryField('image', upload_to='services/icons/', blank=True, null=True)
    image = CloudinaryField('image', upload_to='services/images/', blank=True, null=True)
    price_starting_from = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    
    # SEO fields
    meta_title = models.CharField(max_length=60, blank=True)
    meta_description = models.CharField(max_length=160, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['order', 'title']

class Industry(TimeStampedModel):
    """Industry model for project categorization"""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'Industries'

class Project(TimeStampedModel):
    """Project/Case Study model"""
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = CKEditor5Field('Text', config_name='default')
    short_description = models.CharField(max_length=300)
    tags = models.ManyToManyField('ProjectTag', blank=True, related_name='projects')
    industry = models.ForeignKey(Industry, on_delete=models.SET_NULL, null=True, blank=True)
    client = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='projects')
    client_name = models.CharField(max_length=200)
    
    # Project details
    project_url = models.URLField(blank=True, null=True)
    duration_months = models.PositiveIntegerField(blank=True, null=True)
    team_size = models.PositiveIntegerField(blank=True, null=True)
    
    # Before/After KPIs
    before_traffic = models.PositiveIntegerField(blank=True, null=True, help_text="Monthly traffic before")
    after_traffic = models.PositiveIntegerField(blank=True, null=True, help_text="Monthly traffic after")
    before_conversion = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, help_text="Conversion rate before (%)")
    after_conversion = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, help_text="Conversion rate after (%)")
    before_revenue = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True, help_text="Monthly revenue before")
    after_revenue = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True, help_text="Monthly revenue after")
    
    # Media
    featured_image = CloudinaryField('image', upload_to='projects/featured/', blank=True, null=True)
    video_url = models.URLField(blank=True, null=True)
    
    # Status
    is_featured = models.BooleanField(default=False)
    is_published = models.BooleanField(default=False)
    
    # SEO fields
    meta_title = models.CharField(max_length=60, blank=True)
    meta_description = models.CharField(max_length=160, blank=True)
    
    def save(self, *args, **kwargs):
        if self.client and not self.client_name:
            self.client_name = self.client.get_full_name()
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-created_at']

class ProjectImage(TimeStampedModel):
    """Additional images for projects"""
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='images')
    image = CloudinaryField('image', upload_to='projects/gallery/')
    caption = models.CharField(max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order']

class ProjectTag(TimeStampedModel):
    """Tags for projects"""
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Testimonial(TimeStampedModel):
    """Client testimonials"""
    name = models.CharField(max_length=100)
    company = models.CharField(max_length=100, blank=True)
    testimonial_text = CKEditor5Field('Text', config_name='default')
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        default=5
    )
    photo = CloudinaryField('image', upload_to='testimonials/', blank=True, null=True)
    company_logo = CloudinaryField('image', upload_to='testimonials/logos/', blank=True, null=True)
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True, blank=True)
    is_featured = models.BooleanField(default=False)
    is_published = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.name} - {self.company}"
    
    class Meta:
        ordering = ['-created_at']

class BlogCategory(TimeStampedModel):
    """Blog post categories"""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    description = CKEditor5Field('Text', config_name='default')
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'Blog Categories'

class BlogTag(TimeStampedModel):
    """Blog post tags"""
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name

class BlogPost(TimeStampedModel):
    """Blog posts"""
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    content = CKEditor5Field('Text', config_name='default')
    excerpt = models.CharField(max_length=300, blank=True)
    featured_image = CloudinaryField('image', upload_to='blog/featured/', blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    category = models.ForeignKey(BlogCategory, on_delete=models.SET_NULL, null=True, blank=True)
    tags = models.ManyToManyField(BlogTag, blank=True)
    
    # Status
    is_published = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    published_at = models.DateTimeField(blank=True, null=True)
    
    # SEO fields
    meta_title = models.CharField(max_length=60, blank=True)
    meta_description = models.CharField(max_length=160, blank=True)
    
    # Analytics
    views_count = models.PositiveIntegerField(default=0)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-published_at', '-created_at']

class Package(TimeStampedModel):
    """Pricing packages"""
    PACKAGE_TYPES = [
        ('starter', 'Starter'),
        ('growth', 'Growth'),
        ('enterprise', 'Enterprise'),
    ]
    
    name = models.CharField(max_length=100)
    package_type = models.CharField(max_length=20, choices=PACKAGE_TYPES)
    description = CKEditor5Field('Text', config_name='default')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    billing_period = models.CharField(max_length=20, default='monthly')  # monthly, yearly
    features = models.JSONField(default=list)  # List of features
    is_popular = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return f"{self.name} - ${self.price}/{self.billing_period}"
    
    class Meta:
        ordering = ['order', 'price']

class Lead(TimeStampedModel):
    """Contact form leads"""
    LEAD_STATUS = [
        ('new', 'New'),
        ('contacted', 'Contacted'),
        ('qualified', 'Qualified'),
        ('converted', 'Converted'),
        ('lost', 'Lost'),
    ]
    
    LEAD_SOURCE = [
        ('website', 'Website'),
        ('referral', 'Referral'),
        ('social_media', 'Social Media'),
        ('email', 'Email'),
        ('other', 'Other'),
    ]
    
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    company = models.CharField(max_length=100, blank=True)
    message = models.TextField()
    status = models.CharField(max_length=20, choices=LEAD_STATUS, default='new')
    source = models.CharField(max_length=20, choices=LEAD_SOURCE, default='website')
    interested_service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True, blank=True)
    budget_range = models.CharField(max_length=50, blank=True)
    
    # Follow-up
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    notes = models.TextField(blank=True)
    follow_up_date = models.DateTimeField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.name} - {self.email}"
    
    class Meta:
        ordering = ['-created_at']

class TeamMember(TimeStampedModel):
    """Team member profiles"""
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    bio = models.TextField()
    photo = CloudinaryField('image', upload_to='team/', blank=True, null=True)
    email = models.EmailField(blank=True)
    linkedin_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.name} - {self.role}"
    
    class Meta:
        ordering = ['order', 'name']

class Job(TimeStampedModel):
    """Job postings"""
    JOB_TYPES = [
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
        ('contract', 'Contract'),
        ('internship', 'Internship'),
    ]
    
    JOB_STATUS = [
        ('open', 'Open'),
        ('closed', 'Closed'),
        ('on_hold', 'On Hold'),
    ]
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = CKEditor5Field('Text', config_name='default')
    requirements = models.TextField()
    job_type = models.CharField(max_length=20, choices=JOB_TYPES)
    location = models.CharField(max_length=100)
    salary_range = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=20, choices=JOB_STATUS, default='open')
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-created_at']

class JobApplication(TimeStampedModel):
    """Job applications"""
    APPLICATION_STATUS = [
        ('submitted', 'Submitted'),
        ('reviewing', 'Under Review'),
        ('shortlisted', 'Shortlisted'),
        ('interviewed', 'Interviewed'),
        ('hired', 'Hired'),
        ('rejected', 'Rejected'),
    ]
    
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    resume = models.FileField(upload_to='resumes/', storage=RawMediaCloudinaryStorage())
    cover_letter = models.TextField(blank=True)
    portfolio_url = models.URLField(blank=True)
    status = models.CharField(max_length=20, choices=APPLICATION_STATUS, default='submitted')
    notes = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.name} - {self.job.title}"
    
    class Meta:
        ordering = ['-created_at']

class FAQ(TimeStampedModel):
    """Frequently Asked Questions"""
    question = models.CharField(max_length=300)
    answer = models.TextField()
    category = models.CharField(max_length=100, blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.question
    
    class Meta:
        ordering = ['order', 'question']

class Invoice(TimeStampedModel):
    """Client invoices"""
    INVOICE_STATUS = [
        ('draft', 'Draft'),
        ('sent', 'Sent'),
        ('paid', 'Paid'),
        ('overdue', 'Overdue'),
        ('cancelled', 'Cancelled'),
    ]
    
    invoice_number = models.CharField(max_length=50, unique=True)
    client = models.ForeignKey(User, on_delete=models.PROTECT, related_name='invoices')
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
    description = CKEditor5Field('Text', config_name='default')
    due_date = models.DateField()
    status = models.CharField(max_length=20, choices=INVOICE_STATUS, default='draft')
    paid_date = models.DateTimeField(blank=True, null=True)
    
    def save(self, *args, **kwargs):
        self.total_amount = self.amount + self.tax_amount
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Invoice {self.invoice_number} - {self.client.email}"
    
    class Meta:
        ordering = ['-created_at']

class SiteSettings(TimeStampedModel):
    """Site-wide settings"""
    # Hero section
    hero_title = models.CharField(max_length=200, default="Welcome to Saim Enterprises")
    hero_subtitle = models.CharField(max_length=300, default="Your Digital Success Partner")
    hero_description = models.TextField(default="We help businesses grow with cutting-edge digital solutions.")
    hero_cta_text = models.CharField(max_length=50, default="Get Started")
    hero_cta_url = models.CharField(max_length=200, default="/contact")
    
    # Contact info
    company_name = models.CharField(max_length=100, default="Saim Enterprises")
    company_email = models.EmailField(default="info@saienterprises.com")
    company_phone = models.CharField(max_length=20, default="+1 (555) 123-4567")
    company_address = models.TextField(default="123 Business St, City, State 12345")
    
    # Social links
    facebook_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    youtube_url = models.URLField(blank=True)
    
    # 3D model settings
    model_speed = models.FloatField(default=1.0)
    model_primary_color = models.CharField(max_length=7, default="#3B82F6")
    model_secondary_color = models.CharField(max_length=7, default="#1E40AF")
    
    # SEO
    site_title = models.CharField(max_length=60, default="Saim Enterprises - Digital Agency")
    site_description = models.CharField(max_length=160, default="Professional digital agency providing web development, design, and marketing services.")
    
    class Meta:
        verbose_name = 'Site Settings'
        verbose_name_plural = 'Site Settings'
    
    def __str__(self):
        return "Site Settings"
