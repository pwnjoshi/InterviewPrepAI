from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from interview.models import Resume, Profile
from interview.db_operations import insert_resume


class Command(BaseCommand):
    help = 'Create sample users and resumes for testing'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample test data...')
        
        # Sample user data
        test_users = [
            {
                'username': 'john_doe',
                'email': 'john@example.com',
                'password': 'testpass123',
                'resume_data': {
                    'username': 'john_doe',
                    'email': 'john@example.com',
                    'phone': '+1234567890',
                    'skills': ['Python', 'Django', 'JavaScript', 'React', 'SQL'],
                    'experience': 'Senior Software Engineer with 5 years of experience in web development. Proficient in Python, Django, and modern JavaScript frameworks.',
                    'education': 'Bachelor of Science in Computer Science, MIT'
                }
            },
            {
                'username': 'jane_smith',
                'email': 'jane@example.com',
                'password': 'testpass123',
                'resume_data': {
                    'username': 'jane_smith',
                    'email': 'jane@example.com',
                    'phone': '+1987654321',
                    'skills': ['Java', 'Spring', 'Microservices', 'Docker', 'Kubernetes'],
                    'experience': 'Full Stack Developer with expertise in Java ecosystem. 3 years of experience building scalable microservices.',
                    'education': 'Master of Computer Applications, Stanford University'
                }
            },
            {
                'username': 'test_beginner',
                'email': 'beginner@example.com',
                'password': 'testpass123',
                'resume_data': {
                    'username': 'test_beginner',
                    'email': 'beginner@example.com',
                    'phone': '+1122334455',
                    'skills': ['HTML', 'CSS', 'JavaScript', 'Git'],
                    'experience': 'Fresh graduate looking to start career in web development. Completed online courses in web technologies.',
                    'education': 'Bachelor of Technology in Information Technology'
                }
            }
        ]
        
        created_count = 0
        for user_data in test_users:
            # Create or get user
            user, user_created = User.objects.get_or_create(
                username=user_data['username'],
                defaults={
                    'email': user_data['email']
                }
            )
            
            if user_created:
                user.set_password(user_data['password'])
                user.save()
                self.stdout.write(self.style.SUCCESS(f'✓ Created user: {user_data["username"]}'))
                
                # Insert resume
                try:
                    result = insert_resume(user_data['resume_data'])
                    self.stdout.write(self.style.SUCCESS(f'  ✓ Created resume for {user_data["username"]}'))
                    self.stdout.write(f'    User ID: {result["user_id"]}')
                    created_count += 1
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'  ✗ Error creating resume: {e}'))
            else:
                self.stdout.write(f'  User already exists: {user_data["username"]}')
        
        self.stdout.write(self.style.SUCCESS(f'\n✅ Successfully created {created_count} test users with resumes!'))
        self.stdout.write(f'Total users: {User.objects.count()}')
        self.stdout.write(f'Total resumes: {Resume.objects.count()}')
        self.stdout.write(f'Total profiles: {Profile.objects.count()}')
        self.stdout.write('\n📝 Login credentials for all test users: password = "testpass123"')
