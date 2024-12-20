import { title } from "@/components/primitives";
import DefaultLayout from "@/layouts/default";
import { Tabs, Tab } from "@nextui-org/tabs";
import PredictRating from "./predictRating";

export default function Queries() {
  return (
    <DefaultLayout>
      <div className="flex flex-col items-center justify-center gap-4 p-8">
        <div className="inline-block max-w-lg text-center justify-center">
          <h1 className={title({ color: "blue" })}>Queries</h1>
        </div>
        <div className="flex flex-col w-full">
          <Tabs className="justify-center">
            <Tab title="Predict Rating">
              <PredictRating />
            </Tab>
            <Tab title="Find Similar Song">
              
            </Tab>
            <Tab title="Generic Queries">

            </Tab>
          </Tabs>
        </div>
      </div>
    </DefaultLayout>
  );
}
