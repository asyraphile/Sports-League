from django.shortcuts import render, redirect
from django.db.models import F
import mimetypes, io
from .models import Upload, Team, User, Match
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.core.mail import send_mail
# Create your views here.
#auth
def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = User.objects.filter(email=email)
        if not user:
            messages.error(request, "User does not exist in our system!")
            pass
        else:
            user = User.objects.get(email=email)
            is_valid_password = check_password(password, user.password)
            if is_valid_password == True:
                request.session['name'] = user.name
                request.session['email'] = user.email
                
                return redirect('Main Page')
            else:
                messages.error(request, "Wrong Password!")
            pass
    return render(request, "auth/login.html",{})

def logout(request):

    request.session.flush()
    return redirect('Login')
def signup(request):
    if request.method == 'POST':
        email = request.POST['email']
        name = request.POST['name']
        password = request.POST['password']
        confirmpassword = request.POST['confirmpassword']
        user = User.objects.filter(email=email)
        if password != confirmpassword:
            messages.error(request, "Password and confirm password does not match!")
            pass
        elif user:
            messages.error(request, "This email has already registered in our system!")
            pass
        else:
            User.objects.create(email=email, name=name, password=make_password(password)) 
            subject = 'Sports League Registration'
            message = 'You have successfully registered to Sports League system. Please login at http://localhost:8000/login/'
            from_email = 'celery2511@gmail.com'
            recipient_list = [email]
            send_mail(subject, message, from_email, recipient_list)
            messages.success(request, "Registration successful!")

        
    return render(request, "auth/signup.html",{})

def forgotpassword(request):
    return render(request, "auth/forgotpassword.html",{})

#main
def mainpage(request):
    try:
        print(request.session['name'])
    except:
        return redirect('Login')
    if request.method == "POST":
        csv_file = request.FILES['csv_file']
        mime_type= mimetypes.guess_type(csv_file.name)[0]
        try:
            if mime_type == 'text/csv':
                file_size = len(csv_file.read())
                csv_file.seek(0)
                text_stream = io.StringIO(csv_file.read().decode('utf-8'))
                team_list = []
                team_dict = {}
                exception = False
                for line in text_stream:
                    line_parts = line.split(',')
                    try:
                        if len(line_parts) == 4:
                            try:
                                if not isinstance(line_parts[0], str):
                                    exception = True
                                    raise Exception
                                elif not isinstance(line_parts[2], str):
                                    exception = True
                                    raise Exception
                                else:
                                    try:
                                        team_dict = {
                                        'team_1_name': line_parts[0],
                                        'team_1_score': int(line_parts[1]),
                                        'team_2_name': line_parts[2],
                                        'team_2_score': int(line_parts[3].replace('\r\n',''))
                                        }
                                        team_list.append(team_dict)
                                    except ValueError:
                                        exception = True
                                        message = line_parts[3] +" or " + line_parts[1] + " is not an integer! Please change it to integer."
                                        messages.error(request, message)
                                        pass
                                    
                            except:
                                exception = True
                                message = line_parts[0] + " and " + line_parts[2] + " has to be string! Please change it to string."
                                messages.error(request, message)
                                pass
                        else:
                            raise Exception
                    except:
                        exception = True
                        message = str(csv_file) + " columns length should only be 4."
                        messages.error(request, message)
                        pass
            else:
                raise Exception
        except:
            exception = True
            message = str(csv_file) + " is not type csv. Please try again."
            messages.error(request, message)
            pass
        if exception == False:
            #Create Upload objects    
            Upload.objects.create(file=csv_file, mime=mime_type, size=file_size)
            message = str(csv_file) + " has been uploaded successfully."
            messages.success(request, message)
            latestUpload = Upload.objects.latest('date_created')
            for each in team_list:
                team_exist = Team.objects.all().values_list('name', flat=True)
                if each['team_1_name'] not in team_exist:
                    Team.objects.create(name=each['team_1_name'], upload=latestUpload)
                if each['team_2_name'] not in team_exist:
                    Team.objects.create(name=each['team_2_name'], upload=latestUpload)

                #create match
                match = Match()
                match.team_1 = Team.objects.get(name=each['team_1_name'])
                match.team_1_score = int(each['team_1_score'])
                match.team_2 = Team.objects.get(name=each['team_2_name'])
                match.team_2_score = int(each['team_2_score'])
                match.save()

                if each['team_1_score'] == each['team_2_score']: #draw
                    print("HERE")
                    Team.objects.filter(name=each['team_1_name']).update(point=F('point')+1, upload=latestUpload)
                    Team.objects.filter(name=each['team_2_name']).update(point=F('point')+1, upload=latestUpload)
                elif each['team_1_score'] > each['team_2_score']: #team 1 wins
                    Team.objects.filter(name=each['team_1_name']).update(point=F('point')+3, upload=latestUpload)
                    Team.objects.filter(name=each['team_2_name']).update(point=F('point')+0, upload=latestUpload)
                elif each['team_2_score'] > each['team_1_score']: #team 2 wins
                    Team.objects.filter(name=each['team_2_name']).update(point=F('point')+3, upload=latestUpload)
                    Team.objects.filter(name=each['team_1_name']).update(point=F('point')+0, upload=latestUpload)
        

    return render(request, "main/mainpage.html",{})
