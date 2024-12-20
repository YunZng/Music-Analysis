export const api = "http://127.0.0.1:8000";

export async function getTrackByDate(date: string, order: string) {
  const response = await fetch(`${api}/music/tracks?date=${date}&order=${order}`, {
    headers: {
      "Content-Type": "application/json",
    },
  });
  const data = await response.json();
  return data["data"];
}

export async function getMostPopular() {
  const response = await fetch(`${api}/music/popular`, {
    headers: {
      "Content-Type": "application/json",
    },
  });
  const data = await response.json();
  return data["data"];
}

export async function getLongestLoudest(){
  const response = await fetch(`${api}/music/longest_loudest`, {
    headers: {
      "Content-Type": "application/json",
    },
  });
  const data = await response.json();
  return data["data"];
}

export async function getAnalysis(){
  const response = await fetch(`${api}/music/analysis`, {
    headers: {
      "Content-Type": "application/json",
    },
  });
  const data = await response.json();
  return data["data"];
}