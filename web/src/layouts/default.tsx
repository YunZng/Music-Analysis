import { Navbar } from "@/components/navbar";

export default function DefaultLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="flex h-screen w-screen grid grid-cols-6 overflow-hidden">
      <div className="col-span-1">
        <Navbar />
      </div>
      <main className="col-span-5 overflow-y-scroll">
        {children}
      </main>
    </div>
  );
}