#Sidebar Match List
def match_list(request):
    try:
        print(request.session['name'])
    except:
        return redirect('Login')
    match_list = Match.objects.all()
    team_list = Team.objects.all()
    context = {
        'match_list': match_list,
        'team_list': team_list,
    }
    if request.method == "POST":
        if request.POST['choice'] == 'edit':
            print(request.POST)
            #recalculating the scores
            match = Match.objects.get(matchid=request.POST['match'])
            team_1 = Team.objects.filter(teamid=match.team_1)
            team_2 = Team.objects.filter(teamid=match.team_2)
            if request.POST['team_1_score'] == request.POST['team_2_score']: #draw
                team_1.update(point=F('point')+1)
                team_2.update(point=F('point')+1)
            elif request.POST['team_1_score'] > request.POST['team_2_score']: #team 1 wins
                team_1.update(point=F('point')+3)
            elif request.POST['team_2_score'] > request.POST['team_1_score']: #team 2 wins
                team_2.update(point=F('point')+3)
            #updating match
            Match.objects.filter(matchid=request.POST['match']).update(team_1_score=request.POST['team_1_score'], team_2_score=request.POST['team_2_score'])
        elif request.POST['choice'] == 'add':
            #Check existence
            team_1 = Team.objects.filter(name=request.POST['team_1'])
            team_2 = Team.objects.filter(name=request.POST['team_2'])
            #creating teams if it does not exist
            if not team_1:
                Team.objects.create(name=request.POST['team_1'])
            elif not team_2:
                Team.objects.create(name=request.POST['team_2'])

            #Set teams again    
            team_1 = Team.objects.filter(name=request.POST['team_1'])
            team_2 = Team.objects.filter(name=request.POST['team_2'])

            if request.POST['team_1_score'] == request.POST['team_2_score']: #draw
                team_1.update(point=F('point')+1)
                team_2.update(point=F('point')+1)
            elif request.POST['team_1_score'] > request.POST['team_2_score']: #team 1 wins
                team_1.update(point=F('point')+3)
            elif request.POST['team_2_score'] > request.POST['team_1_score']: #team 2 wins
                team_2.update(point=F('point')+3)
            #getting teams instances
            team_1 = Team.objects.get(name=request.POST['team_1'])
            team_2 = Team.objects.get(name=request.POST['team_2'])
            #creating match
            Match.objects.create(team_1=team_1, team_1_score=request.POST['team_1_score'], team_2=team_1, team_2_score=request.POST['team_2_score'])
        
        elif request.POST['choice'] == 'delete':
            match = Match.objects.get(matchid=request.POST['match'])
            team_1 = Team.objects.filter(teamid=match.team_1)
            team_2 = Team.objects.filter(teamid=match.team_2)
            if match.team_1_score == match.team_2_score: #draw
                    team_1.update(point=F('point')-1)
                    team_2.update(point=F('point')-1)
            elif match.team_1_score > match.team_2_score: #team 1 wins
                team_1.update(point=F('point')-3)
            elif match.team_2_score > match.team_1_score: #team 2 wins
                team_2.update(point=F('point')-3)
            #deleting match
            Match.objects.filter(matchid=request.POST['match']).delete()
    return render(request, "main/match_list.html", context)
#Sidebar Team List
def team_list(request):
    try:
        print(request.session['name'])
    except:
        return redirect('Login')
    team_list = Team.objects.all()
    context = {
        'team_list': team_list,
    }
    return render(request, "main/team_list.html", context)
#Sidebar Scoreboard
def scoreboard(request):
    try:
        print(request.session['name'])
    except:
        return redirect('Login')
    team_list = Team.objects.all().order_by('-point', 'name')
    context = {
        'team_list': team_list,
    }
    return render(request, "main/scoreboard.html", context)