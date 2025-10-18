from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import CandidateProfile
from .resume_parser import extract_text_from_resume, extract_skills

@login_required(login_url='/login/')
def upload_resume(request):
    try:
        profile = CandidateProfile.objects.get(user=request.user)
        profile_exists = True
    except CandidateProfile.DoesNotExist:
        profile = None
        profile_exists = False

    if request.method == 'POST':
        resume_file = request.FILES.get('resume')
        if not resume_file:
            return render(request, 'interview/upload_resume.html', {'error': 'No file selected.'})

        if profile_exists:
            # Update existing profile
            profile.resume = resume_file
        else:
            # Create new profile
            profile = CandidateProfile(user=request.user, resume=resume_file)

        profile.save()  # Save the new file or updated file

        # Parse the resume
        try:
            # Extract text from resume
            file_path = profile.resume.path
            extracted_text = extract_text_from_resume(file_path)
            profile.full_text = extracted_text

            # Extract skills
            extracted_skills = extract_skills(extracted_text)
            profile.parsed_skills = extracted_skills # Save the list to the JSONField

            # save both full_text and parsed_skills
            profile.save(update_fields=['full_text', 'parsed_skills'])
            
        except Exception as e:
            print(f"Could not parse resume or skills: {e}")

        return redirect('interview_dashboard')  # Redirect after upload/update

    return render(request, 'interview/upload_resume.html')


# dashboard view

@login_required(login_url='/login/')
def dashboard(request):
    try:
        # Get the user's profile
        profile = CandidateProfile.objects.get(user=request.user)
        context = {
            'profile': profile,
            'skills': profile.parsed_skills # Pass the skills to the template
        }
        return render(request, 'interview/dashboard.html', context)
    except CandidateProfile.DoesNotExist:
        # If they don't have a profile, send them to the upload page
        return redirect('upload_resume')