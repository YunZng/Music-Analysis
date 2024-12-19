import useQuery from "@/hooks/use-query";
import { Link } from "@nextui-org/link";
import {
  Table,
  TableBody,
  TableCell,
  TableColumn,
  TableHeader,
  TableRow,
} from "@nextui-org/table";
import { useEffect } from "react";
import { Spinner } from "@nextui-org/spinner";
import { subtitle } from "@/components/primitives";

export default function MostPopular() {
  const { mostPopular, loadMostPopular } = useQuery();

  useEffect(() => {
    loadMostPopular();
  }, []);

  return (
    <div className="flex flex-col justify-center text-center">
      <p className={subtitle()}>All time Top 10</p>
      {mostPopular.length == 0 ? (
        <Spinner size="lg" />
      ) : (
        <Table>
          <TableHeader>
            <TableColumn>Track</TableColumn>
            <TableColumn>Artist</TableColumn>
            <TableColumn>Popularity</TableColumn>
          </TableHeader>
          <TableBody>
            {mostPopular.map((item) => (
              <TableRow key={item.url}>
                <TableCell>
                  <Link href={item.url} isExternal={true}>
                    {item.name}
                  </Link>
                </TableCell>
                <TableCell>{item.artist}</TableCell>
                <TableCell>{item.popularity}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      )}
    </div>
  );
}
