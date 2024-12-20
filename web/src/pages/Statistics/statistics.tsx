import { api } from "@/api/api";
import { title } from "@/components/primitives";
import DefaultLayout from "@/layouts/default";
import { useEffect } from "react";
import { Spinner } from "@nextui-org/spinner";
import { useStore } from "@nanostores/react";
import { $analysis, setAnalysis } from "@/store/store";

export default function Statistics() {
  const analysis = useStore($analysis);

  useEffect(() => {
    fetch(`${api}/music/analysis`)
      .then((response) => response.json())
      .then((data) => {
        setAnalysis(data["data"]);
      });
  }, []);

  return (
    <DefaultLayout>
      <section className="flex flex-col items-center justify-center gap-4 p-8">
        <div className="inline-block max-w-lg text-center justify-center">
          <h1 className={title({ color: "green" })}>Statistics</h1>
        </div>
        <div className="flex flex-col gap-4 justify-center">
          {analysis ? (
            <img src={`data:image/png;base64,${analysis}`} alt="Analysis" />
          ) : (
            <Spinner color="success" label="Generating Statistics..." />
          )}
        </div>
      </section>
    </DefaultLayout>
  );
}
