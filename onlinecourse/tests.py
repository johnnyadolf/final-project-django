from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from datetime import date
from .models import (
    Instructor, Learner, Course, Lesson, 
    Enrollment, Question, Choice, Submission
)
import json


class InstructorModelTest(TestCase):
    """Test cases for Instructor model"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='instructor1',
            password='testpass123',
            first_name='John',
            last_name='Doe'
        )
        
    def test_instructor_creation(self):
        """Test creating an instructor"""
        instructor = Instructor.objects.create(
            user=self.user,
            full_time=True,
            total_learners=100
        )
        self.assertEqual(instructor.user.username, 'instructor1')
        self.assertTrue(instructor.full_time)
        self.assertEqual(instructor.total_learners, 100)
        
    def test_instructor_str_method(self):
        """Test instructor string representation"""
        instructor = Instructor.objects.create(
            user=self.user,
            full_time=True,
            total_learners=50
        )
        self.assertEqual(str(instructor), 'instructor1')
        
    def test_instructor_default_full_time(self):
        """Test instructor default full_time value"""
        instructor = Instructor.objects.create(
            user=self.user,
            total_learners=0
        )
        self.assertTrue(instructor.full_time)


class LearnerModelTest(TestCase):
    """Test cases for Learner model"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='learner1',
            password='testpass123'
        )
        
    def test_learner_creation(self):
        """Test creating a learner"""
        learner = Learner.objects.create(
            user=self.user,
            occupation=Learner.STUDENT,
            social_link='https://linkedin.com/learner1'
        )
        self.assertEqual(learner.user.username, 'learner1')
        self.assertEqual(learner.occupation, 'student')
        
    def test_learner_occupation_choices(self):
        """Test all occupation choices"""
        occupations = [Learner.STUDENT, Learner.DEVELOPER, 
                      Learner.DATA_SCIENTIST, Learner.DATABASE_ADMIN]
        for occupation in occupations:
            learner = Learner.objects.create(
                user=self.user,
                occupation=occupation,
                social_link='https://example.com'
            )
            self.assertIn(learner.occupation, [choice[0] for choice in Learner.OCCUPATION_CHOICES])
            learner.delete()  # Clean up
            
    def test_learner_str_method(self):
        """Test learner string representation"""
        learner = Learner.objects.create(
            user=self.user,
            occupation=Learner.DEVELOPER,
            social_link='https://github.com/learner1'
        )
        self.assertEqual(str(learner), 'learner1,developer')
        
    def test_learner_default_occupation(self):
        """Test learner default occupation"""
        learner = Learner.objects.create(
            user=self.user,
            social_link='https://example.com'
        )
        self.assertEqual(learner.occupation, Learner.STUDENT)


class CourseModelTest(TestCase):
    """Test cases for Course model"""
    
    def setUp(self):
        self.instructor_user = User.objects.create_user(
            username='instructor',
            password='testpass123'
        )
        self.instructor = Instructor.objects.create(
            user=self.instructor_user,
            total_learners=0
        )
        
    def test_course_creation(self):
        """Test creating a course"""
        course = Course.objects.create(
            name='Python 101',
            description='Introduction to Python programming',
            pub_date=date.today(),
            total_enrollment=0
        )
        course.instructors.add(self.instructor)
        
        self.assertEqual(course.name, 'Python 101')
        self.assertEqual(course.total_enrollment, 0)
        self.assertIn(self.instructor, course.instructors.all())
        
    def test_course_str_method(self):
        """Test course string representation"""
        course = Course.objects.create(
            name='Django Course',
            description='Learn Django framework',
            pub_date=date.today()
        )
        expected = "Name: Django Course,Description: Learn Django framework"
        self.assertEqual(str(course), expected)
        
    def test_course_default_values(self):
        """Test course default values"""
        course = Course.objects.create(
            description='Test description'
        )
        self.assertEqual(course.name, 'online course')
        self.assertEqual(course.total_enrollment, 0)


class LessonModelTest(TestCase):
    """Test cases for Lesson model"""
    
    def setUp(self):
        self.course = Course.objects.create(
            name='Test Course',
            description='Test Description'
        )
        
    def test_lesson_creation(self):
        """Test creating a lesson"""
        lesson = Lesson.objects.create(
            title='Introduction',
            order=1,
            course=self.course,
            content='Welcome to the course'
        )
        self.assertEqual(lesson.title, 'Introduction')
        self.assertEqual(lesson.order, 1)
        self.assertEqual(lesson.course, self.course)
        
    def test_lesson_default_values(self):
        """Test lesson default values"""
        lesson = Lesson.objects.create(
            course=self.course,
            content='Test content'
        )
        self.assertEqual(lesson.title, 'title')
        self.assertEqual(lesson.order, 0)


