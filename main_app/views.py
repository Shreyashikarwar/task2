from django.shortcuts import render, redirect
from main_app.models import Movie, Casting, Dialogue
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
# Create your views here.


def home(request):
    return render(request, 'index.html')

@csrf_exempt
def add_movie(request):
    if request.method == 'GET':
        return render(request, 'movieform.html')
    
    elif request.method == "POST":
        
        try:
            data = json.loads(request.body)
            #add movie
            name=data['name']
            duration=data['duration']
            movie = Movie.objects.create(
                name=name, 
                duration=duration
                )
            
            #add casting
            for casting_data in data['casting']:
                character_name=casting_data['character_name']
                cast_name=casting_data['cast_name']
                gender=casting_data['gender']
                Casting.objects.create(
                    movie=movie,
                    character_name=character_name,
                    cast_name=cast_name,
                    gender=gender
                )
            print("cast ")
            #add dialogue
            for dialogue_data in data['dialogue']:
                start_time= dialogue_data['start_time']
                end_time=dialogue_data['end_time']
                character_name=dialogue_data['character_name']
                dialogue=dialogue_data['dialogue']
                Dialogue.objects.create(
                        movie=movie,
                        start_time=start_time,
                        end_time=end_time,
                        character_name=character_name,
                        dialogue=dialogue
                    )
            print("dial")
            return JsonResponse({'message': 'Movie added successfully'}, status=201)
        except KeyError:
            return JsonResponse({'error': 'Invalid request data'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'message': 'Method not allowed'}, status=405)

@csrf_exempt
def edit_movie(request, movie_id):
    try:
        if request.method == "POST":
            data = json.loads(request.body)
            movie = Movie.objects.get(pk=movie_id)

            #add movie
            name=data['name'] or movie.name
            print(type(name), name)
            duration=data['duration'] or movie.duration
            movie = Movie.objects.update(
                name=name, 
                duration=duration
                )
            
            #add casting
            for casting_data in data['casting']:
                cast = Casting.objects.get(movie=movie)
                character_name=casting_data['character_name'] or cast.character_name
                cast_name=casting_data['cast_name'] or cast.cast_name
                gender=casting_data['gender'] or cast.gender
                Casting.objects.update(
                    movie=movie,
                    character_name=character_name,
                    cast_name=cast_name,
                    gender=gender
                )
            #add dialogue
            for dialogue_data in data['dialogue']:

                dial = Dialogue.objects.get(movie=movie)
                start_time= dialogue_data['start_time'] or dial.start_time
                end_time=dialogue_data['end_time'] or dial.end_time
                character_name=dialogue_data['character_name'] or dial.character_name
                dialogue=dialogue_data['dialogue'] or dial.dialogue
                Dialogue.objects.update(
                        movie=movie,
                        start_time=start_time,
                        end_time=end_time,
                        character_name=character_name,
                        dialogue=dialogue
                    )
            return JsonResponse({'message': 'Movie updated successfully'}, status=201)
    except:
        return JsonResponse({'message': 'Movie not found'}, status=404)
        


def movie_list(request):
    return render(request, 'movie_list.html')
@csrf_exempt
def update_movie(request, movie_id):
    try:
        if request.method == "GET":
            return render(request, 'editmovie.html')
        
        elif request.method == "POST":
                data = json.loads(request.body)
                print(data)
                movie = Movie.objects.get(pk=movie_id)

                #add movie
                name=data['name'] or movie.name
                print(type(name), name)
                duration=data['duration'] or movie.duration
                movie.name = name
                movie.duration = duration
                movie.save()
                print(movie)
                #add casting
                for casting_data in data['casting']:
                    print(casting_data,"hjkgjggh")
                    cast = Casting.objects.filter(movie=movie)
                    print(cast,"jhghgf")
                    character_name=casting_data['character_name'] or cast.character_name
                    cast_name=casting_data['cast_name'] or cast.cast_name
                    gender=casting_data['gender'] or cast.gender
                    cast= Casting.objects.filter(movie=movie, cast_name=cast_name).update(
                        movie=movie,
                        cast_name=cast_name,
                        gender=gender,
                        character_name=character_name
                    )
                #add dialogue
                for dialogue_data in data['dialogue']:
                    print(dialogue_data)
                    dial = Dialogue.objects.filter(movie=movie, character_name=dialogue_data['character_name']).update(
                        dialogue = dialogue_data['dialogue'],
                        start_time = dialogue_data['start_time'],
                        end_time = dialogue_data['end_time'],
                        movie = movie,
                    )
                    
                return JsonResponse({'message': 'Movie updated successfully'}, status=201)
    except:
        return JsonResponse({'message': 'Movie not found'}, status=404)
        

def get_movie(request):
    if request.method == "GET":
        try:
            # data = json.loads(request.body)
            # if data['movie_id']!="" and Movie.objects.filter(pk=data["movie_id"]).exists():
            #     movies = Movie.objects.filter(pk=data['movie_id'])
            # else:
            movies = Movie.objects.all()
            movie_data = []
            print(movies)
            for movie in movies:
                castings = movie.casting_set.all()
                dialogues = movie.dialogue_set.all()

                casting_data = []
                for casting in castings:
                    dialogue_data = []
                    for dialogue in dialogues:
                        if dialogue.character_name == casting.character_name:
                            dialogue_data.append({
                                'start_time': dialogue.start_time,
                                'end_time': dialogue.end_time,
                                'dialogue': dialogue.dialogue,
                                'character_name':dialogue.character_name
                            })
                    casting_data.append({
                        'character_name': casting.character_name,
                        'cast_name': casting.cast_name,
                        'gender': casting.gender,
                        'dialogues': dialogue_data
                    })

                movie_data.append({
                    'id': movie.pk,
                    'name': movie.name,
                    'duration': movie.duration,
                    'castings': casting_data
                })

            return JsonResponse({'message': movie_data}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'message': 'Method not allowed'}, status=405)

def get_movie_details(request, movie_id):
    if request.method == "GET":
        try:
            
            movies = Movie.objects.filter(pk=movie_id)
            movie_data =[]
            print(movies)
            for movie in movies:
                castings = movie.casting_set.all()
                dialogues = movie.dialogue_set.all()

                casting_data = []
                for casting in castings:
                    dialogue_data = []
                    for dialogue in dialogues:
                        if dialogue.character_name == casting.character_name:
                            dialogue_data.append({
                                'start_time': dialogue.start_time,
                                'end_time': dialogue.end_time,
                                'dialogue': dialogue.dialogue
                            })
                    casting_data.append({
                        'character_name': casting.character_name,
                        'cast_name': casting.cast_name,
                        'gender': casting.gender,
                        'dialogues': dialogue_data
                    })

                movie_data.append({
                    'id': movie.pk,
                    'name': movie.name,
                    'duration': movie.duration,
                    'castings': casting_data
                })

            return JsonResponse({'message': movie_data}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'message': 'Method not allowed'}, status=405)
    
def delete_movie(request, movie_id):
    if request.method == "GET":
        try:
            if Movie.objects.filter(pk=movie_id).exists():
                movies = Movie.objects.filter(pk=movie_id).delete()
                return redirect('movie_list')
            else:
                return JsonResponse({'message': "No movie found"}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
