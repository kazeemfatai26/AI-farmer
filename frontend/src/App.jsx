import React from "react";
import { Routes, Route} from "react-router-dom";
import Auth from "./pages/Auth";
import Dashboard from "./Dashboard";

const App = () => {
  return (
    <div className="App">
      <Routes>
        <Route path="/auth" element={<Auth />} />
         <Route path="/dashboard" element={<Dashboard />} />
      </Routes>
    </div>
  );
};

export default App;