class EnrollmentModelTest(TestCase):
    """Test cases for Enrollment model"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='student',
            password='testpass123'
        )
        self.course = Course.objects.create(
            name='Test Course',
            description='Test Description'
        )
        
    def test_enrollment_creation(self):
        """Test creating an enrollment"""
        enrollment = Enrollment.objects.create(
            user=self.user,
            course=self.course,
            mode=Enrollment.HONOR
        )
        self.assertEqual(enrollment.user, self.user)
        self.assertEqual(enrollment.course, self.course)
        self.assertEqual(enrollment.mode, 'honor')
        
    def test_enrollment_default_values(self):
        """Test enrollment default values"""
        enrollment = Enrollment.objects.create(
            user=self.user,
            course=self.course
        )
        self.assertEqual(enrollment.mode, Enrollment.AUDIT)
        self.assertEqual(enrollment.rating, 5.0)
        self.assertIsNotNone(enrollment.date_enrolled)
        
    def test_enrollment_modes(self):
        """Test all enrollment modes"""
        modes = [Enrollment.AUDIT, Enrollment.HONOR, Enrollment.BETA]
        for mode in modes:
            enrollment = Enrollment.objects.create(
                user=self.user,
                course=self.course,
                mode=mode
            )
            self.assertIn(enrollment.mode, [choice[0] for choice in Enrollment.COURSE_MODES])
            enrollment.delete()


class QuestionAndChoiceModelTest(TestCase):
    """Test cases for Question and Choice models"""
    
    def setUp(self):
        self.course = Course.objects.create(
            name='Test Course',
            description='Test Description'
        )
        self.question = Question.objects.create(
            course=self.course,
            content='What is 2+2?',
            grade=10
        )
        
    def test_question_creation(self):
        """Test creating a question"""
        self.assertEqual(self.question.content, 'What is 2+2?')
        self.assertEqual(self.question.grade, 10)
        self.assertEqual(self.question.course, self.course)
        
    def test_question_str_method(self):
        """Test question string representation"""
        self.assertEqual(str(self.question), 'Question: What is 2+2?')
        
    def test_question_default_grade(self):
        """Test question default grade"""
        question = Question.objects.create(
            course=self.course,
            content='Test question'
        )
        self.assertEqual(question.grade, 50)
        
    def test_choice_creation(self):
        """Test creating choices"""
        choice1 = Choice.objects.create(
            question=self.question,
            content='4',
            is_correct=True
        )
        choice2 = Choice.objects.create(
            question=self.question,
            content='5',
            is_correct=False
        )
        self.assertTrue(choice1.is_correct)
        self.assertFalse(choice2.is_correct)
        
    def test_question_is_get_score_correct(self):
        """Test is_get_score with correct answers"""
        choice1 = Choice.objects.create(
            question=self.question,
            content='4',
            is_correct=True
        )
        choice2 = Choice.objects.create(
            question=self.question,
            content='5',
            is_correct=False
        )
        
        # Select only correct answer
        result = self.question.is_get_score([choice1.id])
        self.assertTrue(result)
        
    def test_question_is_get_score_incorrect(self):
        """Test is_get_score with incorrect answers"""
        choice1 = Choice.objects.create(
            question=self.question,
            content='4',
            is_correct=True
        )
        choice2 = Choice.objects.create(
            question=self.question,
            content='5',
            is_correct=False
        )
        
        # Select wrong answer
        result = self.question.is_get_score([choice2.id])
        self.assertFalse(result)
        
    def test_question_is_get_score_multiple_correct(self):
        """Test is_get_score with multiple correct answers"""
        choice1 = Choice.objects.create(
            question=self.question,
            content='4',
            is_correct=True
        )
        choice2 = Choice.objects.create(
            question=self.question,
            content='2+2',
            is_correct=True
        )
        choice3 = Choice.objects.create(
            question=self.question,
            content='5',
            is_correct=False
        )
        
        # Select all correct answers
        result = self.question.is_get_score([choice1.id, choice2.id])
        self.assertTrue(result)
        
        # Select only one correct answer (should fail)
        result = self.question.is_get_score([choice1.id])
        self.assertFalse(result)


class SubmissionModelTest(TestCase):
    """Test cases for Submission model"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='student',
            password='testpass123'
        )
        self.course = Course.objects.create(
            name='Test Course',
            description='Test Description'
        )
        self.enrollment = Enrollment.objects.create(
            user=self.user,
            course=self.course
        )
        self.question = Question.objects.create(
            course=self.course,
            content='Test question',
            grade=10
        )
        self.choice = Choice.objects.create(
            question=self.question,
            content='Test answer',
            is_correct=True
        )
        
    def test_submission_creation(self):
        """Test creating a submission"""
        submission = Submission.objects.create(
            enrollment=self.enrollment
        )
        submission.choices.add(self.choice)
        
        self.assertEqual(submission.enrollment, self.enrollment)
        self.assertIn(self.choice, submission.choices.all())
        
    def test_submission_str_method(self):
        """Test submission string representation"""
        submission = Submission.objects.create(
            enrollment=self.enrollment
        )
        expected = f"Submission for {self.user.username} - {self.course.name}"
        self.assertEqual(str(submission), expected)


