import { getCustomQuery, getSpecificCustomQuery } from "@/api/api";
import { $queryResult, setQueryResult } from "@/store/store";
import { useStore } from "@nanostores/react";
import { useState } from "react";

export default function useGeneric() {
  const queryResult = useStore($queryResult);
  const [isLoading, setIsLoading] = useState(false);

  async function loadCustomQuery(query: string) {
    setIsLoading(true);
    try {
      const data = await getCustomQuery(query);
      setQueryResult(data);
    } catch (error) {
      console.error(error);
    } finally {
      setIsLoading(false);
    }
  }

  async function loadSpecificCustomQuery(id: number) {
    setIsLoading(true);
    try {
      const data = await getSpecificCustomQuery(id);
      setQueryResult(data);
    } catch (error) {
      console.error(error);
    } finally {
      setIsLoading(false);
    }
  }

  return { queryResult, isLoading, loadCustomQuery, loadSpecificCustomQuery };
}
