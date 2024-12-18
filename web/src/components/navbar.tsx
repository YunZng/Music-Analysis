import { Link } from "@nextui-org/link";
import {
  DashboardIcon,
  HomeIcon,
  PersonIcon,
  TableIcon,
} from "@radix-ui/react-icons";
import { link as linkStyles } from "@nextui-org/theme";
import clsx from "clsx";
import { ThemeSwitch } from "./theme-switch";

export const Navbar = () => {
  return (
    <section className="bg-slate-100 dark:bg-zinc-900 w-64 h-full overflow-auto p-4">
      <div className="grid gap-8">
        <Link
          className={clsx(
            linkStyles({ color: "foreground" }),
            "data-[active=true]:text-primary data-[active=true]:font-medium"
          )}
          color="foreground"
          href="/"
        >
          <div className="flex items-center gap-4">
            <HomeIcon className="w-6 h-6" />
            <p className="text-base font-semibold">Home</p>
          </div>
        </Link>
        <Link
          className={clsx(
            linkStyles({ color: "foreground" }),
            "data-[active=true]:text-primary data-[active=true]:font-medium"
          )}
          color="foreground"
          href="/tables"
        >
          <div className="flex items-center gap-4">
            <TableIcon className="w-6 h-6" />
            <p className="text-base font-semibold">Tables</p>
          </div>
        </Link>
        <Link
          className={clsx(
            linkStyles({ color: "foreground" }),
            "data-[active=true]:text-primary data-[active=true]:font-medium"
          )}
          color="foreground"
          href="/dashboard"
        >
          <div className="flex items-center gap-4">
            <DashboardIcon className="w-6 h-6" />
            <p className="text-base font-semibold">Dashboard</p>
          </div>
        </Link>
        <Link
          className={clsx(
            linkStyles({ color: "foreground" }),
            "data-[active=true]:text-primary data-[active=true]:font-medium"
          )}
          color="foreground"
          href="/artists"
        >
          <div className="flex items-center gap-4">
            <PersonIcon className="w-6 h-6" />
            <p className="text-base font-semibold">Artists</p>
          </div>
        </Link>
        <ThemeSwitch/>
      </div>
    </section>
  );
};
