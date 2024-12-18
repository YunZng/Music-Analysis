import { title } from "@/components/primitives";
import DefaultLayout from "@/layouts/default";

export default function Statistics() {
  return (
    <DefaultLayout>
      <section className="flex flex-col items-center justify-center gap-4 p-8">
        <div className="inline-block max-w-lg text-center justify-center">
          <h1 className={title({ color: "green" })}>Statistics</h1>
        </div>
      </section>
    </DefaultLayout>
  );
}
