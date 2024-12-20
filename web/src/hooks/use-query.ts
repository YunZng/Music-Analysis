import { getLongestLoudest, getMostPopular, getTrackByDate } from "@/api/api";
import {
  $mostPopular,
  $nonstopBlashing,
  $tracks,
  setMostPopular,
  setNonstopBlashing,
  setTracks,
} from "@/store/store";
import { useStore } from "@nanostores/react";
import { useState } from "react";

export default function useQuery() {
  const tracks = useStore($tracks);
  const mostPopular = useStore($mostPopular);
  const longestLoudest = useStore($nonstopBlashing);
  

  const [isLoading, setIsLoading] = useState(false);

  const loadTracks = async (date: string, order: string) => {
    setIsLoading(true);
    try {
      const data = await getTrackByDate(date, order);
      setTracks(data);
    } catch (error) {
      console.error(error);
    } finally {
      setIsLoading(false);
    }
  };

  const loadMostPopular = async () => {
    setIsLoading(true);
    try {
      const data = await getMostPopular();
      setMostPopular(data);
    } catch (error) {
      console.error(error);
    } finally {
      setIsLoading(false);
    }
  };

  const loadLongestLoudest = async () => {
    setIsLoading(true);
    try {
      const data = await getLongestLoudest();
      setNonstopBlashing(data);
    } catch (error) {
      console.error(error);
    } finally {
      setIsLoading(false);
    }
  }

  return { tracks, loadTracks, mostPopular, loadMostPopular, longestLoudest, loadLongestLoudest, isLoading };
}
