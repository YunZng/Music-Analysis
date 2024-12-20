import { getLongestLoudest, getMostPopular } from "@/api/api";
import {
  $mostPopular,
  $nonstopBlashing,
  setMostPopular,
  setNonstopBlashing,
} from "@/store/store";
import { useStore } from "@nanostores/react";
import { useState } from "react";

export default function useQuery() {
  const mostPopular = useStore($mostPopular);
  const longestLoudest = useStore($nonstopBlashing);

  const [isLoading, setIsLoading] = useState(false);

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

  return { mostPopular, loadMostPopular, longestLoudest, loadLongestLoudest, isLoading };
}
