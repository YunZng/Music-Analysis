const api = 'http://127.0.0.1:8000'

export async function getTrackByDate(date: string, order: string) {
  const response = await fetch(`${api}/tracks?date=${date}&order=${order}`, {
    headers: {
      'Content-Type': 'application/json',
    },
  });
  const data = await response.json();
  return data['items'];
}
