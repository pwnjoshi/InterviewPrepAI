from django.core.management.base import BaseCommand
from interview.models import Question


class Command(BaseCommand):
    help = 'Populate the database with sample interview questions'

    def handle(self, *args, **options):
        self.stdout.write('Populating database with sample questions...')
        
        questions_data = [
            # Beginner Python Questions
            {
                'keywords': ['python', 'basics', 'syntax'],
                'level': 'beginner',
                'question_text': 'What is Python and why is it popular?',
                'answer': 'Python is a high-level, interpreted programming language known for its simplicity and readability. It is popular due to its easy-to-learn syntax, extensive libraries, cross-platform compatibility, and strong community support.'
            },
            {
                'keywords': ['python', 'data types', 'variables'],
                'level': 'beginner',
                'question_text': 'What are the basic data types in Python?',
                'answer': 'Python has several basic data types: int (integers), float (floating-point numbers), str (strings), bool (boolean), list, tuple, dict (dictionary), and set.'
            },
            {
                'keywords': ['python', 'list', 'tuple', 'difference'],
                'level': 'beginner',
                'question_text': 'What is the difference between a list and a tuple?',
                'answer': 'Lists are mutable (can be changed after creation) and use square brackets [], while tuples are immutable (cannot be changed) and use parentheses (). Lists have more methods and are slower than tuples.'
            },
            
            # Intermediate Python Questions
            {
                'keywords': ['python', 'oop', 'class', 'object'],
                'level': 'intermediate',
                'question_text': 'Explain Object-Oriented Programming in Python.',
                'answer': 'OOP in Python is based on classes and objects. Key concepts include: Encapsulation (bundling data and methods), Inheritance (creating new classes from existing ones), Polymorphism (using same interface for different types), and Abstraction (hiding complex implementation).'
            },
            {
                'keywords': ['python', 'decorator', 'function'],
                'level': 'intermediate',
                'question_text': 'What are decorators in Python?',
                'answer': 'Decorators are a design pattern that allows you to modify or extend the behavior of functions or methods without changing their code. They are called using the @ symbol and are essentially functions that take another function as an argument.'
            },
            {
                'keywords': ['python', 'generator', 'yield'],
                'level': 'intermediate',
                'question_text': 'What is a generator in Python?',
                'answer': 'Generators are functions that use yield instead of return to produce a series of values lazily (on-demand). They save memory by generating values one at a time rather than storing all values in memory.'
            },
            
            # Hard Python Questions
            {
                'keywords': ['python', 'gil', 'threading', 'concurrency'],
                'level': 'hard',
                'question_text': 'Explain the Global Interpreter Lock (GIL) in Python.',
                'answer': 'The GIL is a mutex that protects access to Python objects, preventing multiple threads from executing Python bytecode simultaneously. This makes Python single-threaded for CPU-bound tasks, though it allows concurrency for I/O-bound operations. Multiprocessing can bypass the GIL.'
            },
            {
                'keywords': ['python', 'metaclass', 'advanced'],
                'level': 'hard',
                'question_text': 'What are metaclasses in Python?',
                'answer': 'Metaclasses are classes of classes that define how classes behave. They control class creation and can modify class attributes, methods, or inheritance. The default metaclass is type. They are used for framework development and advanced customization.'
            },
            
            # JavaScript Questions
            {
                'keywords': ['javascript', 'closure', 'scope'],
                'level': 'intermediate',
                'question_text': 'What is a closure in JavaScript?',
                'answer': 'A closure is a function that has access to variables in its outer (enclosing) lexical scope, even after the outer function has returned. Closures are created every time a function is created and enable data privacy and factory functions.'
            },
            {
                'keywords': ['javascript', 'promise', 'async', 'await'],
                'level': 'intermediate',
                'question_text': 'Explain Promises and async/await in JavaScript.',
                'answer': 'Promises represent asynchronous operations that can be pending, fulfilled, or rejected. async/await is syntactic sugar over promises, making asynchronous code look synchronous. async functions return promises, and await pauses execution until the promise resolves.'
            },
            
            # Java Questions
            {
                'keywords': ['java', 'jvm', 'bytecode'],
                'level': 'intermediate',
                'question_text': 'How does the JVM work?',
                'answer': 'The JVM (Java Virtual Machine) executes Java bytecode. It includes: Class Loader (loads .class files), Runtime Data Area (memory management), Execution Engine (interprets/compiles bytecode), and Garbage Collector (automatic memory management). This enables platform independence.'
            },
            
            # React Questions
            {
                'keywords': ['react', 'hooks', 'state'],
                'level': 'intermediate',
                'question_text': 'What are React Hooks and why are they useful?',
                'answer': 'Hooks are functions that let you use state and other React features in functional components. Common hooks include useState (state management), useEffect (side effects), useContext (context API), and useRef (mutable references). They simplify component logic and enable code reuse.'
            },
            
            # Django Questions
            {
                'keywords': ['django', 'orm', 'models'],
                'level': 'intermediate',
                'question_text': 'Explain Django ORM and models.',
                'answer': 'Django ORM (Object-Relational Mapping) allows database interaction using Python objects instead of SQL. Models are Python classes that define database schema. The ORM provides methods like filter(), get(), create(), and supports relationships (ForeignKey, ManyToMany).'
            },
            {
                'keywords': ['django', 'middleware', 'request'],
                'level': 'intermediate',
                'question_text': 'What is Django middleware?',
                'answer': 'Middleware is a framework of hooks into Django\'s request/response processing. It\'s a lightweight plugin system for globally altering input/output. Examples include authentication, session handling, CSRF protection, and custom logging.'
            },
            
            # SQL/Database Questions
            {
                'keywords': ['sql', 'join', 'database'],
                'level': 'intermediate',
                'question_text': 'Explain different types of SQL JOINs.',
                'answer': 'SQL JOINs combine rows from multiple tables: INNER JOIN (matching rows from both tables), LEFT JOIN (all from left + matching from right), RIGHT JOIN (all from right + matching from left), FULL OUTER JOIN (all rows from both tables), and CROSS JOIN (cartesian product).'
            },
            
            # Data Structures Questions
            {
                'keywords': ['algorithm', 'time complexity', 'big o'],
                'level': 'intermediate',
                'question_text': 'Explain Big O notation and common time complexities.',
                'answer': 'Big O describes algorithm performance as input size grows. Common complexities: O(1) constant, O(log n) logarithmic, O(n) linear, O(n log n) linearithmic, O(n²) quadratic, O(2^n) exponential. It helps evaluate algorithm efficiency and scalability.'
            },
            
            # Git Questions
            {
                'keywords': ['git', 'version control', 'merge'],
                'level': 'beginner',
                'question_text': 'What is Git and why is it important?',
                'answer': 'Git is a distributed version control system that tracks code changes. It enables collaboration, maintains history, supports branching/merging, and allows reverting to previous versions. It\'s essential for team development and project management.'
            },
            
            # API Questions
            {
                'keywords': ['rest', 'api', 'http'],
                'level': 'intermediate',
                'question_text': 'What is a RESTful API?',
                'answer': 'REST (Representational State Transfer) is an architectural style for APIs. Key principles: stateless communication, client-server separation, cacheable responses, uniform interface, and resource-based URLs. Common HTTP methods: GET (read), POST (create), PUT (update), DELETE (remove).'
            },
            
            # Testing Questions
            {
                'keywords': ['testing', 'unit test', 'pytest'],
                'level': 'intermediate',
                'question_text': 'What is unit testing and why is it important?',
                'answer': 'Unit testing tests individual components/functions in isolation. Benefits: early bug detection, documentation, refactoring confidence, and better design. Python uses unittest or pytest frameworks. Tests should be independent, repeatable, and fast.'
            },
        ]
        
        created_count = 0
        for q_data in questions_data:
            question, created = Question.objects.get_or_create(
                question_text=q_data['question_text'],
                defaults={
                    'keywords': q_data['keywords'],
                    'level': q_data['level'],
                    'answer': q_data['answer']
                }
            )
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'✓ Created: {q_data["question_text"][:60]}...'))
            else:
                self.stdout.write(f'  Already exists: {q_data["question_text"][:60]}...')
        
        self.stdout.write(self.style.SUCCESS(f'\n✅ Successfully created {created_count} new questions!'))
        self.stdout.write(f'Total questions in database: {Question.objects.count()}')
