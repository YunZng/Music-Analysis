import { api } from "@/api/api";
import { useState } from "react";
import { Form } from "@nextui-org/form";
import { Button } from "@nextui-org/button";
import { Input } from "@nextui-org/input";
import { Card, CardBody, CardFooter } from "@nextui-org/card";
import { Chip } from "@nextui-org/chip";
import { Avatar } from "@nextui-org/avatar";
import { Spinner } from "@nextui-org/spinner";

export default function PredictRating() {
  const [submitted, setSubmitted] = useState<boolean>(false);
  const [prediction, setPrediction] = useState();
  const [isLoading, setIsLoading] = useState(false);

  const fields = [
    "Acousticness",
    "Danceability",
    "Energy",
    "Instrumentalness",
    "Liveness",
    "Speechiness",
    "Valence",
    "Loudness",
    "Tempo",
    "Duration Minutes",
  ];

  const onSubmit = (e: any) => {
    e.preventDefault();

    const formData = new FormData(e.currentTarget);
    const data = Object.fromEntries(
      Array.from(formData.entries()).map(([key, value]) => [
        key,
        isNaN(Number(value)) ? value : Number(value),
      ])
    );
    console.log(data);
    getPrediction(data);
    setSubmitted(true);
  };

  const getPrediction = (data: any) => {
    setIsLoading(true);
    fetch(`${api}/music/rating`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    })
      .then((response) => response.json())
      .then((data) => {
        setPrediction(data["data"]);
      })
      .finally(() => setIsLoading(false));
  };

  return (
    <>
      <div className="h-full flex justify-center gap-4">
        <Card shadow="sm">
          <Form
            className="w-full"
            validationBehavior="native"
            onSubmit={onSubmit}
          >
            <CardBody className="overflow-visible p-4 w-full grid grid-cols-5 gap-4">
              {fields.map((field) => (
                <Input
                  key={field}
                  isRequired
                  label={field}
                  labelPlacement="outside"
                  name={field}
                  placeholder={`Enter ${field.toLowerCase()}`}
                  type="number"
                />
              ))}
            </CardBody>
            <CardFooter className="w-full flex gap-4 grid grid-cols-5">
              <Button type="submit" variant="ghost" color="primary">
                Predict Popularity
              </Button>
              {submitted ? (
                isLoading ? (
                  <Spinner color="primary" label="Calculating score" />
                ) : (
                  <Chip
                    avatar={<Avatar src="./fire.jpg" />}
                    variant="shadow"
                    size="lg"
                  >
                    {prediction}
                  </Chip>
                )
              ) : null}
            </CardFooter>
          </Form>
        </Card>
      </div>
    </>
  );
}
