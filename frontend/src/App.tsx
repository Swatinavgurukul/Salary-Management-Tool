import { BrowserRouter, Routes, Route, NavLink } from "react-router-dom";
import EmployeeListPage from "./pages/EmployeeListPage";
import EmployeeFormPage from "./pages/EmployeeFormPage";
import InsightsPage from "./pages/InsightsPage";
import "./App.css";

function App() {
  return (
    <BrowserRouter>
      <div className="app">
        <header>
          <h1>Salary Management</h1>
          <nav>
            <NavLink to="/" end>
              Employees
            </NavLink>
            <NavLink to="/insights">Insights</NavLink>
          </nav>
        </header>
        <main>
          <Routes>
            <Route path="/" element={<EmployeeListPage />} />
            <Route path="/employees/new" element={<EmployeeFormPage />} />
            <Route path="/employees/:id/edit" element={<EmployeeFormPage />} />
            <Route path="/insights" element={<InsightsPage />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  );
}

export default App;