class HealthCheckViewTest(TestCase):
    """Test cases for health check endpoint"""
    
    def setUp(self):
        self.client = Client()
        
    def test_health_check_success(self):
        """Test health check endpoint returns success"""
        response = self.client.get(reverse('onlinecourse:health_check'), follow=True)
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.content)
        self.assertEqual(data['status'], 'healthy')
        self.assertEqual(data['database'], 'connected')


class RegistrationViewTest(TestCase):
    """Test cases for user registration"""
    
    def setUp(self):
        self.client = Client()
        
    def test_registration_get_request(self):
        """Test registration page loads"""
        response = self.client.get(reverse('onlinecourse:registration'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'onlinecourse/user_registration_bootstrap.html')
        
    def test_registration_success(self):
        """Test successful user registration using view directly"""
        from .views import registration_request
        from django.test import RequestFactory
        
        factory = RequestFactory()
        
        # Create POST request
        request = factory.post('/onlinecourse/registration/', {
            'username': 'newuser',
            'psw': 'testpass123',
            'firstname': 'New',
            'lastname': 'User'
        })
        
        # Add session to request
        from django.contrib.sessions.middleware import SessionMiddleware
        middleware = SessionMiddleware(lambda x: None)
        middleware.process_request(request)
        request.session.save()
        
        # Call view
        response = registration_request(request)
        
        # User should be created
        user_exists = User.objects.filter(username='newuser').exists()
        self.assertTrue(user_exists, "User was not created")
        
        # Check user details
        user = User.objects.get(username='newuser')
        self.assertEqual(user.first_name, 'New')
        self.assertEqual(user.last_name, 'User')
        
    def test_registration_duplicate_user(self):
        """Test registration with existing username"""
        # Create existing user
        User.objects.create_user(
            username='existinguser',
            password='testpass123'
        )
        
        # Get initial user count
        initial_count = User.objects.count()
        
        # Try to create duplicate
        from .views import registration_request
        from django.test import RequestFactory
        
        factory = RequestFactory()
        request = factory.post('/onlinecourse/registration/', {
            'username': 'existinguser',
            'psw': 'newpass123',
            'firstname': 'Test',
            'lastname': 'User'
        })
        
        # Add session
        from django.contrib.sessions.middleware import SessionMiddleware
        middleware = SessionMiddleware(lambda x: None)
        middleware.process_request(request)
        request.session.save()
        
        response = registration_request(request)
        
        # User count should not increase
        final_count = User.objects.count()
        self.assertEqual(final_count, initial_count, "Duplicate user was created")


class LoginViewTest(TestCase):
    """Test cases for user login"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
    def test_login_get_request(self):
        """Test login page loads"""
        response = self.client.get(reverse('onlinecourse:login'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'onlinecourse/user_login_bootstrap.html')
        
    def test_login_success(self):
        """Test successful login"""
        response = self.client.post(reverse('onlinecourse:login'), {
            'username': 'testuser',
            'psw': 'testpass123'
        }, follow=True)
        
        # Should redirect after successful login
        self.assertEqual(response.status_code, 200)
        
    def test_login_invalid_credentials(self):
        """Test login with invalid credentials"""
        # Try to authenticate with wrong password
        from django.contrib.auth import authenticate
        
        user = authenticate(username='testuser', password='wrongpassword')
        
        # Authentication should fail
        self.assertIsNone(user, "User was authenticated with wrong password")
        
        # Try login via client
        response = self.client.post('/onlinecourse/login/', {
            'username': 'testuser',
            'psw': 'wrongpassword'
        }, follow=True)
        
        # User should not be logged in
        self.assertNotIn('_auth_user_id', self.client.session)


class LogoutViewTest(TestCase):
    """Test cases for user logout"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
    def test_logout(self):
        """Test user logout"""
        # Login first
        self.client.login(username='testuser', password='testpass123')
        
        # Logout
        response = self.client.get(reverse('onlinecourse:logout'), follow=True)
        self.assertEqual(response.status_code, 200)
        
        # User should not be authenticated
        response = self.client.get(reverse('onlinecourse:index'))
        self.assertNotIn('_auth_user_id', self.client.session)


class CourseListViewTest(TestCase):
    """Test cases for course list view"""
    
    def setUp(self):
        self.client = Client()
        # Create multiple courses
        for i in range(12):
            Course.objects.create(
                name=f'Course {i}',
                description=f'Description {i}',
                total_enrollment=i
            )
        
    def test_course_list_view(self):
        """Test course list view loads"""
        response = self.client.get(reverse('onlinecourse:index'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'onlinecourse/course_list_bootstrap.html')
        
    def test_course_list_max_10_courses(self):
        """Test course list shows maximum 10 courses"""
        response = self.client.get(reverse('onlinecourse:index'), follow=True)
        self.assertEqual(len(response.context['course_list']), 10)
        
    def test_course_list_ordered_by_enrollment(self):
        """Test courses are ordered by total_enrollment"""
        response = self.client.get(reverse('onlinecourse:index'), follow=True)
        courses = response.context['course_list']
        
        # Check if ordered descending
        enrollments = [course.total_enrollment for course in courses]
        self.assertEqual(enrollments, sorted(enrollments, reverse=True))


class EnrollViewTest(TestCase):
    """Test cases for enrollment functionality"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='student',
            password='testpass123'
        )
        self.course = Course.objects.create(
            name='Test Course',
            description='Test Description',
            total_enrollment=0
        )
        
    def test_enroll_authenticated_user(self):
        """Test authenticated user can enroll"""
        self.client.login(username='student', password='testpass123')
        
        response = self.client.get(
            reverse('onlinecourse:enroll', args=[self.course.id]),
            follow=True
        )
        
        # Should redirect to course details
        self.assertEqual(response.status_code, 200)
        
        # Enrollment should be created
        enrollment_exists = Enrollment.objects.filter(
            user=self.user,
            course=self.course
        ).exists()
        self.assertTrue(enrollment_exists)
        
        # Course enrollment count should increase
        self.course.refresh_from_db()
        self.assertEqual(self.course.total_enrollment, 1)
        
    def test_enroll_unauthenticated_user(self):
        """Test unauthenticated user cannot enroll"""
        response = self.client.get(
            reverse('onlinecourse:enroll', args=[self.course.id]),
            follow=True
        )
        
        # Should redirect (no error)
        self.assertEqual(response.status_code, 200)
        
        # No enrollment should be created
        enrollment_count = Enrollment.objects.filter(course=self.course).count()
        self.assertEqual(enrollment_count, 0)
        
    def test_enroll_already_enrolled(self):
        """Test enrolling in same course twice"""
        self.client.login(username='student', password='testpass123')
        
        # Enroll first time
        self.client.get(reverse('onlinecourse:enroll', args=[self.course.id]), follow=True)
        
        # Try to enroll again
        self.client.get(reverse('onlinecourse:enroll', args=[self.course.id]), follow=True)
        
        # Should only have one enrollment
        enrollment_count = Enrollment.objects.filter(
            user=self.user,
            course=self.course
        ).count()
        self.assertEqual(enrollment_count, 1)
        
        # Total enrollment should only be 1
        self.course.refresh_from_db()
        self.assertEqual(self.course.total_enrollment, 1)


class SubmitExamViewTest(TestCase):
    """Test cases for exam submission"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='student',
            password='testpass123'
        )
        self.course = Course.objects.create(
            name='Test Course',
            description='Test Description'
        )
        self.enrollment = Enrollment.objects.create(
            user=self.user,
            course=self.course
        )
        self.question = Question.objects.create(
            course=self.course,
            content='Test question',
            grade=10
        )
        self.choice1 = Choice.objects.create(
            question=self.question,
            content='Correct answer',
            is_correct=True
        )
        self.choice2 = Choice.objects.create(
            question=self.question,
            content='Wrong answer',
            is_correct=False
        )
        
    def test_submit_unauthenticated(self):
        """Test unauthenticated user cannot submit"""
        response = self.client.post(
            f'/onlinecourse/{self.course.id}/submit/',
            {'choice_1': self.choice1.id}
        )
        
        # Should redirect (301 or 302)
        self.assertIn(response.status_code, [301, 302])
        
        # No submission should be created
        submission_count = Submission.objects.count()
        self.assertEqual(submission_count, 0, "Submission was created for unauthenticated user")
        
    def test_submit_not_enrolled(self):
        """Test user must be enrolled to submit"""
        # Create another user who is not enrolled
        other_user = User.objects.create_user(
            username='other',
            password='testpass123'
        )
        self.client.login(username='other', password='testpass123')
        
        response = self.client.post(
            reverse('onlinecourse:submit', args=[self.course.id]),
            {'choice_1': self.choice1.id},
            follow=True
        )
        
        # Should redirect to course details
        self.assertEqual(response.status_code, 200)
        
    def test_submit_success(self):
        """Test successful exam submission using view directly"""
        from .views import submit
        from django.test import RequestFactory
        
        factory = RequestFactory()
        
        # Create authenticated request
        request = factory.post(
            f'/onlinecourse/{self.course.id}/submit/',
            {'choice': str(self.choice1.id)}
        )
        request.user = self.user
        
        # Call submit view directly
        response = submit(request, self.course.id)
        
        # Should create submission
        submission_exists = Submission.objects.filter(
            enrollment=self.enrollment
        ).exists()
        self.assertTrue(submission_exists, "Submission was not created")
        
        # Check submission has correct choices
        submission = Submission.objects.get(enrollment=self.enrollment)
        choice_ids = [c.id for c in submission.choices.all()]
        self.assertIn(self.choice1.id, choice_ids, 
                     f"Choice {self.choice1.id} not in submission")


class ExamResultViewTest(TestCase):
    """Test cases for exam result view"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='student',
            password='testpass123'
        )
        self.course = Course.objects.create(
            name='Test Course',
            description='Test Description'
        )
        self.enrollment = Enrollment.objects.create(
            user=self.user,
            course=self.course
        )
        
        # Create question with choices
        self.question = Question.objects.create(
            course=self.course,
            content='What is 2+2?',
            grade=100
        )
        self.correct_choice = Choice.objects.create(
            question=self.question,
            content='4',
            is_correct=True
        )
        self.wrong_choice = Choice.objects.create(
            question=self.question,
            content='5',
            is_correct=False
        )
        
    def test_exam_result_correct_answer(self):
        """Test exam result with correct answer"""
        # Create submission with correct answer
        submission = Submission.objects.create(enrollment=self.enrollment)
        submission.choices.add(self.correct_choice)
        
        response = self.client.get(
            reverse('onlinecourse:exam_result', 
                   args=[self.course.id, submission.id]),
            follow=True
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['grade'], 100)
        
    def test_exam_result_wrong_answer(self):
        """Test exam result with wrong answer"""
        # Create submission with wrong answer
        submission = Submission.objects.create(enrollment=self.enrollment)
        submission.choices.add(self.wrong_choice)
        
        response = self.client.get(
            reverse('onlinecourse:exam_result', 
                   args=[self.course.id, submission.id]),
            follow=True
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['grade'], 0)
        
    def test_exam_result_multiple_questions(self):
        """Test exam result with multiple questions"""
        # Create second question
        question2 = Question.objects.create(
            course=self.course,
            content='What is 3+3?',
            grade=50
        )
        correct_choice2 = Choice.objects.create(
            question=question2,
            content='6',
            is_correct=True
        )
        
        # Submit both correct answers
        submission = Submission.objects.create(enrollment=self.enrollment)
        submission.choices.add(self.correct_choice, correct_choice2)
        
        response = self.client.get(
            reverse('onlinecourse:exam_result', 
                   args=[self.course.id, submission.id]),
            follow=True
        )
        
        # Should get full score (100 + 50 = 150)
        self.assertEqual(response.context['grade'], 150)


class UtilityFunctionsTest(TestCase):
    """Test cases for utility functions"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='student',
            password='testpass123'
        )
        self.course = Course.objects.create(
            name='Test Course',
            description='Test Description'
        )
        
    def test_check_if_enrolled_true(self):
        """Test check_if_enrolled returns True when enrolled"""
        from .views import check_if_enrolled
        
        Enrollment.objects.create(user=self.user, course=self.course)
        result = check_if_enrolled(self.user, self.course)
        self.assertTrue(result)
        
    def test_check_if_enrolled_false(self):
        """Test check_if_enrolled returns False when not enrolled"""
        from .views import check_if_enrolled
        
        result = check_if_enrolled(self.user, self.course)
        self.assertFalse(result)
        
    def test_extract_answers(self):
        """Test extract_answers function"""
        from .views import extract_answers
        from django.test import RequestFactory
        
        factory = RequestFactory()
        request = factory.post('/submit/', {
            'choice_1': '10',
            'choice_2': '20',
            'other_field': 'ignored'
        })
        
        answers = extract_answers(request)
        self.assertEqual(len(answers), 2)
        self.assertIn(10, answers)
        self.assertIn(20, answers)
