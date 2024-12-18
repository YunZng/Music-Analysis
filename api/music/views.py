from django.db import connection, DatabaseError
from django.http import JsonResponse, HttpResponseBadRequest
from django.db import connection
import datetime


def home(request):
    return JsonResponse({"message": "hello people"}, status=201)


def get_artists(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM likesArtist;")
        rows = cursor.fetchall()
    return JsonResponse({'items': rows})


def get_tracks(request):
    # Validate and retrieve the 'date' parameter
    date = request.GET.get('date')
    order = request.GET.get('order', 'DESC')
    if date is None:
        return HttpResponseBadRequest('Missing date parameter')
    try:
        datetime.datetime.strptime(date, '%Y-%m-%d')
    except ValueError:
        return HttpResponseBadRequest('Invalid date format. Expected YYYY-MM-DD.')

    try:
        with connection.cursor() as cursor:
            query = f"""
                SELECT `Track URI`, `Track Name`, `Album Name`, `Artist Names`, `Album Release Date`
                FROM mytable
                WHERE `Album Release Date` >= %s
                ORDER BY `Album Release Date` {order}, `Track Name` {order};
            """
            # Query parameter
            cursor.execute(query, [date])
            rows = cursor.fetchall()

        items = [
            {
                'url': row[0].replace('spotify:track:', 'https://open.spotify.com/track/'),
                'name': row[1],
                'album': row[2],
                'artist': row[3],
                'date': row[4],
            } for row in rows
        ]
        return JsonResponse({'items': items})

    except DatabaseError as e:
        return JsonResponse({'error': str(e)}, status=500)
