import { title } from "@/components/primitives";
import DefaultLayout from "@/layouts/default";
import { Button } from "@nextui-org/button";
import {
  Table,
  TableHeader,
  TableBody,
  TableColumn,
  TableRow,
  TableCell,
} from "@nextui-org/table";
import { Pagination } from "@nextui-org/pagination";
import { Alert } from "@nextui-org/alert";
import useQuery from "@/hooks/use-query";
import { useMemo, useState } from "react";
import { Link } from "@nextui-org/link";
import { Input } from "@nextui-org/input";

export default function Queries() {
  const { tracks, loadTracks } = useQuery();

  const [rowsPerPage, setRowsPerPage] = useState(25);
  const [order, setOrder] = useState<"ASC" | "DESC">("DESC");

  const toggleOrder = () => {
    setOrder(order === "ASC" ? "DESC" : "ASC");
  };

  const handleGetTracks = () => {
    const date = (document.getElementById("date") as HTMLInputElement).value;
    loadTracks(date, order);
  };
  const [page, setPage] = useState(1);
  const pages = Math.ceil(tracks.length / rowsPerPage);
  const items = useMemo(() => {
    const start = (page - 1) * rowsPerPage;
    const end = start + rowsPerPage;
    return tracks.slice(start, end);
  }, [page, tracks]);

  return (
    <DefaultLayout>
      <div className="flex flex-col items-center justify-center gap-4 p-8">
        <div className="inline-block max-w-lg text-center justify-center">
          <h1 className={title({ color: "blue" })}>Queries</h1>
        </div>
        <div className="w-full h-12 flex justify-center gap-4">
          <Input
            id="date"
            type="date"
            variant="bordered"
            label="Tracks released after"
            className="w-48 h-full"
          />
          <Button
            onClick={handleGetTracks}
            variant="bordered"
            color="primary"
            className="h-full"
          >
            Submit
          </Button>
          <Input
            type="number"
            min={5}
            defaultValue={rowsPerPage.toString()}
            max={100}
            onChange={(e) => setRowsPerPage(parseInt(e.target.value))}
            label="Items per page"
            labelPlacement="outside-left"
            variant="bordered"
            className="w-48 h-full"
          />
          <Button
            variant="bordered"
            onClick={toggleOrder}
            className="w-24 h-full"
          >
            {order}
          </Button>
        </div>
        {tracks.length == 0 ? (
          <Alert color="secondary" variant="bordered" classname="w-48">
            No data found
          </Alert>
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
                <TableColumn>Track Name</TableColumn>
                <TableColumn>Artist</TableColumn>
                <TableColumn>Album</TableColumn>
                <TableColumn>Date</TableColumn>
              </TableHeader>
              <TableBody>
                {items.map((track) => (
                  <TableRow key={crypto.randomUUID()}>
                    <TableCell>
                      <Link href={track.url} isExternal={true}>
                        {track.name}
                      </Link>
                    </TableCell>
                    <TableCell>{track.artist}</TableCell>
                    <TableCell>{track.album}</TableCell>
                    <TableCell>{track.date}</TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </div>
        )}
      </div>
    </DefaultLayout>
  );
}
