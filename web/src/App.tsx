import { Route, Routes } from "react-router-dom";

import Home from "./pages/home";
import Queries from "./pages/queries";
import Dashboard from "./pages/dashboard";
import Artists from "./pages/artists";

function App() {
  return (
    <Routes>
      <Route element={<Home />} path="/" />
      <Route element={<Queries />} path="/tables" />
      <Route element={<Dashboard />} path="/dashboard" />
      <Route element={<Artists />} path="/artists" />
    </Routes>
  );
}

export default App;
