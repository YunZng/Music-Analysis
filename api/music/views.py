import json
from django.db import connection, DatabaseError
from django.http import JsonResponse, HttpResponseBadRequest
from django.db import connection
import uuid
import datetime
from analysis import analyze, predict_rating, predict_recommand
from django.views.decorators.csrf import csrf_exempt


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
                SELECT `Album Name`, total_duration, `Artist Names`, `Album URI`
                FROM (
                    SELECT `Album Name`, SUM(`Track Duration ms`) AS total_duration, `Artist Names`, `Album URI`
                    FROM mytable
                    WHERE `Artist Names` IN (
                        SELECT `Artist Names`
                        FROM mytable
                        GROUP BY `Artist Names`
                        HAVING ABS(AVG(Loudness)) >= 10
                    )
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


def get_analysis(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT *
                FROM mytable
                WHERE 
                    `Danceability` IS NOT NULL AND
                    `Energy` IS NOT NULL AND
                    `Loudness` IS NOT NULL AND
                    `Speechiness` IS NOT NULL AND
                    `Acousticness` IS NOT NULL AND
                    `Instrumentalness` IS NOT NULL AND
                    `Liveness` IS NOT NULL AND
                    `Valence` IS NOT NULL AND
                    `Tempo` IS NOT NULL AND
                    `Explicit` IS NOT NULL
            """)
            rows = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            images = analyze(columns, rows)

        return JsonResponse({"data": images})
    except DatabaseError as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
def get_predict_rating(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT *
                    FROM mytable
                """)
                rows = cursor.fetchall()
                columns = [desc[0] for desc in cursor.description]
                prediction = predict_rating(rows, columns, data)

            return JsonResponse({"data": prediction})
        except DatabaseError as e:
            return JsonResponse({'error': str(e)}, status=500)
    return HttpResponseBadRequest('Invalid request method. Expected POST.')


def get_predict_recommand(request):
    song_name = request.GET.get('song_name')
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT *
                FROM mytable
                WHERE 
                    `Danceability` IS NOT NULL AND
                    `Energy` IS NOT NULL AND
                    `Loudness` IS NOT NULL AND
                    `Speechiness` IS NOT NULL AND
                    `Acousticness` IS NOT NULL AND
                    `Instrumentalness` IS NOT NULL AND
                    `Liveness` IS NOT NULL AND
                    `Valence` IS NOT NULL AND
                    `Tempo` IS NOT NULL AND
                    `Explicit` IS NOT NULL
            """)
            rows = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            prediction = predict_recommand(rows, columns, song_name)

        return JsonResponse({"data": prediction})
    except DatabaseError as e:
        return JsonResponse({'error': str(e)}, status=500)
