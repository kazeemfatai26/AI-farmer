import { useState } from "react";
import AddFarmer from "./AddFarmer";
import FarmerList from "./FarmerList";
import { MdDashboard, MdPersonAdd } from "react-icons/md";
import { FaSeedling } from "react-icons/fa";
// import { GiWheat } from "react-icons/gi";

const Dashboard = () =>{
    const [view, setView] = useState("list")

    const [farmers, setFarmers] = useState([
  { name: "Amina Nkurunziza", phone: "078 123 4567", location: "Kinigi, Musanze", farmSize: "2.4 acres" },
  { name: "Jean Baptiste Habimana", phone: "072 555 8891", location: "Nyamagabe", farmSize: "1.1 acres" },
  { name: "Grace Uwimana", phone: "079 302 1156", location: "Rubavu", farmSize: "3.0 acres" },
]);

const addFarmer = (newFarmer) => {
  setFarmers((prevFarmers) => [...prevFarmers, newFarmer]);
};
    return(
        <div className="flex min-h-screen bg-gray-50">
            {/*Sidebar*/}
            <aside className="w-60 bg-white border-r border-gray-200 p-4">
                <div className="flex items-center gap-2">
                <FaSeedling className="text-green-700 text-3xl mb-8"/>
                <h2 className="text-xl font-bold text-green-700 mb-8">Advisory System</h2>
                </div>
                <nav>
                    <button onClick={() => setView("list")}
                    className="w-full text-left px-3 py-2 rounded-md text-md font-medium transition duration-150 hover:bg-green-700 hover:text-white focus:outline-none focus:bg-green-700 focus:text-white">
                        <MdDashboard className="inline-block mr-2" />
                        Dashboard
                    </button>
                    <button onClick={() => setView("add")}
                    className="w-full text-left px-3 py-2 rounded-md text-md font-medium transition duration-150 hover:bg-green-700 hover:text-white focus:outline-none focus:bg-green-700 focus:text-white mt-6">
                        <MdPersonAdd className="inline-block mr-2" />
                        Add Farmer
                    </button>
                </nav>
            </aside>
            {/*Main Content*/}
            <main className="flex-1 p-6">
                {view === "list" && (
                    <div>
                        {/* <h3 className="text-lg font-semibold mb-4">Farmer List</h3> */}
                        <FarmerList farmers={farmers} />
                    </div>
                )}
                {view === "add" && (
                    <div>
                        {/* <h3 className="text-lg font-semibold mb-4">Add Farmer</h3> */}
                        <AddFarmer onAddFarmer={addFarmer} />
                    </div>
                )}
            </main>
        </div>
        
    );
};

export default Dashboard;