import { getTrackByDate } from "@/api/api";
import { $tracks, setTracks } from "@/store/store";
import { useStore } from "@nanostores/react";
import { useState } from "react";

export default function useQuery() {
  const tracks = useStore($tracks);
  const [isLoading, setIsLoading] = useState(false);

  const getTracks = async (
    date: string,
    order: string
  ) => {
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

  // useEffect(() => {
  //   loadPosts();
  //   // eslint-disable-next-line react-hooks/exhaustive-deps
  // }, [showMine]);

  return { tracks, getTracks, isLoading };
}