import { api } from "@/api/api";
import { title } from "@/components/primitives";
import DefaultLayout from "@/layouts/default";
import { useEffect, useState } from "react";
import { Spinner } from "@nextui-org/spinner";

export default function Statistics() {
  const [image, setImage] = useState(); // State to store image base64 strings

  useEffect(() => {
    fetch(`${api}/music/analysis`)
      .then((response) => response.json())
      .then((data) => {
        setImage(data["data"]);
      });
  }, []);

  return (
    <DefaultLayout>
      <section className="flex flex-col items-center justify-center gap-4 p-8">
        <div className="inline-block max-w-lg text-center justify-center">
          <h1 className={title({ color: "green" })}>Statistics</h1>
        </div>
        <div className="flex flex-col gap-4 justify-center">
          {image ? (
            <img src={`data:image/png;base64,${image}`} alt="Analysis" />
          ) : (
            <Spinner color="success" label="Generating Statistics..." />
          )}
        </div>
      </section>
    </DefaultLayout>
  );
}
