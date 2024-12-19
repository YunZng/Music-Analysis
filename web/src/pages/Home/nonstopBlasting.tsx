import useQuery from "@/hooks/use-query";
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

export default function NonstopBlasting() {
  const { longestLoudest, loadLongestLoudest } = useQuery();

  useEffect(() => {
    loadLongestLoudest();
  }, []);

  return (
    <div className="flex flex-col justify-center text-center">
      <p className={subtitle()}>Non-stop Blasting Albums</p>
      {longestLoudest.length == 0 ? (
        <Spinner size="lg" />
      ) : (
        <Table>
          <TableHeader>
            <TableColumn>Album</TableColumn>
            <TableColumn>Artist</TableColumn>
            <TableColumn>Duration (sec)</TableColumn>
          </TableHeader>
          <TableBody>
            {longestLoudest.map((item) => (
              <TableRow key={item.id}>
                <TableCell>
                    {item.album}
                </TableCell>
                <TableCell>{item.artist}</TableCell>
                <TableCell>{item.duration}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      )}
    </div>
  );
}
