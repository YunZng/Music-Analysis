
import { title } from "@/components/primitives";
import DefaultLayout from "@/layouts/default";

export default function Home() {
  return (
    <DefaultLayout>
      <section className="flex flex-col items-center justify-center gap-4 py-8 md:py-10">
        <div className="inline-block max-w-lg text-center justify-center">
          <span className={title({ color: "violet" })}>Home</span>
        </div>
        <div className="w-full h-full overflow-y-auto">
        </div>
      </section>
    </DefaultLayout>
  );
}
