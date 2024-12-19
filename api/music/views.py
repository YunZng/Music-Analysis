from django.db import connection, DatabaseError
from django.http import JsonResponse, HttpResponseBadRequest
from django.db import connection
import uuid
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
        return JsonResponse({"data": items})
    except DatabaseError as e:
        return JsonResponse({'error': str(e)}, status=500)


def get_most_popular(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT `Track URI`, `Track Name`, `Artist Names`, `Popularity`
                FROM mytable
                ORDER BY Popularity DESC
                LIMIT 10;
            """)
            rows = cursor.fetchall()
            items = [
                {
                    'url': row[0].replace('spotify:track:', 'https://open.spotify.com/track/'),
                    'name': row[1],
                    'artist': row[2],
                    'popularity': row[3],
                } for row in rows
            ]
        return JsonResponse({"data": items})
    except DatabaseError as e:
        return JsonResponse({'error': str(e)}, status=500)

def get_longest_loudest(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT `Album Name`, total_duration, `Artist Names`
                FROM (
                    SELECT `Album Name`, SUM(`Track Duration ms`) AS total_duration, `Artist Names`
                    FROM (
                        SELECT *
                        FROM mytable
                        GROUP BY `Artist Names`
                        ORDER BY AVG(Loudness) DESC
                        LIMIT 10
                    ) AS top_artists
                    GROUP BY `Album Name`
                ) AS album_durations
                ORDER BY total_duration DESC
                LIMIT 10;
            """)
            rows = cursor.fetchall()
            items = [
                {
                    'album': row[0],
                    'duration': f'{row[1]/1000: .2f}',
                    'artist': row[2],
                    'id': uuid.uuid4(),
                } for row in rows
            ]
        return JsonResponse({"data": items})
    except DatabaseError as e:
        return JsonResponse({'error': str(e)}, status=500)