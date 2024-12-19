import { title } from "@/components/primitives";
import DefaultLayout from "@/layouts/default";
import MostPopular from "./mostPopular";
import NonstopBlasting from "./nonstopBlasting";

export default function Home() {
  return (
    <DefaultLayout>
      <section className="flex flex-col items-center justify-center gap-4 p-8">
        <div className="inline-block max-w-lg text-center justify-center">
          <span className={title({ color: "violet" })}>Home</span>
        </div>
        <div className="w-full h-full overflow-y-auto grid grid-cols-2 gap-4">
          <div className="w-full overflow-hidden">
            <MostPopular />
          </div>
          <div className="w-full overflow-hidden">
            <NonstopBlasting />
          </div>
        </div>
      </section>
    </DefaultLayout>
  );
}
