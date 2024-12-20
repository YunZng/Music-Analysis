import useGeneric from "@/hooks/use-generic";
import { Card, CardBody, CardHeader } from "@nextui-org/card";
import {
  Table,
  TableHeader,
  TableBody,
  TableColumn,
  TableRow,
  TableCell,
  getKeyValue,
} from "@nextui-org/table";
import { Pagination } from "@nextui-org/pagination";
import { Alert } from "@nextui-org/alert";
import { useEffect, useMemo, useState } from "react";
import { Textarea } from "@nextui-org/input";
import {
  Modal,
  ModalContent,
  ModalHeader,
  ModalBody,
  ModalFooter,
  useDisclosure,
} from "@nextui-org/modal";
import { Button } from "@nextui-org/button";
import { Spinner } from "@nextui-org/spinner";

export default function GenericQueries() {
  const { isOpen, onOpen, onOpenChange } = useDisclosure();
  const [userQuery, setUserQuery] = useState("");

  const { isLoading, loadCustomQuery, loadSpecificCustomQuery, queryResult } =
    useGeneric();
  const rowsPerPage = 25;
  const [page, setPage] = useState(1);
  const pages = Math.ceil(queryResult.length / rowsPerPage);
  const items = useMemo(() => {
    const start = (page - 1) * rowsPerPage;
    const end = start + rowsPerPage;
    return queryResult.slice(start, end);
  }, [page, queryResult]);

  useEffect(() => {
    console.log(items);
    console.log(queryResult);
  }, [queryResult]);

  const queries = [
    {
      title: "Active artists in the last 2 years",
      description:
        "List artists in who released songs in both 2023 and 2024, along with the total streams in both years and latest track score",
      id: 1,
    },
    {
      title: "Consistent top hits",
      description:
        "Retrieve songs from 2023 that appear in the top 50 of 2024, including their rank",
      id: 2,
    },
    {
      title: "Top danceable genres",
      description:
        "Top 10 genres with the highest average danceability, considering only tracks with Energy above the overall average",
      id: 3,
    },
    {
      title: "Yearly loudness",
      description: "Calculate the average loudness and tempo for each year",
      id: 4,
    },
  ];
  const customQuery = {
    title: "Run your own query",
    description: "Use the query editor to run your own SQL queries",
  };

  return (
    <div className="flex flex-col gap-4">
      <div className="w-full grid grid-cols-5 gap-4">
        {queries.map((query, index) => (
          <Card
            key={index}
            isPressable
            onPress={() => {
              loadSpecificCustomQuery(query.id);
              setPage(1);
            }}
          >
            <CardHeader className="text-left">
              <h1 className="font-medium text-large">{query.title}</h1>
            </CardHeader>
            <CardBody>
              <p>{query.description}</p>
            </CardBody>
          </Card>
        ))}
        <Card isPressable onPress={onOpen}>
          <CardHeader className="text-left">
            <h1 className="font-medium text-large">{customQuery.title}</h1>
          </CardHeader>
          <CardBody>
            <p>{customQuery.description}</p>
          </CardBody>
        </Card>
        <Modal
          isOpen={isOpen}
          onOpenChange={onOpenChange}
          onClose={() => setUserQuery("")}
        >
          <ModalContent>
            {(onClose) => (
              <>
                <ModalHeader className="flex flex-col gap-1">
                  Modal Title
                </ModalHeader>
                <ModalBody>
                  <Textarea
                    label="SQL Query"
                    variant="bordered"
                    isClearable
                    placeholder="Type your SQL query here."
                    onChange={(e) => setUserQuery(e.target.value)}
                    value={userQuery}
                  />
                </ModalBody>
                <ModalFooter>
                  <Button color="danger" variant="light" onPress={onClose}>
                    Close
                  </Button>
                  <Button
                    color="primary"
                    onPress={() => {
                      loadCustomQuery(userQuery);
                      setUserQuery("");
                      setPage(1);
                      onClose();
                    }}
                  >
                    Run Query
                  </Button>
                </ModalFooter>
              </>
            )}
          </ModalContent>
        </Modal>
      </div>
      {queryResult.length == 0 ? (
        <Alert color="secondary" variant="bordered" classname="w-48">
          No data found
        </Alert>
      ) : isLoading ? (
        <Spinner label="Loading..." size="lg" />
      ) : (
        <div className="w-full overflow-x-auto">
          <Table
            aria-label="Result table with pagination"
            bottomContent={
              <div className="flex w-full justify-center">
                <Pagination
                  isCompact
                  showControls
                  showShadow
                  color="secondary"
                  page={page}
                  total={pages}
                  onChange={(page) => setPage(page)}
                />
              </div>
            }
          >
            <TableHeader>
              {Object.keys(queryResult[0]).map((column: any) => (
                <TableColumn key={column}>{column}</TableColumn>
              ))}
            </TableHeader>
            <TableBody items={items}>
              {(item: any) => (
                <TableRow key={item[Object.keys(queryResult[0])[0]]}>
                  {(columnKey) => (
                    <TableCell>{getKeyValue(item, columnKey)}</TableCell>
                  )}
                </TableRow>
              )}
            </TableBody>
          </Table>
        </div>
      )}
    </div>
  );
}
