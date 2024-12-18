import { Route, Routes } from "react-router-dom";

import Home from "./pages/Home/home";
import Queries from "./pages/Queries/queries";
import Statistics from "./pages/Statistics/statistics";

function App() {
  return (
    <Routes>
      <Route element={<Home />} path="/" />
      <Route element={<Queries />} path="/queries" />
      <Route element={<Statistics />} path="/statistics" />
    </Routes>
  );
}

export default App;
